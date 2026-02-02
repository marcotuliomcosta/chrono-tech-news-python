"""
Adiciona notícias de exemplo para testar
"""
from datetime import datetime, timedelta
from app.core.database import SessionLocal
from app.models.article import Article
import random

def add_sample_news():
    db = SessionLocal()

    sample_news = [
        {
            "title": "Python 3.13 traz melhorias significativas de performance",
            "summary": "A nova versão do Python inclui otimizações no interpretador que podem acelerar a execução em até 20%",
            "source_name": "Tecnoblog",
            "country_code": "BR"
        },
        {
            "title": "FastAPI se torna o framework Python mais popular para APIs",
            "summary": "Pesquisa mostra que FastAPI ultrapassou Flask em popularidade entre desenvolvedores",
            "source_name": "TechCrunch",
            "country_code": "US"
        },
        {
            "title": "IA generativa transforma desenvolvimento de software",
            "summary": "Ferramentas de IA estão mudando a forma como desenvolvedores escrevem código",
            "source_name": "The Verge",
            "country_code": "US"
        },
        {
            "title": "SQLite 3.45 lançado com novos recursos de performance",
            "summary": "O banco de dados mais usado do mundo recebe atualizações importantes",
            "source_name": "Olhar Digital",
            "country_code": "BR"
        },
        {
            "title": "GitHub Copilot agora oferece sugestões de código ainda melhores",
            "summary": "A ferramenta de IA da Microsoft recebe atualização com modelo de linguagem mais avançado",
            "source_name": "Gizmodo Brasil",
            "country_code": "BR"
        }
    ]

    try:
        now = datetime.now()

        for i, news in enumerate(sample_news):
            # Criar notícias em horários diferentes
            published_at = now - timedelta(hours=i)

            article = Article(
                title=news["title"],
                summary=news["summary"],
                url=f"https://example.com/news/{i}",
                source_name=news["source_name"],
                country_code=news["country_code"],
                published_at=published_at
            )
            db.add(article)
            print(f"[OK] Adicionada: {news['title'][:50]}...")

        db.commit()
        print(f"\n[OK] {len(sample_news)} notícias de exemplo criadas!")

    except Exception as e:
        print(f"[ERROR] {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("[*] Adicionando notícias de exemplo...\n")
    add_sample_news()
