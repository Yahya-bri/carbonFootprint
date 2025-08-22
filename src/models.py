from typing import List, Optional
from datetime import date
from sqlalchemy import ForeignKey, Column, String, Integer, DATE, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Sondeur(Base):
    __tablename__ = 'sondeurs'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    unites: Mapped[List["UniteTravail"]] = relationship(
        "UniteTravail", back_populates="sondeur", cascade="all, delete-orphan"
    )
    # Liste des essais accessibles via les unités de travail (read-only)
    essais: Mapped[List["Essai"]] = relationship("Essai", secondary="unite_travail", viewonly=True)


class Essai(Base):
    __tablename__ = 'essais'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    unites: Mapped[List["UniteTravail"]] = relationship(
        "UniteTravail", back_populates="essai", cascade="all, delete-orphan"
    )


class Chantier(Base):
    __tablename__ = 'chantiers'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    date: Mapped[Optional[date]] = mapped_column(DATE, nullable=True)

    unites: Mapped[List["UniteTravail"]] = relationship(
        "UniteTravail", back_populates="chantier", cascade="all, delete-orphan"
    )
    # Essais planifiés pour ce chantier (lecture seule, via les unités de travail)
    essais: Mapped[List["Essai"]] = relationship("Essai", secondary="unite_travail", viewonly=True)


class UniteTravail(Base):
    """Association object représentant une unité de travail:
    un essai à réaliser pour un chantier, affecté à un sondeur, avec date et durée.
    """
    __tablename__ = 'unite_travail'
    # Add an auto-increment ID to allow multiple sondeurs per chantier-essai
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chantier_id: Mapped[int] = mapped_column(ForeignKey("chantiers.id"))
    essai_id: Mapped[int] = mapped_column(ForeignKey("essais.id"))
    sondeur_id: Mapped[int] = mapped_column(ForeignKey("sondeurs.id"))
    days: Mapped[int] = mapped_column(Integer, nullable=False)
    date_debut: Mapped[Optional[date]] = mapped_column(DATE, nullable=True)
    # Carbon footprint fields
    distance_km: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    co2_kg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    chantier: Mapped[Chantier] = relationship("Chantier", back_populates="unites")
    essai: Mapped[Essai] = relationship("Essai", back_populates="unites")
    sondeur: Mapped[Sondeur] = relationship("Sondeur", back_populates="unites")


