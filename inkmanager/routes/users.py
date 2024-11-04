from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from inkmanager.database import get_session
from inkmanager.models import User
from inkmanager.schemas import Message, UserPublic, UserSchema
from inkmanager.security import get_password_hash

Session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/register', response_model=UserPublic, status_code=HTTPStatus.CREATED
)
def register_user(user: UserSchema, session: Session):
    db_user = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )

    print('verificou o user')

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='email already exists',
            )

    hashed_pass = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        password=hashed_pass,
        email=user.email,
        fullname=user.fullname,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.patch('/update/{user_id}', response_model=UserPublic)
def update_user(user_id: str, user: UserSchema, session: Session):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='user not found'
        )

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.delete('/delete/{user_id}', response_model=Message)
def delete_user(user_id: str, session: Session):
    user = session.scalar(select(User).where(User.id == user_id))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='user not found'
        )

    session.delete(user)
    session.commit()

    return {'detail': 'user has been deleted'}
