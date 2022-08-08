# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC
"""
import json
from flasgger import SwaggerView, swag_from
from flask import current_app, request, jsonify, Response
from marshmallow import ValidationError

from apps import db
from apps.api.util import Translator
from apps.api.models import Measurements, MeasurementsData, SensorsStatus, SensorsHistory
from apps.api.schemas import MeasurementsSchema, MSchema, AdaptersDataSchema
from core.utils.zabbix import DataParser
from core.utils.history_recorder import HistoryRecorder


class AddMeasurementsView(SwaggerView):
    __doc__ = """
        Добавление новых измерений с датчиков."""

    # Redefine SwaggerView attributes
    summary = 'Добавление новых измерений с датчика'
    definitions = {
        'AdaptersDataSchema': AdaptersDataSchema}

    @staticmethod
    @swag_from('docs/add_measurements.yml')
    def post():
        current_app.logger.debug(json.dumps(request.json, indent=4, ensure_ascii=False))

        try:
            # Use schema.load(request.json) -> if no Nested field in schema
            # Use schema.dump(request.json) -> if Nested
            valid_data = AdaptersDataSchema().dump(request.json)
        except ValueError as err:
            current_app.logger.error(err.args)
            return jsonify({"status": err.args}), 400
        except ValidationError as err:
            current_app.logger.error(err.args)
            return jsonify({"status": err.args}), 400

        current_app.logger.debug(valid_data)

        if not isinstance(valid_data.get("measurements"), list):
            return jsonify({"status": "Type Error!"}), 400

        if not valid_data.get("system", None):
            # return Response(status=400, response='Received data is empty!')
            current_app.logger.error("Validation Error!")
            return jsonify({"status": "Validation Error!"}), 400

        try:
            # FIXME: Need new json from sensors to fill in 'host_creds'
            #   {
            #       "address": "XX, XX, XX, XXX777",
            #       "system": "XXX",
            #       "measurements": [
            #           {
            #               data: {
            #                   "msg": "xxxx",
            #                   "state": 1,
            #                   "status": 8
            #               },
            #               sybsystem: "xxxx"
            #           },
            #       ]
            #   }
            # Parse and send data to Zabbix Server
            DataParser(
                measurements=valid_data.get("measurements"),
                host_creds={
                    "system": valid_data.get("system"),
                    "host_name": "SensOrs",
                    "host_group_name": "Astra Servers Group",
                }
            ).proceed().push_to_zabbix()
        except Exception as err:
            current_app.logger.error(err.args)
            pass

        translator = Translator()

        _system_ru = valid_data.get("system")

        for measur in valid_data.get("measurements"):
            _subsystem_ru = measur.get('subsystem')

            if _subsystem_ru is None:
                current_app.logger.error('ID was not found!')
                return Response(status=400, response='ID was not found!')

            # Достаем запись Измерения
            is_exist_measurement = db.session.query(Measurements).filter_by(subsystem=_subsystem_ru).first()
            # Если запись уже есть, меняем состояние
            if is_exist_measurement:
                # TODO: if запись есть такая же -> не комитить
                is_exist_measurement.measurements_data.state = measur["data"]["state"]
                is_exist_measurement.measurements_data.msg = measur["data"]["msg"]
                # FIXME: Warning! Hardcode data["status"].
                is_exist_measurement.measurements_data.system = _system_ru
                db.session.commit()

                # Достаем запись Статуса
                is_exist_sensor_status = db.session.query(SensorsStatus).filter_by(id=is_exist_measurement.id).first()
                # Если запись уже есть,
                if is_exist_sensor_status:
                    # и, состояние больше 0 (неисправно) -> заменить на текущее от датчика в
                    if int(measur["data"]["state"]) == 1:
                        if is_exist_sensor_status.status <= 1:
                            # - [Статус] и в
                            is_exist_sensor_status.status = 2
                            is_exist_sensor_status.message = measur["data"]["msg"]

                            db.session.commit()
                            # - [Истории].
                            record = SensorsHistory(
                                measurements_id=is_exist_measurement.id,
                                status=measur["data"]["state"],
                                message=measur["data"]["msg"]
                            )
                            db.session.add(record)
                            db.session.commit()
                        else:
                            pass
                    else:
                        # TODO: Add 5 minutes waiting before add to history
                        if is_exist_sensor_status.status > 1:

                            is_exist_sensor_status.status = 0
                            is_exist_sensor_status.message = "Датчик сообщил об исправности!"

                            db.session.commit()

                            record = SensorsHistory(
                                measurements_id=is_exist_measurement.id,
                                status=measur["data"]["state"],
                                message=measur["data"]["msg"]
                            )
                            db.session.add(record)
                            db.session.commit()

            # Иначе создаем новую запись в Измерениях и Статусах
            else:
                # FIXME: move DBMS logic to HistoryRecorder
                record = Measurements(
                    device="",
                    path="",
                    system=_system_ru,
                    key=translator.ru_cyr_to_lat(_subsystem_ru),
                    subsystem=_subsystem_ru,
                    measurements_data=MeasurementsData(**measur["data"]))

                db.session.add(record)
                db.session.commit()

                # Достаем созданную запись Измерения
                created_measurement = db.session.query(Measurements).filter_by(subsystem=_subsystem_ru).first()

                history_recorder = HistoryRecorder(
                    measurement_id=created_measurement.id,
                    status=measur["data"]["state"],
                    message=measur["data"]["msg"]
                )

                # Если состояние НЕ норма
                if int(measur["data"]["state"]) == 1:
                    # Записать НЕ норму
                    record = SensorsStatus(
                        id=created_measurement.id,
                        status=2,
                        message=measur["data"]["msg"])

                    db.session.add(record)
                    db.session.commit()

                    history_recorder.init_history()

                elif int(measur["data"]["state"]) == 0:
                    record = SensorsStatus(
                        id=created_measurement.id,
                        status=created_measurement.measurements_data.state,
                        message=measur["data"]["msg"])

                    db.session.add(record)
                    db.session.commit()

                    history_recorder.init_history()

                # Для случая: if int(measur["data"]["state"]) == 10
                else:
                    record = SensorsStatus(
                        id=created_measurement.id,
                        status=created_measurement.measurements_data.state,
                        message=measur["data"]["msg"])

                    db.session.add(record)
                    db.session.commit()

                    history_recorder.init_history()

        return jsonify({"status": "Success!"}), 201


class GetMeasurementsView(SwaggerView):
    __doc__ = """
        Запрос данных с базы по датчикам СВЭС."""

    # Redefine SwaggerView attributes
    summary = 'Запрос данных с базы по датчикам'
    definitions = {
        'MeasurementsSchema': MeasurementsSchema}

    @staticmethod
    @swag_from('docs/get_measurements.yml')
    def get():

        req = dict(request.args).get("data")
        current_app.logger.debug(request.args)

        if isinstance(req, list):
            req = dict(request.args).get("data")[0]

        if req:
            current_app.logger.debug(req)
            subsystems = req.split('|')
            current_app.logger.debug(subsystems)

            query = MSchema(many=True).dump(
                db.session.query(
                    Measurements
                ).filter(
                    Measurements.subsystem.in_(subsystems)
                )
            )

        else:
            return jsonify({"status": "Validation Error!"}), 400

        current_app.logger.debug(json.dumps(query, indent=4, ensure_ascii=False))

        if query:
            return jsonify(query), 201
        return jsonify({"status": "Data Not Found!"}), 404
