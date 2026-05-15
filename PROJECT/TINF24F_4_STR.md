# Software Test Report (STR)

*Dokumentverantwortliche: Testmanagement / Qualitätssicherung, Team Semantic Wikibase*

## Versionskontrolle

| Version | Datum | Autor | Kommentar |
|-|-|-|-|
| 0.1 | 14.05.2026 | Team Semantic Wikibase | Erstellung der STR-Ausfüllvorlage auf Basis des STP |
| 0.2 | 15.05.2026 | Team Semantic Wikibase | Anpassung an aktualisierten STP, SRS-Anforderungsnummerierung und Traceability Matrix |

<br>

## Inhaltsverzeichnis

- [Software Test Report (STR)](#software-test-report-str)
  - [Versionskontrolle](#versionskontrolle)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [1. Einführung in den Software Test Report](#1-einführung-in-den-software-test-report)
  - [2. Testgegenstand](#2-testgegenstand)
  - [3. Testbasis](#3-testbasis)
  - [4. Testumfang](#4-testumfang)
    - [4.1 Durchgeführte Testarten](#41-durchgeführte-testarten)
    - [4.2 Nicht durchgeführte Tests](#42-nicht-durchgeführte-tests)
  - [5. Testumgebung](#5-testumgebung)
  - [6. Zusammenfassung der Testergebnisse](#6-zusammenfassung-der-testergebnisse)
    - [6.1 Ergebnisübersicht pro Testfall](#61-ergebnisübersicht-pro-testfall)
  - [7. Detaillierte Testergebnisse](#7-detaillierte-testergebnisse)
  - [8. Fehler, Auffälligkeiten und Abweichungen](#8-fehler-auffälligkeiten-und-abweichungen)
    - [8.1 Übersicht erkannter Fehler](#81-übersicht-erkannter-fehler)
    - [8.2 Detailbeschreibung der Fehler](#82-detailbeschreibung-der-fehler)
  - [9. Bewertung der Anforderungen](#9-bewertung-der-anforderungen)
  - [10. Traceability Matrix](#10-traceability-matrix)
  - [11. Screenshots und Nachweise](#11-screenshots-und-nachweise)
  - [12. Gesamteinschätzung](#12-gesamteinschätzung)
    - [12.1 Zusammenfassung](#121-zusammenfassung)
    - [12.2 Testfazit](#122-testfazit)
  - [13. Offene Punkte und Empfehlungen](#13-offene-punkte-und-empfehlungen)
  - [14. Referenzen und Anhang](#14-referenzen-und-anhang)
    - [14.1 Referenzen](#141-referenzen)
    - [14.2 Beispielhafte API-Requests](#142-beispielhafte-api-requests)
    - [14.3 Beispielhafte Testdaten](#143-beispielhafte-testdaten)
    - [14.4 Statusdefinitionen](#144-statusdefinitionen)

---

## 1. Einführung in den Software Test Report

Der Software Test Report (STR) dokumentiert die Durchführung und Ergebnisse der im Software Test Plan (STP) definierten Systemtests für das Projekt **Semantic Wikibase**.

Während der STP beschreibt, welche Tests geplant sind, hält der STR fest, welche Tests tatsächlich durchgeführt wurden, welche Ergebnisse dabei entstanden sind und welche Fehler, Auffälligkeiten oder offenen Punkte festgestellt wurden.

Der Schwerpunkt dieses STR liegt auf den im STP definierten **Black-Box-Systemtests**. Dabei wird das System aus Sicht eines Nutzers oder API-Clients betrachtet. Interne Implementierungsdetails des Quellcodes stehen nicht im Vordergrund. Entscheidend ist, ob das System bei definierten Eingaben die erwarteten Reaktionen und Ausgaben liefert.

> **Hinweis:** Dieses Dokument ist als Ausfüllvorlage vorbereitet. Da die Tests zum Zeitpunkt der Erstellung noch nicht vollständig durchgeführt wurden, sind die Felder „Tatsächliches Ergebnis“, „Status“, „Nachweis“ und „Bemerkung“ nach der Testdurchführung zu ergänzen.

---

## 2. Testgegenstand

Getestet wird das Projekt **Semantic Wikibase**. Ziel des Systems ist die Verwaltung, Veröffentlichung und Abfrage semantischer Definitionen für die Asset Administration Shell (AAS). Concept Descriptions sollen über auflösbare URIs bereitgestellt und über eine REST-API in einem AAS- bzw. IEC-61360-orientierten JSON-Format abrufbar sein.

Der Testgegenstand umfasst insbesondere:

- Startseite und grundlegende Benutzeroberfläche,
- Suchfunktion und Auffindbarkeit der SemanticId-Suche,
- Detailansicht semantischer Einträge,
- REST-API zum Abruf von semanticIds bzw. Concept Descriptions,
- Query-Parameter für Sprache, Sortierung und Filterung,
- Fehlerbehandlung bei ungültigen Eingaben,
- Mapping-Ergebnisse aus QUDT, VEC und KBL,
- Import- und Exportfunktionen der API.

Nicht im Fokus stehen interne Unit-Tests einzelner Funktionen, vollständige Penetrationstests oder vollständige Lasttests unter Produktivbedingungen. Diese Bereiche werden nur betrachtet, sofern sie im Rahmen der Systemtests von außen sichtbar werden.

---

## 3. Testbasis

Die Testdurchführung basiert auf folgenden Dokumenten und Projektartefakten:

- STP – Software Test Plan Semantic Wikibase,
- CRS – Lastenheft Semantic Wikibase,
- SRS – Pflichtenheft Semantic Wikibase,
- SAS – Software Architecture Specification Semantic Wikibase,
- SAS_AAS_Wikibase – AAS Concept Description API & Sucherweiterung,
- MOD – Moduldokumentation zur OpenAPI-Spezifikation und Mapping-Zusammenführung,
- BC – Business Case Semantic Wikibase,
- PM – Projektplan Semantic Wikibase,
- Projektbeschreibung **Semantic Wikibase**,
- GitHub-Issue #25 zur verbesserten Suchfunktion,
- GitHub-Issue #26 zur neuen Startseitenstruktur,
- GitHub-Issue #27 zur API gemäß AAS Concept Description Specification,
- Vorlesung **Von der Anforderung zum Testfall**,
- Vorlesung **Analytische Qualitätssicherung**,
- Vorlesung **Requirements Engineering**,
- Vorlesung **Digitaler Zwilling, Verwaltungsschale und AAS**.

Die Testfälle wurden im STP anforderungsbasiert definiert. Die Ergebnisse werden in diesem STR den jeweiligen Anforderungen zugeordnet, um die Nachvollziehbarkeit zwischen Anforderungen, Testfällen und Testergebnissen sicherzustellen.

Besonders relevant sind die aktualisierten Anforderungen aus dem SRS:

| Anforderung | Bedeutung für diesen STR |
|-|-|
| FA.001 | Auflösbare URIs und Detailseiten werden durch UI- und API-Tests geprüft. |
| FA.002 | Die REST-API wird anhand von Abruf-, Filter-, Fehler- und Import-/Exportfällen geprüft. |
| FA.003 | Das IEC61360-orientierte Zielmodell wird anhand der JSON-Ausgaben geprüft. |
| FA.004 | Die sprachabhängige API-Ausgabe wird über `lang=de` und `lang=en` geprüft. |
| FA.006 | Quellenverweise werden insbesondere in Detailansicht, API-Ausgabe und Mapping geprüft. |
| FA.009 | Automatisierter Import externer Concept Descriptions per URI wird im Rahmen von Import-/Mapping-Tests betrachtet. |
| FA.010 | Die überarbeitete Startseite und verbesserte Suchfunktion werden durch UI- und Suchtests geprüft. |
| FA.011 | Quellenspezifische Mapper für QUDT, VEC und KBL werden anhand ihrer Zielmodell-Ausgaben geprüft. |
| NFA.001 | Stabilität und Erreichbarkeit werden während der Tests beobachtet. |
| NFA.002 | Antwortzeiten werden zumindest qualitativ betrachtet, sofern kein vollständiger Performancetest durchgeführt wird. |
| NFA.003 | Sicherheit und kontrollierter Schreibzugriff werden im Rahmen der Import-/Schreibfunktionen bewertet, sofern implementiert. |
| NFA.004 | Benutzerfreundlichkeit wird anhand Startseite, Suche und Ergebnisdarstellung geprüft. |

---

## 4. Testumfang

### 4.1 Durchgeführte Testarten

| Testart | Beschreibung | Durchführung |
|-|-|-|
| Funktionale Tests | Prüfung sichtbarer Funktionen wie Suche, API-Abruf, Import und Export | [einfügen: durchgeführt / teilweise / nicht durchgeführt] |
| Systemtests | Prüfung des Gesamtsystems aus Nutzer- und API-Client-Sicht | [einfügen] |
| API-Tests | Prüfung von Endpunkten, HTTP-Statuscodes, Query-Parametern und JSON-Strukturen | [einfügen] |
| Mapping-Tests | Prüfung der sichtbaren Mapping-Ergebnisse aus QUDT, VEC und KBL | [einfügen] |
| Fehlertests | Prüfung von ungültigen Suchbegriffen, ungültigen Identifiern und nicht vorhandenen Daten | [einfügen] |
| Usability-orientierte Tests | Prüfung der Auffindbarkeit und Bedienbarkeit der Suchfunktion | [einfügen] |

### 4.2 Nicht durchgeführte Tests

Folgende Tests sind nicht Bestandteil dieses STR oder wurden nur eingeschränkt betrachtet:

| Nicht durchgeführter Testbereich | Begründung |
|-|-|
| Vollständige Last- und Performancetests | Im Rahmen des Systemtests nicht vorgesehen bzw. nicht vollständig umsetzbar. |
| Security-Penetrationstests | Nicht Bestandteil des geplanten STP-Umfangs. |
| Vollständige fachliche Prüfung aller externen Datenquellen | Externe Quellen wie QUDT, VEC und KBL werden nur anhand ausgewählter Beispiele geprüft. |
| Vollständige Unit-Tests einzelner Funktionen | Fokus liegt auf Black-Box-Systemtests. |
| Vollständige Rechteverwaltung | Laut Projektstand später durch FoP Consult GmbH bzw. gesonderte Implementierung vorgesehen. |

---

## 5. Testumgebung

Die Tests werden in einer lokalen Entwicklungs- und Testumgebung durchgeführt.

| Komponente | Wert / Beschreibung |
|-|-|
| Betriebssystem | [einfügen, z. B. Windows 11] |
| Entwicklungsumgebung | [einfügen, z. B. Visual Studio Code] |
| Browser | [einfügen, z. B. Chrome / Edge / Firefox + Version] |
| API-Testwerkzeug | [einfügen, z. B. curl / Postman / Browser] |
| Programmiersprache | Python |
| API-Framework | [einfügen, z. B. FastAPI / Flask] |
| Lokale API-URL | [einfügen, z. B. `http://localhost:8000`] |
| Wikibase-/Semantic-Hub-URL | [einfügen] |
| Datenquellen | QUDT, VEC, KBL |
| Repository / Branch | [einfügen, z. B. GitHub-Repo + Branch + Commit-ID] |
| Testdatum | [einfügen] |
| Tester | [einfügen] |

---

## 6. Zusammenfassung der Testergebnisse

| Kennzahl | Anzahl |
|-|-:|
| Geplante Testfälle | 10 |
| Durchgeführte Testfälle | [einfügen] |
| Bestanden | [einfügen] |
| Teilweise bestanden | [einfügen] |
| Fehlgeschlagen | [einfügen] |
| Blockiert / nicht durchführbar | [einfügen] |
| Offen / noch nicht getestet | [einfügen] |

### 6.1 Ergebnisübersicht pro Testfall

| Testfall-ID | Kurzbeschreibung | Status | Nachweis |
|-|-|-|-|
| ST-01 | Aufruf der Startseite und Prüfung der Erreichbarkeit | Noch nicht durchgeführt | [Screenshot/Link einfügen] |
| ST-02 | Suchfeld auf der Startseite auffindbar | Noch nicht durchgeführt | [Screenshot/Link einfügen] |
| ST-03 | Suche nach bekannter semanticId | Noch nicht durchgeführt | [Screenshot/Link einfügen] |
| ST-04 | Suche mit Teilbegriff, Sonderzeichen und ohne Treffer | Noch nicht durchgeführt | [Screenshot/Link einfügen] |
| ST-05 | Liste aller semanticIds abrufen | Noch nicht durchgeführt | [Screenshot/Output einfügen] |
| ST-06 | Einzelne semanticId abrufen und Sprachparameter prüfen | Noch nicht durchgeführt | [Screenshot/Output einfügen] |
| ST-07 | Sortierung und Filterung der semanticIds prüfen | Noch nicht durchgeführt | [Screenshot/Output einfügen] |
| ST-08 | Ungültigen Identifier abrufen | Noch nicht durchgeführt | [Screenshot/Output einfügen] |
| ST-09 | QUDT-Daten in AAS-Concept-Description-Struktur prüfen | Noch nicht durchgeführt | [Screenshot/Output einfügen] |
| ST-10 | VEC-/KBL-Mapping sowie Import und Export prüfen | Noch nicht durchgeführt | [Screenshot/Output einfügen] |

**Statuswerte:** Bestanden, Teilweise bestanden, Fehlgeschlagen, Blockiert, Noch nicht durchgeführt.

---

## 7. Detaillierte Testergebnisse

### Testfall ST-01: Aufruf der Startseite

| Feld | Beschreibung |
|-|-|
| Testfall-ID | ST-01 |
| Testobjekt | Startseite / Benutzeroberfläche |
| Zugehörige Anforderung | FA.001, FA.010, NFA.001, NFA.004 |
| Ziel | Prüfen, ob die Startseite des Semantic Hub korrekt erreichbar ist. |
| Vorbedingung | Lokale Wikibase-/Semantic-Hub-Instanz ist gestartet. |
| Testdaten | URL der lokalen Instanz. |
| Testschritte | 1. Browser öffnen.<br>2. URL der lokalen Instanz aufrufen.<br>3. Prüfen, ob die Startseite geladen wird. |
| Erwartetes Ergebnis | Die Startseite wird ohne Fehlermeldung geladen. Wichtige Einstiegspunkte wie Suche oder Navigation sind sichtbar. |
| Tatsächliches Ergebnis | [einfügen] |
| Status | Noch nicht durchgeführt |
| Nachweis | [Screenshot-Datei einfügen, z. B. `images/str-st01-startseite.png`] |
| Bemerkung | [einfügen] |

---

### Testfall ST-02: Suchfeld auf der Startseite ist auffindbar

| Feld | Beschreibung |
|-|-|
| Testfall-ID | ST-02 |
| Testobjekt | Suchfunktion / Startseite |
| Zugehörige Anforderung | FA.010, NFA.004 |
| Ziel | Prüfen, ob Nutzer die Suche einfach auf der Startseite finden. |
| Vorbedingung | Startseite ist geöffnet. |
| Testdaten | Keine besonderen Testdaten. |
| Testschritte | 1. Startseite öffnen.<br>2. Prüfen, ob ein Suchfeld oder ein Link zur Suche sichtbar ist.<br>3. Prüfen, ob die Suche ohne Umwege erreichbar ist. |
| Erwartetes Ergebnis | Das Suchfeld oder der Suchzugang ist klar sichtbar und direkt verwendbar. |
| Tatsächliches Ergebnis | [einfügen] |
| Status | Noch nicht durchgeführt |
| Nachweis | [Screenshot-Datei einfügen] |
| Bemerkung | [einfügen] |

---

### Testfall ST-03: Suche nach einer bekannten semanticId

| Feld | Beschreibung |
|-|-|
| Testfall-ID | ST-03 |
| Testobjekt | Suchfunktion |
| Zugehörige Anforderung | FA.001, FA.010, NFA.004 |
| Ziel | Prüfen, ob eine bekannte semanticId gefunden wird. |
| Vorbedingung | Mindestens ein semantischer Eintrag ist in Wikibase/Semantic Hub vorhanden. |
| Testdaten | Beispiel: `http://qudt.org/vocab/unit/V` oder eine bekannte semanticId aus dem Projekt. |
| Testschritte | 1. Suchfunktion öffnen.<br>2. Bekannte semanticId eingeben.<br>3. Suche ausführen.<br>4. Ergebnisliste prüfen.<br>5. Gefundenen Eintrag öffnen. |
| Erwartetes Ergebnis | Der passende Eintrag wird gefunden und angezeigt. Der Nutzer kann den Eintrag öffnen und die Detailansicht wird geladen. |
| Tatsächliches Ergebnis | [einfügen] |
| Status | Noch nicht durchgeführt |
| Nachweis | [Screenshot-Datei einfügen] |
| Bemerkung | [einfügen] |

---

### Testfall ST-04: Suche mit Teilbegriff, Sonderzeichen und ohne Treffer

| Feld | Beschreibung |
|-|-|
| Testfall-ID | ST-04 |
| Testobjekt | Suchfunktion / Fehlerbehandlung |
| Zugehörige Anforderung | FA.010, NFA.001, NFA.004 |
| Ziel | Prüfen, ob die Suchfunktion unterschiedliche Eingaben kontrolliert verarbeitet. |
| Vorbedingung | Suchfunktion ist erreichbar und mindestens ein semantischer Eintrag ist vorhanden. |
| Testdaten | `Volt`, `V`, `Unit`, `http://qudt.org/vocab/unit/V`, `xyzTestEintragNichtVorhanden123` |
| Testschritte | 1. Suchfunktion öffnen.<br>2. Teilbegriff oder Label eingeben und Ergebnis prüfen.<br>3. URI mit Sonderzeichen eingeben und Ergebnis prüfen.<br>4. Nicht vorhandenen Suchbegriff eingeben und Meldung prüfen. |
| Erwartetes Ergebnis | Passende Einträge werden bei gültigen Teilbegriffen oder URIs angezeigt. Bei nicht vorhandenen Begriffen zeigt das System eine verständliche Meldung wie „Keine Ergebnisse gefunden“. Es treten keine Darstellungsfehler oder Systemabbrüche auf. |
| Tatsächliches Ergebnis | [einfügen] |
| Status | Noch nicht durchgeführt |
| Nachweis | [Screenshot-Dateien einfügen] |
| Bemerkung | [einfügen] |

---

### Testfall ST-05: Liste aller semanticIds abrufen

| Feld | Beschreibung |
|-|-|
| Testfall-ID | ST-05 |
| Testobjekt | REST-API |
| Zugehörige Anforderung | FA.002, NFA.001, NFA.002 |
| Ziel | Prüfen, ob über die API eine Liste aller verfügbaren semanticIds zurückgegeben wird. |
| Vorbedingung | API ist gestartet und erreichbar. |
| Testdaten | `GET /semanticIds` |
| Testschritte | 1. API-Anfrage mit Browser, curl oder Postman ausführen.<br>2. HTTP-Status prüfen.<br>3. Antwortinhalt prüfen.<br>4. JSON-Struktur der Antwort kontrollieren. |
| Erwartetes Ergebnis | Die API liefert HTTP-Status 200 und eine strukturierte JSON-Antwort mit verfügbaren semanticIds. |
| Tatsächliches Ergebnis | [einfügen] |
| Status | Noch nicht durchgeführt |
| Nachweis | [Screenshot oder Konsolenausgabe einfügen] |
| Bemerkung | [einfügen] |

Beispiel für den Nachweis:

```bash
curl http://localhost:8000/semanticIds
```

```json
[Antwort hier einfügen]
```

---

### Testfall ST-06: Einzelne semanticId abrufen und Sprachparameter prüfen

| Feld | Beschreibung |
|-|-|
| Testfall-ID | ST-06 |
| Testobjekt | REST-API / Sprachparameter |
| Zugehörige Anforderung | FA.001, FA.002, FA.003, FA.004 |
| Ziel | Prüfen, ob ein einzelner Eintrag über seinen Identifier abgerufen wird und die API sprachabhängige Antworten unterstützt. |
| Vorbedingung | API ist erreichbar und ein gültiger Identifier ist vorhanden. |
| Testdaten | `GET /semanticIds/{identifier}`, `GET /semanticIds/{identifier}?lang=de`, `GET /semanticIds/{identifier}?lang=en` |
| Testschritte | 1. Bekannten Identifier auswählen.<br>2. API-Anfrage ohne Sprachparameter ausführen.<br>3. API-Anfrage mit `lang=de` ausführen.<br>4. API-Anfrage mit `lang=en` ausführen.<br>5. Antworten vergleichen. |
| Erwartetes Ergebnis | Die API liefert den passenden Eintrag als JSON zurück. Relevante Felder wie Identifier, semanticId, Beschreibung, Definition oder weitere gemappte Eigenschaften sind enthalten. Bei gesetztem Sprachparameter werden vorhandene Sprachdaten passend zurückgegeben oder fehlende Übersetzungen kontrolliert behandelt. |
| Tatsächliches Ergebnis | [einfügen] |
| Status | Noch nicht durchgeführt |
| Nachweis | [Screenshot oder Konsolenausgabe einfügen] |
| Bemerkung | [einfügen] |

Beispiel für den Nachweis:

```bash
curl http://localhost:8000/semanticIds/volt
curl "http://localhost:8000/semanticIds/volt?lang=de"
curl "http://localhost:8000/semanticIds/volt?lang=en"
```

```json
[Antworten hier einfügen]
```

---

### Testfall ST-07: Sortierung und Filterung der semanticIds prüfen

| Feld | Beschreibung |
|-|-|
| Testfall-ID | ST-07 |
| Testobjekt | REST-API / Query-Parameter |
| Zugehörige Anforderung | FA.002, FA.006, NFA.002 |
| Ziel | Prüfen, ob die API Query-Parameter zur Sortierung und Filterung korrekt verarbeitet. |
| Vorbedingung | API ist erreichbar und mehrere semanticIds aus unterschiedlichen Quellen sind vorhanden. |
| Testdaten | `GET /semanticIds?sortbyDate=asc`, `GET /semanticIds?sortbyDate=desc`, `GET /semanticIds?filterbyURI=qudt.org` |
| Testschritte | 1. API-Anfrage mit aufsteigender Sortierung ausführen.<br>2. API-Anfrage mit absteigender Sortierung ausführen.<br>3. API-Anfrage mit URI-Domain-Filter ausführen.<br>4. Ergebnislisten vergleichen. |
| Erwartetes Ergebnis | Die API gibt semanticIds in der angeforderten Sortierreihenfolge zurück. Beim Domain-Filter werden nur passende Einträge angezeigt. Ungültige oder nicht passende Parameter werden verständlich behandelt. |
| Tatsächliches Ergebnis | [einfügen] |
| Status | Noch nicht durchgeführt |
| Nachweis | [Screenshot oder Konsolenausgabe einfügen] |
| Bemerkung | [einfügen] |

Beispiel für den Nachweis:

```bash
curl "http://localhost:8000/semanticIds?sortbyDate=asc"
curl "http://localhost:8000/semanticIds?sortbyDate=desc"
curl "http://localhost:8000/semanticIds?filterbyURI=qudt.org"
```

```json
[Antworten hier einfügen]
```

---

### Testfall ST-08: Ungültigen Identifier abrufen

| Feld | Beschreibung |
|-|-|
| Testfall-ID | ST-08 |
| Testobjekt | REST-API / Fehlerbehandlung |
| Zugehörige Anforderung | FA.002, NFA.001 |
| Ziel | Prüfen, ob die API bei nicht vorhandenen Einträgen korrekt reagiert. |
| Vorbedingung | API ist erreichbar. |
| Testdaten | `GET /semanticIds/nichtVorhanden123` |
| Testschritte | 1. API-Anfrage mit ungültigem Identifier ausführen.<br>2. HTTP-Status prüfen.<br>3. Fehlermeldung prüfen.<br>4. Kontrollieren, ob das System weiterhin erreichbar bleibt. |
| Erwartetes Ergebnis | Die API liefert eine verständliche Fehlermeldung, z. B. mit HTTP-Status 404. Das System stürzt nicht ab und bleibt für weitere Anfragen erreichbar. |
| Tatsächliches Ergebnis | [einfügen] |
| Status | Noch nicht durchgeführt |
| Nachweis | [Screenshot oder Konsolenausgabe einfügen] |
| Bemerkung | [einfügen] |

Beispiel für den Nachweis:

```bash
curl -i http://localhost:8000/semanticIds/nichtVorhanden123
```

```json
[Fehlerantwort hier einfügen]
```

---

### Testfall ST-09: QUDT-Daten in AAS-Concept-Description-Struktur prüfen

| Feld | Beschreibung |
|-|-|
| Testfall-ID | ST-09 |
| Testobjekt | QUDT-Mapper / API-Ausgabe |
| Zugehörige Anforderung | FA.003, FA.006, FA.009, FA.011 |
| Ziel | Prüfen, ob QUDT-Daten korrekt in das AAS-Concept-Description-Format übertragen werden. |
| Vorbedingung | QUDT-Daten wurden geladen und gemappt. |
| Testdaten | Beispiel: QUDT Unit Volt, `http://qudt.org/vocab/unit/V`. |
| Testschritte | 1. QUDT-Eintrag importieren oder vorhandenen Eintrag verwenden.<br>2. API-Abfrage zum Eintrag ausführen.<br>3. JSON-Antwort prüfen.<br>4. Felder mit erwarteter AAS-CD-Struktur vergleichen.<br>5. Prüfen, ob Quellenbezug bzw. URI nachvollziehbar ist. |
| Erwartetes Ergebnis | Die API-Antwort enthält eine strukturierte Concept Description. Relevante Eigenschaften wie semanticId, preferredName, shortName, definition, unit, symbol oder Beschreibung sind korrekt zugeordnet, sofern sie in der Quelle vorhanden sind. Quellenverweise bleiben nachvollziehbar. |
| Tatsächliches Ergebnis | [einfügen] |
| Status | Noch nicht durchgeführt |
| Nachweis | [Screenshot oder JSON-Ausgabe einfügen] |
| Bemerkung | [einfügen] |

Beispielhafte Feldprüfung:

| Feld | Erwartung | Tatsächlicher Wert | Bewertung |
|-|-|-|-|
| semanticId | `http://qudt.org/vocab/unit/V` | [einfügen] | [bestanden / nicht bestanden] |
| preferredName | Volt oder sprachabhängiger Name | [einfügen] | [einfügen] |
| symbol | `V` | [einfügen] | [einfügen] |
| dataType | Unit / qudt:Unit | [einfügen] | [einfügen] |
| source / URI | Quelle nachvollziehbar | [einfügen] | [einfügen] |

---

### Testfall ST-10: VEC-/KBL-Mapping sowie Import und Export prüfen

| Feld | Beschreibung |
|-|-|
| Testfall-ID | ST-10 |
| Testobjekt | VEC-Mapper, KBL-Mapper, REST-API / Import und Export |
| Zugehörige Anforderung | FA.002, FA.003, FA.009, FA.011, NFA.003 |
| Ziel | Prüfen, ob VEC- und KBL-Daten nachvollziehbar in das gemeinsame semantische Modell übertragen und über Import-/Export-Funktionen verarbeitet werden können. |
| Vorbedingung | VEC- und KBL-Beispieldaten oder Mapping-Dateien sind vorhanden. Die API unterstützt Import und Export. |
| Testdaten | Beispielhafte VEC-/KBL-Begriffe, `POST /semanticIds`, `GET /semanticIds/export` |
| Testschritte | 1. VEC- und KBL-Testdaten vorbereiten.<br>2. Mapping ausführen oder vorhandene Mapping-Ergebnisse verwenden.<br>3. Mehrere semanticIds über `POST /semanticIds` importieren.<br>4. Export über `GET /semanticIds/export` ausführen.<br>5. Prüfen, ob die importierten und exportierten Daten nachvollziehbar dem Zielmodell entsprechen.<br>6. Falls Schreibzugriffe geschützt sind, prüfen, ob unautorisierte Schreibzugriffe abgewiesen werden. |
| Erwartetes Ergebnis | VEC- und KBL-Daten werden in eine einheitliche Struktur übertragen. Fehlende oder abweichende Felder werden kontrolliert behandelt. Import und Export liefern strukturierte Daten, die mit dem semantischen Zielmodell kompatibel sind. Schreibzugriffe werden entsprechend dem aktuellen Projektstand kontrolliert oder als offene Einschränkung dokumentiert. |
| Tatsächliches Ergebnis | [einfügen] |
| Status | Noch nicht durchgeführt |
| Nachweis | [Screenshot oder JSON-Ausgabe einfügen] |
| Bemerkung | [einfügen] |

Beispiel für den Nachweis:

```bash
curl -X POST http://localhost:8000/semanticIds \
  -H "Content-Type: application/json" \
  -d '[Testdaten hier einfügen]'

curl http://localhost:8000/semanticIds/export
```

```json
[Import-/Export-Antwort hier einfügen]
```

---

## 8. Fehler, Auffälligkeiten und Abweichungen

### 8.1 Übersicht erkannter Fehler

| Fehler-ID | Zugehöriger Testfall | Beschreibung | Schweregrad | Status | Verantwortlich |
|-|-|-|-|-|-|
| ERR-001 | [einfügen] | [einfügen] | [kritisch / hoch / mittel / niedrig] | [offen / behoben / akzeptiert] | [einfügen] |
| ERR-002 | [einfügen] | [einfügen] | [einfügen] | [einfügen] | [einfügen] |
| ERR-003 | [einfügen] | [einfügen] | [einfügen] | [einfügen] | [einfügen] |

### 8.2 Detailbeschreibung der Fehler

#### ERR-001: [Titel einfügen]

| Feld | Beschreibung |
|-|-|
| Fehler-ID | ERR-001 |
| Gefunden in Testfall | [einfügen] |
| Beschreibung | [einfügen] |
| Schritte zur Reproduktion | [einfügen] |
| Erwartetes Verhalten | [einfügen] |
| Tatsächliches Verhalten | [einfügen] |
| Schweregrad | [kritisch / hoch / mittel / niedrig] |
| Status | [offen / behoben / akzeptiert] |
| Nachweis | [Screenshot / Log / API-Antwort einfügen] |

---

## 9. Bewertung der Anforderungen

| Anforderung | Beschreibung | Zugeordnete Testfälle | Bewertung nach Testdurchführung |
|-|-|-|-|
| FA.001 | Auflösbare URIs / Detailseiten | ST-01, ST-03, ST-06 | [erfüllt / teilweise erfüllt / nicht erfüllt / offen] |
| FA.002 | REST-API zum Abrufen von Concept Descriptions | ST-05, ST-06, ST-07, ST-08, ST-10 | [einfügen] |
| FA.003 | Mapping auf IEC-61360-Datentemplate | ST-06, ST-09, ST-10 | [einfügen] |
| FA.004 | Sprachabhängige API-Ausgabe | ST-06 | [einfügen] |
| FA.006 | Verlinkung externer Quellen | ST-07, ST-09 | [einfügen] |
| FA.009 | Automatisierter Import externer Concept Descriptions per URI | ST-09, ST-10 | [einfügen] |
| FA.010 | Überarbeitete Startseite und verbesserte Suchfunktion | ST-01, ST-02, ST-03, ST-04 | [einfügen] |
| FA.011 | Quellenspezifische Mapper für QUDT, VEC und KBL auf IEC61360 | ST-09, ST-10 | [einfügen] |
| NFA.001 | Verfügbarkeit / Stabilität | ST-01, ST-04, ST-05, ST-08 | [einfügen] |
| NFA.002 | Performance / Antwortzeit | ST-05, ST-06, ST-07 | [einfügen] |
| NFA.003 | Sicherheit / kontrollierter Schreibzugriff | ST-10 | [einfügen] |
| NFA.004 | Benutzerfreundlichkeit | ST-01, ST-02, ST-03, ST-04 | [einfügen] |

---

## 10. Traceability Matrix

Die Traceability Matrix zeigt, welche Testfälle welche Anforderungen abdecken und welches Ergebnis nach der Testdurchführung erzielt wurde.

| Testfall-ID | Abgedeckte Anforderungen | Ergebnis |
|-|-|-|
| ST-01 | FA.001, FA.010, NFA.001, NFA.004 | Noch nicht durchgeführt |
| ST-02 | FA.010, NFA.004 | Noch nicht durchgeführt |
| ST-03 | FA.001, FA.010, NFA.004 | Noch nicht durchgeführt |
| ST-04 | FA.010, NFA.001, NFA.004 | Noch nicht durchgeführt |
| ST-05 | FA.002, NFA.001, NFA.002 | Noch nicht durchgeführt |
| ST-06 | FA.001, FA.002, FA.003, FA.004 | Noch nicht durchgeführt |
| ST-07 | FA.002, FA.006, NFA.002 | Noch nicht durchgeführt |
| ST-08 | FA.002, NFA.001 | Noch nicht durchgeführt |
| ST-09 | FA.003, FA.006, FA.009, FA.011 | Noch nicht durchgeführt |
| ST-10 | FA.002, FA.003, FA.009, FA.011, NFA.003 | Noch nicht durchgeführt |

---

## 11. Screenshots und Nachweise

Zur Nachvollziehbarkeit der Testdurchführung werden Screenshots, API-Antworten und Konsolenausgaben gesammelt.

| Nachweis-ID | Zugehöriger Testfall | Beschreibung | Datei / Pfad |
|-|-|-|-|
| N-01 | ST-01 | Startseite erreichbar | `images/str-st01-startseite.png` |
| N-02 | ST-02 | Suchfeld sichtbar | `images/str-st02-suchfeld.png` |
| N-03 | ST-03 | Suchergebnis für bekannte semanticId | `images/str-st03-semanticid-suche.png` |
| N-04 | ST-04 | Suche ohne Treffer / Sonderzeichen | `images/str-st04-suchvarianten.png` |
| N-05 | ST-05 | API-Antwort `GET /semanticIds` | `images/str-st05-api-semanticids.png` |
| N-06 | ST-06 | API-Antwort mit Sprachparameter | `images/str-st06-api-lang.png` |
| N-07 | ST-07 | API-Antwort mit Sortierung / Filterung | `images/str-st07-api-filter-sort.png` |
| N-08 | ST-08 | Fehlerantwort bei ungültigem Identifier | `images/str-st08-api-error.png` |
| N-09 | ST-09 | QUDT-Mapping-Ausgabe | `images/str-st09-qudt-mapping.png` |
| N-10 | ST-10 | VEC-/KBL-Mapping, Import und Export | `images/str-st10-import-export.png` |
| N-11 | ST-05 / ST-06 / ST-09 | API-v3-Suchantwort `GET /api/v3/search?search=Volt&lang=de&types=unit` | `images/str-api-v3-search.png` |

Beispiel für die Einbindung eines Screenshots:

```markdown
![API-Antwort semanticIds](images/str-st05-api-semanticids.png)

Abbildung 1 zeigt die JSON-Antwort des Endpunkts `GET /semanticIds` während der Testdurchführung.
```

---

## 12. Gesamteinschätzung

Nach Durchführung der Tests ist zu bewerten, ob die Semantic Wikibase die im STP definierten Systemtestziele erfüllt.

### 12.1 Zusammenfassung

[Hier nach der Testdurchführung eine kurze Zusammenfassung einfügen.]

Beispieltext, falls die meisten Tests erfolgreich waren:

> Die durchgeführten Systemtests zeigen, dass die grundlegenden Funktionen der Semantic Wikibase im getesteten Umfang funktionsfähig sind. Die Startseite ist erreichbar, die Suchfunktion ist nutzbar und die API liefert strukturierte JSON-Antworten. Die Mapping-Ergebnisse aus QUDT, VEC und KBL sind grundsätzlich nachvollziehbar. Einzelne Funktionen befinden sich weiterhin im prototypischen Zustand und müssen im weiteren Projektverlauf stabilisiert oder erweitert werden.

Beispieltext, falls viele Funktionen noch offen sind:

> Die durchgeführten Systemtests zeigen, dass Teile der geplanten Funktionalität bereits vorbereitet oder prototypisch vorhanden sind. Mehrere Testfälle konnten jedoch noch nicht vollständig durchgeführt werden, da einzelne API-Endpunkte, Mapping-Funktionen oder UI-Elemente noch nicht final implementiert sind. Die offenen Punkte werden im weiteren Projektverlauf priorisiert und im Rahmen weiterer Tests erneut überprüft.

### 12.2 Testfazit

| Bereich | Bewertung |
|-|-|
| Startseite / UI | [einfügen] |
| Suchfunktion | [einfügen] |
| REST-API | [einfügen] |
| Query-Parameter | [einfügen] |
| Fehlerbehandlung | [einfügen] |
| QUDT-Mapping | [einfügen] |
| VEC-/KBL-Mapping | [einfügen] |
| Import / Export | [einfügen] |
| Sicherheit / Schreibzugriff | [einfügen] |
| Gesamtbewertung | [einfügen] |

---

## 13. Offene Punkte und Empfehlungen

| Offener Punkt | Beschreibung | Empfehlung | Priorität |
|-|-|-|-|
| OP-01 | [einfügen] | [einfügen] | [hoch / mittel / niedrig] |
| OP-02 | [einfügen] | [einfügen] | [einfügen] |
| OP-03 | [einfügen] | [einfügen] | [einfügen] |

Mögliche offene Punkte nach der Testdurchführung können sein:

- Suchfunktion findet nicht alle semanticIds zuverlässig,
- Suchfeld ist auf der Startseite noch nicht deutlich genug sichtbar,
- API-Endpunkte weichen von der geplanten Spezifikation ab,
- Sprachparameter liefern noch keine unterschiedlichen Ausgaben,
- Fehlerantworten sind technisch korrekt, aber für Nutzer nicht verständlich genug,
- Mapping-Felder aus QUDT, VEC oder KBL sind noch unvollständig,
- Import- und Exportfunktionen sind nur teilweise implementiert,
- Rechteverwaltung für Schreibzugriffe ist noch nicht umgesetzt,
- API-v3-Suche und `/semanticIds`-Endpunkte müssen ggf. im STR voneinander abgegrenzt werden.

---

## 14. Referenzen und Anhang

### 14.1 Referenzen

- STP – Software Test Plan Semantic Wikibase
- CRS – Lastenheft Semantic Wikibase
- SRS – Pflichtenheft Semantic Wikibase
- SAS – Software Architecture Specification Semantic Wikibase
- SAS_AAS_Wikibase – AAS Concept Description API & Sucherweiterung
- MOD – Moduldokumentation zur OpenAPI-Spezifikation und Mapping-Zusammenführung
- BC – Business Case Semantic Wikibase
- PM – Projektplan Semantic Wikibase
- Projektbeschreibung **Semantic Wikibase**
- Vorlesung Software Engineering I: **Von der Anforderung zum Testfall**
- Vorlesung Software Engineering I: **Analytische Qualitätssicherung**
- Vorlesung Software Engineering I: **Requirements Engineering**
- Vorlesung Software Engineering I: **Digitaler Zwilling, Verwaltungsschale und AAS**
- GitHub-Issue #25: **Implementierung verbesserter Suchfunktion**
- GitHub-Issue #26: **Neue Startseitenstruktur mit den vorgegebenen Inhalten**
- GitHub-Issue #27: **API gemäß AAS Concept Description Specification**

### 14.2 Beispielhafte API-Requests

```bash
curl http://localhost:8000/semanticIds
curl http://localhost:8000/semanticIds/volt
curl "http://localhost:8000/semanticIds/volt?lang=de"
curl "http://localhost:8000/semanticIds/volt?lang=en"
curl "http://localhost:8000/semanticIds?filterbyURI=qudt.org"
curl "http://localhost:8000/semanticIds?sortbyDate=asc"
curl "http://localhost:8000/semanticIds?sortbyDate=desc"
curl -i http://localhost:8000/semanticIds/nichtVorhanden123
curl http://localhost:8000/semanticIds/export
curl "http://localhost:8000/api/v3/search?search=Volt&lang=de&types=unit"
```

### 14.3 Beispielhafte Testdaten

| Quelle | Beispiel | Zweck |
|-|-|-|
| QUDT | `http://qudt.org/vocab/unit/V` | Test einer bekannten Einheit. |
| QUDT | `Volt` | Suche nach Label oder Begriff. |
| QUDT | `V` | Suche nach Symbol / Kurzbegriff. |
| API v3 | `GET /api/v3/search?search=Volt&lang=de&types=unit` | Prüfung des dokumentierten Such-Endpunkts aus MOD/SAS_AAS. |
| VEC | Beispielhafter VEC-Begriff aus Mapping-Datei | Prüfung des VEC-Mappings. |
| KBL | Beispielhafter KBL-Begriff aus Mapping-Datei | Prüfung des KBL-Mappings. |
| Testdaten | `xyzTestEintragNichtVorhanden123` | Negativtest ohne Treffer. |
| API | `nichtVorhanden123` | Negativtest für ungültigen Identifier. |

### 14.4 Statusdefinitionen

| Status | Bedeutung |
|-|-|
| Bestanden | Erwartetes Ergebnis wurde vollständig erreicht. |
| Teilweise bestanden | Kernfunktion funktioniert, aber es gibt Einschränkungen oder Abweichungen. |
| Fehlgeschlagen | Erwartetes Ergebnis wurde nicht erreicht. |
| Blockiert | Test konnte wegen fehlender Voraussetzung nicht durchgeführt werden. |
| Noch nicht durchgeführt | Test wurde zum Zeitpunkt der STR-Erstellung noch nicht ausgeführt. |
