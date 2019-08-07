import uuid

from sqlalchemy.dialects.postgresql import UUID

from src.extensions import DB
from src.models import BaseModel


class Ply(BaseModel):
    __tablename__ = "plies"
    id = DB.Column(UUID(as_uuid=True), primary_key=True)
    current_position = DB.Column(DB.String, DB.ForeignKey("positions.fen"))
    next_position = DB.Column(DB.String, DB.ForeignKey("positions.fen"))
    algebraic_notation = DB.Column(DB.String)  # ex: "e6".
    game_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("games.id"))

    def __init__(self, current_position: str, next_position: str, algebraic_notation: str, game_id: UUID):
        self.id = uuid.uuid4()
        self.current_position = current_position
        self.next_position = next_position
        self.algebraic_notation = algebraic_notation
        self.game_id = game_id
