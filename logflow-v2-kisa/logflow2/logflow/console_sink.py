from .log_record import LogRecord
from .sink import Sink


class ConsoleSink(Sink[LogRecord]):
    """Her LogRecord'u konsola tek satir olarak yazar."""

    def consume(self, item: LogRecord) -> None:
        print(f"{item.timestamp.isoformat(sep=' ')} {item.client_ip} {item.method} "
              f"{item.path} -> {item.status} ({item.bytes} B) ua=\"{item.user_agent}\"")
