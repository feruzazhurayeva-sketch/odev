# ARCHITECTURE — Artırım 1

Odak: **bileşenler ve bağlayıcılar; arayüz ile uygulama farkı.**
Arayüz *ne* yapılacağını, uygulama *nasıl* yapıldığını söyler. `Pipeline` yalnızca
`Source`, `Stage`, `Sink` arayüzlerini bilir.

## İki Kutu Diyagramı

    +-----------------------+     Emitter.emit(str)     +-----------------------+
    |    FileLineSource     | ------------------------> |      ConsoleSink      |
    |   (implements Source) |   bağlayıcı (connector)   |    (implements Sink)  |
    +-----------------------+                           +-----------------------+

## Genişletilmiş görünüm (sonraki artırımlar)

    Source --emit--> [Stage 1] --emit--> [Stage 2] --emit--> Sink
                     (araya Pipeline'a dokunmadan eklenir)

## Arayüzler
| Arayüz | Sözleşme |
|---|---|
| `Source[O]` | `produce(out)` — kayıtları üretip `out`'a verir |
| `Stage[I,O]` | `process(item, out)`, `open()`, `close()` |
| `Sink[I]` | `consume(item)` |
| `Emitter[T]` | `emit(item)` — bileşenler arası bağlayıcı |

## Kararlar
1. **Emitter, dönüş değeri yerine.** Filtre 0, bölücü N çıktı üretebilir.
2. **Küçük arayüzler.** Tek sorumluluk; testte kolayca taklit edilir.
3. **Main'de iş mantığı yok.** Yalnızca argüman → kurulum → `run()`.
4. **Yaşam döngüsü güvenli.** `open` sırayla, `close` ters sırayla ve hata olsa bile çağrılır.
5. **Bilinen sınırlama.** `Pipeline[R]` tek kayıt tipiyle çalışır (`Stage[R,R]`);
   tip değiştiren stage'ler (`str → LogEntry`) sonraki artırımda ele alınacak.

---

# Artırım 2 — Tipli kayıtlar

    FileLineSource --str--> ParserStage --LogRecord--> ConsoleSink

6. **Kayıt değişmezdir**; aşamalar kaydı değiştirmez, yenisini üretir.
7. **`attributes`** genişleme noktasıdır (5–7. haftalar).
8. **`parse_line` saf fonksiyondur**; `ParserStage` yalnızca çağırır, sayar, yayar.
9. **Hatalı satır:** bu hafta atla ve say; doğru ele alma 5. haftada.
10. **`Pipeline[I, O]`:** Artırım 1'deki tek tip sınırlaması kalktı (yalnızca tip ipuçları).

**Demo — hangi dosyalar değişti?** Davranış olarak yalnızca `main.py` ve `console_sink.py`;
`pipeline.py`'da sadece tip ipuçları. `emitter`, `stage`, `source`, `sink`, `file_line_source` değişmedi.

**Demo — test dosya okumadan nasıl çalışır?** `ParserStage` yalnızca `process(item, out)` sözleşmesine
bağlıdır: girdi dizgidir, çıktı `Emitter` arayüzüne verilir. Testte gerçek sink yerine
`CollectingEmitter` (test dublörü) toplar. Hızlıdır, diske bağlı değildir, hata tek aşamaya daralır.
