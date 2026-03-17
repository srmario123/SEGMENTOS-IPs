from datetime import datetime

from pydantic import EmailStr

from app.schemas.common import ORMModel


class UserRead(ORMModel):
    id: int
    username: str
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
