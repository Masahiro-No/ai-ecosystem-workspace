from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.model import User
from api.auth.repository import AuthRepository
from api.auth.schema import UserResponse
from api.auth.service import EmailAlreadyExistsError, get_current_user
from api.users.schema import UpdateUserRequest
from db.database import get_db_session


async def get_all_users(
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(get_current_user),  # requires auth
) -> list[UserResponse]:
    repo = AuthRepository(session)
    users = await repo.get_all_users()
    return [UserResponse.model_validate(u) for u in users]


async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(get_current_user),
) -> UserResponse:
    repo = AuthRepository(session)
    user = await repo.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.model_validate(user)


async def update_user(
    user_id: int,
    payload: UpdateUserRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot modify another user")

    repo = AuthRepository(session)
    user = await repo.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # ตรวจว่า email ใหม่ซ้ำกับคนอื่นไหม
    existing = await repo.get_user_by_email(payload.email)
    if existing is not None and existing.id != user_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already taken")

    updated = await repo.update_user_email(user, payload.email)
    return UserResponse.model_validate(updated)


async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> dict:
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete another user")

    repo = AuthRepository(session)
    user = await repo.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    await repo.delete_user(user)
    return {"detail": "User deleted successfully"}
