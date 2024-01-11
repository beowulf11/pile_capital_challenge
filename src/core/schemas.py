import re
from functools import partial

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict


def snake2camel(snake: str, start_lower: bool = False) -> str:
    camel = snake.title()
    camel = re.sub("([0-9A-Za-z])_(?=[0-9A-Z])", lambda m: m.group(1), camel)
    if start_lower:
        camel = re.sub("(^_*[A-Z])", lambda m: m.group(1).lower(), camel)
    return camel


class APIModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=partial(snake2camel, start_lower=True),
    )


class PaginationDataAPIModel(APIModel):
    count: int
    offset: int
    limit: int
    total: int


class APIException(HTTPException):
    pass


class PaginatedAPIModel(APIModel):
    metadata: PaginationDataAPIModel
