from fastapi import APIRouter, Depends, HTTPException, status
from ..services.database import SessionDep
from ..models import Store, StoreUpdate, StoreDisplay, StoreCreate
from sqlmodel import select
from typing import List


router = APIRouter(prefix="/stores", tags=["stores"])


# GET request
@router.get("/", response_model=List[Store])
async def read_stores(session: SessionDep, offset: int = 0, limit: int = 100):
    """Get a list of stores."""
    return session.exec(select(Store).offset(offset).limit(limit)).all()


@router.get("/{store_id}", response_model=StoreDisplay)
async def read_store(store_id: int, session: SessionDep):
    """Get a store by ID."""
    store = session.get(Store, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


# POST request
@router.post("/", response_model=StoreDisplay, status_code=status.HTTP_201_CREATED)
async def create_store(store: StoreCreate, session: SessionDep):
    """Create a new store."""
    store = Store.model_validate(store)
    session.add(store)
    session.commit()
    session.refresh(store)
    return store


# PATCH request
@router.patch("/{store_id}", response_model=StoreDisplay)
async def update_store(store_id: int, store: StoreUpdate, session: SessionDep):
    """Update a store by ID."""
    store_db = session.get(Store, store_id)  # get the store from the database
    if not store_db:
        raise HTTPException(status_code=404, detail="Store not found")
    store_data = store.model_dump(
        exclude_unset=True
    )  # store data as dict excluding unset values
    store_db.sqlmodel_update(store_data)  # update the store_db object with the new data
    session.add(store_db)
    session.commit()
    session.refresh(store_db)
    return store_db


# DELETE request
@router.delete("/{store_id}", response_model=StoreDisplay)
async def delete_store(store_id: int, session: SessionDep):
    """Delete a store by ID."""
    store = session.get(Store, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    session.delete(store)
    session.commit()
    return {"ok": True}
