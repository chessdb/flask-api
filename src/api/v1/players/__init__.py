from http import HTTPStatus

from flask_restplus import Namespace, fields, Resource

from src.models.player import Player

PLAYERS = Namespace(name="players", description="Endpoints for players.")

MODEL = PLAYERS.model(
    name="user_model",
    model={
        "id": fields.String(),
        "given_name": fields.String(),
        "surname": fields.String(),
        "date_of_birth": fields.Date(),
        "club_id": fields.String
    }
)


@PLAYERS.route("/")
class Players(Resource):
    def get(self):
        results = Player.query.all()
        return Player.serialize_list(results), HTTPStatus.OK
