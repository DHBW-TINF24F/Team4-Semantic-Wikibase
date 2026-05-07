# VEC IEC61360 SemanticHub Mapper (Python)

Dieses Python-Skript lädt Daten aus der VEC-Ontologie (TTL-Datei), parst diese lokal und mappt sie auf ein IEC61360-orientiertes JSON-Format.

Die Ausgabe enthält genau einen passenden Eintrag als ConceptDescription.

---

## Datenquelle

https://ecad-wiki.prostep.org/specifications/vec/v220/vec-2.2.0-ontology.ttl

---

## Was wird gemacht

- TTL-Datei wird heruntergeladen
- RDF-Daten werden mit rdflib geparst
- Begriff oder Semantic-ID wird gesucht
- RDF-Daten werden extrahiert
- Mapping auf IEC61360 erfolgt
- Ergebnis wird als JSON ausgegeben

---

## Suche

Das Skript unterscheidet zwischen:

- Begriffssuche → "WireElement"
- Semantic-ID → "http://...#WireElement"

---

## Mapping (VEC → IEC61360)

| IEC Feld | Property | Quelle |
|--------|--------|-------|
| semanticId | P1 | URI |
| preferredName | P35 | rdfs:label |
| shortName | P36 | Name |
| sourceOfDefinition | P40 | TTL URL |
| dataType | P42 | rdf:type |
| Definition | P44 | rdfs:comment |

Nicht vorhandene Felder → `null`

---

## Ausgabe

Die Ausgabe enthält:

- query
- total
- result

---

## additionalProperties

Alle nicht gemappten RDF-Properties werden hier gespeichert, z. B.:

- rdfs:subClassOf
- weitere Beziehungen

---

## Besonderheit

VEC ist eine Ontologie:

- basiert auf RDF/OWL
- enthält echte Bedeutungen
- enthält Beziehungen (z. B. Vererbung)
- enthält Definitionen

---

## Fazit

VEC liefert semantische Daten, die direkt sinnvoll auf IEC61360 gemappt werden können.
