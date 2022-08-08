# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC
"""
from sqlalchemy import func

from apps import db


class Measurements(db.Model):

    __tablename__ = 'measurements'
    # __table_args__ = tuple(db.UniqueConstraint('key', 'subsystem'))

    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(128), nullable=True, doc='Device')
    path = db.Column(db.String(128), nullable=True, doc='Doted path')
    system = db.Column(db.String(128), nullable=False, doc='System system')
    subsystem = db.Column(db.String(128), nullable=False, unique=True, doc='Subsystem for zabbix')
    key = db.Column(db.String(128), nullable=False, unique=True, doc='Translated subsystem for zabbix')

    # One-To-One
    measurements_data_id = db.Column(
        db.Integer(),
        db.ForeignKey('measurements_data.id', onupdate='CASCADE', ondelete=None))  # RESTRICT/CASCADE/DELETE/
    measurements_data = db.relationship(
        'MeasurementsData',
        backref=db.backref('measurements', uselist=False),  # returned data will be list = False -> one-to-one
        cascade='all, delete',                              # all, delete-orphan
        doc='Data from Json')                               # lazy='dynamic', single_parent=True, passive_deletes=True

    def __init__(self, device, path, system, key, subsystem, measurements_data):
        self.device = device
        self.path = path
        self.system = system
        self.key = key
        self.subsystem = subsystem
        self.measurements_data = measurements_data

    def __repr__(self):
        return '<{class_name}: |{device}|{path}|{system}|{key}|{subsystem}|{measurements_data}|>'.format(
            class_name=self.__class__.__name__,
            device=self.device,
            path=self.path,
            system=self.system,
            key=self.key,
            subsystem=self.subsystem,
            measurements_data=self.measurements_data)


class MeasurementsData(db.Model):

    __tablename__ = 'measurements_data'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Integer, default="СВЭС", doc='State')
    msg = db.Column(db.String(255), doc='Message')
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, state, msg):
        self.state = state
        self.msg = msg

    def __repr__(self):
        return '<{class_name}: |{state}|{msg}|{time_created}|{time_updated}|>'.format(
            class_name=self.__class__.__name__,
            state=self.state,
            msg=self.msg,
            time_created=self.time_created,
            time_updated=self.time_updated)


class SensorsStatus(db.Model):

    __tablename__ = 'sensors_status'

    id = db.Column(db.Integer,  db.ForeignKey(Measurements.id, onupdate='CASCADE', ondelete=None), primary_key=True)
    status = db.Column(db.Integer, nullable=False, doc='Status')
    message = db.Column(db.String(255), doc='Message')
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, status, message):
        self.id = id
        self.status = status
        self.message = message

    def __repr__(self):
        return '<{class_name}: |{id}|{status}|{message}|{time_created}|{time_updated}|>'.format(
            class_name=self.__class__.__name__,
            id=self.id,
            status=self.status,
            message=self.message,
            time_created=self.time_created,
            time_updated=self.time_updated)


class SensorsHistory(db.Model):
    __tablename__ = 'sensors_history'

    id = db.Column(db.Integer, primary_key=True)
    measurements_id = db.Column(db.Integer, db.ForeignKey(Measurements.id, onupdate='CASCADE', ondelete=None))
    status = db.Column(db.Integer, nullable=False, doc='Status')
    message = db.Column(db.String(255), doc='Message')
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, measurements_id, status, message):
        self.measurements_id = measurements_id
        self.status = status
        self.message = message

    def __repr__(self):
        return '<{class_name}: |{measurements_id}|{status}|{message}|{time_created}|{time_updated}|>'.format(
            class_name=self.__class__.__name__,
            measurements_id=self.measurements_id,
            status=self.status,
            message=self.message,
            time_created=self.time_created,
            time_updated=self.time_updated)
