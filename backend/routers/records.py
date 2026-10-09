from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import DNSRecord, HostedZone
from schemas import (
    DNSRecordCreate,
    DNSRecordUpdate,
    DNSRecordResponse
)


router = APIRouter()


VALID_RECORD_TYPES = {
    "A",
    "AAAA",
    "CNAME",
    "TXT",
    "MX",
    "NS",
    "PTR",
    "SRV",
    "CAA"
}


@router.get(
    "/zones/{zone_id}/records",
    response_model=list[DNSRecordResponse]
)
def get_records(
    zone_id: int,
    search: str = "",
    db: Session = Depends(get_db)
):

    zone = db.query(
        HostedZone
    ).filter(
        HostedZone.id == zone_id
    ).first()

    if not zone:
        raise HTTPException(
            status_code=404,
            detail="Hosted zone not found"
        )

    query = db.query(
        DNSRecord
    ).filter(
        DNSRecord.zone_id == zone_id
    )

    if search:
        query = query.filter(
            DNSRecord.name.ilike(
                f"%{search}%"
            )
        )

    return query.order_by(
        DNSRecord.id.desc()
    ).all()


@router.post(
    "/zones/{zone_id}/records",
    response_model=DNSRecordResponse
)
def create_record(
    zone_id: int,
    data: DNSRecordCreate,
    db: Session = Depends(get_db)
):

    zone = db.query(
        HostedZone
    ).filter(
        HostedZone.id == zone_id
    ).first()

    if not zone:
        raise HTTPException(
            status_code=404,
            detail="Hosted zone not found"
        )

    if data.type not in VALID_RECORD_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid DNS record type"
        )

    record = DNSRecord(
        zone_id=zone_id,
        name=data.name,
        type=data.type,
        ttl=data.ttl,
        value=data.value,
        routing_policy=data.routing_policy
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@router.put(
    "/records/{record_id}",
    response_model=DNSRecordResponse
)
def update_record(
    record_id: int,
    data: DNSRecordUpdate,
    db: Session = Depends(get_db)
):

    record = db.query(
        DNSRecord
    ).filter(
        DNSRecord.id == record_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    if data.name is not None:
        record.name = data.name

    if data.type is not None:

        if data.type not in VALID_RECORD_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Invalid record type"
            )

        record.type = data.type

    if data.ttl is not None:
        record.ttl = data.ttl

    if data.value is not None:
        record.value = data.value

    if data.routing_policy is not None:
        record.routing_policy = data.routing_policy

    db.commit()
    db.refresh(record)

    return record


@router.delete("/records/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db)
):

    record = db.query(
        DNSRecord
    ).filter(
        DNSRecord.id == record_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    db.delete(record)
    db.commit()

    return {
        "message": "Record deleted successfully"
    }