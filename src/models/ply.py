import uuid

from sqlalchemy.dialects.postgresql import UUID

from src.extensions import DB
from src.models import BaseModel


class Ply(BaseModel):
    __tablename__ = "plies"
    id = DB.Column(UUID(as_uuid=True), primary_key=True)
    current_position = DB.Column(DB.String, DB.ForeignKey("positions.fen"))
    next_position = DB.Column(DB.String, DB.ForeignKey("positions.fen"))
    game_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("games.id"))
    __table_args__ = (
        DB.UniqueConstraint("current_position",
                            "next_position",
                            "game_id",
                            name="unique_ply",
                            ),
    )

    def __init__(self, current_position: str, next_position: str, game_id: UUID):
        self.id = uuid.uuid4()
        self.current_position = current_position
        self.next_position = next_position
        self.game_id = game_id
