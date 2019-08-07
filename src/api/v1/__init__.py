from flask import Blueprint
from flask_restplus import Api

from src.api.v1.players import PLAYERS
from src.api.v1.clubs import CLUBS
from src.api.v1.games import GAMES
from src.api.v1.plies import PLIES
from src.api.v1.positions import POSITIONS
from src.api.v1.tournaments import TOURNAMENTS

API_V1 = Blueprint(
    name="api_v1",
    import_name=__name__,
    url_prefix="/api/v1"
)

API = Api(
    API_V1,
    title="chessdb API",
    version="0.0.1",
    description="API for chessdb",
    contact_email="nymannjakobsen@gmail.com",
    contact_url="https://github.com/chessdb/api/",
    license="GNU General Public License v3.0",
    license_url="https://www.gnu.org/licenses/gpl-3.0.en.html"
)

# /api/players
API.add_namespace(PLAYERS)

# /api/clubs
API.add_namespace(CLUBS)

# /api/tournaments
API.add_namespace(TOURNAMENTS)

# /api/games
API.add_namespace(GAMES)

# /api/plies
API.add_namespace(PLIES)

# /api/positions
API.add_namespace(POSITIONS)
