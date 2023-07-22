from datetime import datetime, timezone


def datetime_to_milliseconds(dt: datetime) -> int:
    return int(round(dt.replace(tzinfo=timezone.utc).timestamp() * 1000))
