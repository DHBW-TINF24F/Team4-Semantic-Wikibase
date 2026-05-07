# QUDT to IEC 61360 Mapper

Ein Python-Tool zum Mapping von **QUDT** (Quantities, Units, Dimensions and Types) RDF/Turtle-Dateien auf **IEC 61360** konforme ConceptDescriptions für Asset Administration Shells (AAS).

---

## Features

- Mapping von QUDT-Einheiten, QuantityKinds und Konstanten nach IEC 61360
- Unterstützung mehrsprachiger Labels und Definitionen
- Automatische Unit-Auflösung (inkl. optionaler SI-Unit-ID)
- Erzeugung AAS-kompatibler `ConceptDescription`-Strukturen
- Suche nach Begriff oder URI
- Saubere JSON-Ausgabe

---

## Voraussetzungen

- QUDT Turtle-Dateien (z. B. `volt.ttl`, `qudt-units.ttl`)

### Installation

```bash
pip install -r requirements.txt

```

### Ausführung

Im Code die Search Variable anpassen z.B. SEARCH = "Volt"

```bash

python qudt_mapper.py

```

### Mapping-Tabelle

Anhand des Beispiels des Eintrages "Volt"

| Ziel-Property       | QUDT-Quelle                                      | Beispielwert (für "Volt")                     | Bemerkung |
|---------------------|-----------------------------|--------------------------------------------------|-----------------------------------------------|
| semanticId                                    | Subject-URI (QUDT-IRI)                           | `http://qudt.org/vocab/unit/V`                | Beste Wahl als globale Semantik-ID |
| preferredName                                | `rdfs:label` (mit Sprache)                       | `{"value": "Volt", "lang": "en"}`             | Sprachabhängig |
| shortName                                    | Lokaler Name der URI                             | `V`                                           | Optional, nicht mit Symbol verwechseln |
| unit                                         | `qudt:symbol`                                    | `V`                                           | Nur bei quantitativen Properties |
| unitId                                       | QUDT-URI                                         | `http://qudt.org/vocab/unit/V`                | Konsistent mit `unit` |
| sourceOfDefinition                          | `rdfs:isDefinedBy`, `qudt:informativeReference` | `http://qudt.org/3.2.1/vocab/unit`           | Quellenangaben |
| Symbol                                      | `qudt:symbol`                                    | `V`                                           | Direktes 1:1-Mapping |
| dataType                                     | Nicht direkt aus QUDT-Unit ableitbar             | `null`                                        | Muss aus der gemessenen Property kommen |
| Definition                                   | `dcterms:description` oder `qudt:latexDefinition` | `"Volt is the SI unit of electric potential..."` | Textuelle Definition |
| valueFormat                                 | Nicht direkt ableitbar                           | `null`                                        | Nur bei konkreten Werteformaten |
| valueList                                    | Nicht für Einheiten                              | `null`                                        | Nur für Enumerationen |
| value                                       | Nicht für Einheiten                              | `null`                                        | Nur für konkrete Werte |
| levelType                                    | Nicht aus QUDT-Unit ableitbar                    | `null`                                        | MIN/NOM/TYP/MAX |



### Funktionsweise des Mappers

- Zuerst wird ein passendes QUDT-Konzept über eine SPARQL-Abfrage gesucht.
- Anschließend werden alle relevanten Eigenschaften des Konzepts abgerufen.
- Die Daten werden exakt nach obiger Tabelle in die IEC 61360-Struktur gemappt.
- Felder ohne passendes QUDT-Prädikat werden explizit auf `null` gesetzt.
- Der Mapper kann auch ohne die API eigenständig verwendet werden.

