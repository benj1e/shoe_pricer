from typing import List, Optional
from sqlmodel import Session, select
from ..models import PriceAlert


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


def delete_price_alert(price_alert_id: int, session: Session):
    """Delete a price alert from the database."""
    price_alert = session.get(PriceAlert, price_alert_id)
    if not price_alert:
        return None
    session.delete(price_alert)
    session.commit()
    return {"ok": True}
