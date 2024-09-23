from uuid import UUID
from datetime import datetime, date
import dataclasses
import json


class JSONEncoder(json.JSONEncoder):
    """
    Custom encode that extends supported types: date/datetime,
    UUID and dataclasses
    """

    def default(self, o):
        if isinstance(o, datetime) or isinstance(o, date):
            return o.isoformat()
        if isinstance(o, UUID):
            return str(o)
        if dataclasses and dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
