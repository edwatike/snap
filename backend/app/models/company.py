from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from app.db import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    website = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    description = Column(Text)
    category = Column(String(100))
    location = Column(String(255))
    
    # Дополнительные данные в JSON
    metadata = Column(JSON, default={})
    
    # Статус валидации email
    email_valid = Column(Boolean, default=False)
    email_checked_at = Column(DateTime)
    
    # Системные поля
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Поля для рассылки
    last_email_sent_at = Column(DateTime)
    email_status = Column(String(50))  # sent, failed, bounced, etc
    campaign_id = Column(String(100))  # ID кампании рассылки 