"""
Scheduler para jobs automáticos (cron)
"""
from apscheduler.schedulers.background import BackgroundScheduler
from app.core.config import settings
from app.core.database import SessionLocal
from app.services.news_scraper import scrape_and_save_news

scheduler = BackgroundScheduler()


def fetch_news_job():
    """
    Job que busca notícias periodicamente
    """
    print("[*] Executando job de busca de noticias...")
    db = SessionLocal()
    try:
        scrape_and_save_news(db)
        print("[OK] Job concluido com sucesso")
    except Exception as e:
        print(f"[ERROR] Erro no job: {e}")
    finally:
        db.close()


def start_scheduler():
    """
    Inicia o scheduler com todos os jobs
    """
    # Job: Buscar notícias a cada X minutos
    scheduler.add_job(
        fetch_news_job,
        'interval',
        minutes=settings.FETCH_NEWS_INTERVAL_MINUTES,
        id='fetch_news',
        replace_existing=True
    )

    scheduler.start()
    print(f"[OK] Scheduler iniciado - Job rodara a cada {settings.FETCH_NEWS_INTERVAL_MINUTES} min")


def shutdown_scheduler():
    """
    Para o scheduler
    """
    if scheduler.running:
        scheduler.shutdown()
        print("[*] Scheduler parado")
