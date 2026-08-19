<p align="center">
  <h1 align="center">🏛️ Public Pulse</h1>
  <p align="center">
    <strong>India's first Public Problem Discovery & Prioritization Platform — turning scattered citizen voices into a clear national agenda.</strong>
  </p>
  <p align="center">
    <a href="#-the-problem">The Problem</a> •
    <a href="#-the-solution">The Solution</a> •
    <a href="#-tech-stack">Tech Stack</a> •
    <a href="#-getting-started">Getting Started</a> •
    <a href="#-contributing">Contributing</a>
  </p>
</p>

---

## 🔴 The Problem

Every day, millions of Indians voice the same frustrations — bad roads, power cuts, water shortages, controversial bills, policy failures — across WhatsApp groups, Instagram, and Twitter. But these scattered voices never converge into a single, clear picture.

**The result:**

- 🏛️ **Governments** don't know what citizens actually prioritize
- 👥 **Citizens** don't know if millions of others face the same issue
- 🤝 **NGOs & Organizations** can't tell which problems affect the most people
- 📢 **Complaints stay loud but invisible** — no one is listening at scale

> **There is no single platform that answers: _"What are the most important problems people want solved right now?"_**

---

## 💡 The Solution

**Public Pulse** is a **Public Problem Discovery & Prioritization Platform** — a place where:

1. **Citizens report real problems** — from local potholes to national-level issues like parliamentary bills, policy changes, and systemic failures
2. **Communities validate and vote** — upvote issues that affect them, adding weight and legitimacy
3. **A transparent ranking emerges** — showing what matters most, right now, at every level

### What Makes This Different?

This is **not** just another complaint box or civic grievance portal. Public Pulse captures the **pulse of the nation** across every scale:

| Scope | Example Issues |
|-------|---------------|
| 🏘️ **Local** | Broken roads, water supply disruptions, garbage collection failures |
| 🏙️ **City-wide** | Public transport gaps, pollution spikes, housing shortages |
| 🗺️ **State-level** | Power grid failures, education policy, healthcare access |
| 🇮🇳 **National** | Parliamentary bills, economic policy, constitutional amendments, national security |

### Core Features

- 📝 **Problem Reporting** — Citizens submit issues with evidence (photos, documents, links) across any category and scale
- 🗳️ **Community Voting & Validation** — Upvote, discuss, and validate issues to surface what truly matters
- 📊 **Live Priority Rankings** — Transparent, real-time leaderboard of issues ranked by public urgency
- 🤖 **AI-Powered Deduplication** — Automatically detects and merges duplicate reports using semantic similarity
- 🗺️ **Spatial Intelligence** — Geolocation-powered clustering to identify regional problem hotspots
- 📈 **Trend Detection** — Track how issues gain or lose public attention over time
- 🔐 **Verified Identities** — Authenticated users for credible, accountable participation

---

## 🎯 Who Is This For?

| Stakeholder | Value |
|-------------|-------|
| **Citizens** | Finally see if your problem is shared by thousands — and push it up the priority ladder |
| **Government Bodies** | Data-driven insight into what citizens actually care about — no more guesswork |
| **NGOs & Activists** | Identify high-impact issues to rally behind with real community backing |
| **Media & Journalists** | Discover emerging public concerns before they become headlines |
| **Researchers** | Access structured, crowd-validated data on public sentiment and priorities |

---

## 🛠️ Tech Stack

