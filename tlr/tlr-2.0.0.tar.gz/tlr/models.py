from sqlalchemy import Column, DateTime, Float, create_engine
from sqlalchemy.ext.automap import automap_base

from . import settings

Base = automap_base()
engine = create_engine(settings.DATABASE_ENGINE)


class Temperature0(Base):
    __tablename__ = 'vgms_l530_0'

    timestamp = Column('dtime', DateTime, primary_key=True, index=True)
    temperature1 = Column('temp1', Float, index=True, nullable=True)
    temperature2 = Column('temp2', Float, index=True, nullable=True)
    temperature3 = Column('temp3', Float, index=True, nullable=True)
    temperature4 = Column('temp4', Float, index=True, nullable=True)
    battery_voltage = Column('V_bat', Float, index=True, nullable=True)


class Temperature1(Base):
    __tablename__ = 'vgms_l530_2'

    timestamp = Column('dtime', DateTime, primary_key=True, index=True)
    temperature = Column('temp', DateTime, index=True, nullable=True)


class Temperature2(Base):
    __tablename__ = 'vgms_l530_3'

    timestamp = Column('dtime', DateTime, primary_key=True, index=True)
    temperature = Column('temp', DateTime, index=True, nullable=True)


class Emission(Base):
    __tablename__ = 'vgms_l530_1'

    timestamp = Column('dtime', DateTime, primary_key=True, index=True)
    co2_min = Column('co2_min', Float, index=True, nullable=True)
    co2_max = Column('co2_max', Float, index=True, nullable=True)
    co2_avg = Column('co2_avg', Float, index=True, nullable=True)
    temperature_min = Column('temp_min', Float, index=True, nullable=True)
    temperature_max = Column('temp_max', Float, index=True, nullable=True)
    temperature_avg = Column('temp_avg', Float, index=True, nullable=True)
    humidity_min = Column('humi_min', Float, index=True, nullable=True)
    humidity_max = Column('humi_max', Float, index=True, nullable=True)
    humidity_avg = Column('humi_avg', Float, index=True, nullable=True)
    input_battery_voltage = Column('V_in', Float, index=True, nullable=True)


if settings.MIGRATED:
    Base.prepare(engine, reflect=True)
