import uuid
from datetime import datetime

from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from src.extensions import DB
from src.models import BaseModel


class Game(BaseModel):
    __tablename__ = "games"
    id = DB.Column(UUID(as_uuid=True), primary_key=True)
    white = DB.Column(UUID(as_uuid=True), DB.ForeignKey("players.id"))
    black = DB.Column(UUID(as_uuid=True), DB.ForeignKey("players.id"))
    tournament_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("tournaments.id"))
    result = DB.Column(DB.String)  # TODO MAKE ENUM
    playing_round = DB.Column(DB.Integer)
    utc_date = DB.Column(DB.Date)
    utc_time = DB.Column(DB.Time(timezone=True))
    white_elo = DB.Column(DB.Integer)
    black_elo = DB.Column(DB.Integer)
    eco = DB.Column(DB.String)
    time_control = DB.Column(DB.String)
    variant = DB.Column(DB.String)
    site = DB.Column(DB.String)
    raw = DB.Column(DB.String, unique=True)
    parsed_timestamp = DB.Column(DB.DateTime(timezone=True), server_default=func.now())

    def __init__(self, white, black, result, utc_date, white_elo, black_elo, eco, time_control, variant, site, raw,
                 tournament_id=None, playing_round=None, utc_time=None):
        self.id = uuid.uuid4()
        self.white = white
        self.black = black
        self.tournament_id = tournament_id
        self.result = result
        self.playing_round = playing_round
        self.utc_date = utc_date
        self.utc_time = utc_time
        self.white_elo = white_elo
        self.black_elo = black_elo
        self.eco = eco
        self.time_control = time_control
        self.variant = variant
        self.site = site
        self.raw = raw

    @classmethod
    def lichess(cls, **kwargs):
        # Event, Site, Date, Round, White, Black, Result, BlackElo, WhiteElo, ECO, TimeControl, UTCDate, UTCTime
        utc_date = datetime.strptime(kwargs.get("UTCDate"), "%Y.%m.%d").date()
        playing_round = kwargs.get("Round")
        playing_round = None if playing_round == "-" else int(playing_round)

        white_elo = kwargs.get("WhiteElo")
        white_elo = None if white_elo == "?" else int(white_elo)
        black_elo = kwargs.get("BlackElo")
        black_elo = None if black_elo == "?" else int(black_elo)

        return cls(
            white=kwargs.get("white"),
            black=kwargs.get("black"),
            result=kwargs.get("Result"),
            playing_round=playing_round,
            utc_date=utc_date,
            white_elo=white_elo,
            black_elo=black_elo,
            time_control=kwargs.get("TimeControl"),
            variant=kwargs.get("Variant"),
            eco=kwargs.get("ECO"),
            site=kwargs.get("Site"),
            raw=kwargs.get("raw")
        )

    @classmethod
    def standard(cls, **kwargs):
        # Event, Site, Date, Round, White, Black, Result, WhiteElo, BlackElo, Event, TimeControl, Date
        utc_date = kwargs.get("Date")
        utc_date = None if "?" in utc_date else utc_date
        if utc_date:
            utc_date = datetime.strptime(utc_date, "%Y.%m.%d").date()

        playing_round = kwargs.get("Round")
        playing_round = str(playing_round).replace(".", "")
        try:
            playing_round = int(playing_round)
        except TypeError:
            playing_round = None
        except ValueError:
            playing_round = None

        white_elo = kwargs.get("WhiteElo")
        try:
            white_elo = int(white_elo)
        except TypeError:
            white_elo = None
        black_elo = kwargs.get("BlackElo")
        try:
            black_elo = int(black_elo)
        except TypeError:
            black_elo = None

        return cls(
            white=kwargs.get("white"),
            black=kwargs.get("black"),
            result=kwargs.get("Result"),
            playing_round=playing_round,
            utc_date=utc_date,
            white_elo=white_elo,
            black_elo=black_elo,
            time_control=kwargs.get("TimeControl"),
            variant=kwargs.get("Variant"),
            eco=kwargs.get("ECO"),
            site=kwargs.get("Site"),
            raw=kwargs.get("raw")
        )

    def serialize(self) -> dict:
        return {
            "id": str(self.id),
            "white": str(self.white),
            "black": str(self.black),
            "tournament_id": str(self.tournament_id),
            "result": self.result,
            "round": self.playing_round,
            "utc_date": self.utc_date.strftime("%Y-%m-%d"),
            "white_elo": self.white_elo,
            "black_elo": self.black_elo,
            "eco": self.eco,
            "time_control": self.time_control,
            "variant": self.variant,
            "site": self.site,
            "raw": self.raw
        }
