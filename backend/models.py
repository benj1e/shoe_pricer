"""Defines database models for shoes, stores, alerts"""

from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Mapped


class StoreBase(SQLModel):
    name: str
    url: str | None = None
    img_url: str | None = None


class Store(StoreBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date_added: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    shoes: list["Shoe"] = Relationship(back_populates="store")


class StoreDisplay(StoreBase):
    id: int


class StoreUpdate(StoreBase):
    name: str | None = None
    url: str | None = None
    img_url: str | None = None


class StoreCreate(StoreBase):
    pass


class ShoeBase(SQLModel):
    name: str
    brand: str | None = None
    price: int
    category: str | None = None


class Shoe(ShoeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    store_id: int | None = Field(default=None, foreign_key="store.id")
    date_added: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    price_history: list["PriceHistory"] = Relationship(back_populates="shoe")
    store: Optional["Store"] = Relationship(back_populates="shoes")


class ShoeCreate(ShoeBase):
    store_id: int | None = None


class ShoeDisplay(ShoeBase):
    id: int
    store_id: int | None


class ShoeUpdate(ShoeBase):
    name: str | None = None
    brand: str | None = None
    price: int | None = None
    store_id: int | None = None


class PriceHistoryBase(SQLModel):
    price: int


class PriceHistory(PriceHistoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date_added: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    shoe_id: int | None = Field(default=None, foreign_key="shoe.id")
    shoe: Optional["Shoe"] = Relationship(back_populates="price_history")


class PriceHistoryDisplay(PriceHistoryBase):
    id: int
    shoe_id: int | None = None
    date_added: datetime | None = None


class PriceHistoryUpdate(PriceHistoryBase):
    id: int | None = None
    price: int | None = None
    shoe_id: int | None = None
    date_added: datetime | None = None


class PriceHistoryCreate(PriceHistoryBase):
    shoe_id: int | None = Field(default=None, foreign_key="shoe.id")


class PriceAlert(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    message: str
