from fastapi import APIRouter, HTTPException
from ..services.database import SessionDep
from ..models import Shoe, ShoeUpdate, ShoeDisplay, ShoeCreate
from sqlmodel import select


router = APIRouter(prefix="/shoes", tags=["shoes"])


@router.post("/", response_model=ShoeDisplay)
async def create_shoe(shoe: ShoeCreate, session: SessionDep):
    """Create a new shoe."""
    shoe = Shoe.model_validate(shoe)
    session.add(shoe)
    session.commit()
    session.refresh(shoe)
    return shoe


@router.get("/", response_model=list[Shoe])
async def read_shoes(session: SessionDep, offset: int = 0, limit: int = 100):
    """Get a list of shoes."""
    return session.exec(select(Shoe).offset(offset).limit(limit)).all()


@router.get("/{shoe_id}", response_model=ShoeDisplay)
async def read_shoe(shoe_id: int, session: SessionDep):
    """Get a shoe by ID."""
    return session.get(Shoe, shoe_id)


@router.patch("/{shoe_id}", response_model=ShoeDisplay)
async def update_shoe(shoe_id: int, shoe: ShoeUpdate, session: SessionDep):
    """Update a shoe by ID."""
    shoe_db = session.get(Shoe, shoe_id)  # get the shoe from the database
    if not shoe_db:
        raise HTTPException(status_code=404, detail="Shoe not found")
    shoe_data = shoe.model_dump(
        exclude_unset=True
    )  # shoe data as dict excluding unset values
    shoe_db.sqlmodel_update(shoe_data)  # update the shoe_db object with the new data
    session.add(shoe_db)
    session.commit()
    session.refresh(shoe_db)
    return shoe_db


@router.delete("/{shoe_id}", response_model=ShoeDisplay)
async def delete_shoe(shoe_id: int, session: SessionDep):
    """Delete a shoe by ID."""
    shoe = session.get(Shoe, shoe_id)
    if not shoe:
        raise HTTPException(status_code=404, detail="Shoe not found")
    session.delete(shoe)
    session.commit()
    return {"ok": True}
