import unittest

from logflow.parser_stage import ParserStage
from tests.collecting_emitter import CollectingEmitter

GOOD = '85.105.14.9 - - [29/Sep/2026:10:00:00 +0300] "GET / HTTP/1.1" 200 16169 "-" "Mozilla/5.0"'


def line(ts="29/Sep/2026:10:00:00 +0300", status="200", ua="ua", path="/"):
    return f'1.2.3.4 - - [{ts}] "GET {path} HTTP/1.1" {status} 10 "-" "{ua}"'


class ParserStageTests(unittest.TestCase):
    """Dosyaya dokunmaz: stage'e dizgi verilir, ciktiyi CollectingEmitter toplar."""

    def setUp(self):
        self.stage, self.out = ParserStage(), CollectingEmitter()

    def run_stage(self, text):
        self.stage.process(text, self.out)
        return self.out.items

    def test_valid_line(self):
        (r,) = self.run_stage(GOOD)
        self.assertEqual((r.client_ip, r.method, r.path, r.status, r.bytes, r.user_agent),
                         ("85.105.14.9", "GET", "/", 200, 16169, "Mozilla/5.0"))
        self.assertEqual(r.timestamp.isoformat(), "2026-09-29T10:00:00+03:00")
        self.assertEqual((dict(r.attributes), r.raw), ({}, GOOD))
        self.assertEqual((self.stage.parsed_count, self.stage.skipped_count), (1, 0))

    def test_missing_field(self):
        self.assertEqual(self.run_stage('1.2.3.4 - - [29/Sep/2026:10:00:00 +0300] "GET / HTTP/1.1"'), [])
        self.assertEqual(self.stage.skipped_count, 1)

    def test_bad_timestamp(self):
        for ts in ("29/Foo/2026:10:00:00 +0300", "32/Sep/2026:10:00:00 +0300", "dun aksam"):
            self.run_stage(line(ts=ts))
        self.assertEqual((self.out.items, self.stage.skipped_count), ([], 3))

    def test_bad_status_code(self):
        for status in ("abc", "20", "2000", "999"):
            self.run_stage(line(status=status))
        self.assertEqual((self.out.items, self.stage.skipped_count), ([], 4))

    def test_empty_line(self):
        for text in ("", "   "):
            self.run_stage(text)
        self.assertEqual((self.out.items, self.stage.skipped_count), ([], 2))

    def test_extra_whitespace(self):
        (r,) = self.run_stage('  85.105.14.9  -  -  [29/Sep/2026:10:00:00 +0300]  '
                              '"GET / HTTP/1.1"  200  16169  "-"  "Mozilla/5.0"  ')
        self.assertEqual((r.client_ip, r.status, r.bytes), ("85.105.14.9", 200, 16169))

    def test_quoted_user_agent_with_spaces(self):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        (r,) = self.run_stage(line(ua=ua))
        self.assertEqual(r.user_agent, ua)

    def test_query_string(self):
        (r,) = self.run_stage(line(path="/products?id=42&x=1"))
        self.assertEqual(r.path, "/products?id=42&x=1")

    def test_dash_bytes_is_zero_and_counters_reset(self):
        (r,) = self.run_stage(GOOD.replace("16169", "-"))
        self.assertEqual(r.bytes, 0)
        self.stage.open()
        self.assertEqual((self.stage.parsed_count, self.stage.skipped_count), (0, 0))


if __name__ == "__main__":
    unittest.main()
