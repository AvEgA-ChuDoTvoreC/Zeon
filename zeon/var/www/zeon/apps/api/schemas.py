# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC
"""
from marshmallow import post_dump, fields
from marshmallow_sqlalchemy import ModelSchema
# from flasgger import Schema, fields

from apps.api.models import Measurements, MeasurementsData


class MDSchema(ModelSchema):
    __doc__ = """
        Схема, которая сериализуют поля по таблице 'measurements_data'."""

    class Meta:
        model = MeasurementsData
        exclude = ('id', 'measurements')


class MSchema(ModelSchema):
    __doc__ = """
        Схема, которая сериализуют поля по таблице 'measurements'."""

    class Meta:
        model = Measurements
        exclude = ('id', 'key')

    # Подключение схемы MDSchema для парсинга вложенности
    measurements_data = fields.Nested(MDSchema)

    @post_dump
    def serialize(self, data, **kwargs):
        # Замена имени внешнего ключа 'measurements_data' на 'data'
        data["data"] = data.pop("measurements_data")
        # Замена имени ключа 'subsystem' на 'id'
        # data["id"] = data.pop("subsystem")
        return data


class MeasurementsDataSchema(ModelSchema):
    __doc__ = """
        Схема, которая сериализуют поля по таблице 'measurements_data' для Swagger."""

    class Meta:
        model = MeasurementsData
        exclude = ('id', 'time_created', 'time_updated')


class MeasurementsSchema(ModelSchema):
    __doc__ = """
        Схема, которая сериализуют поля по таблице 'measurements' для Swagger."""

    class Meta:
        model = Measurements
        exclude = ('id',)

    # Подключение схемы MeasurementsDataSchema для парсинга вложенности
    data = fields.Nested(MeasurementsDataSchema)


class MeasurementsDataCropedSchema(ModelSchema):
    __doc__ = """
        Схема, которая сериализуют поля по обрезанной таблице 'measurements_data'."""

    msg = fields.Str(required=True)
    state = fields.Integer(required=True)
    status = fields.Integer(required=False)


class ListOfMeasurementsSchema(ModelSchema):
    __doc__ = """
        Схема, которая валидирует поля JSON, полученного из POST запроса, для каждого элемента."""

    subsystem = fields.Str(required=True)
    data = fields.Nested(MeasurementsDataCropedSchema)
    # data = fields.List(fields.Nested(MeasurementsDataSchema))

    @post_dump
    def delete_spaces(self, data: dict, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()

        return data


class AdaptersDataSchema(ModelSchema):
    __doc__ = """
        Схема, которая сериализуют поля по обрезанной таблице 'measurements_data'."""

    system = fields.Str(required=True)
    measurements = fields.List(fields.Nested(ListOfMeasurementsSchema))
