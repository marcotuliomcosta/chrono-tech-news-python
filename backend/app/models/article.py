"""
Modelo de Artigo/Notícia
"""
from sqlalchemy import Column, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class Article(Base):
    __tablename__ = "news_articles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    summary = Column(Text)
    content = Column(Text)
    url = Column(String, unique=True, nullable=False)
    image_url = Column(String)
    source_name = Column(String, nullable=False)
    country_code = Column(String(2))
    published_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "content": self.content,
            "url": self.url,
            "image_url": self.image_url,
            "source_name": self.source_name,
            "country_code": self.country_code,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
