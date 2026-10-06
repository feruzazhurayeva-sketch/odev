# LogFlow — Artırım 2: Tipli Kayıtlar ve İlk Gerçek Filtre

Log dosyasını hat (pipeline) üzerinden okur, her satırı değişmez bir `LogRecord`'a çevirir,
konsola tek satır olarak yazar. Hatalı satırlar **atlanır ve sayılır** (doğru ele alınmaları 5. haftada).

## Çalıştırma (Python 3.8+, ek paket yok)

    py main.py data/access-small.log            # macOS / Linux: python3
    py main.py data/access-with-errors.log      # hatalı satırlı örnek
    py -m unittest discover -s tests -v         # testler

Örnek çıktı: `2026-09-29 10:00:00+03:00 85.105.14.9 GET / -> 200 (16169 B) ua="Mozilla/5.0"`
ve en sonda `Toplam: 200 kayit islendi, 0 hatali satir atlandi.`

## Kapsama (line coverage)

**%99,4** (169 satırın 168'i; yalnızca `main.py` sonundaki `sys.exit(main())` çalışmıyor).
Ölçüm Python'un `trace` modülüyle yapıldı; `coverage` ile: `pip install coverage`,
`python -m coverage run -m unittest discover -s tests`, `python -m coverage report -m`.

## Yapı
    logflow/log_record.py     değişmez alan kaydı (attributes = genişleme noktası)
    logflow/parser_stage.py   CLF ayrıştırıcı (str -> LogRecord)
    logflow/console_sink.py   LogRecord -> tek satır
    logflow/pipeline.py ...   Artırım 1 bileşenleri (emitter, stage, source, sink)
    tests/                    22 test; collecting_emitter.py = test dublörü
    CHANGELOG.md  ARCHITECTURE.md

## Tasarım notları
- `attributes`: sonraki aşamalar (5–7. hafta) ayrıştırıcının bilmediği veriyi kayda ekleyecek;
  yeni alan eklemeden, mevcut kodlara dokunmadan taşınır. Ayrıştırıcı şimdilik boş bırakır.
- `ParserStage` testleri dosyaya dokunmaz: dizgi verilir, çıktı `CollectingEmitter` ile yakalanır.
- Hatalı sayılanlar: boş satır, eksik alan, geçersiz zaman damgası, geçersiz durum kodu (100–599 dışı).

Sürüm: `v2`
