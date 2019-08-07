from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from src.extensions import DB
from src.models import BaseModel


class Game(BaseModel):
    __tablename__ = "games"
    id = DB.Column(UUID(as_uuid=True), primary_key=True)
    white = DB.Column(UUID, DB.ForeignKey("players.id"))
    black = DB.Column(UUID, DB.ForeignKey("players.id"))
    tournament_id = DB.Column(UUID, DB.ForeignKey("tournaments.id"))
    result = DB.Column(DB.Integer)  # TODO MAKE ENUM
    playing_round = DB.Column(DB.Integer)
    utc_date = DB.Column(DB.Date)
    utc_time = DB.Column(DB.Time(timezone=True))

    parsed_timestamp = DB.Column(DB.DateTime(timezone=True), server_default=func.now())
