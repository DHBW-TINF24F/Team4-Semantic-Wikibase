# Projekt 4: Semantic Wikibase – Einfach erklärt

## Übersicht

Das Projekt „Semantic Wikibase“ beschäftigt sich damit, wie Begriffe aus der Industrie (wie Maßeinheiten, Bauteile, Eigenschaften) eindeutig, offen und für Computer verständlich im Internet beschrieben werden können. Ziel ist es, eine Plattform zu bauen, auf der jeder solche Begriffe anlegen, beschreiben und wiederverwenden kann – ähnlich wie bei Wikipedia, aber speziell für industrielle Begriffe.

---

## Was ist das Problem?

- Es gibt schon Datenbanken für solche Begriffe (z.B. IEC-CDD, ECLASS), aber die sind oft:
  - schwer zugänglich
  - nicht offen für alle
  - technisch altmodisch (schlechte APIs, langsame Prozesse)
- Begriffe haben keine sprechenden, eindeutigen Web-Links (URIs), die man einfach benutzen kann.
- Neue Begriffe einzufügen oder zu standardisieren dauert lange.
- Maschinen und Programme können Begriffe nicht einfach und eindeutig nachschlagen.

---

## Was ist die Lösung des Projekts?

- Wir nutzen **Wikibase** (die Software hinter Wikidata/Wikipedia), um ein „Wikipedia für Industrie-Begriffe“ zu bauen.
- Jeder Begriff bekommt eine eigene, eindeutige Internetadresse (URI).
- Jeder kann neue Begriffe anlegen, beschreiben und nutzen.
- Die Plattform ist offen, modern und leicht zugänglich.
- Programme können über eine REST-API Begriffe abfragen und weiterverwenden.
- Später können Begriffe auf existierende Standards (IEC, ECLASS, etc.) gemappt oder weitergeleitet werden.

---

## Was ist AAS?

**AAS** steht für **Asset Administration Shell** („Verwaltungsschale“):

- Das ist das digitale „Datenblatt“ oder der „Steckbrief“ eines physischen Objekts (z.B. Maschine, Bauteil).
- Die AAS sammelt und verwaltet alle Daten über ein Asset, damit Computer diese Informationen automatisch nutzen können.
- Sie ist ein zentrales Konzept in der Industrie 4.0 und macht aus jedem Ding einen digitalen Zwilling.

---

## Projektstruktur

1. **Verstehen, wie Begriffe heute beschrieben werden:** Einarbeitung in AAS Concept Descriptions, Wikibase, vorhandene Standards.
2. **Wikibase aufsetzen und konfigurieren:** Testen, wie Begriffe angelegt und beschriftet werden können.
3. **Eine API entwickeln:** Damit andere Programme Begriffe abfragen können.
4. **Testen und vergleichen:** Funktioniert die Lösung besser als die alten Systeme?
5. **Community einbinden:** Lösung vorstellen, Feedback einholen, gemeinsam verbessern.

---

## Ziele des Projekts

- **Offene, auflösbare URIs** für Begriffe schaffen.
- **Niedrigschwelliger Zugang:** Jeder kann Begriffe anlegen und verwenden.
- **Migration und Weiterleitung:** Begriffe können auf offizielle Standards gemappt werden.
- **Spezifikation und Prototyp:** Einen ersten lauffähigen Prototypen und eine klare Beschreibung erstellen.
- **Optimale Wikibase-Konfiguration:** Damit der Arbeitsablauf einfach und effektiv ist.

---

## Warum ist das wichtig?

- Maschinen und Programme können so eindeutige Begriffe verwenden und verstehen.
- Firmen können weltweit besser zusammenarbeiten.
- Begriffe sind für alle zugänglich, offen und flexibel nutzbar.

---

## Quellen und Links

- [Wikibase](https://de.wikipedia.org/wiki/Wikibase)
- [AAS Concept Description](https://industrialdigitaltwin.io/aas-specifications/IDTA-01001/v3.2/spec-metamodel/concept-description.html)
- [Beispiel im Wiki](https://semanticid.aas-connect.com/w/index.php?title=Item:Q21&oldid=207)
- [ECLASS Webservice API](https://app.swaggerhub.com/apis/ECLASS_Standard/ECLASS_Download_JSON/2.0.3#/)
