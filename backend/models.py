from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    home_address = Column("homeAddress", String(500), nullable=False)
    emission_factor = Column("emissionFactor", Float, nullable=False, default=2.31)
    consumption = Column(Float, nullable=False, default=8.5)
    study_settings = Column("studySettings", JSON, nullable=True)

    destinations = relationship("Destination", back_populates="vehicle", cascade="all, delete-orphan", order_by="Destination.id")


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    measurements = Column(String(500), default="")
    duration = Column(Float, nullable=False, default=4)
    days = Column(JSON, nullable=False, default=[1])
    distance = Column(Float, nullable=False, default=0)
    round_trip_distance = Column("roundTripDistance", Float, nullable=False, default=0)
    fuel_used = Column("fuelUsed", Float, nullable=False, default=0)
    co2_emissions = Column("co2Emissions", Float, nullable=False, default=0)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)

    vehicle = relationship("Vehicle", back_populates="destinations")
