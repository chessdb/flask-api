import functools
import logging
import os
from http import HTTPStatus

from flask import current_app
from werkzeug.datastructures import FileStorage

from src.api.v1.games.request_parsers import PGN_UPLOAD

LOGGER = logging.getLogger(__name__)


def is_pgn_file(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args = PGN_UPLOAD.parse_args()
        pgn_file = args.get("pgn_file")
        if pgn_file.mimetype == 'application/vnd.chess-pgn':
            return func(pgn_file=pgn_file, *args, **kwargs)
        LOGGER.info("User tried to upload a PGN file, but mimetype was not allowed: '%s'" % pgn_file.mimetype)
        return "Only application/vnd.chess-pgn is allowed.", HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    return wrapper


def save_pgn_file(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pgn_file = kwargs.get("pgn_file")
        kwargs.pop("pgn_file")
        destination = current_app.config.get("PGN_FOLDER")
        if not os.path.exists(destination):
            os.makedirs(destination)
        absolute_path = "%s%s" % (destination, pgn_file.filename)
        pgn_file.save(dst=absolute_path)
        return func(pgn_file_absolute_path=absolute_path, *args, **kwargs)

    return wrapper
