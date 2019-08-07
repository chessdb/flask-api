import logging
import os
import sys

import config
from src import create_app

APP = create_app(os.environ.get("APP_CONFIG") or config.ProductionConfig)

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    APP.run()
