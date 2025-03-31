from typing import List, Optional
from sqlmodel import Session, select
from ..models import Store


def add_store(store: Store, session: Session) -> Store:
    """Add a store to the database."""
    session.add(store)
    session.commit()
    session.refresh(store)
    return store


def get_store_by_id(store_id: int, session: Session) -> Optional[Store]:
    """Get a store by its ID."""
    return session.get(Store, store_id)


def update_store(store: Store, session: Session) -> Store:
    """Update a store in the database."""
    db_store = session.get(Store, store.id)
    if not db_store:
        return None
    store_data = store.model_dump(exclude_unset=True)
    db_store.sqlmodel_update(store_data)
    session.add(db_store)
    session.commit()
    session.refresh(db_store)
    return db_store


def get_stores(session: Session, offset: int = 0, limit: int = 25) -> List[Store]:
    """Get all stores in the database."""
    return session.exec(select(Store).offset(offset).limit(limit)).all()


def delete_store(store_id: int, session: Session) -> Optional[Store]:
    """Delete a store from the database."""
    store = session.get(Store, store_id)
    if not store:
        return None
    session.delete(store)
    session.commit()
    return {"ok": True}
