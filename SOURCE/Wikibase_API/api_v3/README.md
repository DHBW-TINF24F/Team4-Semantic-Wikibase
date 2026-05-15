# API v3

Dieses Modul implementiert die Version 3 (nach der Angabe in dem Semantic-Hub) der EntityShape API, spezialisiert auf die Suche in der QUDT (Quantities, Units, Dimensions and Types) Ontologie.

## Überblick

API v3 bietet eine RESTful-Schnittstelle für die Suche nach QUDT-Entitäten wie Einheiten, Quantitätsarten, Dimensionsvektoren, Konstanten und Systemen von Einheiten oder Quantitätsarten. Die API kommuniziert mit dem QUDT SPARQL-Endpunkt unter `https://qudt.org/fuseki/qudt/query`.

## Dateien

- `api_v3_blueprint.py`: Flask Blueprint mit den API-Routen.
- `qudt_service.py`: Hauptservice für QUDT-Suchen und SPARQL-Abfragen.
- `helper.py`: Hilfsfunktionen (derzeit leer, nach Vorbild der Semantic-Hub).
- `local-test-api.html`: Einfache HTML-Testseite für manuelle Tests der API.

## Endpunkte

### GET /api/v3/info

Gibt grundlegende Informationen über die API zurück.

**Beispiel-Antwort:**

```json
{
  "name": "Meine API",
  "version": "1.0"
}
```

### GET /api/v3/search

Führt eine Suche in QUDT durch.

**Parameter:**

- `search` (erforderlich): Suchbegriff (Begriff, URI oder CURIE).
- `lang` (optional): Sprache für Labels (unterstützt: "en", "de"; Standard: "en").
- `types` (optional): Komma-getrennte Liste von Typen (unit, quantitykind, dimensionvector, constant, sou, soqk; Standard: "unit").

**Beispiel-Anfrage:**

```
GET /api/v3/search?search=Volt&lang=en&types=unit
```

**Beispiel-Antwort:**

```json
{
  "query": {
    "search": "Volt",
    "mode": "term",
    "lang": "en",
    "types": ["unit"]
  },
  "total": 1,
  "result": [...],
  "error": null
}
```

## Verwendung

1. Stelle sicher, dass Flask installiert ist.
2. Registriere den Blueprint in deiner Flask-App.
3. Starte den Server und teste die Endpunkte.

Für Tests kannst du `test.html` in einem Browser öffnen und Suchanfragen senden.

## Abhängigkeiten

- Flask
- requests
- typing (Python-Standard)

## Hinweise

- Die API unterstützt sowohl Begriffssuchen als auch direkte URI/CURIE-Abfragen.
- Fehler werden in der Antwort als "error"-Feld zurückgegeben.
- Die SPARQL-Abfragen sind optimiert für den QUDT-Endpunkt.</content>
