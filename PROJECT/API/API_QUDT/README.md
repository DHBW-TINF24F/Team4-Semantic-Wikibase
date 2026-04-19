# QUDT IEC61360 API

Diese API fragt Daten aus QUDT über den SPARQL-Endpunkt ab und gibt die Ergebnisse als IEC61360-artiges JSON zurück.

## Voraussetzungen

- Node.js installiert
- Internetverbindung

## Installation

```bash
npm install
```

Falls noch keine `package.json` vorhanden ist:

```bash
npm init -y
npm install express node-fetch
```

Falls du `import` verwendest, ergänze in `package.json`:

```json
"type": "module"
```

## Starten

```bash
node server.js
```

Danach läuft der Server unter:

```text
http://localhost:3000
```

## Endpoint

```text
GET /api/concept-description
```

## Query-Parameter

- `search` → Suchbegriff oder Semantic ID, z. B. `Volt` oder `http://qudt.org/vocab/unit/V`
- `lang` → Sprache, z. B. `en` oder `de`
- `types` → QUDT-Bereiche, z. B. `unit,quantitykind`
- `limit` → maximale Anzahl Ergebnisse

## Beispiele

### Suche nach Begriff

```text
http://localhost:3000/api/concept-description?search=Volt&lang=en&types=unit
```

### Suche nach Semantic ID

```text
http://localhost:3000/api/concept-description?search=http://qudt.org/vocab/unit/V&lang=en&types=unit
```

## Was der Code macht

- startet einen Express-Server auf Port 3000
- nimmt HTTP-Anfragen entgegen
- erkennt, ob `search` ein Begriff oder eine ID ist
- fragt QUDT über SPARQL ab
- durchsucht mehrere QUDT-Bereiche:
  - `unit`
  - `quantitykind`
  - `dimensionvector`
  - `constant`
  - `sou`
  - `soqk`
- mappt die Ergebnisse in ein IEC61360-artiges JSON-Format
- fasst doppelte SPARQL-Zeilen zu einem Ergebnis zusammen

## Rückgabe

Die API liefert JSON mit:

- den verwendeten Query-Parametern
- der Anzahl Treffer
- den gemappten Concept Descriptions