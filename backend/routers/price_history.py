from fastapi import APIRouter, Depends, HTTPException
from ..services.database import SessionDep
from ..models import (
    PriceHistory,
    PriceHistoryCreate,
    PriceHistoryDisplay,
    PriceHistoryUpdate,
)
from sqlmodel import select


router = APIRouter(prefix="/price_history", tags=["price_history"])


# GET request
@router.get("/", response_model=list[PriceHistoryDisplay])
async def read_price_history(session: SessionDep, offset: int = 0, limit: int = 100):
    return session.exec(select(PriceHistory).offset(offset).limit(limit)).all()


@router.get("/{price_history_id}", response_model=PriceHistoryDisplay)
async def read_price_history_by_id(session: SessionDep, price_history_id: int):
    return session.get(PriceHistory, price_history_id)


# POST request
@router.post("/", response_model=PriceHistoryDisplay)
async def add_price_history(session: SessionDep, price_history: PriceHistoryCreate):
    price_history = PriceHistory.model_validate(price_history)
    session.add(price_history)
    session.commit()
    session.refresh(price_history)
    return price_history


# PATCH request
@router.patch("/{price_history_id}", response_model=PriceHistoryDisplay)
async def update_price_history(
    session: SessionDep, price_history_id: int, price_history: PriceHistoryUpdate
):
    price_history_db = session.get(PriceHistory, price_history_id)
    if not price_history_db:
        raise HTTPException(404, detail="Price history entry not found!")
    price_history_data = price_history_db.model_dump(exclude_unset=True)
    price_history_db.sqlmodel_update(price_history_data)
    session.add(price_history_db)
    session.commit()
    session.refresh(price_history_db)
    return price_history_db


# DELETE request
@router.delete("/{price_history_id}", response_model=PriceHistoryDisplay)
async def delete_price_history(session: SessionDep, price_history_id: int):
    price_history = session.get(PriceHistory, price_history_id)
    if not price_history:
        raise HTTPException(404, detail="Price history entry not found!")

    session.delete(price_history)
    session.commit()
    return {"ok": True}
