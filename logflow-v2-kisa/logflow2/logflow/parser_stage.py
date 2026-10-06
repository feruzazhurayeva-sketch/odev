import re
from datetime import datetime
from typing import Optional

from .emitter import Emitter
from .log_record import LogRecord
from .stage import Stage

# host ident user [tarih] "METOD yol protokol" durum bayt ["referer" "user-agent"]
_LINE = re.compile(
    r'^(\S+)\s+\S+\s+\S+\s+\[([^\]]+)\]\s+"(\S+)\s+(\S+)[^"]*"\s+([1-5]\d\d)\s+(\d+|-)'
    r'(?:\s+"[^"]*"\s+"([^"]*)")?$')


def parse_line(line: str) -> Optional[LogRecord]:
    """CLF satirini LogRecord'a cevirir; gecersizse None doner."""
    m = _LINE.match(line.strip())
    if not m:
        return None
    ip, ts, method, path, status, size, agent = m.groups()
    try:
        when = datetime.strptime(ts, "%d/%b/%Y:%H:%M:%S %z")
    except ValueError:
        return None
    return LogRecord(when, ip, method, path, int(status),
                     0 if size == "-" else int(size), agent or "", {}, line)


class ParserStage(Stage[str, LogRecord]):
    """str -> LogRecord. Hatali satirlar bu hafta yalnizca atlanir ve sayilir
    (dogru ele alinmalari 5. haftada gelecek)."""

    def __init__(self) -> None:
        self.parsed_count = self.skipped_count = 0

    def open(self) -> None:
        self.parsed_count = self.skipped_count = 0

    def process(self, item: str, out: Emitter[LogRecord]) -> None:
        record = parse_line(item)
        if record is None:
            self.skipped_count += 1
            return
        self.parsed_count += 1
        out.emit(record)
