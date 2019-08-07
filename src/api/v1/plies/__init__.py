from http import HTTPStatus

from flask_restplus import Namespace, fields, Resource

from src.models.ply import Ply

PLIES = Namespace(name="plies", description="Endpoints for plies.")

MODEL = PLIES.model(
    name="user_model",
    model={
        "id": fields.String(),
        "current_position": fields.String(),
        "next_position": fields.String(),
        "algebraic_notation": fields.Date(),
        "game_id": fields.String()
    }
)


@PLIES.route("/")
class Plies(Resource):
    def get(self):
        results = Ply.query.all()
        return Ply.serialize_list(results), HTTPStatus.OK
