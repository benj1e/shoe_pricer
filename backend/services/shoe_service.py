from sqlmodel import Session, select
from ..models import Shoe, ShoeDisplay, ShoeUpdate
from typing import List, Optional


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
