from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    home_address = Column("homeAddress", String(255), nullable=False)
    emission_factor = Column("emissionFactor", Float, nullable=False)
    consumption = Column(Float, nullable=False)
    study_settings = Column("studySettings", JSON, nullable=True)

    destinations = relationship("Destination", back_populates="vehicle", cascade="all, delete-orphan")


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    measurements = Column(String(255), default="")
    duration = Column(Integer, nullable=False)
    days = Column(JSON, nullable=False)
    distance = Column(Float, nullable=False)
    round_trip_distance = Column("roundTripDistance", Float, nullable=False)
    fuel_used = Column("fuelUsed", Float, nullable=False)
    co2_emissions = Column("co2Emissions", Float, nullable=False)

    vehicle = relationship("Vehicle", back_populates="destinations")
