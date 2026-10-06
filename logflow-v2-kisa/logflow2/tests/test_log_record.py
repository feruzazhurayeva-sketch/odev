import dataclasses
import unittest
from datetime import datetime, timezone

from logflow.console_sink import ConsoleSink
from logflow.log_record import LogRecord
import contextlib
import io

REC = LogRecord(datetime(2026, 9, 29, 10, tzinfo=timezone.utc), "1.2.3.4", "GET", "/", 200, 10,
                "ua", {"a": "1"})


class LogRecordTests(unittest.TestCase):
    def test_immutable(self):
        with self.assertRaises(dataclasses.FrozenInstanceError):
            REC.status = 500
        with self.assertRaises(TypeError):
            REC.attributes["b"] = "2"

    def test_console_sink_prints_single_line(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            ConsoleSink().consume(REC)
        self.assertEqual(buf.getvalue(),
                         '2026-09-29 10:00:00+00:00 1.2.3.4 GET / -> 200 (10 B) ua="ua"\n')


if __name__ == "__main__":
    unittest.main()
