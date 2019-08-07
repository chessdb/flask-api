import logging
from uuid import UUID

from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError

from src.extensions import DB

LOGGER = logging.getLogger(__name__)


class BaseModel(DB.Model):
    __abstract__ = True

    def store(self) -> bool:
        DB.session.add(self)
        return commit()

    def remove(self) -> bool:
        DB.session.delete(self)
        return commit()

    def serialize(self) -> dict:
        result = {}
        for key in inspect(self).attrs.keys():
            attribute = getattr(self, key)
            if isinstance(key, UUID):
                attribute = str(attribute)
            result.update({key: attribute})
        return result

    @staticmethod
    def serialize_list(list_to_serialize: []):
        return [element.serialize() for element in list_to_serialize]


def commit() -> bool:
    """
    Commits the transaction to the database.
    :return: True if transaction was successful, otherwise False.
    """
    try:
        DB.session.commit()
        return True
    except SQLAlchemyError as e:
        LOGGER.info(str(e))
        # TODO except a more specific exception, so we can further specify whether to use info,
        # debug, error or critical for our logging message (SEE
        # https://docs.sqlalchemy.org/en/13/core/exceptions.html).
        DB.session.rollback()
        return False
