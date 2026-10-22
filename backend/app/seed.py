"""
Seed script — populates the database with default categories and sample problems.
Run: python -m backend.app.seed
"""
import asyncio
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from backend.app.core.database import SessionLocal, engine, Base
from backend.app.models import User, Category, Problem, Vote
from backend.app.models.problem import ProblemType, ProblemStatus, ProblemScope


# ── Default Categories ─────────────────────────────────────────────────────

DEFAULT_CATEGORIES = [
    {"name": "Infrastructure", "slug": "infrastructure", "icon": "🏗️", "color": "#f59e0b", "description": "Roads, bridges, buildings, water supply, drainage"},
    {"name": "Power & Energy", "slug": "power-energy", "icon": "⚡", "color": "#ef4444", "description": "Electricity outages, transformer faults, energy policy"},
    {"name": "Healthcare", "slug": "healthcare", "icon": "🏥", "color": "#10b981", "description": "Hospital issues, medicine shortages, public health"},
    {"name": "Education", "slug": "education", "icon": "📚", "color": "#6366f1", "description": "Schools, universities, examination systems, policies"},
    {"name": "Water & Sanitation", "slug": "water-sanitation", "icon": "💧", "color": "#0ea5e9", "description": "Water supply, sewage, drainage, cleanliness"},
    {"name": "Transport", "slug": "transport", "icon": "🚌", "color": "#8b5cf6", "description": "Public transport, traffic, road safety"},
    {"name": "Governance", "slug": "governance", "icon": "🏛️", "color": "#ec4899", "description": "Policy failures, corruption, bureaucratic issues"},
    {"name": "Environment", "slug": "environment", "icon": "🌱", "color": "#22c55e", "description": "Pollution, deforestation, climate impact"},
    {"name": "Public Safety", "slug": "public-safety", "icon": "🛡️", "color": "#f97316", "description": "Crime, safety hazards, emergency response"},
    {"name": "Digital & Telecom", "slug": "digital-telecom", "icon": "📡", "color": "#14b8a6", "description": "Internet connectivity, telecom failures, digital services"},
]


# ── Sample Problems ────────────────────────────────────────────────────────

MOCK_USER_ID = uuid.UUID("00000000-0000-4000-8000-000000000001")

SAMPLE_PROBLEMS = [
    {
        "title": "NEET Entrance Exam System Failure",
        "description": "Reported irregularities and paper leaks in the national medical college entrance exam, affecting over 2 million students nationwide. Multiple centers reported question paper distribution before official start time.",
        "problem_type": ProblemType.curated,
        "status": ProblemStatus.published,
        "scope": ProblemScope.national,
        "location_name": "National / Multi-State",
        "vote_count": 14205,
        "evidence_count": 184,
        "category_slug": "education",
    },
    {
        "title": "Sector 4 Burnt Distribution Transformer",
        "description": "Main transformer burnt out yesterday at 14:20 PM. Sparks observed before total power failure. Entire sector currently without electricity. Over 200 families affected.",
        "problem_type": ProblemType.community,
        "status": ProblemStatus.published,
        "scope": ProblemScope.local,
        "location_name": "Plot 42, Sector 4, Indiranagar",
        "vote_count": 342,
        "evidence_count": 3,
        "category_slug": "power-energy",
    },
    {
        "title": "Major Pothole Bottleneck on NH-48",
        "description": "Deep potholes spanning across three lanes right after the airport exit bridge. Heavy traffic jams and minor accidents observed daily during peak hours. Multiple vehicles damaged.",
        "problem_type": ProblemType.community,
        "status": ProblemStatus.published,
        "scope": ProblemScope.city,
        "location_name": "NH-48 Expressway, Exit 4",
        "vote_count": 728,
        "evidence_count": 12,
        "category_slug": "infrastructure",
    },
    {
        "title": "Government Hospital Medicine Shortage",
        "description": "Outpatient pharmacy is out of primary diabetes (Metformin) and hypertension (Amlodipine) medications for the past three weeks. Patients forced to buy from expensive private pharmacies.",
        "problem_type": ProblemType.curated,
        "status": ProblemStatus.published,
        "scope": ProblemScope.state,
        "location_name": "State General Hospital Network",
        "vote_count": 894,
        "evidence_count": 22,
        "category_slug": "healthcare",
    },
    {
        "title": "Contaminated Water Supply in Ward 17",
        "description": "Residents reporting muddy, foul-smelling water from municipal taps for the past 10 days. Several children hospitalized with gastrointestinal issues. Water testing results pending from authorities.",
        "problem_type": ProblemType.community,
        "status": ProblemStatus.published,
        "scope": ProblemScope.local,
        "location_name": "Ward 17, Vijayanagar",
        "vote_count": 1156,
        "evidence_count": 8,
        "category_slug": "water-sanitation",
    },
    {
        "title": "Bus Route 42 Cancelled Without Notice",
        "description": "The city transport authority cancelled Bus Route 42 (Central Station → Industrial Area) without prior announcement. Over 3,000 daily commuters left stranded with no alternative public transport.",
        "problem_type": ProblemType.community,
        "status": ProblemStatus.published,
        "scope": ProblemScope.city,
        "location_name": "Central Station Bus Terminal",
        "vote_count": 567,
        "evidence_count": 5,
        "category_slug": "transport",
    },
]


async def seed():
    """Seed the database with default categories and sample problems."""
    async with SessionLocal() as session:
        # ── 1. Create mock user if not exists ──
        result = await session.execute(select(User).where(User.id == MOCK_USER_ID))
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                id=MOCK_USER_ID,
                display_name="Dev User",
                supabase_id=None,
                reputation=100,
            )
            session.add(user)
            print("✅ Created mock dev user")
        else:
            print("⏭️  Mock dev user already exists")

        # ── 2. Seed categories ──
        category_map = {}
        for cat_data in DEFAULT_CATEGORIES:
            result = await session.execute(
                select(Category).where(Category.slug == cat_data["slug"])
            )
            existing = result.scalar_one_or_none()
            if not existing:
                category = Category(**cat_data)
                session.add(category)
                category_map[cat_data["slug"]] = category
                print(f"  ✅ Category: {cat_data['icon']} {cat_data['name']}")
            else:
                category_map[cat_data["slug"]] = existing
                print(f"  ⏭️  Category already exists: {cat_data['name']}")

        await session.flush()  # Flush to get category IDs

        # ── 3. Seed sample problems ──
        result = await session.execute(select(Problem).limit(1))
        if result.scalar_one_or_none() is not None:
            print("\n⏭️  Problems already seeded, skipping")
        else:
            for prob_data in SAMPLE_PROBLEMS:
                category_slug = prob_data.pop("category_slug")
                category = category_map.get(category_slug)
                problem = Problem(
                    **prob_data,
                    author_id=MOCK_USER_ID,
                    category_id=category.id if category else None,
                )
                session.add(problem)
                print(f"  ✅ Problem: {prob_data['title'][:50]}...")

        await session.commit()
        print("\n🎉 Seed complete!")


if __name__ == "__main__":
    print("🌱 Seeding Public Pulse database...\n")
    asyncio.run(seed())
