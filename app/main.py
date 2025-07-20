from fastapi import FastAPI
from app.api.events import router as events_router
from app.api.metrics import router as metrics_router
from app.api.charts import router as charts_router
from app.api.auth import router as auth_router

app = FastAPI(title="BCN Event Processor")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(events_router, prefix="/events", tags=["Event Ingestion"])
app.include_router(metrics_router, prefix="/metrics", tags=["Vendor Metrics"])
app.include_router(charts_router, prefix="/metrics", tags=["Chart Visuals"])