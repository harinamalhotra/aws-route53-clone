from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import HostedZone
from schemas import (
    HostedZoneCreate,
    HostedZoneUpdate,
    HostedZoneResponse
)


router = APIRouter()


@router.get(
    "/",
    response_model=list[HostedZoneResponse]
)
def get_zones(
    search: str = "",
    db: Session = Depends(get_db)
):

    query = db.query(HostedZone)

    if search:
        query = query.filter(
            HostedZone.name.ilike(
                f"%{search}%"
            )
        )

    return query.order_by(
        HostedZone.id.desc()
    ).all()


@router.post(
    "/",
    response_model=HostedZoneResponse
)
def create_zone(
    data: HostedZoneCreate,
    db: Session = Depends(get_db)
):

    zone = HostedZone(
        name=data.name,
        zone_type=data.zone_type,
        comment=data.comment,
        user_id=1
    )

    db.add(zone)
    db.commit()
    db.refresh(zone)

    return zone


@router.get(
    "/{zone_id}",
    response_model=HostedZoneResponse
)
def get_zone(
    zone_id: int,
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

    return zone


@router.put(
    "/{zone_id}",
    response_model=HostedZoneResponse
)
def update_zone(
    zone_id: int,
    data: HostedZoneUpdate,
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

    if data.name is not None:
        zone.name = data.name

    if data.zone_type is not None:
        zone.zone_type = data.zone_type

    if data.comment is not None:
        zone.comment = data.comment

    db.commit()
    db.refresh(zone)

    return zone


@router.delete("/{zone_id}")
def delete_zone(
    zone_id: int,
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

    db.delete(zone)
    db.commit()

    return {
        "message": "Hosted zone deleted successfully"
    }