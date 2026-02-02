"""
Modelo de Fonte de Notícias
"""
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class NewsSource(Base):
    __tablename__ = "news_sources"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    country_code = Column(String(2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "is_active": self.is_active,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
