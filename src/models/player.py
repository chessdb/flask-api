from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from src.extensions import DB
from src.models import BaseModel


class Player(BaseModel):
    __tablename__ = "players"

    id = DB.Column(UUID(as_uuid=True), primary_key=True)
    given_name = DB.Column(DB.String)
    surname = DB.Column(DB.String)
    date_of_birth = DB.Column(DB.Date)
    club_id = DB.Column(UUID, DB.ForeignKey("clubs.id"))

    last_updated = DB.Column(DB.DateTime(timezone=True), onupdate=func.now())
