"""
Rotas de Artigos
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List

from app.core.database import get_db
from app.models import Article

router = APIRouter()


@router.get("/")
async def get_articles(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    country: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retorna artigos paginados do dia atual
    """
    # Data de hoje (início do dia)
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Query base
    query = db.query(Article).filter(Article.published_at >= today)

    # Filtro por país
    if country:
        query = query.filter(Article.country_code == country)

    # Contar total
    total = query.count()

    # Paginação
    offset = (page - 1) * limit
    articles = query.order_by(desc(Article.published_at)).offset(offset).limit(limit).all()

    return {
        "articles": [article.to_dict() for article in articles],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit  # ceil division
        }
    }


@router.get("/{article_id}")
async def get_article(
    article_id: str,
    db: Session = Depends(get_db)
):
    """
    Retorna um artigo específico
    """
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        return {"error": "Article not found"}, 404

    return article.to_dict()


@router.get("/stats/count")
async def get_articles_count(db: Session = Depends(get_db)):
    """
    Retorna contagem de artigos do dia
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    count = db.query(Article).filter(Article.published_at >= today).count()

    return {"count": count, "date": today.isoformat()}
