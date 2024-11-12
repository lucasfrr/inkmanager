from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from inkmanager.database import get_session
from inkmanager.models import User
from inkmanager.schemas import Message, UserPublic, UserSchema
from inkmanager.security import get_current_user, get_password_hash

DBSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    path='/register', response_model=UserPublic, status_code=HTTPStatus.CREATED
)
def register_user(user: UserSchema, session: DBSession):
    db_user = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )

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


@router.put(path='/update/{user_id}', response_model=UserPublic)
def update_user(
    user_id: str,
    user: UserSchema,
    session: DBSession,
    current_user: CurrentUser,
):
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='not enough permissions'
        )

    try:
        for key, value in user.model_dump(exclude_unset=True).items():
            if key == 'password':
                current_user.password = get_password_hash(value)

            setattr(current_user, key, value)

        session.add(current_user)
        session.commit()
        session.refresh(current_user)

        return current_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='username or email already exists',
        )


@router.delete(path='/delete/{user_id}', response_model=Message)
def delete_user(
    user_id: str,
    session: DBSession,
    current_user: CurrentUser,
):
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'detail': 'user has been deleted'}
