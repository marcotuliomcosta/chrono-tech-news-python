"""
Rotas do Scraper
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.news_scraper import scrape_and_save_news

router = APIRouter()


@router.post("/fetch")
async def fetch_news(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Dispara busca manual de notícias (roda em background)
    """
    background_tasks.add_task(scrape_and_save_news, db)

    return {"message": "News fetch started in background"}


@router.get("/status")
async def scraper_status():
    """
    Status do scraper
    """
    return {"status": "ready"}
