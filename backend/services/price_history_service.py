from sqlmodel import Session, select
from typing import List, Optional
from ..models import PriceHistory, PriceAlert, Shoe

def add_price_history(price_history: PriceHistory, session: Session) -> PriceHistory:
    """Add a price history entry to the database."""
    session.add(price_history)
    session.commit()
    session.refresh(price_history)
    return price_history

def delete_price_history(price_history_id: int, session: Session) -> Optional[PriceHistory]:
    """Delete a price history entry from the database."""
    price_history = session.get(PriceHistory, price_history_id)
    if not price_history:
        return None
    session.delete(price_history)
    session.commit()
    return {"ok": True}