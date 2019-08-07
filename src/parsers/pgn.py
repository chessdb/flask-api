import time
from uuid import UUID

import chess.pgn

from src.models.game import Game
from src.models.player import Player
from src.models.ply import Ply
from src.models.position import Position


def game_generator(filename: str):
    game_counter = 0
    start = time.time()
    with open(filename) as pgn:
        game = chess.pgn.read_game(pgn)
        while game:
            yield game
            game = chess.pgn.read_game(pgn)
    end = time.time()
    elapsed = end - start
    print(f"Game counter: {game_counter}. In {elapsed} seconds.")


def parse(filename: str):
    for game in game_generator(filename=filename):
        variant = game.headers.get("Variant")
        if variant != "Standard" and variant is not None:
            print(f"Variant was not supported: '{variant}'")
            continue

        site = game.headers.get("Site")
        if "lichess.org" in site:
            white = get_or_create_player(game.headers.get("White"))
            black = get_or_create_player(game.headers.get("Black"))
            chess_game = get_or_create_game(headers=game.headers, white=white.id, black=black.id)
            parse_moves(game=game, game_model=chess_game)
        else:
            print(f"{site} is not supported.")


def get_or_create_player(lichess_username: str):
    player = Player.query.filter_by(lichess_username=lichess_username).one_or_none()
    if not player:
        player = Player(lichess_username=lichess_username)
        player.store()
    return player


def get_or_create_game(headers: dict, white: UUID, black: UUID) -> Game:
    chess_game = Game.query.filter_by(site=headers.get("Site")).one_or_none()
    if chess_game:
        return chess_game
    chess_game = Game.lichess(**headers, white=white, black=black)
    chess_game.store()
    return chess_game


def parse_moves(game, game_model: Game):
    board = game.board()
    for move in game.mainline_moves():
        current_position = board.board_fen()
        if current_position is None:
            raise Exception("NEXT POSITION IS NONE")
        insert_position_if_not_already_exists(fen=current_position)
        uci_move = move.uci()
        board.push(move)
        next_position = board.board_fen()
        if next_position is None:
            raise Exception("NEXT POSITION IS NONE")
        insert_position_if_not_already_exists(fen=next_position)
        insert_ply_if_not_already_exists(current_position=current_position, next_position=next_position,
                                         uci_move=uci_move, game_id=game_model.id)


def insert_position_if_not_already_exists(fen: str):
    position = Position.query.get(fen)
    if position:
        return position
    position = Position(fen=fen)

    if not position.store():
        print(f"Failed to add: {fen}.")
    return position


def insert_ply_if_not_already_exists(current_position: str, next_position: str, uci_move: str, game_id: UUID):
    ply = Ply.query.filter_by(game_id=game_id, current_position=current_position,
                              next_position=next_position).one_or_none()
    if ply:
        return ply
    ply = Ply(current_position=current_position, next_position=next_position, algebraic_notation=uci_move,
              game_id=game_id)
    ply.store()
    return ply
