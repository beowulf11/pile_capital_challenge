import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase

meta = sa.MetaData()


class ModelBase(DeclarativeBase):
    """Base for all DB models."""

    metadata = meta
