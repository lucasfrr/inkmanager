import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 20


class Message(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


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


class InkSchema(BaseModel):
    name: str
    brand: str
    color: str
    weight: str
    in_use: bool


class InkPublic(BaseModel):
    id: uuid.UUID
    name: str
    brand: str
    color: str
    weight: str
    in_use: bool
    created_at: datetime
    updated_at: datetime


class InkList(BaseModel):
    inks: list[InkPublic]


class InkUpdate(BaseModel):
    name: str | None = None
    brand: str | None = None
    color: str | None = None
    weight: str | None = None
    in_use: bool | None = None


class NeedleSchema(BaseModel):
    name: str
    brand: str
    model: str
    size: str
    amount: int


class NeedlePublic(BaseModel):
    id: uuid.UUID
    name: str
    brand: str
    model: str
    size: str
    amount: int
    created_at: datetime
    updated_at: datetime


class NeddleList(BaseModel):
    needles: list[NeedlePublic]


class NeedleUpdate(BaseModel):
    name: str | None = None
    brand: str | None = None
    model: str | None = None
    size: str | None = None
    amount: int | None = None
