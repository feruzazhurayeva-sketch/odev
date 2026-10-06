# Değişiklik Günlüğü

## v2 — Tipli kayıtlar ve ParserStage
**Yeni:** `logflow/log_record.py`, `logflow/parser_stage.py`, `tests/collecting_emitter.py`,
`tests/test_parser_stage.py`, `tests/test_log_record.py`, `data/access-with-errors.log`, `CHANGELOG.md`

**Değişen:**
- `main.py` — hatta `ParserStage` eklendi, sonda toplam/atlanan sayısı yazılır
- `logflow/console_sink.py` — `Sink[LogRecord]`, tek satırlık biçim
- `logflow/pipeline.py` — yalnızca tip ipuçları (`Pipeline[I, O]`); mantık aynı
- `tests/test_pipeline.py` — uçtan uca testler yeni çıktıya göre güncellendi
- `README.md`, `ARCHITECTURE.md`, `.github/workflows/tests.yml`

**Değişmeyen:** `emitter.py`, `stage.py`, `source.py`, `sink.py`, `file_line_source.py`

## v1 — İskelet hat
