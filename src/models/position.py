from src.extensions import DB
from src.models import BaseModel


class Position(BaseModel):
    __tablename__ = "positions"
    fen = DB.Column(DB.String, primary_key=True)
