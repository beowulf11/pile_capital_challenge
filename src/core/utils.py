import decimal
import json
from typing import Any


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def json_dumps(obj: Any, **kwargs) -> str:  # type: ignore
    return json.dumps(obj, **kwargs, cls=DecimalEncoder)
