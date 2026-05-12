# Benutzer Manual - Semantic Wikibase
## Nutzung der Weboberfläche und API im aktuellen Projektstand

*Dokumentverantwortliche: Technische Redakteure, Lucrezia Trabalza und Marina Hidalgo Burova*

---

## Versionskontrolle 

| Version | Datum | Autor | Kommentar |
|---------|-------|-------|-----------|
| 1.0     | 27.04.2026 | Lucrezia Trabalza | Erstellung & erster Entwurf |
| 1.1     | 12.05.2026 | Lucrezia Trabalza, Marina Hidalgo Burova | Erweiterung der Benutzeranleitung um Plattformbeschreibung, Suchfunktion, API-Nutzung, lokale Tests, Fehlerfälle und Projektstand |

---

## Inhaltsverzeichnis

- [1. Einleitung](#1-einleitung)
- [2. Zweck der Semantic Wikibase](#2-zweck-der-semantic-wikibase)
- [3. Zielgruppen](#3-zielgruppen)
- [4. Grundbegriffe](#4-grundbegriffe)
  - [Asset Administration Shell (AAS)](#asset-administration-shell-aas)
  - [Concept Description](#concept-description)
  - [Semantic ID](#semantic-id)
  - [IEC 61360](#iec-61360)
  - [Wikibase](#wikibase)
- [5. Geplante Funktionsweise der Wikibase](#5-geplante-funktionsweise-der-wikibase)
  - [5.1 Startseite und Suche](#51-startseite-und-suche)
  - [5.2 Concept Description anzeigen](#52-concept-description-anzeigen)
  - [5.3 Concept Description erstellen oder bearbeiten](#53-concept-description-erstellen-oder-bearbeiten)
  - [5.4 Nutzung durch externe Systeme](#54-nutzung-durch-externe-systeme)
- [6. Nutzung der API](#6-nutzung-der-api)
  - [6.1 Übersicht der relevanten API-Endpunkte](#61-übersicht-der-relevanten-api-endpunkte)
  - [6.2 Zweck der API](#62-zweck-der-api)
  - [6.3 Suche nach semantischen Definitionen](#63-suche-nach-semantischen-definitionen)
  - [6.4 Abruf einer Concept Description](#64-abruf-einer-concept-description)
  - [6.5 Beispielantwort](#65-beispielantwort)
  - [6.6 Fehlerfälle](#66-fehlerfälle)
- [7. Lokales Testen der API](#7-lokales-testen-der-api)
  - [7.1 Voraussetzungen](#71-voraussetzungen)
  - [7.2 Übersicht der lokalen Testvarianten](#72-übersicht-der-lokalen-testvarianten)
  - [7.3 Starten der API](#73-starten-der-api)
  - [7.4 Test über Browser](#74-test-über-browser)
  - [7.5 Test über Swagger UI](#75-test-über-swagger-ui)
  - [7.6 Test über curl](#76-test-über-curl)
- [8. Typische Nutzungsszenarien](#8-typische-nutzungsszenarien)
  - [8.1 Nutzer sucht nach einer Einheit](#81-nutzer-sucht-nach-einer-einheit)
  - [8.2 Entwickler testet die API](#82-entwickler-testet-die-api)
  - [8.3 AAS-System löst eine Semantic ID auf](#83-aas-system-löst-eine-semantic-id-auf)
  - [8.4 Daten aus externer Quelle werden gemappt](#84-daten-aus-externer-quelle-werden-gemappt)
- [9. Bekannte Einschränkungen](#9-bekannte-einschränkungen)
- [10. Zusammenfassung](#10-zusammenfassung)
  
---

## 1. Einleitung

Diese Benutzeranleitung beschreibt die geplante und teilweise vorbereitete Nutzung der **Semantic Wikibase**.

Die Plattform dient als zentrale, webbasierte Umgebung zur Verwaltung und Bereitstellung semantischer Definitionen. Diese semantischen Definitionen werden im Kontext der **Asset Administration Shell (AAS)** als **Concept Descriptions** verwendet.

Ziel ist es, Begriffe, Eigenschaften, Einheiten und Definitionen eindeutig auffindbar, referenzierbar und maschinenlesbar bereitzustellen.

Die Benutzeranleitung richtet sich sowohl an normale Nutzer der Weboberfläche als auch an Entwickler, die die API testen oder in externe Systeme integrieren möchten.

Da sich das Projekt noch in der Entwicklung befindet, beschreibt dieses Dokument sowohl den geplanten Zielzustand als auch die bereits vorbereiteten bzw. umgesetzten Funktionen.

---

## 2. Zweck der Semantic Wikibase

Die Semantic Wikibase soll eine offene Plattform bereitstellen, auf der semantische Definitionen verwaltet und veröffentlicht werden können.

Im Mittelpunkt stehen sogenannte **Semantic IDs** bzw. **auflösbare URIs**. Jede Concept Description soll über eine eindeutige Adresse erreichbar sein. Dadurch können externe Systeme eindeutig auf die jeweilige Bedeutung eines Begriffs verweisen.

Die Plattform soll insbesondere folgende Probleme lösen:

- semantische Definitionen sollen zentral auffindbar sein
- Begriffe sollen über stabile URIs referenziert werden können
- AAS-Systeme sollen Concept Descriptions über eine API abrufen können
- Daten aus verschiedenen Quellen sollen in ein gemeinsames Format überführt werden
- Nutzer sollen Begriffe über eine Weboberfläche suchen und ansehen können

Dadurch soll die Semantic Wikibase langfristig als zentrale Registry für semantische Definitionen dienen.

---

## 3. Zielgruppen

Die Semantic Wikibase richtet sich an verschiedene Nutzergruppen.

| Zielgruppe | Nutzung |
|-----------|---------|
| **Normale Nutzer** | Suchen und Anzeigen semantischer Definitionen |
| **Fachexperten** | Prüfen, Ergänzen oder Erstellen von Concept Descriptions |
| **Entwickler** | Testen und Einbinden der REST-API |
| **AAS-Systeme** | Maschinenlesbarer Abruf von Concept Descriptions |
| **Systemintegratoren** | Anbindung der Semantic Wikibase an bestehende Systeme |
| **Projektteam** | Dokumentation, Weiterentwicklung und Qualitätssicherung |

Die Benutzeranleitung ist deshalb so aufgebaut, dass sowohl nicht-technische Nutzer als auch Entwickler die wichtigsten Funktionen nachvollziehen können.

---

## 4. Grundbegriffe

### Asset Administration Shell (AAS)

Die **Asset Administration Shell** ist der digitale Zwilling eines realen oder virtuellen Assets. Ein Asset kann zum Beispiel eine Maschine, ein Bauteil, ein Sensor oder ein technisches System sein.

Die AAS beschreibt dieses Asset in strukturierter und maschinenlesbarer Form.

---

### Concept Description

Eine **Concept Description** beschreibt die semantische Bedeutung eines Begriffs oder einer Eigenschaft.

Beispiel:

Ein Submodel-Element besitzt den Namen `Voltage`. Die Concept Description beschreibt dann eindeutig, dass damit elektrische Spannung gemeint ist, welche Einheit verwendet wird und welche externe Quelle dazu gehört.

---

### Semantic ID

Eine **Semantic ID** ist eine eindeutige Referenz auf eine semantische Definition.

Beispiel:

```text
http://qudt.org/vocab/unit/V
```
Diese ID kann von externen Systemen genutzt werden, um die Bedeutung einer Eigenschaft eindeutig zu bestimmen.

---

### IEC 61360

IEC 61360 ist ein Datenmodell zur standardisierten Beschreibung technischer Merkmale. Im Projekt dient dieses Modell als Orientierung für die Struktur der Concept Descriptions.

Typische Felder sind:

- preferredName
- shortName
- definition
- unit
- symbol
- dataType
- valueFormat
- sourceOfDefinition

---

### Wikibase

Wikibase ist die technische Grundlage der Plattform. Sie ermöglicht das strukturierte Speichern, Bearbeiten, Verknüpfen und Versionieren von semantischen Daten.

---

## 5. Geplante Funktionsweise der Wikibase

Die Semantic Wikibase soll Nutzern eine einfache Möglichkeit bieten, semantische Definitionen zu suchen, anzuzeigen und perspektivisch auch zu bearbeiten.

Die Plattform orientiert sich dabei an bekannten Wiki-Systemen. Nutzer sollen Begriffe nicht nur als Text sehen, sondern strukturierte Informationen erhalten, die auch von Maschinen verarbeitet werden können.

---

### 5.1 Startseite und Suche

Die Startseite der Semantic Wikibase soll Nutzern einen einfachen Einstieg ermöglichen.

Geplant ist ein gut sichtbares Suchfeld, über das Nutzer nach semantischen Definitionen suchen können.

Gesucht werden kann nach:

- Namen, z. B. `Volt`
- Semantic IDs
- URIs
- Eigenschaften
- Quellen, z. B. `QUDT`, `VEC` oder `KBL`

Beispiel:

```text
Volt
```

oder:

```text
http://qudt.org/vocab/unit/V
```

Nach dem Absenden der Suche soll die passende Concept Description angezeigt oder eine Liste möglicher Treffer ausgegeben werden.

---

### 5.2 Concept Description anzeigen

Eine Concept Description soll in der Weboberfläche mit ihren wichtigsten Eigenschaften angezeigt werden.

Typische Informationen sind:

| Feld | Bedeutung |
|------|----------|
| ID / URI | Eindeutige semantische ID |
| preferredName | Bevorzugter Name des Begriffs |
| shortName | Kurzname |
| definition | Beschreibung / Definition |
| unit | Einheit |
| symbol | Einheitensymbol |
| dataType | Datentyp oder semantische Klasse |
| sourceOfDefinition | Quelle der Definition |
| externalReference | Verweis auf externe Standards |

Beispiel für eine Concept Description:

| Feld | Beispiel |
|------|----------|
| ID | `http://qudt.org/vocab/unit/V` |
| preferredName | Volt |
| shortName | V |
| symbol | V |
| dataType | Unit |
| source | QUDT |

Die Anzeige soll so aufgebaut sein, dass sowohl Menschen als auch externe Systeme die Bedeutung eines Begriffs nachvollziehen können. Für normale Nutzer steht die verständliche Darstellung im Vordergrund, während für Entwickler und AAS-Systeme vor allem die eindeutige URI und die maschinenlesbaren Daten wichtig sind.

---

### 5.3 Concept Description erstellen oder bearbeiten

Berechtigte Nutzer sollen Concept Descriptions in der Wikibase erstellen oder bearbeiten können.

Ein Nutzer kann dabei:

1. einen neuen Begriff anlegen
2. eine eindeutige ID bzw. URI vergeben
3. Namen und Beschreibungen ergänzen
4. Einheiten oder Symbole eintragen
5. externe Quellen verlinken
6. Änderungen speichern

Diese Funktion ist im aktuellen Projektstand konzeptionell vorgesehen und abhängig vom späteren Rechtemodell der Wikibase. Erste Strukturen sind vorbereitet, eine vollständige produktive Bearbeitungs- und Freigabefunktion ist jedoch noch nicht abgeschlossen.

Im geplanten Zielsystem sollen nicht alle Nutzer uneingeschränkt schreiben dürfen. Für spätere Versionen ist ein Rollen- und Rechtekonzept vorgesehen. Dadurch soll verhindert werden, dass fehlerhafte oder nicht geprüfte Daten unkontrolliert in die Semantic Wikibase übernommen werden.

---

### 5.4 Nutzung durch externe Systeme

Externe Systeme, zum Beispiel AAS-Backends oder AASX-Tools, sollen Concept Descriptions nicht manuell auslesen müssen.

Stattdessen können sie über eine REST-API eine Semantic ID oder einen Suchbegriff anfragen und erhalten eine strukturierte JSON-Antwort.

Beispielhafter Ablauf:

1. Ein AAS-System besitzt eine Semantic ID.
2. Das System sendet eine Anfrage an die API.
3. Die API sucht die passende Concept Description.
4. Die Daten werden in einem IEC61360-nahen JSON-Format zurückgegeben.
5. Das AAS-System kann die Antwort weiterverarbeiten.

Dadurch können semantische Definitionen zentral gepflegt und von mehreren Systemen wiederverwendet werden.

---

## 6. Nutzung der API

Die API dient dazu, semantische Definitionen maschinenlesbar bereitzustellen.

Sie ermöglicht:

- Suche nach Concept Descriptions
- Abruf einzelner semantischer Definitionen
- sprachabhängige Rückgabe von Daten
- Filterung nach Typen
- Bereitstellung der Daten im JSON-Format
- Mapping externer Quellen auf ein gemeinsames Zielmodell

Die API ist besonders für Entwickler und externe Systeme relevant, die Concept Descriptions automatisiert abrufen möchten.

Im Projekt wird die API genutzt, um externe Datenquellen wie QUDT, VEC oder KBL in ein gemeinsames Format zu überführen. Dieses gemeinsame Zielmodell orientiert sich am IEC61360-Datentemplate der Asset Administration Shell.

---

### 6.1 Übersicht der relevanten API-Endpunkte

Im Projekt werden verschiedene API-Endpunkte betrachtet. Einige davon sind bereits lokal testbar, andere beschreiben den geplanten Zielzustand der Semantic Wikibase.

| Endpunkt | Status | Zweck |
|---------|--------|-------|
| `/api/v3/search` | vorbereitet / prototypisch | Suche nach semantischen Definitionen über Suchbegriff, Sprache und Typfilter |
| `/map` | lokal testbar | Mapping von QUDT-Daten auf eine IEC61360-nahe JSON-Struktur |
| `/semanticIds/{identifier}` | geplant | Abruf einer bestimmten Semantic ID |
| `/semanticIds` | geplant | Auflistung, Import oder Export mehrerer Semantic IDs |
| `/semantic/{sid}` | geplant / Zielarchitektur | Auflösung einer Semantic ID als Concept Description |

Diese Übersicht dient dazu, zwischen bereits testbaren Funktionen und geplanten Ziel-Endpunkten zu unterscheiden. Dadurch ist nachvollziehbar, welche Bestandteile aktuell prototypisch umgesetzt sind und welche Funktionen im weiteren Projektverlauf ergänzt werden sollen.

---

### 6.2 Zweck der API

Der Zweck der API besteht darin, semantische Daten nicht nur über die Weboberfläche, sondern auch technisch nutzbar bereitzustellen.

Dadurch können AAS-Systeme, Entwickler oder andere Anwendungen auf semantische Definitionen zugreifen, ohne diese manuell aus der Wikibase auslesen zu müssen.

Die API nimmt eine Anfrage entgegen, sucht die passende semantische Definition und gibt das Ergebnis als JSON zurück.

Ein typischer Ablauf sieht wie folgt aus:

1. Ein Client sendet eine Anfrage mit einem Suchbegriff oder einer Semantic ID.
2. Die API verarbeitet die Anfrage.
3. Die passende Datenquelle wird abgefragt oder ein vorhandener Eintrag wird gelesen.
4. Die Daten werden auf das gemeinsame Zielmodell gemappt.
5. Die API gibt eine strukturierte JSON-Antwort zurück.

---

### 6.3 Suche nach semantischen Definitionen

Ein Such-Endpunkt kann verwendet werden, um nach Begriffen, IDs oder URIs zu suchen.

Beispiel:

```http
GET /api/v3/search?search=Volt&lang=de&types=unit
```

Bedeutung der Parameter:

| Parameter | Bedeutung | Beispiel |
|----------|-----------|----------|
| `search` | Suchbegriff, URI oder ID | `Volt` |
| `lang` | Sprache der Antwort | `de` oder `en` |
| `types` | Typfilter | `unit` |

Beispiel mit vollständiger URI:

```http
GET /api/v3/search?search=http://qudt.org/vocab/unit/V&lang=de&types=unit
```

Die Anfrage sucht nach der semantischen Definition der Einheit `Volt` und gibt das Ergebnis in deutscher Sprache zurück, sofern entsprechende Daten vorhanden sind.

Der Such-Endpunkt ist besonders nützlich, wenn ein Nutzer oder ein externes System nicht die genaue interne ID der Concept Description kennt, sondern nur einen Begriff oder eine externe URI besitzt.

---

### 6.4 Abruf einer Concept Description

Für den direkten Abruf einer Concept Description ist ein Endpunkt vorgesehen, der eine Semantic ID oder einen Identifier entgegennimmt.

Beispielhaft:

```http
GET /semanticIds/{identifier}
```

oder als geplante semantische API:

```http
GET /semantic/{sid}?lang=de
```

Beispiel:

```http
GET /semantic/http://qudt.org/vocab/unit/V?lang=de
```

Die API gibt anschließend die passende Concept Description zurück.

Der Abruf einer einzelnen Concept Description ist besonders wichtig für AAS-Systeme, da diese häufig bereits eine Semantic ID besitzen und nur die dazugehörige Beschreibung auflösen müssen.

Im aktuellen Projektstand ist dieser direkte Abruf als Zielarchitektur vorgesehen. Lokal testbar sind vor allem die Such- und Mapping-Endpunkte, über die semantische Definitionen anhand eines Suchbegriffs oder einer URI gefunden und in eine IEC61360-nahe Struktur überführt werden können.

---

### 6.5 Beispielantwort

Eine vereinfachte Beispielantwort kann wie folgt aussehen:

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

Die Antwort enthält die wichtigsten Informationen zur angefragten Concept Description.

| Feld | Bedeutung |
|------|----------|
| `modelType` | Gibt an, dass es sich um eine Concept Description handelt |
| `id` | Eindeutige semantische ID oder URI |
| `idShort` | Kurzbezeichnung des Eintrags |
| `preferredName` | Bevorzugter Name des Begriffs |
| `symbol` | Symbol der Einheit oder Eigenschaft |
| `dataType` | Typ des Eintrags |
| `definition` | Beschreibung oder Definition |
| `source` | Herkunft der Daten |

Eine ausführlichere Antwort kann zusätzlich eine IEC61360-nahe Struktur enthalten:

```json
{
  "modelType": "ConceptDescription",
  "id": "http://qudt.org/vocab/unit/V",
  "idShort": "V",
  "embeddedDataSpecifications": [
    {
      "dataSpecificationContent": {
        "modelType": "DataSpecificationIec61360",
        "semanticId": {
          "value": "http://qudt.org/vocab/unit/V"
        },
        "preferredName": {
          "value": [
            {
              "value": "Volt",
              "lang": "en"
            }
          ]
        },
        "unit": {
          "value": "Volt"
        },
        "symbol": {
          "value": "V"
        },
        "dataType": {
          "value": "qudt:Unit"
        }
      }
    }
  ]
}
```

Diese Struktur ist besonders für AAS-Systeme relevant, da sie sich am Aufbau einer Concept Description nach IEC61360 orientiert.

---

### 6.6 Fehlerfälle

Wenn eine Anfrage nicht korrekt verarbeitet werden kann, gibt die API eine strukturierte Fehlermeldung zurück.

Typische Fehlerfälle sind:

| Fehler | Ursache | Beispiel |
|-------|---------|----------|
| Leerer Suchbegriff | Parameter `search` fehlt oder ist leer | `400 Bad Request` |
| Kein Treffer | Es wurde keine passende Concept Description gefunden | `404 Not Found` |
| Datenquelle nicht erreichbar | Externe Quelle wie QUDT ist nicht verfügbar | `500 Internal Server Error` |
| Ungültiger Typfilter | Der angegebene Typ wird nicht unterstützt | `400 Bad Request` |
| Mapping-Fehler | Externe Daten konnten nicht korrekt umgewandelt werden | `500 Internal Server Error` |

Beispiel für eine Fehlermeldung:

```json
{
  "detail": "Parameter 'search' darf nicht leer sein."
}
```

Durch strukturierte Fehlermeldungen kann besser nachvollzogen werden, warum eine Anfrage fehlgeschlagen ist. Das erleichtert sowohl die Entwicklung als auch die Fehlersuche beim Testen der API.

---

## 7. Lokales Testen der API

Dieses Kapitel beschreibt, wie die API lokal gestartet und getestet werden kann.

Das lokale Testen ist wichtig, um einzelne Funktionen unabhängig von einer produktiven Serverumgebung zu prüfen. Dadurch können Entwickler testen, ob Suchanfragen, Mapping und JSON-Antworten korrekt funktionieren.

---

### 7.1 Voraussetzungen

Für das lokale Testen der API werden folgende Werkzeuge benötigt:

- Python 3.11 oder eine kompatible Python-Version
- installierte Python-Abhängigkeiten aus dem Projekt
- Zugriff auf das Projekt-Repository
- Terminal oder VS Code Terminal
- optional: Browser für Swagger UI
- optional: curl für API-Tests über die Kommandozeile

Vor dem Start sollte geprüft werden, ob Python korrekt installiert ist:

```bash
python --version
```

oder:

```bash
python3 --version
```

Außerdem sollte sichergestellt werden, dass man sich im richtigen Projektordner befindet.

---

### 7.2 Übersicht der lokalen Testvarianten

Im Projekt existieren zwei relevante lokale Testvarianten. Je nach verwendeter Implementierung wird entweder eine FastAPI- oder eine Flask-basierte API gestartet.

| Variante | Startbefehl | Beispiel-URL |
|---------|-------------|--------------|
| FastAPI-QUDT-Mapping | `uvicorn api_qudt:app --reload` | `http://localhost:8000/map?search=Volt&lang=de&types=unit` |
| Flask-Wikibase-API | `python app.py` | `http://localhost:5000/api/v3/search?search=Volt&lang=de&types=unit` |

Die FastAPI-Variante eignet sich besonders zum Testen des QUDT-Mappings. Die Flask-Variante beschreibt die API-Struktur der Semantic Wikibase und kann zur Suche nach semantischen Definitionen verwendet werden.

Welche Variante genutzt wird, hängt davon ab, welcher Projektordner und welche Implementierung lokal gestartet wird.

---

### 7.3 Starten der API

Zuerst wird in den passenden Projektordner gewechselt. Der genaue Ordner hängt davon ab, ob die Flask- oder FastAPI-Variante getestet wird.

Beispiel für die Flask-basierte API:

```bash
cd SOURCE/Wikibase_API
```

Falls ein virtuelles Python-Environment verwendet wird, kann dieses wie folgt erstellt werden:

```bash
python -m venv .venv
```

Aktivieren unter Windows:

```bash
.venv\Scripts\activate
```

Aktivieren unter macOS/Linux:

```bash
source .venv/bin/activate
```

Anschließend werden die benötigten Abhängigkeiten installiert:

```bash
pip install -r requirements.txt
```

Danach kann die Flask-basierte API gestartet werden:

```bash
python app.py
```

Falls die FastAPI-Implementierung verwendet wird, kann diese alternativ mit Uvicorn gestartet werden:

```bash
uvicorn api_qudt:app --reload
```

Nach dem Start sollte im Terminal angezeigt werden, unter welcher lokalen Adresse die API erreichbar ist. Typische lokale Adressen sind:

```text
http://localhost:5000
```

für Flask oder:

```text
http://localhost:8000
```

für FastAPI.

---

### 7.4 Test über Browser

Nach dem Start kann die API direkt im Browser getestet werden.

Beispiel für eine FastAPI-Variante:

```text
http://localhost:8000/map?search=Volt&lang=de&types=unit
```

Beispiel für eine Flask-Variante:

```text
http://localhost:5000/api/v3/search?search=Volt&lang=de&types=unit
```

Wenn die API korrekt läuft, wird eine JSON-Antwort mit Informationen zur Einheit `Volt` ausgegeben.

Falls keine Antwort erscheint, sollten folgende Punkte geprüft werden:

- Läuft die API im Terminal?
- Wurde der richtige Port verwendet?
- Befindet man sich im richtigen Projektordner?
- Sind alle benötigten Python-Pakete installiert?
- Ist die externe Datenquelle erreichbar?

---

### 7.5 Test über Swagger UI

Falls die FastAPI-Variante genutzt wird, kann die automatische API-Dokumentation geöffnet werden.

Beispiel:

```text
http://localhost:8000/docs
```

Dort kann der Endpunkt direkt im Browser getestet werden.

Vorgehen:

1. Swagger UI öffnen
2. Endpunkt `/map` auswählen
3. `Try it out` anklicken
4. Parameter eintragen, z. B.:
   - `search`: `Volt`
   - `lang`: `de`
   - `types`: `unit`
5. Anfrage ausführen
6. JSON-Antwort prüfen

Swagger UI ist besonders hilfreich, weil die API dort ohne zusätzliches Tool getestet werden kann.

---

### 7.6 Test über curl

Die API kann auch über die Kommandozeile mit `curl` getestet werden.

Beispiel für FastAPI:

```bash
curl "http://localhost:8000/map?search=Volt&lang=de&types=unit"
```

Beispiel für Flask:

```bash
curl "http://localhost:5000/api/v3/search?search=Volt&lang=de&types=unit"
```

Erwartet wird eine JSON-Antwort mit Informationen zur Einheit `Volt`.

Wenn eine Fehlermeldung zurückgegeben wird, sollte geprüft werden, ob der Suchbegriff korrekt ist und ob die API tatsächlich läuft.

---

## 8. Typische Nutzungsszenarien

In diesem Kapitel werden typische Anwendungsfälle der Semantic Wikibase beschrieben.

Die Szenarien zeigen, wie normale Nutzer, Entwickler und externe Systeme mit der Plattform arbeiten können.

---

### 8.1 Nutzer sucht nach einer Einheit

Ein Nutzer möchte Informationen zur Einheit `Volt` finden.

Ablauf:

1. Der Nutzer öffnet die Semantic Wikibase.
2. Der Nutzer gibt `Volt` in das Suchfeld ein.
3. Das System zeigt passende Concept Descriptions an.
4. Der Nutzer öffnet den passenden Eintrag.
5. Der Nutzer sieht URI, Symbol, Beschreibung und Quelle.

Ziel dieses Szenarios ist es, semantische Definitionen einfach auffindbar und verständlich darzustellen.

---

### 8.2 Entwickler testet die API

Ein Entwickler möchte prüfen, ob die API eine Concept Description korrekt zurückgibt.

Ablauf:

1. Der Entwickler startet die API lokal.
2. Der Entwickler ruft den Such-Endpunkt auf.
3. Die API verarbeitet den Suchbegriff.
4. Die passenden Daten werden aus der Quelle gelesen.
5. Die Daten werden in ein gemeinsames Zielmodell überführt.
6. Die API gibt eine JSON-Antwort zurück.
7. Der Entwickler prüft die Antwort.

Beispiel:

```http
GET /api/v3/search?search=Volt&lang=de&types=unit
```

Dieses Szenario ist besonders wichtig für die Entwicklung und Qualitätssicherung der API.

---

### 8.3 AAS-System löst eine Semantic ID auf

Ein AAS-System enthält eine Semantic ID zu einem Submodel-Element.

Ablauf:

1. Das AAS-System liest die Semantic ID.
2. Das System sendet eine Anfrage an die Semantic Wikibase API.
3. Die API sucht die passende Concept Description.
4. Die API gibt die Daten im JSON-Format zurück.
5. Das AAS-System verwendet die Antwort zur semantischen Interpretation des Elements.

Dadurch kann ein AAS-System externe semantische Definitionen zentral abrufen, ohne diese lokal speichern zu müssen.

---

### 8.4 Daten aus externer Quelle werden gemappt

Eine externe Quelle wie QUDT, VEC oder KBL soll in die gemeinsame Struktur überführt werden.

Ablauf:

1. Die externe Quelle wird eingelesen.
2. Relevante Eigenschaften werden extrahiert.
3. Die Daten werden auf das gemeinsame Zielmodell gemappt.
4. Die API stellt das Ergebnis als JSON bereit.
5. Die Daten können perspektivisch in Wikibase gespeichert werden.

Dieses Szenario zeigt den technischen Kern des Projekts, da unterschiedliche Datenquellen in eine einheitliche Form gebracht werden.

---

## 9. Bekannte Einschränkungen

Im aktuellen Projektstand sind nicht alle Funktionen vollständig umgesetzt.

Bekannte Einschränkungen:

- Die vollständige produktive Wikibase-Integration ist noch nicht abgeschlossen.
- Import- und Exportfunktionen sind teilweise geplant, aber nicht vollständig umgesetzt.
- Das Rechtemanagement ist als zukünftige Erweiterung vorgesehen.
- Authentifizierung und rollenbasierte API-Zugriffe sind noch nicht vollständig umgesetzt.
- Die API dient aktuell vor allem zur Demonstration und zum Testen des Mapping-Konzepts.
- Die Suchfunktion und SemanticId-Suche sind vorgesehen bzw. teilweise vorbereitet.
- Batch-Import und Export von Semantic IDs sind geplant, aber noch nicht produktiv verfügbar.
- Die vollständige MediaWiki-/Wikibase-Extension für eine direkte SemanticId-Suche ist noch weiter auszubauen.
- Die vollständige Integration externer Quellen wie QUDT, VEC und KBL ist abhängig vom jeweiligen Datenformat und der Verfügbarkeit der Quellen.
- Die Benutzeroberfläche befindet sich noch im konzeptionellen bzw. prototypischen Zustand.

Diese Einschränkungen bedeuten, dass die Benutzeranleitung teilweise den geplanten Zielzustand beschreibt. Bereits vorbereitete oder prototypisch umgesetzte Funktionen werden dabei entsprechend berücksichtigt.

Ziel ist es, die vorbereiteten API- und Mapping-Funktionen schrittweise mit der Wikibase-Plattform zu verbinden und dadurch eine vollständig nutzbare Semantic Wikibase mit Weboberfläche, Suche, API-Zugriff und kontrollierter Bearbeitung von Concept Descriptions bereitzustellen.

---

## 10. Zusammenfassung

Die Semantic Wikibase soll eine offene, webbasierte Plattform zur Verwaltung semantischer Definitionen bereitstellen.

Im Mittelpunkt stehen Concept Descriptions, die über eindeutige Semantic IDs bzw. URIs referenziert werden können. Dadurch können Nutzer, Entwickler und externe AAS-Systeme semantische Informationen zentral abrufen und wiederverwenden.

Die wichtigsten Funktionen sind:

- Suche nach semantischen Definitionen
- Anzeige von Concept Descriptions
- Bereitstellung auflösbarer URIs
- API-Zugriff für externe Systeme
- Mapping externer Datenquellen auf ein gemeinsames Zielmodell
- perspektivische Bearbeitung und Pflege von Einträgen über Wikibase

Auch wenn noch nicht alle Funktionen vollständig umgesetzt sind, bildet die Semantic Wikibase eine Grundlage für eine offene und maschinenlesbare Verwaltung semantischer Definitionen im AAS-Kontext.
