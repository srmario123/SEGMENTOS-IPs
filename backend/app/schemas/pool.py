from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


class PoolBase(BaseModel):
    name: str
    description: str | None = None


class PoolCreate(PoolBase):
    pass


class PoolUpdate(PoolBase):
    pass


class PoolRead(ORMModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
