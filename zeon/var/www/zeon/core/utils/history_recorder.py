# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC
"""

from apps import db
from apps.api.models import SensorsStatus, SensorsHistory


class HistoryRecorder:
    def __init__(self, measurement_id, status, message):
        self.measurement_id = measurement_id
        self.status = status
        self.message = message

    def init_history(self):
        """
        Создаём записи в истории:
            1 - Init sensor
            2 - Сообщение датчика
        """
        #
        record = SensorsHistory(
            measurements_id=self.measurement_id,
            status=self.status,
            message='Init sensor'
        )
        db.session.add(record)
        db.session.commit()
        #
        record = SensorsHistory(
            measurements_id=self.measurement_id,
            status=self.status,
            message=self.message
        )
        db.session.add(record)
        db.session.commit()

    def save_to_history(self):
        pass
