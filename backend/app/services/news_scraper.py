"""
Serviço de scraping de notícias
"""
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Article, NewsSource
from app.services.ai_analyzer import analyze_article


async def scrape_website(url: str, source_name: str) -> list:
    """
    Faz scraping de um site de notícias
    NOTA: Implementação simplificada - adaptar para cada site
    """
    articles = []

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Exemplo genérico - adaptar para cada site
        # Aqui você implementaria a lógica específica de cada fonte
        for article_tag in soup.find_all('article')[:10]:  # Limita a 10
            try:
                title = article_tag.find('h2').get_text(strip=True) if article_tag.find('h2') else None
                link = article_tag.find('a')['href'] if article_tag.find('a') else None
                img = article_tag.find('img')['src'] if article_tag.find('img') else None

                if title and link:
                    # Garantir URL absoluta
                    if not link.startswith('http'):
                        from urllib.parse import urljoin
                        link = urljoin(url, link)

                    articles.append({
                        'title': title,
                        'url': link,
                        'image_url': img,
                        'source_name': source_name
                    })
            except Exception as e:
                print(f"Erro ao processar artigo: {e}")
                continue

    except Exception as e:
        print(f"Erro ao fazer scraping de {url}: {e}")

    return articles


def scrape_and_save_news(db: Session):
    """
    Busca notícias de todas as fontes ativas e salva no banco
    """
    print("📰 Iniciando busca de notícias...")

    # Buscar fontes ativas
    sources = db.query(NewsSource).filter(NewsSource.is_active == True).all()

    if not sources:
        print("⚠️ Nenhuma fonte ativa encontrada")
        return

    total_saved = 0

    for source in sources:
        print(f"🔍 Buscando em: {source.name}")

        try:
            # Scraping (síncrono simplificado - melhorar para async)
            import asyncio
            articles = asyncio.run(scrape_website(source.url, source.name))

            for article_data in articles:
                try:
                    # Verificar se já existe
                    existing = db.query(Article).filter(Article.url == article_data['url']).first()

                    if existing:
                        continue

                    # Analisar com IA
                    analysis = analyze_article(
                        article_data['title'],
                        article_data.get('content', '')
                    )

                    # Criar artigo
                    article = Article(
                        title=article_data['title'],
                        url=article_data['url'],
                        image_url=article_data.get('image_url'),
                        source_name=source.name,
                        country_code=source.country_code,
                        summary=analysis.get('summary', ''),
                        published_at=datetime.now()
                    )

                    db.add(article)
                    db.commit()
                    total_saved += 1

                except IntegrityError:
                    db.rollback()
                    continue
                except Exception as e:
                    db.rollback()
                    print(f"Erro ao salvar artigo: {e}")
                    continue

        except Exception as e:
            print(f"Erro ao processar fonte {source.name}: {e}")
            continue

    print(f"✅ Busca concluída! {total_saved} notícias salvas")
    return total_saved
