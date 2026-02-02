"""
Chrono Tech News - Python FastAPI Backend
Entry point da aplicação
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import articles, sources, scraper
from app.services.scheduler import start_scheduler, shutdown_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação
    """
    # Startup
    print("[*] Iniciando Chrono Tech News...")

    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    print("[OK] Tabelas criadas/verificadas")

    # Iniciar scheduler (cron jobs)
    if settings.CRON_ENABLED:
        start_scheduler()
        print(f"[*] Scheduler iniciado (intervalo: {settings.FETCH_NEWS_INTERVAL_MINUTES} min)")

    yield

    # Shutdown
    print("[*] Encerrando aplicação...")
    if settings.CRON_ENABLED:
        shutdown_scheduler()


app = FastAPI(
    title="Chrono Tech News API",
    description="API para agregação de notícias de tecnologia com análise por IA",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(articles.router, prefix="/api/articles", tags=["articles"])
app.include_router(sources.router, prefix="/api/sources", tags=["sources"])
app.include_router(scraper.router, prefix="/api/scraper", tags=["scraper"])


@app.get("/")
async def root():
    return {
        "message": "Chrono Tech News API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
