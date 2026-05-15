# SOURCE

Dieser Ordner enthält den Quellcode für die verschiedenen APIs und Mapper des Projekts "Semantic Wikibase". Die Hauptkomponenten sind Mapping-APIs, die semantische Daten aus Quellen wie QUDT, KBL und VEC auf das IEC61360-Format abbilden.

## Unterordner

- **API_gateway/**: API-Gateway zur Orchestrierung der Mapping-APIs. Ermöglicht das lokale Starten und Testen aller APIs.
- **API_KBL/**: REST-API für das Mapping von KBL-XSD-Begriffen (z.B. Wire_occurrence) auf IEC61360-ConceptDescriptions.
- **API_QUDT/**: REST-API für das Mapping von QUDT-Begriffen (z.B. Volt) auf IEC61360-ConceptDescriptions über SPARQL-Abfragen.
- **API_VEC/**: REST-API für das Mapping von VEC-Ontologie-Begriffen (z.B. WireElement) auf IEC61360-ConceptDescriptions.
- **PROTOTYPEN/**: Prototypen und Testskripte, einschließlich Python-APIs, TTL-Parsern und lokalen Wikibase-API-Integrationen.
- **source_mapping/**: Python-Mapper-Skripte für die direkte Verarbeitung von KBL, QUDT und VEC-Daten.

Alle APIs basieren auf FastAPI und bieten Swagger-UI für Tests. Für detaillierte Anleitungen siehe die README-Dateien in den jeweiligen Unterordnern.
