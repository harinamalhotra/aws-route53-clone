from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from datetime import datetime

from database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    zones = relationship(
        "HostedZone",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class HostedZone(Base):

    __tablename__ = "hosted_zones"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255),
        nullable=False,
        index=True
    )

    zone_type = Column(
        String(50),
        default="Public"
    )

    comment = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="zones"
    )

    records = relationship(
        "DNSRecord",
        back_populates="zone",
        cascade="all, delete-orphan"
    )


class DNSRecord(Base):

    __tablename__ = "dns_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    zone_id = Column(
        Integer,
        ForeignKey("hosted_zones.id"),
        nullable=False
    )

    name = Column(
        String(255),
        nullable=False
    )

    type = Column(
        String(20),
        nullable=False
    )

    ttl = Column(
        Integer,
        default=300
    )

    value = Column(
        Text,
        nullable=False
    )

    routing_policy = Column(
        String(50),
        default="Simple"
    )

    zone = relationship(
        "HostedZone",
        back_populates="records"
    )