import io
import base64
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

from app.db.database import get_db
from app.db.models import Order
from app.api.auth import oauth2_scheme

router = APIRouter(tags=["Chart Visuals"])

@router.get("/chart")
async def get_vendor_chart(
    vendor_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    # Build data for the last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    result = await db.execute(
        select(
            func.strftime("%Y-%m-%d", Order.timestamp).label("date"),
            func.sum(Order.total_amount).label("revenue")
        )
        .where(
            Order.vendor_id == vendor_id,
            Order.timestamp >= seven_days_ago
        )
        .group_by("date")
        .order_by("date")
    )

    data = result.fetchall()
    if not data:
        raise HTTPException(status_code=404, detail="No data for chart.")

    dates = [row.date for row in data]
    revenues = [row.revenue for row in data]

    # Render a simple line chart
    fig, ax = plt.subplots()
    ax.plot(dates, revenues, marker="o", linestyle="-")
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue")
    ax.set_title(f"Revenue Trend for {vendor_id}")
    ax.grid(True)

    # Encode as base64
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")

    return {"vendor_id": vendor_id, "chart_base64": img_base64}

