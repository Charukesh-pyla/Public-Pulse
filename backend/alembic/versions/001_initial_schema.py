"""Initial schema — users, categories, problems, votes, evidence

Revision ID: 001_initial_schema
Revises: None
Create Date: 2026-10-14
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = "001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Enable required PostgreSQL extensions ──
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    op.execute("CREATE EXTENSION IF NOT EXISTS \"postgis\";")
    op.execute("CREATE EXTENSION IF NOT EXISTS \"vector\";")

    # ── Enums ──
    problem_type_enum = sa.Enum("community", "curated", name="problem_type_enum")
    problem_status_enum = sa.Enum(
        "draft", "pending_review", "published", "rejected", "resolved",
        name="problem_status_enum",
    )
    problem_scope_enum = sa.Enum("local", "city", "state", "national", name="problem_scope_enum")
    file_type_enum = sa.Enum("image", "video", "document", "link", name="file_type_enum")

    problem_type_enum.create(op.get_bind(), checkfirst=True)
    problem_status_enum.create(op.get_bind(), checkfirst=True)
    problem_scope_enum.create(op.get_bind(), checkfirst=True)
    file_type_enum.create(op.get_bind(), checkfirst=True)

    # ── Users ──
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("supabase_id", sa.String(255), unique=True, nullable=True),
        sa.Column("display_name", sa.String(100), nullable=False),
        sa.Column("avatar_url", sa.Text, nullable=True),
        sa.Column("reputation", sa.Integer, server_default="0", nullable=False),
        sa.Column("is_moderator", sa.Boolean, server_default="false", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_supabase_id", "users", ["supabase_id"], unique=True)

    # ── Categories ──
    op.create_table(
        "categories",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("name", sa.String(100), unique=True, nullable=False),
        sa.Column("slug", sa.String(100), unique=True, nullable=False),
        sa.Column("icon", sa.String(10), nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("color", sa.String(7), nullable=True),
    )
    op.create_index("ix_categories_slug", "categories", ["slug"], unique=True)

    # ── Problems ──
    op.create_table(
        "problems",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("problem_type", problem_type_enum, nullable=False, server_default="community"),
        sa.Column("status", problem_status_enum, nullable=False, server_default="pending_review"),
        sa.Column("scope", problem_scope_enum, nullable=False, server_default="local"),
        sa.Column("location_name", sa.String(255), nullable=True),
        # PostGIS geometry column
        sa.Column("location", sa.Column("location", sa.Text, nullable=True)),  # Placeholder
        # vote/evidence counters
        sa.Column("vote_count", sa.Integer, server_default="0", nullable=False),
        sa.Column("evidence_count", sa.Integer, server_default="0", nullable=False),
        # Foreign keys
        sa.Column("author_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("category_id", UUID(as_uuid=True), sa.ForeignKey("categories.id"), nullable=True),
        # Timestamps
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    # Add PostGIS geometry column properly
    op.execute("ALTER TABLE problems DROP COLUMN IF EXISTS location;")
    op.execute("SELECT AddGeometryColumn('problems', 'location', 4326, 'POINT', 2);")
    # Add pgvector embedding column
    op.execute("ALTER TABLE problems ADD COLUMN embedding vector(1536);")

    op.create_index("ix_problems_vote_count", "problems", ["vote_count"])
    op.create_index("ix_problems_status_votes", "problems", ["status", "vote_count"])
    op.create_index("ix_problems_scope", "problems", ["scope"])
    op.create_index("ix_problems_created_at", "problems", ["created_at"])

    # ── Votes ──
    op.create_table(
        "votes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("problem_id", UUID(as_uuid=True), sa.ForeignKey("problems.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "problem_id", name="uq_user_problem_vote"),
    )

    # ── Evidence ──
    op.create_table(
        "evidence",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("problem_id", UUID(as_uuid=True), sa.ForeignKey("problems.id"), nullable=False),
        sa.Column("uploaded_by", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("file_url", sa.Text, nullable=False),
        sa.Column("file_type", file_type_enum, nullable=False, server_default="image"),
        sa.Column("caption", sa.String(300), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("evidence")
    op.drop_table("votes")
    op.drop_table("problems")
    op.drop_table("categories")
    op.drop_table("users")

    # Drop enums
    op.execute("DROP TYPE IF EXISTS file_type_enum;")
    op.execute("DROP TYPE IF EXISTS problem_scope_enum;")
    op.execute("DROP TYPE IF EXISTS problem_status_enum;")
    op.execute("DROP TYPE IF EXISTS problem_type_enum;")

    # Don't drop extensions — they may be used by other DBs
