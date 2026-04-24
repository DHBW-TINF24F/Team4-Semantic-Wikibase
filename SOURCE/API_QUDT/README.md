# QUDT IEC61360 SemanticHub API

Diese API fragt Daten aus QUDT über den SPARQL-Endpunkt ab und gibt genau einen passenden Eintrag als JSON zurück.

Die Antwort orientiert sich an einer `ConceptDescription` mit `DataSpecificationIec61360` und enthält:

- die gemappten IEC61360-Felder
- die zugehörigen Property-Nummern wie `P1`, `P35`, `P43`
- zusätzliche, nicht gemappte Properties unter `additionalProperties`

## Voraussetzungen

- Node.js installiert
- Internetverbindung

## Installation

Falls noch keine `package.json` vorhanden ist:

```bash
npm init -y
```

Benötigtes Paket installieren:

```bash
npm install express
```

Falls du `import` in `server.js` verwendest, ergänze in `package.json`:

```json
"type": "module"
```

## Starten

```bash
node server.js
```

Wenn alles funktioniert, erscheint:

```text
Server läuft auf http://localhost:3000
```

## Endpoint

```text
GET /api/concept-description
```

## Query-Parameter

- `search`  
  Suchbegriff oder Semantic ID, z. B. `Volt`, `Ampere`, `unit:V` oder `http://qudt.org/vocab/unit/V`

- `lang`  
  Sprache der Antwort, aktuell z. B. `en` oder `de`

- `types`  
  QUDT-Bereich, z. B.:
  - `unit`
  - `quantitykind`
  - `dimensionvector`
  - `constant`
  - `sou`
  - `soqk`

## Verhalten der Suche

Die API unterscheidet zwischen:

- **Begriffssuche**  
  Beispiel: `Volt`  
  Dabei wird der beste exakte Treffer gesucht und nur **ein** Ergebnis zurückgegeben.

- **Semantic-ID-Suche**  
  Beispiel: `http://qudt.org/vocab/unit/V`  
  Dabei wird exakt diese Ressource geladen und nur **ein** Ergebnis zurückgegeben.

## Beispiele

### Suche nach Begriff

```text
http://localhost:3000/api/concept-description?search=Volt&lang=en&types=unit
```

### Suche nach Semantic ID als vollständige URI

```text
http://localhost:3000/api/concept-description?search=http://qudt.org/vocab/unit/V&lang=en&types=unit
```

### Suche nach Semantic ID als Kurzform

```text
http://localhost:3000/api/concept-description?search=unit:V&lang=en&types=unit
```

### Suche nach QuantityKind

```text
http://localhost:3000/api/concept-description?search=http://qudt.org/vocab/quantitykind/ElectricCurrent&lang=en&types=quantitykind
```

### Suche auf Deutsch

```text
http://localhost:3000/api/concept-description?search=Volt&lang=de&types=unit
```

## Was die API zurückgibt

Die Antwort ist JSON und enthält:

- `query`  
  die verwendeten Suchparameter

- `total`  
  Anzahl Treffer, im Normalfall `1`

- `result`  
  den gefundenen Datensatz als `ConceptDescription`

## Inhalt von `result`

Der Datensatz enthält unter anderem:

- `modelType`
- `id`
- `idShort`
- `embeddedDataSpecifications`
- `dataSpecificationContent`
- `additionalProperties`

## Gemappte IEC61360-Felder

Im Block `dataSpecificationContent` werden wichtige Felder gemappt, z. B.:

- `semanticId` (`P1`)
- `preferredName` (`P35`)
- `shortName` (`P36`)
- `unit` (`P37`)
- `sourceOfDefinition` (`P40`)
- `Symbol` (`P41`)
- `dataType` (`P42`)
- `unitId` (`P43`)
- `Definition` (`P44`)
- `valueFormat` (`P45`)
- `valueList` (`P46`)
- `value` (`P47`)
- `levelType` (`P48`)

Falls ein Feld nicht vorhanden ist, wird es mit `null` zurückgegeben.

## Zusätzliche Properties

Alle weiteren, nicht gemappten QUDT-/RDF-Properties werden unter `additionalProperties` zurückgegeben.

Bereits gemappte Felder wie `rdfs:label` oder `qudt:symbol` sollen dort nicht noch einmal doppelt auftauchen.

## Test im Browser

Nach dem Start kannst du die Beispiele direkt im Browser öffnen, zum Beispiel:

```text
http://localhost:3000/api/concept-description?search=Volt&lang=en&types=unit
```

## Test mit curl

In einem zweiten Terminalfenster:

```bash
curl "http://localhost:3000/api/concept-description?search=Volt&lang=en&types=unit"
```

## Hinweise

- Für `unit` müssen auch Unit-URIs verwendet werden, z. B. `http://qudt.org/vocab/unit/V`
- Für `quantitykind` müssen QuantityKind-URIs verwendet werden, z. B. `http://qudt.org/vocab/quantitykind/ElectricCurrent`
- Wenn `types` nicht zur Semantic ID passt, wird kein Treffer gefunden