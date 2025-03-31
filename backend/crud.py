"""Define functions for interacting with the database."""

from sqlmodel import Session, select
from typing import List, Optional
from .models import *


# SHOE OPERATIONS
def add_shoe(shoe: Shoe, session: Session) -> ShoeDisplay:
    """Add a shoe to the database."""
    session.add(shoe)
    session.commit()
    session.refresh(shoe)
    return shoe


def get_shoe_by_id(shoe_id: int, session: Session) -> Optional[ShoeDisplay]:
    """Get a shoe by its ID."""
    return session.get(Shoe, shoe_id)


def get_shoes(session: Session, offset: int = 0, limit: int = 25) -> List[ShoeDisplay]:
    """Get all shoes in the database."""
    return session.exec(select(Shoe).offset(offset).limit(limit)).all()


def update_shoe(shoe: ShoeUpdate, session: Session) -> ShoeDisplay:
    """Update a shoe in the database."""
    shoe_db = session.get(Shoe, shoe.id)
    if not shoe_db:
        return None
    shoe_data = shoe.model_dump(exclude_unset=True)
    shoe_db.sqlmodel_update(shoe_data)
    session.add(shoe_db)
    session.commit()
    session.refresh(shoe_db)
    return shoe_db


def delete_shoe(shoe_id: int, session: Session) -> Optional[ShoeDisplay]:
    """Delete a shoe from the database."""
    shoe = session.get(Shoe, shoe_id)
    if not shoe:
        return None
    session.delete(shoe)
    session.commit()
    return {"ok": True}


# STORE OPERATIONS
def add_store(store: Store, session: Session) -> Store:
    """Add a store to the database."""
    session.add(store)
    session.commit()
    session.refresh(store)
    return store


def get_store_by_id(store_id: int, session: Session) -> Optional[Store]:
    """Get a store by its ID."""
    return session.get(Store, store_id)


def get_stores(session: Session, offset: int = 0, limit: int = 25) -> List[Store]:
    """Get all stores in the database."""
    return session.exec(select(Store).offset(offset).limit(limit)).all()


# PRICE ALERT OPERATIONS
def add_price_alert(price_alert: PriceAlert, session: Session) -> PriceAlert:
    """Add a price alert to the database."""
    session.add(price_alert)
    session.commit()
    session.refresh(price_alert)
    return price_alert


def get_price_alert_by_id(
    price_alert_id: int, session: Session
) -> Optional[PriceAlert]:
    """Get a price alert by its ID."""
    return session.get(PriceAlert, price_alert_id)


def get_price_alerts(
    session: Session, offset: int = 0, limit: int = 25
) -> List[PriceAlert]:
    """Get all price alerts in the database."""
    return session.exec(select(PriceAlert).offset(offset).limit(limit)).all()
