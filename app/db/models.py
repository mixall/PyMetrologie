# Modely jednotlivých tabulek v databázi

import enum
from datetime import date

from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date, Enum
from .database import Base


class MeterModelEnum(enum.Enum):
    coldcar = "ColdCar 300"
    datalogger = "Datalogger AB-10"
    system_wh = "Systém pro sklady"
    temp_car = "TempCar 2000"

    def __str__(self):
        return str(self.value)


class Meter(Base):
    __tablename__ = "Meter"
    id = Column("Id", Integer, primary_key=True, index=True)
    name = Column("Name", String(25), nullable=False)
    model = Column("Model", Enum(MeterModelEnum, values_callable=lambda x: [str(e.value) for e in MeterModelEnum]))
    status = Column("Status", Boolean, nullable=False, default=True)
    act_dev_id = Column("ActDev", Integer, ForeignKey("Device.Id"), nullable=False)
    act_dev_detail = Column("ActDevDetail", String(25), nullable=True)
    home_dev_status = Column("HomeDevStatus", Boolean, nullable=False, default=False)
    home_dev_id = Column("HomeDev", Integer, ForeignKey("Device.Id"), nullable=True)
    # user_id = Column("UserId", Integer, ForeignKey("User.Id"), nullable=False)
    # note = Column("Note", Text, nullable=True)
    change_date = Column("Change_date", Date, nullable=False, default=date.today())
    act_dev = relationship("Device", foreign_keys=[act_dev_id])
    home_dev = relationship("Device", foreign_keys=[home_dev_id])

    def __repr__(self):
        return f"{self.id} - {self.model}, {self.sn}"

    def return_status(self):
        return "aktivní" if self.status else "neaktivní"


class DeviceTypeEnum(enum.Enum):
    chladici_komora = "Chladící komora"
    mrazak_350 = "Mrazák CALEX F-350"
    mrazak_prenosny = "Mrazák přenosný CALEX FP-50"
    vozidlo = "Vozidlo"

    def __str__(self):
        return str(self.value)

    # @classmethod
    # def choices(cls):
    #    return [(choice, choice.value) for choice in cls]


class Device(Base):
    __tablename__ = "Device"
    id = Column("Id", Integer, primary_key=True, index=True)
    name = Column("Name", String(50), unique=True, nullable=False)
    type = Column("Type", Enum(DeviceTypeEnum, values_callable=lambda x: [str(e.value) for e in DeviceTypeEnum]))
    ns = Column("NS", String(5), nullable=True)
    location_id = Column("LocationId", Integer, ForeignKey("Location.Id"), nullable=False)
    user_id = Column("UserId", Integer, ForeignKey("User.Id"), nullable=False)
    note = Column("Note", Text, nullable=True)
    status = Column("Status", Boolean, nullable=False, default=True)
    change_date = Column("Change_date", Date, nullable=False, default=date.today())

    def __repr__(self):
        return f"{self.id} - {self.name}"

    def return_status(self):
        return "aktivní" if self.status else "neaktivní"


class User(Base):
    __tablename__ = "User"
    id = Column("Id", Integer, primary_key=True, index=True)
    name = Column("Name", String(50), unique=True, nullable=False)
    email = Column("Email", String(50), nullable=False)
    status = Column("Status", Boolean, nullable=False, default=True)
    change_date = Column("Change_date", Date, nullable=False, default=date.today())
    children = relationship(Device)

    def __repr__(self):
        return f"{self.id} - {self.name}"

    def return_status(self):
        return "aktivní" if self.status else "neaktivní"


class Location(Base):
    __tablename__ = "Location"
    id = Column("Id", Integer, primary_key=True, index=True)
    name = Column("Name", String(50), unique=True, nullable=False)
    address = Column("Address", String(150), nullable=False)
    status = Column("Status", Boolean, nullable=False, default=True)
    change_date = Column("Change_date", Date, nullable=False, default=date.today())
    children = relationship(Device)

    def __repr__(self):
        return f"{self.id} - {self.name}"

    def return_status(self):
        return "aktivní" if self.status else "neaktivní"
