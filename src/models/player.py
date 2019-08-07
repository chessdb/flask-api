import uuid
from datetime import date

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
    club_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("clubs.id"))
    elo = DB.Column(DB.Integer)
    lichess_username = DB.Column(DB.String)

    last_updated = DB.Column(DB.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, given_name: str = None, surname: str = None, date_of_birth: date = None, club_id: UUID = None,
                 elo: int = None, lichess_username: str = None):
        self.id = uuid.uuid4()
        self.given_name = given_name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.club_id = club_id
        self.elo = elo
        self.lichess_username = lichess_username

    def serialize(self) -> dict:
        return {
            "id": str(self.id),
            "given_name": self.given_name,
            "surname": self.surname,
            "date_of_birth": self.date_of_birth,
            "club_id": str(self.club_id),
            "lichess_username": self.lichess_username,
            "elo": self.elo,
        }
