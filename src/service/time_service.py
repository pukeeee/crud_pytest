from datetime import datetime, timezone

class TimeService:
    @staticmethod
    def now_utc() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def now_unix() -> int:
        return int(datetime.now(timezone.utc).timestamp())

    @staticmethod
    def format(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        return dt.strftime(fmt)