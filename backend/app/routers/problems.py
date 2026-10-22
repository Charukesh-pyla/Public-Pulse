"""
Problem CRUD router — submit, list, get, update, and delete public problems.
"""
import math
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.core.database import get_db
from backend.app.core.auth import get_current_user
from backend.app.models.user import User
from backend.app.models.problem import Problem, ProblemType, ProblemStatus, ProblemScope
from backend.app.models.vote import Vote
from backend.app.schemas.problem import (
    ProblemCreate,
    ProblemUpdate,
    ProblemResponse,
    ProblemListResponse,
)
from backend.app.schemas.user import UserResponse
from backend.app.schemas.category import CategoryResponse

router = APIRouter(prefix="/api/v1/problems", tags=["Problems"])


# ── Helpers ────────────────────────────────────────────────────────────────

def _build_problem_response(problem: Problem, has_voted: bool = False) -> ProblemResponse:
    """Convert a Problem ORM object to a ProblemResponse schema."""
    return ProblemResponse(
        id=problem.id,
        title=problem.title,
        description=problem.description,
        problem_type=problem.problem_type,
        status=problem.status,
        scope=problem.scope,
        location_name=problem.location_name,
        vote_count=problem.vote_count,
        evidence_count=problem.evidence_count,
        author=UserResponse.model_validate(problem.author),
        category=CategoryResponse.model_validate(problem.category) if problem.category else None,
        has_voted=has_voted,
        created_at=problem.created_at,
        updated_at=problem.updated_at,
    )


# ── Endpoints ──────────────────────────────────────────────────────────────

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ProblemResponse)
async def create_problem(
    payload: ProblemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit a new public problem report."""
    problem = Problem(
        title=payload.title,
        description=payload.description,
        problem_type=payload.problem_type,
        scope=payload.scope,
        location_name=payload.location_name,
        category_id=payload.category_id,
        author_id=current_user.id,
        status=ProblemStatus.pending_review,
    )

    # Set PostGIS point if coordinates provided
    if payload.latitude is not None and payload.longitude is not None:
        from geoalchemy2.elements import WKTElement
        problem.location = WKTElement(
            f"POINT({payload.longitude} {payload.latitude})", srid=4326
        )

    db.add(problem)
    await db.commit()
    await db.refresh(problem, attribute_names=["author", "category"])

    return _build_problem_response(problem, has_voted=False)


@router.get("", response_model=ProblemListResponse)
async def list_problems(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    sort: str = Query("votes", pattern="^(votes|recent|oldest)$", description="Sort order"),
    scope: Optional[ProblemScope] = Query(None, description="Filter by scope"),
    problem_type: Optional[ProblemType] = Query(None, description="Filter by type"),
    category_id: Optional[UUID] = Query(None, description="Filter by category"),
    status_filter: Optional[ProblemStatus] = Query(
        None, alias="status", description="Filter by status"
    ),
    search: Optional[str] = Query(None, max_length=200, description="Search title/description"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List problems with pagination, filtering, and sorting.
    By default returns published problems sorted by most votes.
    """
    # Base query
    query = select(Problem).options(
        selectinload(Problem.author),
        selectinload(Problem.category),
    )

    # Apply filters
    if status_filter:
        query = query.where(Problem.status == status_filter)
    else:
        # Default: only show published problems
        query = query.where(Problem.status == ProblemStatus.published)

    if scope:
        query = query.where(Problem.scope == scope)
    if problem_type:
        query = query.where(Problem.problem_type == problem_type)
    if category_id:
        query = query.where(Problem.category_id == category_id)
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            Problem.title.ilike(search_pattern) | Problem.description.ilike(search_pattern)
        )

    # Count total matching records
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Apply sorting
    if sort == "votes":
        query = query.order_by(desc(Problem.vote_count), desc(Problem.created_at))
    elif sort == "recent":
        query = query.order_by(desc(Problem.created_at))
    elif sort == "oldest":
        query = query.order_by(asc(Problem.created_at))

    # Apply pagination
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    problems = result.scalars().all()

    # Check which problems the current user has voted on
    if problems:
        problem_ids = [p.id for p in problems]
        votes_result = await db.execute(
            select(Vote.problem_id).where(
                Vote.user_id == current_user.id,
                Vote.problem_id.in_(problem_ids),
            )
        )
        voted_ids = set(votes_result.scalars().all())
    else:
        voted_ids = set()

    total_pages = math.ceil(total / per_page) if total > 0 else 1

    return ProblemListResponse(
        items=[
            _build_problem_response(p, has_voted=(p.id in voted_ids))
            for p in problems
        ],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
    )


@router.get("/{problem_id}", response_model=ProblemResponse)
async def get_problem(
    problem_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single problem by ID with full details."""
    result = await db.execute(
        select(Problem)
        .options(selectinload(Problem.author), selectinload(Problem.category))
        .where(Problem.id == problem_id)
    )
    problem = result.scalar_one_or_none()

    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Check if current user has voted
    vote_result = await db.execute(
        select(Vote).where(
            Vote.user_id == current_user.id, Vote.problem_id == problem_id
        )
    )
    has_voted = vote_result.scalar_one_or_none() is not None

    return _build_problem_response(problem, has_voted=has_voted)


@router.patch("/{problem_id}", response_model=ProblemResponse)
async def update_problem(
    problem_id: UUID,
    payload: ProblemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a problem. Only the author or a moderator can update."""
    result = await db.execute(
        select(Problem)
        .options(selectinload(Problem.author), selectinload(Problem.category))
        .where(Problem.id == problem_id)
    )
    problem = result.scalar_one_or_none()

    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Authorization: author or moderator
    if problem.author_id != current_user.id and not current_user.is_moderator:
        raise HTTPException(status_code=403, detail="Not authorized to update this problem")

    # Apply partial updates
    update_data = payload.model_dump(exclude_unset=True)

    # Handle coordinate updates → PostGIS point
    lat = update_data.pop("latitude", None)
    lng = update_data.pop("longitude", None)
    if lat is not None and lng is not None:
        from geoalchemy2.elements import WKTElement
        problem.location = WKTElement(f"POINT({lng} {lat})", srid=4326)

    # Only moderators can change status
    if "status" in update_data and not current_user.is_moderator:
        raise HTTPException(status_code=403, detail="Only moderators can change problem status")

    for field, value in update_data.items():
        setattr(problem, field, value)

    await db.commit()
    await db.refresh(problem, attribute_names=["author", "category"])

    return _build_problem_response(problem, has_voted=False)


@router.delete("/{problem_id}", status_code=status.HTTP_200_OK)
async def delete_problem(
    problem_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a problem. Only the author or a moderator can delete."""
    result = await db.execute(
        select(Problem).where(Problem.id == problem_id)
    )
    problem = result.scalar_one_or_none()

    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    if problem.author_id != current_user.id and not current_user.is_moderator:
        raise HTTPException(status_code=403, detail="Not authorized to delete this problem")

    await db.delete(problem)
    await db.commit()

    return {"message": "Problem deleted successfully", "success": True}
