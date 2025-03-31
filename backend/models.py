"""Defines database models for shoes, stores, alerts"""

from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone


# Base model for common shoe fields
class ShoeBase(SQLModel):
    date_added: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    name: str
    price: float
    url: str
    image_url: Optional[str] = None


class Shoe(ShoeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    store_id: Optional[int] = Field(default=None, foreign_key="store.id")
    store: Optional[Store] = Relationship(back_populates="shoes")

    price_alerts: List[PriceAlert] = Relationship(back_populates="shoe")
    price_history: List[PriceHistory] = Relationship(back_populates="shoe")



class ShoeUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[float] = None
    url: Optional[str] = None
    image_url: Optional[str] = None


class ShoeDisplay(ShoeBase):
    id: int
    store_id: int


# Store model
class StoreBase(SQLModel):
    name: str = Field(index=True, max_length=100)
    url: str


class Store(StoreBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shoes: List[Shoe] = Relationship(back_populates="store")


class StoreUpdate(SQLModel):
    name: Optional[str] = None
    url: Optional[str] = None


class StoreDisplay(StoreBase):
    id: int


# Price Alert model
class PriceAlertBase(SQLModel):
    current_price: float
    user_email: str
    date_added: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PriceAlert(PriceAlertBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shoe_id: Optional[int] = Field(default=None, foreign_key="shoe.id")
    shoe: Optional[Shoe] = Relationship(back_populates="price_alerts")


class PriceAlertUpdate(SQLModel):
    current_price: Optional[float] = None
    user_email: Optional[str] = None


class PriceAlertDisplay(PriceAlertBase):
    id: int
    shoe_id: int


class PriceAlertCreate(PriceAlertBase):
    pass


class PriceHistoryBase(SQLModel):
    date_recorded: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    price: float
    shoe_id: Optional[int] = Field(default=None, foreign_key="shoe.id")

class PriceHistory(PriceHistoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shoe: Optional[Shoe] = Relationship(back_populates="price_history")
    store: Optional[Store] = Relationship(back_populates="price_history")

