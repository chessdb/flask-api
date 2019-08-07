from flask_restplus import reqparse
from werkzeug.datastructures import FileStorage

PGN_UPLOAD = reqparse.RequestParser()
PGN_UPLOAD.add_argument('pgn_file',
                        type=FileStorage,
                        location='files',
                        required=True,
                        help='PGN file')
