import logging
import time

from src.tasks import parse

LOGGER = logging.getLogger(__name__)


def parser(filename: str):
    game_counter = 0
    start = time.time()
    with open(filename) as file_object:
        previous_line = ""
        current_game = ""
        for line in file_object:
            current_game += line
            if previous_line == "\n" and line == "\n":
                parse.delay(current_game)
                LOGGER.error("parsing: \n'%s'\n" % current_game)
                current_game = ""
                previous_line = ""
                continue
            previous_line = line

    end = time.time()
    elapsed = end - start
    print(f"Game counter: {game_counter}. In {elapsed} seconds.")
