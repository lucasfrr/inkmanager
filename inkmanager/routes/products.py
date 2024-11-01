from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from inkmanager.database import get_session
from inkmanager.models import Product
from inkmanager.schemas import (
    Message,
    ProductList,
    ProductPublic,
    ProductSchema,
    ProductUpdate,
)

Session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/products', tags=['products'])


@router.post('/create', response_model=ProductPublic, status_code=201)
def create_product(product: ProductSchema, session: Session):
    db_product: Product = Product(name=product.name, amount=product.amount)

    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product


@router.get('/', response_model=ProductList)
def list_products(session: Session):
    products = session.scalars(select(Product)).all()

    return {'products': products}


@router.patch('/update/{product_id}', response_model=ProductPublic)
def update_product(product_id: str, product: ProductUpdate, session: Session):
    db_product = session.scalar(
        select(Product).where(Product.id == product_id)
    )

    if not db_product:
        raise HTTPException(status_code=404, detail='product not found')

    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)

    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product


@router.delete('/delete/{product_id}', response_model=Message)
def delete_product(product_id: str, session: Session):
    product = session.scalar(select(Product).where(Product.id == product_id))

    if not product:
        raise HTTPException(status_code=404, detail='product not found')

    session.delete(product)
    session.commit()

    return {'detail': 'task has been deleted successful'}
