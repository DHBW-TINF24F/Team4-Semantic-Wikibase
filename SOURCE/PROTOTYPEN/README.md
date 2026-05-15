# PROTOTYPEN

Dieser Ordner enthält Prototypen und Testimplementierungen für verschiedene Komponenten des Projekts, einschließlich APIs, Parser und lokaler Wikibase-Integrationen. Die Prototypen dienen der Entwicklung und Validierung von Funktionen vor der Integration in die Haupt-APIs.

## Unterordner

Für detaillierte Anleitungen zur Installation und Nutzung siehe die README-Dateien in den jeweiligen Unterordnern.

|                         |                                                                                                                                                                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **API_Python/**         | Python-Prototyp für eine QUDT-API. Bietet Funktionen zum Abfragen und Mappen von QUDT-Daten auf IEC61360-Format. Enthält ein Skript zur Suche nach Begriffen oder Semantic-IDs.                                           |
| **TTL_Parser/**         | Testskripte und Parser für QUDT-Turtle-Dateien. Umfasst Python- und JavaScript-Implementierungen zum Laden, Parsen und Extrahieren von RDF-Daten. Beinhaltet auch SPARQL-Abfragen gegen QUDT-Endpunkte.                   |
| **Wikibase_API_lokal/** | Lokale Implementierung, enthält API v3 für die Suche in QUDT-Ontologie über SPARQL. Bietet Flask-basierte Routen und eine Test-HTML-Seite. **_Die API v3 ist benannt nach der Konvention in der Semantic-Hub-Wikibase._** |
