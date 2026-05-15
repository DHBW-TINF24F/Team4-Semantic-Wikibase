# Benutzer Manual - Semantic Wikibase
## Bedienungsanleitung für Weboberfläche und API

*Dokumentverantwortliche: Technische Redakteure, Lucrezia Trabalza und Marina Hidalgo Burova*

---

## Versionskontrolle 

| Version | Datum | Autor | Kommentar |
|---------|-------|-------|-----------|
| 1.0     | 27.04.2026 | Lucrezia Trabalza | Erstellung & erster Entwurf |
| 1.1     | 12.05.2026 | Lucrezia Trabalza, Marina Hidalgo Burova | Erweiterung der Benutzeranleitung um Plattformbeschreibung, Suchfunktion, API-Nutzung, lokale Tests, Fehlerfälle und Projektstand |
| 1.2     | 15.05.2026 | Lucrezia Trabalza, Marina Hidalgo Burova | Umstrukturierung: Getting Started, API-Nutzung und lokale Tests nach oben verschoben sowie Glossar-Verweise ergänzt |

---

## Inhaltsverzeichnis

- [1. Getting Started](#1-getting-started)
  - [1.1 Überblick](#11-überblick)
  - [1.2 Schnellstart für Nutzer der Weboberfläche](#12-schnellstart-für-nutzer-der-weboberfläche)
  - [1.3 Schnellstart für Entwickler und API-Nutzer](#13-schnellstart-für-entwickler-und-api-nutzer)
- [2. Nutzung der Weboberfläche](#2-nutzung-der-weboberfläche)
  - [2.1 Startseite und Suche](#21-startseite-und-suche)
  - [2.2 Concept Description anzeigen](#22-concept-description-anzeigen)
  - [2.3 Concept Description erstellen oder bearbeiten](#23-concept-description-erstellen-oder-bearbeiten)
- [3. Nutzung der API](#3-nutzung-der-api)
  - [3.1 Übersicht der relevanten API-Endpunkte](#31-übersicht-der-relevanten-api-endpunkte)
  - [3.2 Suche nach semantischen Definitionen](#32-suche-nach-semantischen-definitionen)
  - [3.3 Abruf einer Concept Description](#33-abruf-einer-concept-description)
  - [3.4 Beispielantwort](#34-beispielantwort)
  - [3.5 Fehlerfälle](#35-fehlerfälle)
  - [3.6 Weiterführende technische Dokumentation](#36-weiterführende-technische-dokumentation)
- [4. Lokales Testen der API](#4-lokales-testen-der-api)
  - [4.1 Voraussetzungen](#41-voraussetzungen)
  - [4.2 Übersicht der lokalen Testvarianten](#42-übersicht-der-lokalen-testvarianten)
  - [4.3 Starten der API](#43-starten-der-api)
  - [4.4 Test über Browser](#44-test-über-browser)
  - [4.5 Test über Swagger UI](#45-test-über-swagger-ui)
  - [4.6 Test über curl](#46-test-über-curl)
- [5. Typische Nutzungsszenarien](#5-typische-nutzungsszenarien)
  - [5.1 Nutzer sucht nach einer Einheit](#51-nutzer-sucht-nach-einer-einheit)
  - [5.2 Entwickler testet die API](#52-entwickler-testet-die-api)
  - [5.3 AAS-System löst eine Semantic ID auf](#53-aas-system-löst-eine-semantic-id-auf)
  - [5.4 Daten aus externer Quelle werden gemappt](#54-daten-aus-externer-quelle-werden-gemappt)
- [6. Produktinformationen](#6-produktinformationen)
  - [6.1 Zweck der Semantic Wikibase](#61-zweck-der-semantic-wikibase)
  - [6.2 Zielgruppen](#62-zielgruppen)
  - [6.3 Geplante Funktionsweise der Wikibase](#63-geplante-funktionsweise-der-wikibase)
  - [6.4 Nutzung durch externe Systeme](#64-nutzung-durch-externe-systeme)
- [7. Begriffserklärungen und Glossar](#7-begriffserklärungen-und-glossar)
- [8. Bekannte Einschränkungen](#8-bekannte-einschränkungen)
- [9. Zusammenfassung](#9-zusammenfassung)
  
---

## 1. Getting Started

Dieses Benutzer Manual beschreibt die praktische Nutzung der **Semantic Wikibase** über die Weboberfläche und über die API.

Die Anleitung richtet sich an Nutzer, die semantische Definitionen suchen oder anzeigen möchten, sowie an Entwickler, die die API lokal testen oder in externe Systeme einbinden möchten.

Die wichtigsten Nutzungsmöglichkeiten sind:

- Suche nach semantischen Definitionen über die Weboberfläche
- Anzeige einer Concept Description mit URI, Name, Einheit, Datentyp und Quelle
- Abruf semantischer Definitionen über REST-Endpunkte
- lokales Testen der API für Entwicklungs- und Demonstrationszwecke

Weitere Begriffserklärungen befinden sich im [Glossar](./Glossar.md).

Für technische Details zur Architektur und API-Implementierung wird auf die jeweilige Projektdokumentation verwiesen, z. B. auf die Software Architecture Specification (SAS), die Moduldokumentation (MOD) und die README-Dateien der API-Module.

---

### 1.1 Überblick

Die Semantic Wikibase dient dazu, semantische Definitionen zentral auffindbar, referenzierbar und maschinenlesbar bereitzustellen.

Im aktuellen Projektstand stehen vor allem folgende Funktionen im Vordergrund:

| Funktion | Beschreibung |
|---------|--------------|
| Weboberfläche | Nutzer können semantische Definitionen suchen und anzeigen. |
| Semantic-ID-Suche | Semantic IDs bzw. URIs können zur Suche nach passenden Concept Descriptions verwendet werden. |
| REST-API | Entwickler und externe Systeme können semantische Definitionen maschinenlesbar abrufen. |
| Mapping | Externe Datenquellen wie QUDT, VEC oder KBL werden in ein gemeinsames Zielmodell überführt. |
| Lokaler API-Test | Die API kann lokal gestartet und über Browser, Swagger UI oder curl getestet werden. |

---

### 1.2 Schnellstart für Nutzer der Weboberfläche

1. Semantic Wikibase im Browser öffnen.
2. Suchfeld auf der Startseite verwenden.
3. Suchbegriff eingeben, z. B.:

   ```text
   Volt
   ```

4. Passenden Treffer auswählen.
5. Concept Description anzeigen und Informationen wie URI, Name, Einheit, Symbol, Datentyp und Quelle prüfen.

Alternativ kann auch direkt nach einer Semantic ID oder URI gesucht werden, z. B.:

```text
http://qudt.org/vocab/unit/V
```

---

### 1.3 Schnellstart für Entwickler und API-Nutzer

Entwickler können die API nutzen, um semantische Definitionen maschinenlesbar abzurufen.

Beispiel für einen GET-Request:

```http
GET /api/v3/search?search=Volt&lang=de&types=unit
```

Bei lokaler Ausführung kann der Request beispielsweise so im Browser geöffnet werden:

```text
http://localhost:5000/api/v3/search?search=Volt&lang=de&types=unit
```

Falls die FastAPI-QUDT-Variante genutzt wird, kann alternativ folgender Endpunkt verwendet werden:

```text
http://localhost:8000/map?search=Volt&lang=de&types=unit
```

Die Anfrage sucht nach der semantischen Definition der Einheit `Volt` und gibt das Ergebnis als JSON-Antwort zurück.

Die genaue technische Umsetzung der API ist in den jeweiligen README-Dateien der API-Module sowie in der Moduldokumentation beschrieben.

---

## 2. Nutzung der Weboberfläche

Die Weboberfläche der Semantic Wikibase dient dazu, semantische Definitionen direkt im Browser zu suchen und anzuzeigen.

Im Vordergrund steht die einfache Nutzung für Personen, die eine Concept Description nachschlagen möchten, ohne direkt mit der API arbeiten zu müssen.

Die Startseite soll deshalb einen schnellen Einstieg in die Suche ermöglichen. Nutzer sollen Begriffe, Semantic IDs oder URIs eingeben können und anschließend passende semantische Definitionen angezeigt bekommen.

---

### 2.1 Startseite und Suche

Die Startseite der Semantic Wikibase soll Nutzern einen einfachen Einstieg ermöglichen.

Über das Suchfeld kann nach semantischen Definitionen gesucht werden.

Gesucht werden kann zum Beispiel nach:

- Namen, z. B. `Volt`
- Semantic IDs
- URIs
- Eigenschaften
- Quellen, z. B. `QUDT`, `VEC` oder `KBL`

Beispiel für einen Suchbegriff:

```text
Volt
```

Beispiel für eine URI:

```text
http://qudt.org/vocab/unit/V
```

Nach dem Absenden der Suche soll entweder die passende Concept Description angezeigt oder eine Liste möglicher Treffer ausgegeben werden.

Die Suche ist besonders wichtig, damit Nutzer auch ohne technisches Vorwissen semantische Definitionen finden können. Ziel ist, dass ein Nutzer direkt über die Startseite zum passenden Eintrag gelangt.

---

### 2.2 Concept Description anzeigen

Eine Concept Description zeigt die wichtigsten Informationen zu einer semantischen Definition.

Typische Informationen sind:

| Feld | Bedeutung |
|------|----------|
| ID / URI | Eindeutige semantische ID |
| preferredName | Bevorzugter Name des Begriffs |
| shortName | Kurzname |
| definition | Beschreibung oder Definition |
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

Die Anzeige soll so aufgebaut sein, dass sowohl Nutzer als auch externe Systeme die Bedeutung eines Begriffs nachvollziehen können.

Für normale Nutzer steht die verständliche Darstellung im Vordergrund. Für Entwickler und AAS-Systeme sind vor allem die eindeutige URI und die maschinenlesbaren Daten wichtig.

---

### 2.3 Concept Description erstellen oder bearbeiten

Berechtigte Nutzer sollen Concept Descriptions in der Wikibase erstellen oder bearbeiten können.

Ein Nutzer kann dabei:

1. einen neuen Begriff anlegen
2. eine eindeutige ID bzw. URI vergeben
3. Namen und Beschreibungen ergänzen
4. Einheiten oder Symbole eintragen
5. externe Quellen verlinken
6. Änderungen speichern

Diese Funktion ist im aktuellen Projektstand konzeptionell vorgesehen und abhängig vom späteren Rechtemodell der Wikibase.

Im geplanten Zielsystem sollen nicht alle Nutzer uneingeschränkt schreiben dürfen. Für spätere Versionen ist ein Rollen- und Rechtekonzept vorgesehen. Dadurch soll verhindert werden, dass fehlerhafte oder nicht geprüfte Daten unkontrolliert in die Semantic Wikibase übernommen werden.

Im aktuellen Projektstand liegt der Schwerpunkt daher vor allem auf der Suche, Anzeige und API-basierten Bereitstellung semantischer Definitionen.

---

## 3. Nutzung der API

Die API dient dazu, semantische Definitionen maschinenlesbar bereitzustellen.

Sie ermöglicht insbesondere:

- Suche nach Concept Descriptions
- Abruf einzelner semantischer Definitionen
- sprachabhängige Rückgabe von Daten
- Filterung nach Typen
- Bereitstellung der Daten im JSON-Format
- Mapping externer Quellen auf ein gemeinsames Zielmodell

Die API ist besonders für Entwickler, AAS-Systeme und externe Anwendungen relevant, die Concept Descriptions automatisiert abrufen möchten.

Im Projekt wird die API genutzt, um externe Datenquellen wie QUDT, VEC oder KBL in ein gemeinsames Format zu überführen. Dieses Zielmodell orientiert sich am IEC61360-Datentemplate der Asset Administration Shell.

Ein einfacher Beispielaufruf sieht so aus:

```http
GET /api/v3/search?search=Volt&lang=de&types=unit
```

Bei lokaler Ausführung kann der Request beispielsweise über folgende URL getestet werden:

```text
http://localhost:5000/api/v3/search?search=Volt&lang=de&types=unit
```

Für die FastAPI-QUDT-Variante kann alternativ folgender Endpunkt verwendet werden:

```text
http://localhost:8000/map?search=Volt&lang=de&types=unit
```

Die genaue technische Umsetzung ist in den README-Dateien der API-Module, in der Moduldokumentation und in der Software Architecture Specification beschrieben.

---

### 3.1 Übersicht der relevanten API-Endpunkte

Im Projekt werden verschiedene API-Endpunkte betrachtet. Einige Endpunkte sind bereits lokal testbar, andere beschreiben den geplanten Zielzustand der Semantic Wikibase.

| Endpunkt | Status | Zweck |
|---------|--------|-------|
| `/api/v3/search` | vorbereitet / prototypisch | Suche nach semantischen Definitionen über Suchbegriff, Sprache und Typfilter |
| `/map` | lokal testbar | Mapping von QUDT-Daten auf eine IEC61360-nahe JSON-Struktur |
| `/semanticIds/{identifier}` | geplant | Abruf einer bestimmten Semantic ID |
| `/semanticIds` | geplant | Auflistung, Import oder Export mehrerer Semantic IDs |
| `/semanticIds/export` | geplant | Export aller vorhandenen Semantic IDs |

Diese Übersicht unterscheidet zwischen bereits testbaren Funktionen und geplanten Ziel-Endpunkten. Dadurch ist nachvollziehbar, welche Bestandteile aktuell prototypisch umgesetzt sind und welche Funktionen im weiteren Projektverlauf ergänzt werden sollen.

Für die praktische Nutzung im aktuellen Projektstand sind vor allem folgende Endpunkte relevant:

```http
GET /api/v3/search?search=Volt&lang=de&types=unit
```

```http
GET /map?search=Volt&lang=de&types=unit
```

---

### 3.2 Suche nach semantischen Definitionen

Der Such-Endpunkt kann verwendet werden, um nach Begriffen, Semantic IDs oder URIs zu suchen.

Beispiel:

```http
GET /api/v3/search?search=Volt&lang=de&types=unit
```

Bedeutung der Parameter:

| Parameter | Bedeutung | Beispiel |
|----------|-----------|----------|
| `search` | Suchbegriff, URI oder Semantic ID | `Volt` |
| `lang` | Sprache der Antwort | `de` oder `en` |
| `types` | Typfilter | `unit` |

Beispiel mit vollständiger URI:

```http
GET /api/v3/search?search=http://qudt.org/vocab/unit/V&lang=de&types=unit
```

Bei lokaler Ausführung kann der Request beispielsweise im Browser geöffnet werden:

```text
http://localhost:5000/api/v3/search?search=Volt&lang=de&types=unit
```

Die Anfrage sucht nach der semantischen Definition der Einheit `Volt` und gibt das Ergebnis in deutscher Sprache zurück, sofern entsprechende Daten vorhanden sind.

Der Such-Endpunkt ist besonders nützlich, wenn ein Nutzer oder ein externes System nicht die genaue interne ID der Concept Description kennt, sondern nur einen Begriff oder eine externe URI besitzt.

---

### 3.3 Abruf einer Concept Description

Für den direkten Abruf einer Concept Description ist ein Endpunkt vorgesehen, der eine Semantic ID oder einen Identifier entgegennimmt.

Beispielhaft:

```http
GET /semanticIds/{identifier}
```

Beispiel mit URL-kodierter Semantic ID:

```http
GET /semanticIds/http%3A%2F%2Fqudt.org%2Fvocab%2Funit%2FV
```

Die API gibt anschließend die passende Concept Description zurück, sofern ein entsprechender Eintrag vorhanden ist.

Der Abruf einer einzelnen Concept Description ist besonders wichtig für AAS-Systeme. Diese besitzen häufig bereits eine Semantic ID und müssen nur die dazugehörige semantische Beschreibung auflösen.

Im aktuellen Projektstand sind neben dem direkten Abruf einzelner Semantic IDs auch weitere Endpunkte vorgesehen, zum Beispiel:

```http
GET /semanticIds
```

```http
GET /semanticIds/export
```

```http
POST /semanticIds
```

Damit können Semantic IDs perspektivisch aufgelistet, importiert oder exportiert werden.

Lokal testbar sind aktuell vor allem die Such- und Mapping-Endpunkte. Diese ermöglichen es, semantische Definitionen anhand eines Suchbegriffs oder einer URI zu finden und in eine IEC61360-nahe JSON-Struktur zu überführen.

---

### 3.4 Beispielantwort

Die API gibt die Daten im JSON-Format zurück. Die Antwort orientiert sich an einer Concept Description und am IEC61360-nahen Zielmodell.

Vereinfachtes Beispiel:

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

Eine ausführlichere Antwort kann zusätzlich eine IEC61360-nahe Struktur enthalten. Diese Struktur ist besonders für AAS-Systeme relevant, da sie semantische Definitionen maschinenlesbar weiterverarbeiten können.

Beispiel:

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
        },
        "sourceOfDefinition": {
          "value": "QUDT"
        }
      }
    }
  ]
}
```

Die konkrete Antwort kann je nach Datenquelle und verfügbarem Mapping unterschiedlich viele Felder enthalten. Wichtig ist, dass die API eine einheitliche JSON-Struktur zurückgibt und die Herkunft der Daten nachvollziehbar bleibt.

---

### 3.5 Fehlerfälle

Wenn eine Anfrage nicht korrekt verarbeitet werden kann, gibt die API eine strukturierte Fehlermeldung zurück.

Typische Fehlerfälle sind:

| Fehlerfall | Ursache | Erwartete Reaktion |
|-----------|---------|-------------------|
| Leerer Suchbegriff | Parameter `search` fehlt oder ist leer | `400 Bad Request` |
| Kein Treffer | Es wurde keine passende Concept Description gefunden | `404 Not Found` |
| Ungültiger Identifier | Die angefragte Semantic ID ist nicht bekannt oder nicht korrekt formatiert | `404 Not Found` oder `400 Bad Request` |
| Ungültiger Typfilter | Der angegebene Typ wird nicht unterstützt | `400 Bad Request` |
| Datenquelle nicht erreichbar | Externe Quelle wie QUDT, VEC oder KBL ist nicht verfügbar | `500 Internal Server Error` |
| Mapping-Fehler | Externe Daten konnten nicht korrekt in das Zielmodell überführt werden | `500 Internal Server Error` |

Beispiel für eine Fehlermeldung:

```json
{
  "detail": "Parameter 'search' darf nicht leer sein."
}
```

Durch strukturierte Fehlermeldungen kann besser nachvollzogen werden, warum eine Anfrage fehlgeschlagen ist. Das erleichtert sowohl die Entwicklung als auch die Fehlersuche beim lokalen Testen der API.

Bei API-Tests sollten deshalb nicht nur erfolgreiche Anfragen geprüft werden, sondern auch ungültige oder leere Eingaben. Dadurch kann kontrolliert werden, ob die API stabil reagiert und verständliche Rückmeldungen liefert.

---

### 3.6 Weiterführende technische Dokumentation

Für die reine Nutzung der API reichen die Beispiele in diesem Benutzer Manual aus.

Für technische Details zur Implementierung, Architektur und zum Mapping wird auf die weiterführenden Projektdokumente verwiesen:

| Dokument | Inhalt |
|---------|--------|
| [Moduldokumentation (MOD)](./TINF24F_4_MOD.md) | Beschreibung der OpenAPI-Spezifikation, API-Architektur, Mapper, Datenquellen und Mapping-Regeln |
| [Software Architecture Specification (SAS)](./TINF24F_4_SAS.md) | Beschreibung der Gesamtarchitektur, API-Gateway-Struktur, Such-Architektur und Wikibase-Integration |
| [Pflichtenheft (SRS)](./TINF24F_4_SRS.md) | Beschreibung der umzusetzenden Anforderungen, Use Cases und Systemfunktionen |
| [Lastenheft (CRS)](./TINF24F_4_CRS.md) | Beschreibung der ursprünglichen Kundenanforderungen und Projektziele |
| README-Dateien der API-Module | Praktische Hinweise zum lokalen Starten und Testen der jeweiligen API-Module |

Die Moduldokumentation beschreibt insbesondere die konkrete API- und Mapping-Ebene. Dort werden unter anderem die REST-Endpunkte, Beispielanfragen, Beispielantworten sowie die Verarbeitung der Datenquellen QUDT, VEC und KBL dokumentiert.

Die Software Architecture Specification beschreibt dagegen die übergeordnete Architektur. Dazu gehören das Zusammenspiel zwischen API-Gateway, Einzel-APIs, Mappern, Wikibase und externen Datenquellen.

Für Nutzer, die nur semantische Definitionen suchen oder abrufen möchten, ist dieses Benutzer Manual ausreichend. Für Entwickler und Systemintegratoren sind zusätzlich die MOD, SAS und README-Dateien relevant.

---

## 4. Lokales Testen der API

Dieses Kapitel beschreibt, wie die API lokal gestartet und getestet werden kann.

Das lokale Testen ist wichtig, um einzelne API-Funktionen unabhängig von einer produktiven Serverumgebung zu prüfen. Dadurch können Entwickler kontrollieren, ob Suchanfragen, Mapping und JSON-Antworten korrekt funktionieren.

Die Tests können über den Browser, über Swagger UI oder über `curl` durchgeführt werden.

---

### 4.1 Voraussetzungen

Für das lokale Testen der API werden folgende Werkzeuge benötigt:

- Python 3.11 oder eine kompatible Python-Version
- installierte Python-Abhängigkeiten aus dem jeweiligen API-Modul
- Zugriff auf das Projekt-Repository
- Terminal oder VS Code Terminal
- optional: Browser für Swagger UI
- optional: `curl` für API-Tests über die Kommandozeile

Vor dem Start sollte geprüft werden, ob Python korrekt installiert ist:

```bash
python --version
```

oder:

```bash
python3 --version
```

Außerdem sollte sichergestellt werden, dass man sich im richtigen Projektordner befindet und die benötigten Abhängigkeiten installiert sind.

---

### 4.2 Übersicht der lokalen Testvarianten

Im Projekt existieren verschiedene lokale Testvarianten. Je nach verwendeter Implementierung wird entweder eine FastAPI- oder eine Flask-basierte API gestartet.

| Variante | Zweck | Beispiel-URL |
|---------|------|--------------|
| FastAPI-QUDT-Mapping | Test des QUDT-Mappings und der JSON-Ausgabe | `http://localhost:8000/map?search=Volt&lang=de&types=unit` |
| Flask-/Gateway-API | Test der API-Struktur und Suchanfragen über den Such-Endpunkt | `http://localhost:5000/api/v3/search?search=Volt&lang=de&types=unit` |

Welche Variante genutzt wird, hängt davon ab, welcher Projektordner und welche Implementierung lokal gestartet wird.

Für Details zum Start der jeweiligen API-Module sollten zusätzlich die README-Dateien der API-Module verwendet werden.

---

### 4.3 Starten der API

Zuerst wird in den passenden Projektordner gewechselt. Der genaue Ordner hängt davon ab, ob die Flask-/Gateway-API oder die FastAPI-QUDT-Variante getestet wird.

Beispiel:

```bash
cd <pfad-zum-api-ordner>
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

Danach kann die jeweilige API gestartet werden.

Beispiel für eine Flask-basierte API:

```bash
python app.py
```

Beispiel für eine FastAPI-basierte API:

```bash
uvicorn api_qudt:app --reload
```

Nach dem Start sollte im Terminal angezeigt werden, unter welcher lokalen Adresse die API erreichbar ist.

Typische lokale Adressen sind:

```text
http://localhost:5000
```

für Flask oder:

```text
http://localhost:8000
```

für FastAPI.

---

### 4.4 Test über Browser

Nach dem Start kann die API direkt im Browser getestet werden.

Beispiel für die Flask-/Gateway-API:

```text
http://localhost:5000/api/v3/search?search=Volt&lang=de&types=unit
```

Beispiel für die FastAPI-QUDT-Variante:

```text
http://localhost:8000/map?search=Volt&lang=de&types=unit
```

Wenn die API korrekt läuft, wird eine JSON-Antwort mit Informationen zur Einheit `Volt` ausgegeben.

Falls keine Antwort erscheint, sollten folgende Punkte geprüft werden:

- Läuft die API im Terminal?
- Wurde der richtige Port verwendet?
- Befindet man sich im richtigen Projektordner?
- Sind alle benötigten Python-Pakete installiert?
- Ist die externe Datenquelle erreichbar?

---

### 4.5 Test über Swagger UI

Falls eine FastAPI-Variante genutzt wird, kann die automatische API-Dokumentation geöffnet werden.

Beispiel:

```text
http://localhost:8000/docs
```

Dort kann der Endpunkt direkt im Browser getestet werden.

Vorgehen:

1. Swagger UI öffnen.
2. Endpunkt `/map` auswählen.
3. `Try it out` anklicken.
4. Parameter eintragen, z. B.:
   - `search`: `Volt`
   - `lang`: `de`
   - `types`: `unit`
5. Anfrage ausführen.
6. JSON-Antwort prüfen.

Swagger UI ist besonders hilfreich, weil die API dort ohne zusätzliches Tool getestet werden kann.

---

### 4.6 Test über curl

Die API kann auch über die Kommandozeile mit `curl` getestet werden.

Beispiel für die Flask-/Gateway-API:

```bash
curl "http://localhost:5000/api/v3/search?search=Volt&lang=de&types=unit"
```

Beispiel für die FastAPI-QUDT-Variante:

```bash
curl "http://localhost:8000/map?search=Volt&lang=de&types=unit"
```

Erwartet wird eine JSON-Antwort mit Informationen zur Einheit `Volt`.

Wenn eine Fehlermeldung zurückgegeben wird, sollte geprüft werden, ob der Suchbegriff korrekt ist, ob die API läuft und ob die richtige lokale URL verwendet wurde.

---

## 5. Typische Nutzungsszenarien

In diesem Kapitel werden typische Anwendungsfälle der Semantic Wikibase beschrieben.

Die Szenarien zeigen, wie normale Nutzer, Entwickler, AAS-Systeme und Mapper mit der Plattform arbeiten können.

---

### 5.1 Nutzer sucht nach einer Einheit

Ein Nutzer möchte Informationen zur Einheit `Volt` finden.

Ablauf:

1. Der Nutzer öffnet die Semantic Wikibase im Browser.
2. Der Nutzer verwendet das Suchfeld auf der Startseite.
3. Der Nutzer gibt einen Suchbegriff ein, z. B.:

   ```text
   Volt
   ```

4. Das System zeigt passende semantische Definitionen oder eine Trefferliste an.
5. Der Nutzer öffnet den passenden Eintrag.
6. Die Concept Description wird angezeigt.
7. Der Nutzer prüft Informationen wie URI, Name, Einheit, Symbol, Datentyp und Quelle.

Ziel dieses Szenarios ist es, semantische Definitionen einfach auffindbar und verständlich darzustellen.

---

### 5.2 Entwickler testet die API

Ein Entwickler möchte prüfen, ob die API eine Concept Description korrekt zurückgibt.

Ablauf:

1. Der Entwickler startet die API lokal.
2. Der Entwickler ruft den Such-Endpunkt auf.
3. Die API verarbeitet den Suchbegriff.
4. Die passenden Daten werden aus der jeweiligen Quelle gelesen oder aus dem Mapping bereitgestellt.
5. Die Daten werden in ein gemeinsames Zielmodell überführt.
6. Die API gibt eine JSON-Antwort zurück.
7. Der Entwickler prüft die Antwortstruktur.

Beispiel:

```http
GET /api/v3/search?search=Volt&lang=de&types=unit
```

Bei lokaler Ausführung:

```text
http://localhost:5000/api/v3/search?search=Volt&lang=de&types=unit
```

Dieses Szenario ist besonders wichtig für Entwicklung, Integration und Qualitätssicherung der API.

---

### 5.3 AAS-System löst eine Semantic ID auf

Ein AAS-System enthält eine Semantic ID zu einem Submodel-Element.

Ablauf:

1. Das AAS-System liest die vorhandene Semantic ID.
2. Das System sendet eine Anfrage an die Semantic-Wikibase-API.
3. Die API sucht die passende Concept Description.
4. Die API gibt die Daten im JSON-Format zurück.
5. Das AAS-System verwendet die Antwort zur semantischen Interpretation des Elements.

Beispielhafte Semantic ID:

```text
http://qudt.org/vocab/unit/V
```

Dadurch kann ein AAS-System externe semantische Definitionen zentral abrufen, ohne diese lokal speichern zu müssen.

---

### 5.4 Daten aus externer Quelle werden gemappt

Eine externe Quelle wie QUDT, VEC oder KBL soll in die gemeinsame Struktur der Semantic Wikibase überführt werden.

Ablauf:

1. Eine externe Datenquelle wird eingelesen.
2. Relevante Eigenschaften werden extrahiert.
3. Die Daten werden auf das gemeinsame Zielmodell gemappt.
4. Die API stellt das Ergebnis als JSON bereit.
5. Die Daten können perspektivisch in Wikibase gespeichert oder über die API weiterverwendet werden.

Beispiel für einen lokalen Mapping-Aufruf:

```http
GET /map?search=Volt&lang=de&types=unit
```

Bei lokaler Ausführung:

```text
http://localhost:8000/map?search=Volt&lang=de&types=unit
```

Dieses Szenario zeigt den technischen Kern des Projekts, da unterschiedliche Datenquellen in eine einheitliche Form gebracht werden.

---

## 6. Produktinformationen

Dieses Kapitel beschreibt den fachlichen Hintergrund der Semantic Wikibase.

Während die vorherigen Kapitel die praktische Bedienung der Weboberfläche und API erklären, werden hier Ziel, Zweck, Zielgruppen und geplante Funktionsweise des Produkts zusammengefasst.

---

### 6.1 Zweck der Semantic Wikibase

Die Semantic Wikibase soll eine offene Plattform bereitstellen, auf der semantische Definitionen verwaltet und veröffentlicht werden können.

Im Mittelpunkt stehen sogenannte **Semantic IDs** bzw. **auflösbare URIs**. Jede Concept Description soll über eine eindeutige Adresse erreichbar sein. Dadurch können externe Systeme eindeutig auf die jeweilige Bedeutung eines Begriffs verweisen.

Die Plattform soll insbesondere folgende Probleme lösen:

- semantische Definitionen zentral auffindbar machen
- Begriffe über stabile URIs referenzierbar machen
- Concept Descriptions über eine REST-API abrufbar machen
- Daten aus verschiedenen Quellen in ein gemeinsames Format überführen
- Nutzern eine einfache Suche und Anzeige semantischer Definitionen ermöglichen

Langfristig soll die Semantic Wikibase als zentrale Registry für semantische Definitionen dienen.

---

### 6.2 Zielgruppen

Die Semantic Wikibase richtet sich an verschiedene Nutzergruppen.

| Zielgruppe | Nutzung |
|-----------|---------|
| Normale Nutzer | Suchen und Anzeigen semantischer Definitionen |
| Fachexperten | Prüfen, Ergänzen oder Erstellen von Concept Descriptions |
| Entwickler | Testen und Einbinden der REST-API |
| AAS-Systeme | Maschinenlesbarer Abruf von Concept Descriptions |
| Systemintegratoren | Anbindung der Semantic Wikibase an bestehende Systeme |
| Projektteam | Dokumentation, Weiterentwicklung und Qualitätssicherung |

Die Bedienungsanleitung ist deshalb so aufgebaut, dass sowohl nicht-technische Nutzer als auch Entwickler die wichtigsten Funktionen nachvollziehen können.

---

### 6.3 Geplante Funktionsweise der Wikibase

Die Semantic Wikibase soll Nutzern eine einfache Möglichkeit bieten, semantische Definitionen zu suchen, anzuzeigen und perspektivisch auch zu bearbeiten.

Die Plattform orientiert sich dabei an bekannten Wiki-Systemen. Nutzer sollen Begriffe nicht nur als Text sehen, sondern strukturierte Informationen erhalten, die auch von Maschinen verarbeitet werden können.

Geplant sind insbesondere folgende Funktionen:

- Suche nach semantischen Definitionen
- Anzeige von Concept Descriptions
- Bereitstellung auflösbarer URIs
- Verlinkung externer Quellen
- REST-API für externe Systeme
- Mapping externer Datenquellen auf ein gemeinsames Zielmodell
- perspektivisches Erstellen und Bearbeiten von Einträgen durch berechtigte Nutzer

Im aktuellen Projektstand liegt der Schwerpunkt vor allem auf der API-Nutzung, der verbesserten Suche, dem Mapping externer Quellen und der strukturierten Bereitstellung semantischer Definitionen.

---

### 6.4 Nutzung durch externe Systeme

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

## 7. Begriffserklärungen und Glossar

Im Benutzer Manual werden verschiedene fachliche Begriffe verwendet, die im separaten Glossar genauer erklärt werden.

Das Glossar dient dazu, zentrale Begriffe aus dem Projekt einheitlich zu beschreiben und Missverständnisse zu vermeiden.

Siehe: [Glossar](./Glossar.md)

Wichtige Begriffe aus diesem Manual sind:

| Begriff | Bedeutung im Kontext des Projekts | Verweis |
|--------|-----------------------------------|---------|
| AAS | Digitale Verwaltungsschale eines Assets | [Glossar](./Glossar.md) |
| Asset | Physisches oder digitales Objekt mit Wert für das System | [Glossar](./Glossar.md) |
| Submodell | Strukturierter Teilbereich einer AAS | [Glossar](./Glossar.md) |
| Submodel Element | Einzelnes Informations- oder Funktionsbaustein innerhalb eines Submodells | [Glossar](./Glossar.md) |
| Concept Description | Semantische Beschreibung eines Begriffs oder einer Eigenschaft | [Glossar](./Glossar.md) |
| IEC 61360 | Standard zur Beschreibung technischer Merkmale und Eigenschaften | [Glossar](./Glossar.md) |
| URI | Eindeutiger Bezeichner für eine Ressource oder semantische Definition | [Glossar](./Glossar.md) |

Begriffe werden im Manual nur kurz im jeweiligen Nutzungskontext verwendet. Für ausführlichere Erklärungen soll das Glossar genutzt werden.

---

## 8. Bekannte Einschränkungen

Im aktuellen Projektstand sind nicht alle Funktionen vollständig produktiv umgesetzt.

Bekannte Einschränkungen sind:

- Die vollständige produktive Wikibase-Integration ist noch nicht abgeschlossen.
- Einige API-Endpunkte sind geplant oder prototypisch vorbereitet, aber noch nicht vollständig produktiv nutzbar.
- Lokal testbar sind vor allem die Such- und Mapping-Endpunkte.
- Import- und Exportfunktionen für Semantic IDs sind vorgesehen, aber noch nicht vollständig produktiv verfügbar.
- Das Rechtemanagement ist als zukünftige Erweiterung vorgesehen.
- Schreibrechte und rollenbasierte API-Zugriffe sind noch nicht vollständig umgesetzt.
- Die API dient aktuell vor allem zur Demonstration und zum Testen des Mapping-Konzepts.
- Die Suchfunktion und Semantic-ID-Suche sind vorgesehen bzw. teilweise vorbereitet.
- Die vollständige MediaWiki-/Wikibase-Erweiterung für eine direkte Semantic-ID-Suche ist noch weiter auszubauen.
- Die vollständige Integration externer Quellen wie QUDT, VEC und KBL ist abhängig vom jeweiligen Datenformat und der Verfügbarkeit der Quellen.
- Die Benutzeroberfläche befindet sich teilweise noch im konzeptionellen bzw. prototypischen Zustand.

Diese Einschränkungen bedeuten, dass dieses Benutzer Manual teilweise den geplanten Zielzustand beschreibt. Bereits vorbereitete oder prototypisch umgesetzte Funktionen werden entsprechend gekennzeichnet.

Ziel ist es, die vorbereiteten API- und Mapping-Funktionen schrittweise mit der Wikibase-Plattform zu verbinden. Dadurch soll langfristig eine vollständig nutzbare Semantic Wikibase mit Weboberfläche, Suche, API-Zugriff und kontrollierter Bearbeitung von Concept Descriptions entstehen.

---

## 9. Zusammenfassung

Die Semantic Wikibase soll eine offene, webbasierte Plattform zur Verwaltung semantischer Definitionen bereitstellen.

Im Mittelpunkt stehen Concept Descriptions, die über eindeutige Semantic IDs bzw. URIs referenziert werden können. Dadurch können Nutzer, Entwickler und externe AAS-Systeme semantische Informationen zentral abrufen und wiederverwenden.

Dieses Benutzer Manual beschreibt die Nutzung der Semantic Wikibase aus praktischer Sicht. Dazu gehören:

- Suche nach semantischen Definitionen über die Weboberfläche
- Anzeige von Concept Descriptions
- Nutzung der API über konkrete GET-Requests
- lokales Testen der API
- typische Nutzungsszenarien
- Verweise auf weiterführende technische Dokumentation
- Verweis auf das separate Glossar

Die wichtigsten Funktionen sind:

- Bereitstellung auflösbarer URIs
- API-Zugriff für externe Systeme
- Mapping externer Datenquellen auf ein gemeinsames Zielmodell
- strukturierte JSON-Ausgabe im IEC61360-nahen Format
- perspektivische Bearbeitung und Pflege von Einträgen über Wikibase

Auch wenn noch nicht alle Funktionen vollständig produktiv umgesetzt sind, bildet die Semantic Wikibase eine Grundlage für eine offene und maschinenlesbare Verwaltung semantischer Definitionen im AAS-Kontext.

Für Nutzer steht die einfache Suche und Anzeige semantischer Definitionen im Vordergrund. Für Entwickler und Systemintegratoren sind vor allem die API-Endpunkte, Mapping-Funktionen und weiterführenden Projektdokumentationen relevant.
