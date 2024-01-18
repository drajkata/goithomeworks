# Wprowadzenie do wielowątkowości

Dokumentacja: [Python](https://docs.python.org/3/library/concurrency.html)

Ciekawy artykuł: [Współbieżność, równoległość, wątki, procesy, asynchronizacja i synchronizacja — powiązane?](https://medium.com/swift-india/concurrency-parallelism-threads-processes-async-and-sync-related-39fd951bc61d)

## Definicje

**Proces** — obszar pamięci (wirtualnej) + zestaw zasobów + 1 lub więcej wątków.

**Wątek** — sekwencja instrukcji i wywołań systemowych w ramach procesu.

Wszystkie wątki mają dostęp do wszystkich zasobów swojego procesu. Wszystkie procesy są od siebie odizolowane, a wszelkie interakcje między procesami odbywają się wyłącznie poprzez operacje wejścia/wyjścia (wywołania systemowe).

**Global Interpreter Lock (GIL)** - mechanizm, który wymusza blokowanie współbieżnego wykonywania kodu przez różne wątki tego samego procesu Pythona w tym samym czasie.

- Wykonywany jest tylko jeden wątek w procesie Pythona, a wszystkie pozostałe (jeśli istnieją) są w trybie "Sleep".
- Operacje I/O (wywołania systemowe) nie są blokowane przez GIL, lecz ich kolejność — tak.
