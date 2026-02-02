"""
Script para adicionar fontes de notícias ao banco
"""
import sys
from app.core.database import SessionLocal
from app.models.source import NewsSource

def add_default_sources():
    """Adiciona fontes padrão de tecnologia"""
    db = SessionLocal()

    sources = [
        {
            "name": "Tecnoblog",
            "url": "https://tecnoblog.net",
            "country_code": "BR",
            "is_active": True
        },
        {
            "name": "Gizmodo Brasil",
            "url": "https://gizmodo.uol.com.br",
            "country_code": "BR",
            "is_active": True
        },
        {
            "name": "Olhar Digital",
            "url": "https://olhardigital.com.br",
            "country_code": "BR",
            "is_active": True
        },
        {
            "name": "The Verge",
            "url": "https://www.theverge.com",
            "country_code": "US",
            "is_active": True
        },
        {
            "name": "TechCrunch",
            "url": "https://techcrunch.com",
            "country_code": "US",
            "is_active": True
        }
    ]

    try:
        for source_data in sources:
            # Verificar se já existe
            existing = db.query(NewsSource).filter(
                NewsSource.url == source_data["url"]
            ).first()

            if not existing:
                source = NewsSource(**source_data)
                db.add(source)
                print(f"[OK] Adicionada: {source_data['name']}")
            else:
                print(f"[SKIP] Já existe: {source_data['name']}")

        db.commit()
        print(f"\n[OK] {len(sources)} fontes configuradas!")

    except Exception as e:
        print(f"[ERROR] {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("[*] Adicionando fontes de notícias...\n")
    add_default_sources()
