from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from inkmanager.database import get_session
from inkmanager.models import Ink, User
from inkmanager.schemas import (
    FilterPage,
    InkList,
    InkPublic,
    InkSchema,
    InkUpdate,
    Message,
)
from inkmanager.security import get_current_user

DBSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
Filter = Annotated[FilterPage, Query()]

router = APIRouter(prefix='/inks', tags=['ink'])


@router.post(
    path='/create', status_code=HTTPStatus.CREATED, response_model=InkPublic
)
def create_ink(ink: InkSchema, session: DBSession, user: CurrentUser):
    db_ink = Ink(
        name=ink.name,
        brand=ink.brand,
        color=ink.color,
        weight=ink.weight,
        in_use=ink.in_use,
        user_id=user.id,
    )

    session.add(db_ink)
    session.commit()
    session.refresh(db_ink)

    return db_ink


@router.get(path='/', response_model=InkList)
def list_inks(session: DBSession, user: CurrentUser, filter: Filter):
    inks = session.scalars(
        select(Ink)
        .where(Ink.user_id == user.id)
        .offset(filter.offset)
        .limit(filter.limit)
    ).all()

    return {'inks': inks}


@router.get(path='/ink/{ink_id}', response_model=InkPublic)
def get_ink_by_id(session: DBSession, user: CurrentUser, ink_id: str):
    ink = session.scalar(
        select(Ink).where(Ink.id == ink_id, Ink.user_id == user.id)
    )

    if not ink:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='ink not found'
        )

    return ink


@router.patch(path='/update/{ink_id}', response_model=InkPublic)
def update_ink(
    session: DBSession, user: CurrentUser, ink_id: str, ink: InkUpdate
):
    db_ink = session.scalar(
        select(Ink).where(Ink.id == ink_id, Ink.user_id == user.id)
    )

    if not db_ink:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='ink not found'
        )

    for key, value in ink.model_dump(exclude_unset=True).items():
        setattr(db_ink, key, value)

    session.add(db_ink)
    session.commit()
    session.refresh(db_ink)

    return db_ink


@router.delete(path='/delete/{ink_id}', response_model=Message)
def delete_ink(session: DBSession, user: CurrentUser, ink_id: str):
    ink = session.scalar(
        select(Ink).where(Ink.id == ink_id, Ink.user_id == user.id)
    )

    if not ink:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='ink not found'
        )

    session.delete(ink)
    session.commit()

    return {'detail': 'ink has been deleted'}
