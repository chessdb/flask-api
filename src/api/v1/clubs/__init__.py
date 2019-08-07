from http import HTTPStatus

from flask_restplus import Namespace, fields, Resource

from src.models.club import Club

CLUBS = Namespace(name="clubs", description="Endpoints for clubs.")

MODEL = CLUBS.model(
    name="user_model",
    model={
        "id": fields.String(),
        "name": fields.String()
    }
)


@CLUBS.route("/")
class Clubs(Resource):
    def get(self):
        results = Club.query.all()
        return Club.serialize_list(results), HTTPStatus.OK
