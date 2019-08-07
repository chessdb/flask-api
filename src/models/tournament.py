from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from src.extensions import DB
from src.models import BaseModel


class Tournament(BaseModel):
    __tablename__ = "tournaments"

    id = DB.Column(UUID(as_uuid=True), primary_key=True)
    name = DB.Column(DB.String)
