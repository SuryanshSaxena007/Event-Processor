from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from app.db.database import get_db
from app.db.models import Order
from app.api.auth import oauth2_scheme

router = APIRouter(tags=["Vendor Metrics"])

@router.get("/")
async def get_vendor_metrics(
    vendor_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    # Total orders
    total_orders = (await db.execute(
        select(func.count()).where(Order.vendor_id == vendor_id)
    )).scalar()

    # Total revenue
    total_revenue = (await db.execute(
        select(func.coalesce(func.sum(Order.total_amount), 0))
        .where(Order.vendor_id == vendor_id)
    )).scalar()

    # High‑value orders
    high_value_orders = (await db.execute(
        select(func.count())
        .where(Order.vendor_id == vendor_id, Order.high_value == True)
    )).scalar()

    # Anomalous orders (if you added that column)
    anomalous_orders = (await db.execute(
        select(func.count())
        .where(Order.vendor_id == vendor_id, Order.is_anomalous == True)
    )).scalar()

    # Volume in the last 7 days, as YYYY‑MM‑DD strings
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    rows = await db.execute(
        select(
            func.strftime("%Y-%m-%d", Order.timestamp).label("date"),
            func.count().label("count")
        )
        .where(
            Order.vendor_id == vendor_id,
            Order.timestamp >= seven_days_ago
        )
        .group_by("date")
        .order_by("date")
    )
    last_7_days_volume = { row.date: row.count for row in rows.fetchall() }

    return {
        "vendor_id": vendor_id,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "high_value_orders": high_value_orders,
        "anomalous_orders": anomalous_orders,
        "last_7_days_volume": last_7_days_volume
    }

