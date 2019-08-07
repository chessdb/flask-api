from http import HTTPStatus

from flask_restplus import Namespace, fields, Resource

from src.models.position import Position

POSITIONS = Namespace(name="positions", description="Endpoints for positions.")

MODEL = POSITIONS.model(
    name="user_model",
    model={
        "id": fields.String(),
        "current_position": fields.String(),
        "next_position": fields.String(),
        "algebraic_notation": fields.Date(),
        "game_id": fields.String()
    }
)


@POSITIONS.route("/")
class Positions(Resource):
    def get(self):
        results = Position.query.all()
        return Position.serialize_list(results), HTTPStatus.OK
