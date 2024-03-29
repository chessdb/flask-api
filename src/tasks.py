import io
import logging
from uuid import UUID

import chess.pgn
from sqlalchemy import or_
from sqlalchemy.orm.exc import MultipleResultsFound

from src.extensions import CELERY
from src.models.game import Game
from src.models.player import Player
from src.models.ply import Ply
from src.models.position import Position

LOGGER = logging.getLogger(__name__)


@CELERY.task
def parse(pgn_as_str: str):
    pgn = io.StringIO(pgn_as_str)
    game = chess.pgn.read_game(pgn)
    if game is None:
        LOGGER.error("Game was none: %s" % pgn_as_str)
        return
    variant = game.headers.get("Variant")
    if variant != "Standard" and variant is not None:
        LOGGER.info(f"Variant was not supported: '{variant}'")
        return

    site = game.headers.get("Site")
    if "lichess.org" in site:
        white = get_or_create_lichess_player(game.headers.get("White"))
        black = get_or_create_lichess_player(game.headers.get("Black"))
        chess_game = get_or_create_lichess_game(headers=game.headers, white=white.id, black=black.id,
                                                raw=game.__str__())
        parse_moves(game=game, game_model=chess_game)
    else:
        white = get_or_create_player(headers=game.headers, color="White")
        black = get_or_create_player(headers=game.headers, color="Black")
        chess_game = get_or_create_game(headers=game.headers, white=white.id, black=black.id, raw=game.__str__())
        parse_moves(game=game, game_model=chess_game)


def get_or_create_lichess_player(lichess_username: str):
    player = Player.query.filter_by(lichess_username=lichess_username).one_or_none()
    if not player:
        player = Player(lichess_username=lichess_username)
        player.store()
    return player


def get_or_create_player(headers: dict, color: str = "White"):
    name = headers.get(color)  # surname, given_name
    if not name:
        LOGGER.error("Name was empty %s" % headers)
    fide_id_str = f"{color}FideId"
    fide_id = headers.get(fide_id_str)
    given_name = name[name.find(",") + 2:]
    surname = name[:name.find(",")]
    LOGGER.debug(f"given_name: {given_name}, surname: {surname}, fide_id: {fide_id}")
    try:
        player = Player.query.filter(
            or_(Player.fide_id.is_(None), Player.fide_id == fide_id),
            Player.given_name == given_name,
            Player.surname == surname
        ).one_or_none()
    except MultipleResultsFound as e:
        LOGGER.error("Multiple results found for combination: %s, %s fide_id: %s" % (surname, given_name, fide_id))
        player = None
    if not player:
        player = Player(given_name=given_name, surname=surname, fide_id=fide_id)
        player.store()
    return player


def get_or_create_lichess_game(headers: dict, white: UUID, black: UUID, raw: str) -> Game:
    chess_game = Game.query.filter_by(site=headers.get("Site")).one_or_none()
    if chess_game:
        return chess_game
    chess_game = Game.lichess(**headers, white=white, black=black, raw=raw)
    chess_game.store()
    return chess_game


def get_or_create_game(headers: dict, white: UUID, black: UUID, raw: str) -> Game:
    chess_game = Game.query.filter_by(raw=raw).one_or_none()
    if chess_game:
        return chess_game
    chess_game = Game.standard(**headers, white=white, black=black, raw=raw)
    if not chess_game.store():
        logging.error("Couldn't store chess game.")
    return chess_game


def parse_moves(game, game_model: Game):
    board = game.board()
    current_position = board.fen()
    insert_position_if_not_already_exists(fen=current_position)
    for move in game.mainline_moves():
        board.push(move)
        next_position = board.fen()
        insert_position_if_not_already_exists(fen=next_position)
        insert_ply_if_not_already_exists(current_position=current_position, next_position=next_position,
                                         game_id=game_model.id)


def insert_position_if_not_already_exists(fen: str):
    position = Position.query.get(fen)
    if position:
        return position
    position = Position(fen=fen)

    if not position.store():
        print(f"Failed to add: {fen}.")
    return position


def insert_ply_if_not_already_exists(current_position: str, next_position: str, game_id: UUID):
    ply = Ply.query.filter_by(game_id=game_id, current_position=current_position,
                              next_position=next_position).one_or_none()
    if ply:
        return ply
    ply = Ply(current_position=current_position, next_position=next_position,
              game_id=game_id)
    ply.store()
    return ply