| Layer        | Technology                                                                 |
| ------------ | -------------------------------------------------------------------------- |
| **Frontend** | [Next.js 16](https://nextjs.org/) · React 19 · TypeScript · Tailwind CSS 4 |
| **Backend**  | [FastAPI](https://fastapi.tiangolo.com/) · Python 3.11+ · Pydantic v2     |
| **Database** | PostgreSQL 15 + [pgvector](https://github.com/pgvector/pgvector) + PostGIS |
| **Cache**    | Redis 7                                                                    |
| **AI**       | OpenAI API (embeddings for duplicate detection & semantic search)           |
| **Auth**     | Supabase Auth                                                              |
| **Storage**  | Cloudflare R2 (evidence uploads)                                           |
| **DevOps**   | Docker Compose · Concurrently                                              |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Citizens (Browser)                      │
│          Report · Vote · Discover · Track Issues            │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │   Next.js Frontend      │
              │   (localhost:3000)       │
              └────────────┬────────────┘
                           │  REST API
              ┌────────────▼────────────┐
              │   FastAPI Backend       │
              │   AI Dedup · Ranking    │
              │   (localhost:8000)       │
              └──┬──────────────────┬───┘
                 │                  │
     ┌───────────▼───┐    ┌───────▼────────┐
     │  PostgreSQL   │    │     Redis      │
     │  + pgvector   │    │  (Rankings &   │
     │  + PostGIS    │    │   Caching)     │
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
│   ├── requirements.txt       # Python dependencies
│   └── pyproject.toml         # Linter config (Black & Ruff)
│
├── docker-compose.yml         # PostgreSQL + Redis services
├── package.json               # Monorepo scripts
├── .env.example               # Environment variable template
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ & npm
- **Python** 3.11+
- **Docker** & Docker Compose
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

Edit `.env` and configure your credentials:

| Variable                    | Description                         |
| --------------------------- | ----------------------------------- |
| `DATABASE_URL`              | PostgreSQL connection string        |
| `REDIS_URL`                 | Redis connection string             |
| `OPENAI_API_KEY`            | OpenAI API key (for AI dedup)       |
| `SUPABASE_URL`              | Supabase project URL                |
| `SUPABASE_ANON_KEY`         | Supabase anonymous key              |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key           |
| `CF_R2_ACCESS_KEY_ID`       | Cloudflare R2 access key            |
| `CF_R2_SECRET_ACCESS_KEY`   | Cloudflare R2 secret key            |
| `CF_R2_BUCKET_NAME`         | R2 bucket name for evidence storage |
| `CF_R2_ENDPOINT`            | R2 endpoint URL                     |

### 3. Start Infrastructure

```bash
npm run db:up
```

### 4. Install Dependencies

```bash
npm run install:all
```

### 5. Start Development Servers

```bash
npm run dev
```

| Service      | URL                                                    |
| ------------ | ------------------------------------------------------ |
| Frontend     | [http://localhost:3000](http://localhost:3000)          |
| Backend API  | [http://localhost:8000](http://localhost:8000)          |
| API Docs     | [http://localhost:8000/docs](http://localhost:8000/docs) |

---

## 🧰 Available Scripts

| Script               | Description                              |
| -------------------- | ---------------------------------------- |
| `npm run dev`        | Start frontend + backend concurrently    |
| `npm run dev:frontend` | Start Next.js dev server (port 3000)   |
| `npm run dev:backend`  | Start FastAPI dev server (port 8000)   |
| `npm run db:up`      | Start PostgreSQL + Redis containers      |
| `npm run db:down`    | Stop and remove containers               |
| `npm run install:all`| Install all frontend + backend deps      |

---

## 🧪 Running Tests

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm run lint
```

---

## 🗺️ Roadmap

- [x] Project scaffolding & monorepo setup
- [x] Backend API with FastAPI + health checks
- [x] Database infrastructure (PostgreSQL + pgvector + PostGIS)
- [x] Redis caching layer
- [ ] Problem submission & categorization system
- [ ] Community voting & validation engine
- [ ] Live priority ranking algorithm
- [ ] AI-powered duplicate detection pipeline
- [ ] Geospatial hotspot mapping
- [ ] Trend tracking & analytics dashboard
- [ ] User authentication & profiles
- [ ] Evidence upload system (photos, documents)
- [ ] National vs. local issue filtering
- [ ] Public API for NGOs & researchers

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
  <strong>🇮🇳 Built to amplify the voice of every citizen.</strong>
  <br/>
  Built with ❤️ by <a href="https://github.com/Charukesh-pyla">Charukesh Pyla</a>
</p>
