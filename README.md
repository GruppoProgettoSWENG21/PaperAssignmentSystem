# PaperAssignmentSystem
Il progetto consiste nella realizzazione di un Software che ha l'obiettivo di assegnare la revisione dei paper a dei papabili revisori, sulla base delle tematiche e delle relazioni estrapolate da un pool di paper realizzati da tali revisori. Le tecniche utilizzate sono:

- Web Scraping, con l'ausilio della libreria Selenium, per il prelievo dei PDF dalla pagina Web Google Scholar personale dei possibili revisori dei paper.
- Estrapolazione contenuti dai paper; titolo,titolo e abstract,keywords
- Creazione e valutazione delle metriche di analisi; jaccard similarity e cosine similarity

In output sarà prodotta una ranked list dei revisori con il livello di similitudine di ciascuno.
