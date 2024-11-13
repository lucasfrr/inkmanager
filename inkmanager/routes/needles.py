from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from inkmanager.database import get_session
from inkmanager.models import Needle, User
from inkmanager.schemas import (
    FilterPage,
    Message,
    NeddleList,
    NeedlePublic,
    NeedleSchema,
    NeedleUpdate,
)
from inkmanager.security import get_current_user

DBSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
Filter = Annotated[FilterPage, Query()]

router = APIRouter(prefix='/needles', tags=['needles'])


@router.post(
    path='/create', status_code=HTTPStatus.CREATED, response_model=NeedlePublic
)
def create_needle(needle: NeedleSchema, session: DBSession, user: CurrentUser):
    db_needle = Needle(
        name=needle.name,
        brand=needle.brand,
        model=needle.model,
        size=needle.size,
        amount=needle.amount,
        user_id=user.id,
    )

    session.add(db_needle)
    session.commit()
    session.refresh(db_needle)

    return db_needle


@router.get(path='/', response_model=NeddleList)
def list_needles(session: DBSession, user: CurrentUser, filter: Filter):
    needles = session.scalars(
        select(Needle)
        .where(Needle.user_id == user.id)
        .offset(filter.offset)
        .limit(limit=filter.limit)
    ).all()

    return {'needles': needles}


@router.get('/needle/{needle_id}', response_model=NeedlePublic)
def get_needle_by_id(needle_id: str, session: DBSession, user: CurrentUser):
    needle = session.scalar(
        select(Needle).where(Needle.id == needle_id, Needle.user_id == user.id)
    )

    if not needle:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='needle not found'
        )

    return needle


@router.patch(path='/update/{needle_id}', response_model=NeedlePublic)
def update_needle(
    needle_id: str, needle: NeedleUpdate, session: DBSession, user: CurrentUser
):
    db_needle = session.scalar(
        select(Needle).where(Needle.id == needle_id, Needle.user_id == user.id)
    )

    if not db_needle:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='needle not found'
        )

    for key, value in needle.model_dump(exclude_unset=True).items():
        setattr(db_needle, key, value)

    session.add(db_needle)
    session.commit()
    session.refresh(db_needle)

    return db_needle


@router.delete(path='/delete/{needle_id}', response_model=Message)
def delete_model(needle_id: str, session: DBSession, user: CurrentUser):
    needle = session.scalar(
        select(Needle).where(Needle.id == needle_id, Needle.user_id == user.id)
    )

    if not needle:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='needle not found'
        )

    session.delete(needle)
    session.commit()

    return {'detail': 'needle has been deleted'}
