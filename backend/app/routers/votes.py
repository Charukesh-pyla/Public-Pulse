"""
Voting router — toggle votes on problems and check vote status.
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.auth import get_current_user
from backend.app.models.user import User
from backend.app.models.problem import Problem
from backend.app.models.vote import Vote
from backend.app.schemas.vote import VoteToggleResponse

router = APIRouter(prefix="/api/v1/problems", tags=["Votes"])


@router.post("/{problem_id}/vote", response_model=VoteToggleResponse)
async def toggle_vote(
    problem_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Toggle vote on a problem.
    - If not yet voted → cast vote, increment count.
    - If already voted → remove vote, decrement count.
    Returns the updated vote state and new vote count.
    """
    # Verify problem exists
    problem_result = await db.execute(
        select(Problem).where(Problem.id == problem_id)
    )
    problem = problem_result.scalar_one_or_none()

    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Check existing vote
    vote_result = await db.execute(
        select(Vote).where(
            Vote.user_id == current_user.id,
            Vote.problem_id == problem_id,
        )
    )
    existing_vote = vote_result.scalar_one_or_none()

    if existing_vote:
        # Remove vote
        await db.delete(existing_vote)
        # Decrement denormalized count (floor at 0)
        new_count = max(0, problem.vote_count - 1)
        await db.execute(
            update(Problem)
            .where(Problem.id == problem_id)
            .values(vote_count=new_count)
        )
        await db.commit()

        return VoteToggleResponse(
            voted=False,
            new_vote_count=new_count,
            message="Vote removed",
        )
    else:
        # Cast vote
        new_vote = Vote(user_id=current_user.id, problem_id=problem_id)
        db.add(new_vote)
        new_count = problem.vote_count + 1
        await db.execute(
            update(Problem)
            .where(Problem.id == problem_id)
            .values(vote_count=new_count)
        )
        await db.commit()

        return VoteToggleResponse(
            voted=True,
            new_vote_count=new_count,
            message="Vote cast successfully",
        )


@router.get("/{problem_id}/vote")
async def check_vote_status(
    problem_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Check if the current user has voted on a specific problem."""
    vote_result = await db.execute(
        select(Vote).where(
            Vote.user_id == current_user.id,
            Vote.problem_id == problem_id,
        )
    )
    existing_vote = vote_result.scalar_one_or_none()

    return {"voted": existing_vote is not None, "problem_id": str(problem_id)}
