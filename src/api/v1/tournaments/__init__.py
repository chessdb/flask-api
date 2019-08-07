from http import HTTPStatus

from flask_restplus import Namespace, fields, Resource

from src.models.tournament import Tournament

TOURNAMENTS = Namespace(name="tournaments", description="Endpoints for tournaments.")

MODEL = TOURNAMENTS.model(
    name="user_model",
    model={
        "id": fields.String(),
        "name": fields.String()
    }
)


@TOURNAMENTS.route("/")
class Tournaments(Resource):
    def get(self):
        results = Tournament.query.all()
        return Tournament.serialize_list(results), HTTPStatus.OK
