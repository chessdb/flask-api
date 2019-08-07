from http import HTTPStatus

from flask_restplus import Namespace, fields, Resource

from src.api.v1.games.decorators import is_pgn_file, save_pgn_file
from src.api.v1.games.request_parsers import PGN_UPLOAD
from src.models.game import Game

GAMES = Namespace(name="games", description="Endpoints for games.")

MODEL = GAMES.model(
    name="user_model",
    model={
        "id": fields.String(),
        "white": fields.String(),
        "black": fields.String(),
        "tournament_id": fields.String(),
        "result": fields.String(),
        "playing_round": fields.Integer(),
        "utc_date": fields.Date()
    }
)


@GAMES.route("/")
class Games(Resource):
    def get(self):
        results = Game.query.all()
        return Game.serialize_list(results), HTTPStatus.OK

    @GAMES.expect(PGN_UPLOAD)
    @is_pgn_file
    @save_pgn_file
    def post(self, pgn_file_absolute_path):
        from src.parsers.pgn import parse
        print(pgn_file_absolute_path)
        parse(pgn_file_absolute_path)
        return "f3", HTTPStatus.OK
