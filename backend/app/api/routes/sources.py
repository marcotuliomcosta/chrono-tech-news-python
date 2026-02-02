"""
Rotas de Fontes de Notícias
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.models import NewsSource

router = APIRouter()


class SourceCreate(BaseModel):
    name: str
    url: str
    country_code: str | None = None


class SourceUpdate(BaseModel):
    name: str | None = None
    url: str | None = None
    is_active: bool | None = None
    country_code: str | None = None


@router.get("/")
async def get_sources(
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Retorna todas as fontes
    """
    query = db.query(NewsSource)

    if active_only:
        query = query.filter(NewsSource.is_active == True)

    sources = query.all()
    return {"sources": [source.to_dict() for source in sources]}


@router.post("/")
async def create_source(
    source_data: SourceCreate,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova fonte
    """
    source = NewsSource(
        name=source_data.name,
        url=source_data.url,
        country_code=source_data.country_code
    )

    db.add(source)
    db.commit()
    db.refresh(source)

    return source.to_dict()


@router.put("/{source_id}")
async def update_source(
    source_id: str,
    source_data: SourceUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza uma fonte
    """
    source = db.query(NewsSource).filter(NewsSource.id == source_id).first()

    if not source:
        return {"error": "Source not found"}, 404

    if source_data.name is not None:
        source.name = source_data.name
    if source_data.url is not None:
        source.url = source_data.url
    if source_data.is_active is not None:
        source.is_active = source_data.is_active
    if source_data.country_code is not None:
        source.country_code = source_data.country_code

    db.commit()
    db.refresh(source)

    return source.to_dict()


@router.delete("/{source_id}")
async def delete_source(
    source_id: str,
    db: Session = Depends(get_db)
):
    """
    Remove uma fonte
    """
    source = db.query(NewsSource).filter(NewsSource.id == source_id).first()

    if not source:
        return {"error": "Source not found"}, 404

    db.delete(source)
    db.commit()

    return {"message": "Source deleted"}
