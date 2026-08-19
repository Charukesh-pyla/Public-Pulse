<p align="center">
  <h1 align="center">🏛️ Public Pulse</h1>
  <p align="center">
    <strong>A civic-tech platform for crowdsourced public problem reporting with AI-powered deduplication and spatial intelligence.</strong>
  </p>
  <p align="center">
    <a href="#-getting-started">Getting Started</a> •
    <a href="#-tech-stack">Tech Stack</a> •
    <a href="#-architecture">Architecture</a> •
    <a href="#-api-reference">API Reference</a> •
    <a href="#-contributing">Contributing</a>
  </p>
</p>

---

## 📖 Overview

**Public Pulse** is a full-stack civic-tech platform that empowers citizens to report and track public infrastructure issues — from potholes and broken streetlights to water leaks and pollution. It leverages **AI-powered duplicate detection** (via OpenAI embeddings) and **spatial queries** (via PostGIS) to intelligently group similar reports, surface high-priority problems, and help local governments respond faster.

### Key Features

- 🗺️ **Spatial Intelligence** — Geolocation-based issue reporting with PostGIS-powered proximity queries
- 🤖 **AI Deduplication** — OpenAI-driven semantic similarity to automatically detect and merge duplicate reports
- ⚡ **Real-time Caching** — Redis-backed caching layer for lightning-fast response times
- 🔐 **Secure Authentication** — Supabase Auth integration for user management
- 📦 **Evidence Storage** — Cloudflare R2 for scalable media/evidence uploads
- 🩺 **Health Monitoring** — Built-in health checks for all services (database, cache)

---

## 🛠️ Tech Stack

| Layer        | Technology                                                                 |
| ------------ | -------------------------------------------------------------------------- |
| **Frontend** | [Next.js 16](https://nextjs.org/) · React 19 · TypeScript · Tailwind CSS 4 |
| **Backend**  | [FastAPI](https://fastapi.tiangolo.com/) · Python 3.11+ · Pydantic v2     |
| **Database** | PostgreSQL 15 + [pgvector](https://github.com/pgvector/pgvector) + PostGIS |
| **Cache**    | Redis 7                                                                    |
| **AI**       | OpenAI API (embeddings & semantic search)                                  |
| **Auth**     | Supabase Auth                                                              |
| **Storage**  | Cloudflare R2                                                              |
| **DevOps**   | Docker Compose · Concurrently                                              |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client (Browser)                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │   Next.js Frontend      │
              │   (localhost:3000)       │
              └────────────┬────────────┘
                           │  REST API
              ┌────────────▼────────────┐
              │   FastAPI Backend       │
              │   (localhost:8000)       │
              └──┬──────────────────┬───┘
                 │                  │
     ┌───────────▼───┐    ┌───────▼────────┐
     │  PostgreSQL   │    │     Redis      │
     │  + pgvector   │    │   (Cache)      │
     │  + PostGIS    │    │                │
     └───────────────┘    └────────────────┘
```

---

## 📁 Project Structure

```
Public Pulse/
├── frontend/                  # Next.js 16 frontend application
│   ├── src/
│   │   └── app/               # App Router (pages, layouts, styles)
│   ├── public/                # Static assets
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                   # FastAPI backend application
│   ├── app/
│   │   ├── core/              # Core configuration & infrastructure
│   │   │   ├── config.py      # Pydantic settings (env vars)
│   │   │   ├── database.py    # Async SQLAlchemy engine & sessions
│   │   │   └── redis.py       # Async Redis client
│   │   ├── routers/           # API route handlers
│   │   │   └── health.py      # Health check endpoint
│   │   └── main.py            # FastAPI app entrypoint
│   ├── tests/                 # Backend test suite
│   │   └── test_main.py
│   ├── requirements.txt       # Python dependencies
│   └── pyproject.toml         # Black & Ruff config
│
├── docker-compose.yml         # PostgreSQL + Redis services
├── package.json               # Monorepo scripts (concurrently)
├── .env.example               # Environment variable template
├── .gitignore
└── .prettierrc
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ & npm
- **Python** 3.11+
- **Docker** & Docker Compose (for PostgreSQL + Redis)
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/Charukesh-pyla/Public-Pulse.git
cd Public-Pulse
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your actual credentials:

| Variable                    | Description                         |
| --------------------------- | ----------------------------------- |
| `DATABASE_URL`              | PostgreSQL connection string        |
| `REDIS_URL`                 | Redis connection string             |
| `OPENAI_API_KEY`            | Your OpenAI API key                 |
| `SUPABASE_URL`              | Supabase project URL                |
| `SUPABASE_ANON_KEY`         | Supabase anonymous key              |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key           |
| `CF_R2_ACCESS_KEY_ID`       | Cloudflare R2 access key            |
| `CF_R2_SECRET_ACCESS_KEY`   | Cloudflare R2 secret key            |
| `CF_R2_BUCKET_NAME`         | R2 bucket name for evidence storage |
| `CF_R2_ENDPOINT`            | R2 endpoint URL                     |

### 3. Start Infrastructure (PostgreSQL + Redis)

```bash
npm run db:up
# or
docker-compose up -d
```

### 4. Install Dependencies

```bash
# Install all dependencies (frontend + backend)
npm run install:all

# Or install separately:
npm install --prefix frontend        # Frontend
pip install -r backend/requirements.txt  # Backend
```

### 5. Start Development Servers

```bash
# Start both frontend & backend concurrently
npm run dev
```

| Service      | URL                                                    |
| ------------ | ------------------------------------------------------ |
| Frontend     | [http://localhost:3000](http://localhost:3000)          |
| Backend API  | [http://localhost:8000](http://localhost:8000)          |
| API Docs     | [http://localhost:8000/docs](http://localhost:8000/docs) |
| ReDoc        | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

---

## 📡 API Reference

### Root

```
GET /
```

Returns API status and version info.

### Health Check

```
GET /health
```

Returns the health status of all dependent services:

```json
{
  "status": "healthy",
  "services": {
    "database": "online",
    "redis": "online"
  }
}
```

> Full interactive API documentation is available at `/docs` (Swagger UI) or `/redoc` in development mode.

---

## 🧪 Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend lint
cd frontend
npm run lint
```

---

## 🐳 Docker Services

The `docker-compose.yml` provisions the following services:

| Service      | Image                    | Port   | Description                           |
| ------------ | ------------------------ | ------ | ------------------------------------- |
| **db**       | `ankane/pgvector:15-postgis` | `5432` | PostgreSQL 15 with pgvector & PostGIS |
| **redis**    | `redis:7-alpine`         | `6379` | Redis 7 for caching                  |

Both services include health checks and persistent volumes (`pgdata`, `redisdata`).

```bash
npm run db:up    # Start services
npm run db:down  # Stop services
```

---

## 🧰 Available Scripts

| Script           | Command                        | Description                              |
| ---------------- | ------------------------------ | ---------------------------------------- |
| `npm run dev`    | Starts frontend + backend      | Runs both servers concurrently           |
| `npm run dev:frontend` | `next dev`               | Starts Next.js dev server on port 3000   |
| `npm run dev:backend`  | `uvicorn`                | Starts FastAPI dev server on port 8000   |
| `npm run db:up`  | `docker-compose up -d`         | Starts PostgreSQL + Redis containers     |
| `npm run db:down`| `docker-compose down`          | Stops and removes containers             |
| `npm run install:all` | Installs all deps         | Frontend npm + backend pip               |

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## 📄 License

This project is open source. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/Charukesh-pyla">Charukesh Pyla</a>
</p>
