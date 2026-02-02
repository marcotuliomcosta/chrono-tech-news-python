"""
Serviço de análise com IA (OpenAI)
"""
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None


def analyze_article(title: str, content: str) -> dict:
    """
    Analisa um artigo e gera resumo com IA
    """
    if not client or not settings.OPENAI_API_KEY:
        return {
            "summary": title,  # Fallback: usa o título como resumo
            "relevance": "medium"
        }

    try:
        prompt = f"""
Analise esta notícia de tecnologia e forneça:
1. Um resumo em 2-3 frases
2. Relevância (high/medium/low)

Título: {title}
Conteúdo: {content[:1000]}

Responda em JSON:
{{
    "summary": "...",
    "relevance": "..."
}}
"""

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Você é um analista de notícias de tecnologia."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        result = response.choices[0].message.content

        # Parse JSON
        import json
        return json.loads(result)

    except Exception as e:
        print(f"Erro na análise com IA: {e}")
        return {
            "summary": title,
            "relevance": "medium"
        }
