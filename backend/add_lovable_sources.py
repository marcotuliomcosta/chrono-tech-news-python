"""
Adiciona todas as fontes do projeto Lovable
"""
from app.core.database import SessionLocal
from app.models.source import NewsSource

def add_lovable_sources():
    db = SessionLocal()

    # Todas as 21 fontes do Lovable
    sources = [
        # Brasil - 14 fontes
        {"name": "Tecnoblog", "url": "https://tecnoblog.net/", "country_code": "BR"},
        {"name": "Meio Bit", "url": "https://meiobit.com/", "country_code": "BR"},
        {"name": "TechTudo", "url": "https://www.techtudo.com.br/", "country_code": "BR"},
        {"name": "Gizmodo Brasil", "url": "https://gizmodo.uol.com.br/", "country_code": "BR"},
        {"name": "Exame Tecnologia", "url": "https://exame.com/tecnologia/", "country_code": "BR"},
        {"name": "StartSe", "url": "https://www.startse.com/", "country_code": "BR"},
        {"name": "The Hack", "url": "https://thehack.com.br/", "country_code": "BR"},
        {"name": "Mobile Time", "url": "https://www.mobiletime.com.br/", "country_code": "BR"},
        {"name": "Convergência Digital", "url": "https://www.convergenciadigital.com.br/", "country_code": "BR"},
        {"name": "BRStack", "url": "https://brstack.com.br/", "country_code": "BR"},
        {"name": "InfoQ Brasil", "url": "https://www.infoq.com/br/", "country_code": "BR"},
        {"name": "Canaltech", "url": "https://canaltech.com.br/", "country_code": "BR"},
        {"name": "Olhar Digital", "url": "https://olhardigital.com.br/", "country_code": "BR"},
        {"name": "TecMundo", "url": "https://www.tecmundo.com.br/", "country_code": "BR"},

        # Estados Unidos - 7 fontes
        {"name": "TechCrunch", "url": "https://techcrunch.com/", "country_code": "US"},
        {"name": "The Verge", "url": "https://www.theverge.com/", "country_code": "US"},
        {"name": "Wired", "url": "https://www.wired.com/", "country_code": "US"},
        {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/", "country_code": "US"},
        {"name": "VentureBeat AI", "url": "https://venturebeat.com/ai/", "country_code": "US"},
        {"name": "AI News", "url": "https://artificialintelligence-news.com/", "country_code": "US"},
        {"name": "Machine Learning Mastery", "url": "https://machinelearningmastery.com/", "country_code": "US"},
    ]

    try:
        # Limpa fontes existentes para evitar duplicatas
        db.query(NewsSource).delete()
        db.commit()
        print("[*] Fontes anteriores removidas\n")

        # Adiciona todas as fontes
        for source_data in sources:
            source = NewsSource(
                name=source_data["name"],
                url=source_data["url"],
                country_code=source_data["country_code"],
                is_active=True
            )
            db.add(source)
            print(f"[OK] Adicionada: {source_data['name']} ({source_data['country_code']})")

        db.commit()
        print(f"\n[OK] {len(sources)} fontes do Lovable adicionadas com sucesso!")

    except Exception as e:
        print(f"[ERROR] {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("[*] Adicionando fontes do Lovable...\n")
    add_lovable_sources()
