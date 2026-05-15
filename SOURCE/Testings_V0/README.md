# Testings_V0

Dieses Verzeichnis enthält Prototypen und Testskripte für den Zugriff auf QUDT/RDF-Daten und das Parsen von TTL-Dateien.

## Inhalt

- `extract_values_parser.py` - Python-Skript zum Laden, Parsen und Extrahieren von QUDT-Turtle-Daten. Speichert die extrahierten Eigenschaften einer Einheit als JSON.
- `qudt-ttl-parser1.js` - JavaScript-Testskript, das eine QUDT-Unit-Turtle-Datei lädt und mit `n3` parst.
- `qudt-ttl-parser2.js` - JavaScript-Testskript für das Parsen einer QUDT-Turtle-Datei und Umwandeln in ein vereinfachtes JSON-Format.
- `test2.js` - JavaScript-Beispiel, das eine SPARQL-Abfrage gegen das QUDT-Fuseki-Endpoint ausführt und Ergebnisse als JSON ausgibt.
- `test3.js` - JavaScript-Beispiel, das eine suchbasierte SPARQL-Abfrage gegen das QUDT-Fuseki-Endpoint ausführt und Treffer für ein Suchwort zurückgibt.
- `requirements.txt` - Python-Abhängigkeiten für `extract_values_parser.py`.

## Voraussetzungen

- Python 3.x
- Node.js (für die JavaScript-Dateien)
- Internetzugriff zum QUDT-Endpoint bzw. zur QUDT-Turtle-Ressource

## Installation

1. Installiere Python-Abhängigkeiten:

```bash
pip install -r requirements.txt
```

2. Installiere Node.js-Abhängigkeiten, falls noch nicht vorhanden:

```bash
npm install n3
```

> Hinweis: Für `fetch` in Node.js kann bei älteren Versionen ein Polyfill oder `node --experimental-fetch` erforderlich sein.

## Nutzung

### Python-Skript

```bash
python extract_values_parser.py
```

Das Skript lädt die Turtle-Datei der QUDT-Einheit `V` und schreibt eine JSON-Ausgabe nach `output/qudt_volt.json`.

### JavaScript-Skripte

- `qudt-ttl-parser1.js` und `qudt-ttl-parser2.js` können in einer Node.js-Umgebung ausgeführt werden:

```bash
node qudt-ttl-parser1.js
node qudt-ttl-parser2.js
```

- `test2.js` und `test3.js` führen SPARQL-Abfragen gegen das QUDT-Fuseki-Endpoint aus:

```bash
node test2.js
node test3.js
```

## Hinweise

- Die Skripte sind als Test- und Prototypcode gedacht, um das Verhalten von RDF/Turtle-Parsing und SPARQL-Abfragen zu überprüfen.
- Die Abfragen und URLs sind hartkodiert; Anpassungen können notwendig sein, wenn andere QUDT-Ressourcen oder Einheiten verwendet werden.
- `extract_values_parser.py` verwendet `rdflib` zum Parsen und Speichern der Daten.
