# Moduldokumentation (MOD) 

*Dokumentverantwortliche: Technische Redakteure, Lucrezia Trabalza und Marina Hidalgo Burova*

---

## Versionskontrolle

| Version | Datum | Autor | Kommentar |
|---------|-------|-------|-----------|
| 1.0     | 27.04.2026 | Lucrezia Trabalza | Erstellung & erster Entwurf |
| 1.1     | 12.05.2026 | Lucrezia Trabalza, Marina Hidalgo Burova | Erweiterung der Moduldokumentation um OpenAPI-Spezifikation, Mapping-Zusammenführung, API-Architektur, Datenquellen, Wikibase-Integration, Suchfunktion, Fehlerbehandlung und Tests |

---

## Inhaltsverzeichnis

- [1. OpenAPI Spezifikation](#1-openapi-spezifikation)
  - [1.1 Ziel](#11-ziel)
  - [1.2 Funktionsweise der API](#12-funktionsweise-der-api)
  - [1.3 Beispiel-Endpunkt](#13-beispiel-endpunkt)
  - [1.4 Beispiel-Anfrage](#14-beispiel-anfrage)
  - [1.5 Beispiel-Antwort](#15-beispiel-antwort)
- [2. Zusammenführung der Mappings](#2-zusammenführung-der-mappings)
  - [2.1 Ziel](#21-ziel)
  - [2.2 Datenquellen](#22-datenquellen)
  - [2.3 Gemeinsames Zielmodell](#23-gemeinsames-zielmodell)
  - [2.4 Mapping-Regeln](#24-mapping-regeln)
  - [2.5 Zusammenführung der Einzelmappings](#25-zusammenführung-der-einzelmappings)
  - [2.6 Ergebnis](#26-ergebnis)
- [3. Architektur der API](#3-architektur-der-api)
  - [3.1 Überblick](#31-überblick)
- [4. Datenquellen und Mappings](#4-datenquellen-und-mappings)
  - [4.1 QUDT](#41-qudt)
  - [4.2 VEC](#42-vec)
  - [4.3 KBL](#43-kbl)
- [5. Gemeinsames Zielmodell](#5-gemeinsames-zielmodell)
- [6. Mapping-Prozess](#6-mapping-prozess)
- [7. Wikibase-Integration](#7-wikibase-integration)
- [8. Suchfunktion und SemanticId-Suche](#8-suchfunktion-und-semanticid-suche)
- [9. Fehlerbehandlung](#9-fehlerbehandlung)
- [10. Tests der Module](#10-tests-der-module)
- [11. Ergebnis und Ausblick](#11-ergebnis-und-ausblick)

---

## 1. OpenAPI Spezifikation

### 1.1 Ziel 

Ziel der OpenAPI-Spezifikation ist die standardisierte Beschreibung der REST-API der Semantic Wikibase.
Dadurch wird sichergestellt, dass externe Systeme (z. B. AAS-Clients) die API eindeutig verstehen und nutzen können.

---

### 1.2 Funktionsweise der API

Die API stellt semantische Definitionen (Concept Descriptions) auf Basis einer eindeutigen semantischen ID (SID) bereit.

Ein Client kann über eine HTTP-Anfrage eine Concept Description abrufen und erhält eine strukturierte Antwort im IEC 61360-ähnlichen JSON-Format.

---

### 1.3 Beispiel-Endpunkt

Die Semantic Wikibase stellt verschiedene REST-Endpunkte zur Verfügung. Für die Suche nach semantischen Definitionen wird ein API-Endpunkt verwendet, der Suchbegriff, Sprache und Typfilter entgegennehmen kann.

Beispiel eines Such-Endpunkts:

```http
GET /api/v3/search?search=Volt&lang=de&types=unit
```
Zusätzlich existieren bzw. sind folgende Endpunkte vorgesehen:
- Suche nach semantischen Definitionen
- Suche nach Semantic IDs
- Abruf einzelner Concept Descriptions
- Import und Export von Semantic IDs
- Mapping externer Datenquellen auf das IEC61360-Datenmodell

---

### 1.4 Beispiel-Anfrage

Beispiel einer HTTP-Anfrage:

```http
GET /api/v3/search?search=Volt&lang=de&types=unit
Host: semantic-hub.io
Accept: application/json
```
Die Anfrage sucht nach der semantischen Definition der Einheit „Volt“ in deutscher Sprache.

---

### 1.5 Beispiel-Antwort
Die API liefert die Daten im IEC61360-ähnlichen JSON-Format zurück.

Beispiel:

```json
{
  "modelType": "ConceptDescription",
  "id": "http://qudt.org/vocab/unit/V",
  "idShort": "V",
  "preferredName": "Volt",
  "symbol": "V",
  "dataType": "Unit",
  "definition": "Electric potential unit",
  "source": "QUDT"
}
```
Die Antwort enthält die wichtigsten semantischen Eigenschaften der jeweiligen Concept Description.

---

## 2. Zusammenführung der Mappings 

### 2.1 Ziel 

Ziel ist die Vereinheitlichung aller von den Gruppenmitgliedern erstellten Mappings in eine gemeinsame Struktur.

Dadurch wird sichergestellt, dass:
- alle Datenquellen konsistent verarbeitet werden
- die API ein einheitliches Ausgabeformat liefert
- die Daten in Wikibase einheitlich gespeichert werden

---

### 2.2 Datenquellen

Die Mappings basieren auf verschiedenen externen Quellen:
- QUDT
- VEC
- KBL

---

### 2.3 Gemeinsames Zielmodell

Alle externen Datenquellen werden in ein gemeinsames Zielmodell überführt.

Dadurch wird sichergestellt, dass:
- unterschiedliche Ontologien einheitlich verarbeitet werden können
- die REST-API ein konsistentes Ausgabeformat liefert
- Daten standardisiert in Wikibase gespeichert bzw. bereitgestellt werden

Das Zielmodell orientiert sich am IEC61360-Datentemplate der Asset Administration Shell.

Beispielstruktur:
```json
{
  "modelType": "ConceptDescription",
  "id": "http://qudt.org/vocab/unit/V",
  "idShort": "V",
  "preferredName": "Volt",
  "symbol": "V",
  "dataType": "Unit",
  "definition": "Electric potential unit",
  "source": "QUDT"
}
```

---

### 2.4 Mapping-Regeln

Die verschiedenen externen Datenquellen besitzen unterschiedliche Datenstrukturen und Formate.

Damit die Daten gemeinsam verarbeitet werden können, werden Mapping-Regeln definiert.

Dabei werden:
- RDF-Properties
- XML/XSD-Elemente
- Ontologie-Klassen
- sowie externe Attribute

auf ein gemeinsames IEC61360-kompatibles Datenmodell abgebildet.

Beispiele:
- `rdfs:label` → `preferredName`
- `qudt:symbol` → `symbol`
- `rdf:type` → `dataType`
- `dcterms:description` → `definition`
- URI bzw. Semantic ID → `id`
- lokaler URI-Name → `idShort`

Nicht direkt zuordenbare Eigenschaften werden nicht verworfen, sondern als zusätzliche Properties gespeichert oder für spätere Erweiterungen vorgesehen.

---

### 2.5 Zusammenführung der Einzelmappings

Die einzelnen Mapping-Module wurden unabhängig voneinander entwickelt und anschließend in eine gemeinsame Struktur integriert.

Dabei wurden:
- ein gemeinsames JSON-Zielmodell definiert
- gemeinsame Property-Namen festgelegt
- unterschiedliche Datentypen vereinheitlicht
- sowie ein konsistentes IEC61360-Format erstellt

Die Zusammenführung ermöglicht die gemeinsame Nutzung der Datenquellen innerhalb der Semantic Wikibase.

---

### 2.6 Ergebnis

Durch die Zusammenführung der verschiedenen Mappings konnte eine gemeinsame semantische Plattform aufgebaut werden.

Die Semantic Wikibase kann dadurch:
- Daten aus unterschiedlichen Quellen verarbeiten
- semantische Definitionen standardisiert bereitstellen
- sowie Concept Descriptions über REST-Endpunkte ausgeben.

Die entwickelte Struktur bildet die Grundlage für zukünftige Erweiterungen und zusätzliche Ontologien.

---

## 3. Architektur der API

### 3.1 Überblick

Die Semantic Wikibase verwendet eine REST-basierte API-Architektur zur Bereitstellung semantischer Definitionen.

Die API dient als Vermittlungsschicht zwischen:
- externen Datenquellen (QUDT, VEC, KBL)
- der Wikibase
- und externen Clients wie AAS-Systemen oder dem AASX-Explorer

Die Kommunikation erfolgt über HTTP-Endpunkte.
Die Antworten werden als JSON im IEC61360-ähnlichen Format zurückgegeben.

Die Architektur besteht aus folgenden Komponenten:
- API-Schicht (FastAPI / Flask)
- Mapping-Schicht
- Wikibase
- externe semantische Datenquellen

---

## 4. Datenquellen und Mappings

### 4.1 QUDT

QUDT (Quantities, Units, Dimensions and Types) dient als Quelle für physikalische Einheiten und Größen.

Die Daten werden über:
- SPARQL-Abfragen
- RDF/Turtle-Dateien
- sowie REST-Zugriffe

abgerufen.

Die QUDT-Daten werden anschließend auf das IEC61360-Datenmodell gemappt.
Dabei werden unter anderem folgende Eigenschaften übernommen:
- Symbol
- Label
- Beschreibung
- Einheit
- Datentyp
- SI-Ausdruck
- QuantityKind

---

### 4.2 VEC

Die VEC-Ontologie (Vehicle Electric Container) wird verwendet, um semantische Fahrzeug- und Kabelbaumdaten bereitzustellen.

Die Ontologie liegt als RDF/TTL-Modell vor und wird über Python-Mapper verarbeitet.

Die Daten werden analysiert und anschließend in das gemeinsame IEC61360-Zielmodell überführt.

---

### 4.3 KBL

KBL (Kabelbaumliste) basiert auf XML/XSD-Strukturen und beschreibt Kabelbaumdaten.

Die Daten werden über eigene Mapping-Module eingelesen und analysiert.

Anschließend erfolgt die Überführung der Inhalte in das standardisierte JSON-Zielmodell der Semantic Wikibase.

---

## 5. Gemeinsames Zielmodell

Alle externen Datenquellen werden in ein gemeinsames JSON-Zielmodell überführt.

Dadurch können unterschiedliche Ontologien und Standards einheitlich verarbeitet werden.

Beispielstruktur:

```json
{
  "modelType": "ConceptDescription",
  "id": "http://qudt.org/vocab/unit/V",
  "idShort": "V",
  "preferredName": "Volt",
  "symbol": "V",
  "dataType": "Unit",
  "definition": "Electric potential unit",
  "source": "QUDT"
}
```

Das gemeinsame Zielmodell basiert auf dem IEC61360-Datentemplate der Asset Administration Shell.

---

## 6. Mapping-Prozess

Der Mapping-Prozess besteht aus mehreren Verarbeitungsschritten:

1. Abruf der externen Datenquelle
2. Analyse der RDF-, TTL- oder XML-Daten
3. Extraktion relevanter Eigenschaften
4. Transformation in das IEC61360-Format
5. Übergabe an die REST-API
6. Speicherung bzw. Bereitstellung in Wikibase

Durch diesen Prozess können verschiedene semantische Standards gemeinsam verwendet werden.

---

## 7. Wikibase-Integration

Die Semantic Wikibase dient als zentrale Plattform zur Verwaltung semantischer Definitionen.

Die gemappten Daten können:
- über REST-Endpunkte abgefragt
- über Suchfunktionen gefunden
- und über auflösbare URIs referenziert werden.

Die Wikibase ermöglicht außerdem:
- Mehrsprachigkeit
- Versionierung
- Verlinkungen zwischen Concept Descriptions
- sowie die Integration externer Quellen.

Ein Teil der Funktionen ist bereits umgesetzt bzw. vorbereitet. Weitere Funktionen, wie eine vollständige Import-/Export-Schnittstelle und ein erweitertes Rechtemanagement, sind als zukünftige Erweiterungen vorgesehen.

---

## 8. Suchfunktion und SemanticId-Suche

Die Suchfunktion ermöglicht das Auffinden semantischer Definitionen anhand:
- von Namen
- Semantic IDs
- URIs
- Eigenschaften
- oder Quellen.

Zusätzlich wurde eine Suche nach Semantic IDs vorgesehen bzw. integriert. Dadurch können AAS-Systeme gezielt nach bestimmten Concept Descriptions suchen und diese direkt abrufen.

Für die Benutzeroberfläche ist außerdem vorgesehen, den Einstieg in die Suche zu vereinfachen, z. B. durch ein gut sichtbares Suchfeld auf der Startseite. Dadurch sollen auch Nutzer ohne tieferes Wikibase-Wissen schnell passende semantische Definitionen finden können.

---

## 9. Fehlerbehandlung

Die API prüft:
- ungültige Suchanfragen
- fehlende Parameter
- nicht erreichbare Datenquellen
- sowie fehlerhafte Mapping-Ergebnisse.

Fehler werden als strukturierte JSON-Antworten zurückgegeben.

---

## 10. Tests der Module

Die einzelnen API- und Mapping-Module wurden bzw. werden durch verschiedene Testarten überprüft.

Dazu gehören:
- Funktionstests
- API-Tests
- Integrationstests
- Mapping-Tests
- Tests der Suchfunktion

Dabei wird geprüft, ob:
- API-Endpunkte erreichbar sind
- Suchanfragen korrekt verarbeitet werden
- externe Datenquellen korrekt ausgelesen werden
- Mapping-Ergebnisse dem gemeinsamen Zielmodell entsprechen
- Fehlerfälle strukturiert behandelt werden

Die detaillierten Testfälle und Testergebnisse werden im STP und STR dokumentiert.

---

## 11. Ergebnis und Ausblick

Durch die entwickelte bzw. vorbereitete Semantic Wikibase wurde eine gemeinsame Grundlage zur semantischen Verwaltung von Concept Descriptions geschaffen.

Die Integration von:
- QUDT
- VEC
- und KBL

zeigt, dass unterschiedliche semantische Quellen in ein gemeinsames IEC61360-nahes Modell überführt werden können.

Die API- und Mapping-Struktur bildet die Grundlage dafür, semantische Definitionen standardisiert bereitzustellen und über REST-Endpunkte abrufbar zu machen.

Zukünftig könnten weitere Ontologien und Standards integriert werden. Außerdem können die SemanticId-Suche, Import- und Exportfunktionen sowie das Rechtemanagement weiter ausgebaut werden.


