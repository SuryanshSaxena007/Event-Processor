from sqlalchemy import Column, String, Float, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
import datetime
import uuid

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    id           = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    vendor_id    = Column(String, index=True)
    order_id     = Column(String, index=True)
    items        = Column(JSON)
    total_amount = Column(Float)
    high_value   = Column(Boolean, default=False)
    is_anomalous   = Column(Boolean, default=False)    
    timestamp    = Column(DateTime, default=datetime.datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id              = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username        = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)