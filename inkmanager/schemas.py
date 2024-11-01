import uuid
from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    detail: str


class ProductSchema(BaseModel):
    name: str
    amount: int


class ProductPublic(BaseModel):
    id: uuid.UUID
    name: str
    amount: int
    created_at: datetime
    updated_at: datetime


class ProductList(BaseModel):
    products: list[ProductPublic]


class ProductUpdate(BaseModel):
    name: str | None = None
    amount: int | None = None
