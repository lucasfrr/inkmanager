from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from inkmanager.database import get_session
from inkmanager.models import Product, User
from inkmanager.schemas import (
    FilterPage,
    Message,
    ProductList,
    ProductPublic,
    ProductSchema,
    ProductUpdate,
)
from inkmanager.security import get_current_user

DBSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
Filter = Annotated[FilterPage, Query()]

router = APIRouter(prefix='/products', tags=['products'])


@router.post(
    path='/create',
    response_model=ProductPublic,
    status_code=HTTPStatus.CREATED,
)
def create_product(
    product: ProductSchema, session: DBSession, user: CurrentUser
):
    db_product = Product(
        name=product.name, amount=product.amount, user_id=user.id
    )

    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product


@router.get(path='/', response_model=ProductList)
def list_products(
    session: DBSession, user: CurrentUser, filter_products: Filter
):
    products = session.scalars(
        select(Product)
        .where(Product.user_id == user.id)
        .offset(filter_products.offset)
        .limit(filter_products.limit)
    ).all()

    return {'products': products}


@router.get(path='/{product_id}', response_model=ProductPublic)
def get_product_by_id(session: DBSession, product_id: str, user: CurrentUser):
    product = session.scalar(
        select(Product).where(
            Product.id == product_id, Product.user_id == user.id
        )
    )

    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='product not found'
        )

    return product


@router.patch(path='/update/{product_id}', response_model=ProductPublic)
def update_product(
    product_id: str,
    product: ProductUpdate,
    session: DBSession,
    user: CurrentUser,
):
    db_product = session.scalar(
        select(Product).where(
            Product.id == product_id, Product.user_id == user.id
        )
    )

    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='product not found'
        )

    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)

    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product


@router.delete(path='/delete/{product_id}', response_model=Message)
def delete_product(product_id: str, session: DBSession):
    product = session.scalar(select(Product).where(Product.id == product_id))

    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='product not found'
        )

    session.delete(product)
    session.commit()

    return {'detail': 'product has been deleted'}
