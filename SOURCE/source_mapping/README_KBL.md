# KBL IEC61360 SemanticHub Mapper (Python)

Dieses Python-Skript lädt eine KBL-XSD-Datei und extrahiert daraus Strukturinformationen, die auf ein IEC61360-orientiertes JSON-Format gemappt werden.

Die Ausgabe enthält genau einen passenden Eintrag als ConceptDescription.

---

## Datenquelle

https://ecad-wiki.prostep.org/specifications/kbl/v25-sr1/kbl2.5-sr1.xsd

---

## Was wird gemacht

- XSD-Datei wird heruntergeladen
- XML wird geparst
- komplexe Typen werden durchsucht
- gesuchter Typ wird extrahiert
- Struktur wird analysiert
- Mapping auf IEC61360 erfolgt
- Ergebnis wird als JSON ausgegeben

---

## Suche

Das Skript durchsucht:

- xs:complexType
- xs:simpleType
- xs:element

Beispiel:

Wire_occurrence

---

## Mapping (KBL → IEC61360)

| IEC Feld | Property | Quelle |
|--------|--------|-------|
| semanticId | P1 | XSD URL + #Name |
| preferredName | P35 | Typname |
| shortName | P36 | Typname |
| sourceOfDefinition | P40 | XSD URL |
| dataType | P42 | XSDComplexType / XSDSimpleType |
| Definition | P44 | generiert |

Nicht vorhandene Felder → `null`

---

## additionalProperties

Hier wird die Struktur gespeichert:

- xsdType → Typ (ComplexType)
- extensionBase → Vererbung
- children → Elemente
- attributes → Attribute

---

## Beispiel

- Wire_occurrence hat:
  - extensionBase = General_wire_occurrence
  - child = Wire_number

---

## Besonderheit

KBL ist KEINE Ontologie:

- basiert auf XML/XSD
- beschreibt nur Struktur
- keine echten Bedeutungen
- keine semantischen Beziehungen

---

## Warum viele Felder null sind

KBL enthält keine:

- Labels
- Definitionen
- Einheiten

→ deshalb müssen einige Werte generiert werden

---

## Fazit

KBL liefert Strukturinformationen, die auf IEC61360 gemappt werden, auch wenn keine semantischen Inhalte vorhanden sind.