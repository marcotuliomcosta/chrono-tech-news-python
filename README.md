# Chrono Tech News - Python Version

Agregador de notícias de tecnologia com análise por IA, construído com **Python (FastAPI)** + **React**.

## 🚀 Stack

**Backend:**
- Python 3.11+
- FastAPI (API REST)
- PostgreSQL (banco de dados)
- SQLAlchemy (ORM)
- APScheduler (cron jobs)
- OpenAI API (análise com IA)
- httpx + BeautifulSoup (scraping)

**Frontend:**
- React 18 + TypeScript
- Vite
- TailwindCSS + shadcn/ui

## 📁 Estrutura

```
chrono-tech-news-python/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/       # Rotas da API
│   │   ├── core/             # Configurações
│   │   ├── models/           # Modelos SQLAlchemy
│   │   ├── services/         # Lógica de negócio
│   │   └── db/               # Database setup
│   ├── tests/                # Testes
│   └── main.py               # Entry point
├── frontend/                 # React app
└── docker-compose.yml        # Docker setup
```

## 🛠️ Setup Local

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 🌐 URLs

- Backend API: http://localhost:8000
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

## ✨ Features

- ✅ Busca automática de notícias (cron a cada 30 min)
- ✅ Análise de notícias com IA
- ✅ Filtragem por país
- ✅ Paginação
- ✅ Histórico
- ✅ Resumo do período
- ✅ Polling inteligente no frontend
