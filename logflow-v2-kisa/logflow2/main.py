"""Main uc is yapar: argumanlari oku, hatti kur, run() cagir, ozeti yaz."""
import argparse
import sys

from logflow.console_sink import ConsoleSink
from logflow.file_line_source import FileLineSource
from logflow.parser_stage import ParserStage
from logflow.pipeline import Pipeline


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="logflow", description="Log dosyasini yapilandirilmis kayit olarak yazar.")
    ap.add_argument("path", help="okunacak log dosyasi (ornek: data/access-small.log)")
    args = ap.parse_args(argv)

    parser = ParserStage()
    pipeline = Pipeline(FileLineSource(args.path), ConsoleSink()).add_stage(parser)
    try:
        pipeline.run()
    except Exception as e:
        print(f"Hata: {e}", file=sys.stderr)
        return 1
    print(f"Toplam: {parser.parsed_count} kayit islendi, {parser.skipped_count} hatali satir atlandi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
