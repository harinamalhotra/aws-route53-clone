from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# =========================
# AUTHENTICATION
# =========================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# =========================
# HOSTED ZONES
# =========================

class HostedZoneCreate(BaseModel):
    name: str
    zone_type: str = "Public"
    comment: Optional[str] = None


class HostedZoneUpdate(BaseModel):
    name: Optional[str] = None
    zone_type: Optional[str] = None
    comment: Optional[str] = None


class HostedZoneResponse(BaseModel):
    id: int
    name: str
    zone_type: str
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# DNS RECORDS
# =========================

class DNSRecordCreate(BaseModel):
    name: str
    type: str
    ttl: int = 300
    value: str
    routing_policy: str = "Simple"


class DNSRecordUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    ttl: Optional[int] = None
    value: Optional[str] = None
    routing_policy: Optional[str] = None


class DNSRecordResponse(BaseModel):
    id: int
    zone_id: int
    name: str
    type: str
    ttl: int
    value: str
    routing_policy: str

    class Config:
        from_attributes = True