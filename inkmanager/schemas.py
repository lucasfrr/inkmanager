import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


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


class UserSchema(BaseModel):
    fullname: str
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    fullname: str
    model_config = ConfigDict(from_attributes=True)
