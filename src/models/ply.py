from sqlalchemy.dialects.postgresql import UUID

from src.extensions import DB
from src.models import BaseModel


class Ply(BaseModel):
    __tablename__ = "plies"
    id = DB.Column(UUID(as_uuid=True), primary_key=True)
    current_position = DB.Column(DB.String, DB.ForeignKey("positions.fen"))
    next_position = DB.Column(DB.String, DB.ForeignKey("positions.fen"))
    algebraic_notation = DB.Column(DB.String)  # ex: "e6".
    game_id = DB.Column(UUID, DB.ForeignKey("games.id"))
