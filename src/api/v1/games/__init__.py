from http import HTTPStatus

from flask_restplus import Namespace, fields, Resource

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
        "playing_round": fields.String(),
        "utc_date": fields.Date
    }
)


@GAMES.route("/")
class Games(Resource):
    def get(self):
        results = Game.query.all()
        return Game.serialize_list(results), HTTPStatus.OK
