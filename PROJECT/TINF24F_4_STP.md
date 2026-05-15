# Software Test Plan (STP)

*Dokumentverantwortliche: Testmanager, Marvin Igrec und Technische Redakteure, Lucrezia Trabalza und Marina Hidalgo Burova*


## Versionskontrolle

| Version | Datum | Autor | Kommentar |
|-|-|-|-|
| 0.1 | 12.05.2026 | Marvin Igrec | Erstellung & erster Entwurf |
| 0.2 | 12.05.2026 | Marvin Igrec | Anpassung an CRS-, SRS- und SAS-Struktur |
| 0.3 | 12.05.2026 | Marvin Igrec | Reduktion auf ca. 10 Systemtestfälle, Ergänzung der Testbasis und Traceability |
| 0.4 | 12.05.2026 | Marvin Igrec | Ergänzung weiterer Projektartefakte als Referenzen |
| 0.5 | 15.05.2026 | Marvin Igrec | Abgleich mit aktueller SRS-Anforderungsnummerierung, Ergänzung FA.011 und API-v3-Request |

<br>

## Inhaltsverzeichnis

- [Software Test Plan (STP)](#software-test-plan-stp)
  - [Versionskontrolle](#versionskontrolle)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [1. Einführung in den Software Test Plan](#1-einführung-in-den-software-test-plan)
  - [2. Projektziel](#2-projektziel)
  - [3. Testgegenstand und Systemübersicht](#3-testgegenstand-und-systemübersicht)
    - [3.1 Product Perspective](#31-product-perspective)
    - [3.2 Systemgrenze](#32-systemgrenze)
    - [3.3 Begriffserklärung](#33-begriffserklärung)
  - [4. Testbasis](#4-testbasis)
  - [5. Teststrategie](#5-teststrategie)
    - [5.1 Testansatz](#51-testansatz)
    - [5.2 Testarten](#52-testarten)
    - [5.3 Testabdeckung](#53-testabdeckung)
  - [6. Testobjekte](#6-testobjekte)
  - [7. Testumgebung](#7-testumgebung)
  - [8. Testfälle](#8-testfälle)
    - [8.1 Übersicht der Testfälle](#81-übersicht-der-testfälle)
    - [8.2 Ausgearbeitete Systemtestfälle](#82-ausgearbeitete-systemtestfälle)
  - [9. Traceability Matrix](#9-traceability-matrix)
  - [10. Testdurchführung](#10-testdurchführung)
  - [11. Erwartete Testergebnisse](#11-erwartete-testergebnisse)
  - [12. Risiken und Einschränkungen](#12-risiken-und-einschränkungen)
  - [13. Screenshots und Nachweise](#13-screenshots-und-nachweise)
  - [14. Referenzen und Anhang](#14-referenzen-und-anhang)

---

## 1. Einführung in den Software Test Plan

Der Software Test Plan (STP) beschreibt die geplante Vorgehensweise zur Qualitätssicherung des Projekts **Semantic Wikibase**. Das Dokument legt fest, welche Systembestandteile getestet werden, welche Testarten eingesetzt werden, welche Testumgebung verwendet wird und welche Testfälle im Rahmen des Systemtests durchgeführt werden sollen.

Der Schwerpunkt liegt auf **Systemtests nach dem Black-Box-Prinzip**. Das bedeutet, dass das System aus Sicht eines Nutzers oder API-Clients getestet wird. Interne Implementierungsdetails des Quellcodes stehen nicht im Vordergrund. Entscheidend ist, ob das System bei definierten Eingaben die erwarteten Ausgaben und Reaktionen liefert.

Der STP dient als Grundlage für den späteren **Software Test Report (STR)**. Während der STP beschreibt, was getestet werden soll, dokumentiert der STR anschließend, welche Tests tatsächlich durchgeführt wurden und welche Ergebnisse dabei entstanden sind.

---

## 2. Projektziel

Ziel des Projekts **Semantic Wikibase** ist die Entwicklung einer webbasierten Plattform zur Verwaltung, Veröffentlichung und Abfrage semantischer Definitionen für die Asset Administration Shell (AAS). Concept Descriptions sollen über auflösbare URIs bereitgestellt und über eine REST-API im AAS- bzw. IEC-61360-orientierten Format abrufbar sein.

Ein besonderer Fokus liegt auf:

- der einfachen Suche und Anzeige semantischer Begriffe,
- der Bereitstellung maschinenlesbarer Concept Descriptions über eine API,
- dem Mapping externer Datenquellen wie QUDT, VEC und KBL,
- der langfristigen Kompatibilität mit AAS- und IEC-61360-Strukturen,
- einer nachvollziehbaren und benutzerfreundlichen Oberfläche.

---

## 3. Testgegenstand und Systemübersicht

### 3.1 Product Perspective

Die Semantic Wikibase ist eine webbasierte Plattform, die als semantische Registry für Concept Descriptions dient. Nutzer sollen Begriffe suchen, Detailseiten öffnen und semantische Informationen über eine API abrufen können. Die Plattform basiert auf Wikibase und wird durch zusätzliche Komponenten wie Mapper, Parser und eine API-Fassade erweitert.

Die Tests beziehen sich insbesondere auf das von außen sichtbare Verhalten der Plattform. Dazu gehören die Weboberfläche, die Suchfunktion, die REST-API, die Verarbeitung semantischer IDs sowie die sichtbaren Ergebnisse der Mapper.

### 3.2 Systemgrenze

Innerhalb der Testgrenze liegen:

- Startseite und grundlegende Benutzeroberfläche,
- Suchfunktion und Ergebnisdarstellung,
- Detailansicht semantischer Einträge,
- REST-API für semanticIds bzw. Concept Descriptions,
- Query-Parameter für Sortierung und Filterung,
- Mapping-Ergebnisse aus QUDT, VEC und KBL,
- Import- und Exportfunktionen der API,
- Fehlerbehandlung bei ungültigen oder unvollständigen Eingaben.

Außerhalb der Testgrenze liegen:

- vollständige Last- und Performancetests unter Produktivbedingungen,
- tiefgehende Security-Penetrationstests,
- vollständige Prüfung externer Datenquellen auf fachliche Richtigkeit,
- interne Unit-Tests einzelner Funktionen, sofern sie nicht von außen sichtbar sind.

### 3.3 Begriffserklärung

| Begriff | Erklärung |
|-|-|
| AAS | Asset Administration Shell, also die digitale Verwaltungsschale eines Assets. |
| Concept Description (CD) | Semantische Beschreibung eines Begriffs oder einer Eigenschaft innerhalb der AAS. |
| SemanticId / SID | Eindeutige semantische Kennung, häufig als auflösbare URI. |
| Wikibase | MediaWiki-basierte Plattform zur Verwaltung strukturierter semantischer Daten. |
| REST-API | Schnittstelle, über die Daten über HTTP abgefragt oder übertragen werden können. |
| IEC 61360 | Standard zur strukturierten Beschreibung technischer Merkmale und Eigenschaften. |
| Mapper | Komponente, die Daten aus externen Quellen in das interne Zielmodell überführt. |
| STR | Software Test Report, in dem die tatsächlichen Testergebnisse dokumentiert werden. |

---

## 4. Testbasis

Die Testfälle werden aus den Projektanforderungen, Use Cases, Architekturentscheidungen und Projekt-Issues abgeleitet. Als Grundlage dienen insbesondere:

- CRS / Lastenheft mit Use Cases und funktionalen Anforderungen,
- SRS / Pflichtenheft mit konkretisierten Anforderungen und UI-Beschreibung,
- SAS / Software Architecture Specification mit Architektur, API-Fassade, Datenmodell und Deployment-Sicht,
- SAS_AAS_Wikibase mit detaillierter API-Architektur, Such-Architektur und Transformationsschicht,
- Projektbeschreibung **Semantic Wikibase**,
- GitHub-Issue #25 zur verbesserten Suchfunktion,
- GitHub-Issue #26 zur neuen Startseitenstruktur,
- GitHub-Issue #27 zur API gemäß AAS Concept Description Specification,
- vorhandene Mapper- und Parser-Implementierungen für QUDT, VEC und KBL,
- Vorlesung **Von der Anforderung zum Testfall** als methodische Grundlage für anforderungsbasierte Systemtests, Testfallentwurf und Traceability,
- Vorlesung **Analytische Qualitätssicherung** als Grundlage für Black-Box-Tests, dynamische Tests und systematisches Testen,
- Vorlesung **Requirements Engineering** als Grundlage für die Ableitung von Testfällen aus funktionalen und nicht-funktionalen Anforderungen,
- Vorlesung **Digitaler Zwilling, Verwaltungsschale und AAS** als fachliche Grundlage für AAS, Concept Descriptions und semantische Referenzierung,
- Business Case (BC) als Grundlage für Nutzen, Motivation und Risiken des Projekts,
- Projektplan (PM) als Grundlage für Testphase, Zeitplanung und organisatorische Rahmenbedingungen,
- Moduldokumentation (MOD) als Grundlage für OpenAPI-Spezifikation und Mapping-Zusammenführung.

Aus der Vorlesung **Von der Anforderung zum Testfall** wird übernommen, dass Systemtests grundsätzlich anforderungsbasiert entworfen werden. Relevante Anforderungen sollen durch mindestens einen Testfall abgedeckt werden. Aus diesem Grund enthält der STP eine Traceability Matrix, die Anforderungen und Testfälle miteinander verknüpft.

Die Vorlesung **Analytische Qualitätssicherung** unterscheidet außerdem zwischen Debugging und systematischem Testen. Im STP wird deshalb nicht nur ausprobiert, ob Funktionen grundsätzlich laufen, sondern es werden definierte Eingaben, erwartete Ergebnisse und Nachweise festgelegt.

Zusätzlich werden projektspezifische Dokumente wie Business Case, Projektplan und Moduldokumentation berücksichtigt. Der Business Case beschreibt die Motivation und den wirtschaftlichen Nutzen einer offenen Semantic Wikibase. Der Projektplan liefert organisatorische Rahmenbedingungen für Testphase und Dokumentation. Die Moduldokumentation konkretisiert die OpenAPI-Spezifikation sowie die Zusammenführung der Mappings aus QUDT, VEC und KBL.

Besonders relevante Anforderungen für diesen STP sind:

| Anforderung | Bedeutung für den Test |
|-|-|
| FA.001 | Auflösbare URIs und Detailseiten müssen geprüft werden. |
| FA.002 | REST-API muss Concept Descriptions strukturiert zurückgeben. |
| FA.003 | Mapping auf ein IEC-61360-orientiertes Datenmodell muss geprüft werden. |
| FA.004 | Sprachabhängige API-Ausgabe muss berücksichtigt werden. |
| FA.006 | Quellenverweise sollen in Detailansicht oder API nachvollziehbar sein. |
| FA.009 | Import bzw. Verarbeitung externer Concept Descriptions per URI ist relevant für Import- und Mapper-Tests. |
| FA.010 | Startseite und verbesserte Suchfunktion müssen geprüft werden. |
| FA.011 | Quellenspezifische Mapper für QUDT, VEC und KBL müssen gegen das IEC61360-Zielmodell geprüft werden. |
| NFA.001 | System soll während Test und Demo stabil erreichbar sein. |
| NFA.002 | API soll ohne wahrnehmbare Verzögerung antworten. |
| NFA.003 | Schreibzugriffe und sicherheitsrelevante API-Funktionen müssen kontrolliert betrachtet werden. |
| NFA.004 | Benutzeroberfläche und Suche sollen intuitiv nutzbar sein. |

Durch diese Zuordnung wird sichergestellt, dass die Testfälle nicht isoliert betrachtet werden, sondern direkt auf die aktuell dokumentierten Anforderungen aus CRS und SRS zurückgeführt werden können. Besonders wichtig ist dabei die korrekte Abgrenzung zwischen Importfunktionen, verbesserter Suchfunktion und quellenspezifischen Mappern.

---

## 5. Teststrategie

### 5.1 Testansatz

Die Tests werden überwiegend als manuelle Black-Box-Systemtests durchgeführt. Dabei wird geprüft, ob das Gesamtsystem aus Nutzersicht und aus Sicht eines API-Clients korrekt funktioniert.

Die Testfälle werden bewusst zusammengefasst, damit die Vorgabe von ungefähr zehn ausgearbeiteten Systemtestfällen eingehalten wird. Mehrere Anforderungen können dabei durch einen gemeinsamen Testfall abgedeckt werden, sofern sie fachlich zusammengehören.

Der Fokus liegt auf folgenden Fragen:

- Ist die Plattform erreichbar?
- Ist die Suchfunktion einfach auffindbar und nutzbar?
- Werden bekannte semanticIds korrekt gefunden?
- Liefert die API gültige und strukturierte JSON-Antworten?
- Werden Query-Parameter wie Sprache, Sortierung und Filterung korrekt verarbeitet?
- Werden ungültige Eingaben kontrolliert behandelt?
- Sind gemappte Daten aus QUDT, VEC und KBL nachvollziehbar im Zielmodell erkennbar?

### 5.2 Testarten

| Testart | Beschreibung |
|-|-|
| Funktionale Tests | Prüfung einzelner sichtbarer Funktionen, z. B. Suche, API-Abruf, Import oder Export. |
| Integrationstests | Prüfung des Zusammenspiels von Mapper, API und Wikibase-Darstellung. |
| Systemtests | Prüfung des Gesamtsystems aus Nutzersicht. |
| API-Tests | Prüfung von Endpunkten, Query-Parametern, HTTP-Statuscodes und JSON-Strukturen. |
| Mapping-Tests | Prüfung, ob externe Datenquellen korrekt in das interne Modell übertragen werden. |
| Fehlertests | Prüfung des Systemverhaltens bei ungültigen Eingaben oder fehlenden Daten. |
| Usability-orientierte Tests | Prüfung, ob Suche und Einstiegspunkte für Nutzer leicht auffindbar sind. |

### 5.3 Testabdeckung

Die Testfälle decken die wichtigsten Projektbereiche ab:

- Web-UI und Startseite,
- Suchfunktion,
- API-Endpunkte,
- Sprachparameter,
- Sortierung und Filterung,
- Import und Export,
- QUDT-/VEC-/KBL-Mapping,
- Fehlerbehandlung,
- Nachvollziehbarkeit der Ergebnisse.

---

## 6. Testobjekte

| Testobjekt | Beschreibung |
|-|-|
| Startseite | Einstiegspunkt der Plattform und Orientierung für Nutzer. |
| Suchfunktion | Suche nach semanticIds, Labels, Teilbegriffen und URI-Bestandteilen. |
| Detailansicht | Anzeige eines semantischen Eintrags mit Beschreibung, Definition, Einheit und Quelle. |
| REST-API | Abruf, Import, Export und Filterung von semanticIds bzw. Concept Descriptions. |
| QUDT-Mapper | Verarbeitung und Mapping von QUDT-Daten, z. B. Einheiten wie Volt. |
| VEC-Mapper | Überführung von VEC-Begriffen in das gemeinsame Datenmodell. |
| KBL-Mapper | Überführung von KBL-Begriffen in das gemeinsame Datenmodell. |
| JSON-Ausgabe | Strukturierte Ausgabe gemappter Daten. |
| Fehlerbehandlung | Reaktion auf nicht vorhandene Identifier, ungültige Parameter und fehlende Datenfelder. |

---

## 7. Testumgebung

Die Tests werden in einer lokalen Entwicklungs- und Testumgebung durchgeführt.

| Komponente | Beschreibung |
|-|-|
| Betriebssystem | Windows |
| Entwicklungsumgebung | Visual Studio Code |
| Programmiersprache | Python |
| API-Framework | FastAPI, sofern für die lokale API verwendet |
| API-Testwerkzeug | Browser, curl oder Postman |
| Datenquellen | QUDT, VEC, KBL |
| Zielsystem | Lokale Semantic-Hub-/Wikibase-Instanz |
| Versionsverwaltung | GitHub |
| Ausführung | Lokal über Python-Skripte und/oder Docker-Umgebung |

Die genaue Testumgebung wird im späteren STR mit konkreten Versionen, URLs, Ports und Screenshots dokumentiert.

---

## 8. Testfälle

### 8.1 Übersicht der Testfälle

| Testfall-ID | Testbereich | Kurzbeschreibung | Priorität |
|-|-|-|-|
| ST-01 | Startseite | Aufruf der Startseite und Prüfung der Erreichbarkeit | Hoch |
| ST-02 | Suche / UX | Suchfeld auf der Startseite auffindbar | Hoch |
| ST-03 | Suche | Suche nach bekannter semanticId | Hoch |
| ST-04 | Suche / Fehlerbehandlung | Suche mit Teilbegriff, Sonderzeichen und ohne Treffer | Hoch |
| ST-05 | API | Liste aller semanticIds abrufen | Hoch |
| ST-06 | API / Sprache | Einzelne semanticId abrufen und Sprachparameter prüfen | Hoch |
| ST-07 | API / Query-Parameter | Sortierung und Filterung der semanticIds prüfen | Mittel |
| ST-08 | API / Fehlerbehandlung | Ungültigen Identifier abrufen | Hoch |
| ST-09 | Mapping | QUDT-Daten in AAS-Concept-Description-Struktur prüfen | Hoch |
| ST-10 | Integration / Mapping | VEC-/KBL-Mapping sowie Import und Export prüfen | Mittel |

### 8.2 Ausgearbeitete Systemtestfälle

---

### Testfall ST-01: Aufruf der Startseite

| Feld | Beschreibung |
|-|-|
| Testfall-ID | ST-01 |
| Testobjekt | Startseite / Benutzeroberfläche |
| Zugehörige Anforderung | FA.010, NFA.001, NFA.004 |
| Ziel | Prüfen, ob die Startseite des Semantic Hub korrekt erreichbar ist. |
| Vorbedingung | Lokale Wikibase-/Semantic-Hub-Instanz ist gestartet. |
| Testdaten | URL der lokalen Instanz. |
| Testschritte | 1. Browser öffnen.<br>2. URL der lokalen Instanz aufrufen.<br>3. Prüfen, ob die Startseite geladen wird. |
| Erwartetes Ergebnis | Die Startseite wird ohne Fehlermeldung geladen. Wichtige Einstiegspunkte wie Suche oder Navigation sind sichtbar. |
| Tatsächliches Ergebnis | Wird im STR ergänzt. |
| Status | Offen |

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
| Tatsächliches Ergebnis | Wird im STR ergänzt. |
| Status | Offen |

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
| Tatsächliches Ergebnis | Wird im STR ergänzt. |
| Status | Offen |

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
| Tatsächliches Ergebnis | Wird im STR ergänzt. |
| Status | Offen |

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
| Tatsächliches Ergebnis | Wird im STR ergänzt. |
| Status | Offen |

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
| Tatsächliches Ergebnis | Wird im STR ergänzt. |
| Status | Offen |

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
| Tatsächliches Ergebnis | Wird im STR ergänzt. |
| Status | Offen |

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
| Tatsächliches Ergebnis | Wird im STR ergänzt. |
| Status | Offen |

---

### Testfall ST-09: QUDT-Daten in AAS-Concept-Description-Struktur prüfen

| Feld | Beschreibung |
|-|-|
| Testfall-ID | ST-09 |
| Testobjekt | QUDT-Mapper / API-Ausgabe |
| Zugehörige Anforderung | FA.003, FA.006, FA.011 |
| Ziel | Prüfen, ob QUDT-Daten korrekt in das AAS-Concept-Description-Format übertragen werden. |
| Vorbedingung | QUDT-Daten wurden geladen und gemappt. |
| Testdaten | Beispiel: QUDT Unit Volt, `http://qudt.org/vocab/unit/V`. |
| Testschritte | 1. QUDT-Eintrag importieren oder vorhandenen Eintrag verwenden.<br>2. API-Abfrage zum Eintrag ausführen.<br>3. JSON-Antwort prüfen.<br>4. Felder mit erwarteter AAS-CD-Struktur vergleichen.<br>5. Prüfen, ob Quellenbezug bzw. URI nachvollziehbar ist. |
| Erwartetes Ergebnis | Die API-Antwort enthält eine strukturierte Concept Description. Relevante Eigenschaften wie semanticId, preferredName, shortName, definition, unit, symbol oder Beschreibung sind korrekt zugeordnet, sofern sie in der Quelle vorhanden sind. Quellenverweise bleiben nachvollziehbar. |
| Tatsächliches Ergebnis | Wird im STR ergänzt. |
| Status | Offen |

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
| Testschritte | 1. VEC- und KBL-Testdaten vorbereiten.<br>2. Mapping ausführen oder vorhandene Mapping-Ergebnisse verwenden.<br>3. Mehrere semanticIds über `POST /semanticIds` importieren.<br>4. Export über `GET /semanticIds/export` ausführen.<br>5. Prüfen, ob die importierten und exportierten Daten nachvollziehbar dem Zielmodell entsprechen. |
| Erwartetes Ergebnis | VEC- und KBL-Daten werden in eine einheitliche Struktur übertragen. Fehlende oder abweichende Felder werden kontrolliert behandelt. Import und Export liefern strukturierte Daten, die mit dem semantischen Zielmodell kompatibel sind. |
| Tatsächliches Ergebnis | Wird im STR ergänzt. |
| Status | Offen |

---

## 9. Traceability Matrix

Die Traceability Matrix zeigt, welche Anforderungen durch welche Testfälle abgedeckt werden. Sie basiert auf der aktuellen Nummerierung der funktionalen und nicht-funktionalen Anforderungen aus dem SRS.

| Anforderung | Beschreibung | Zugeordnete Testfälle |
|-|-|-|
| FA.001 | Auflösbare URIs / Detailseiten | ST-01, ST-03, ST-06 |
| FA.002 | REST-API zum Abrufen von Concept Descriptions | ST-05, ST-06, ST-07, ST-08, ST-10 |
| FA.003 | Mapping auf IEC-61360-Datentemplate | ST-06, ST-09, ST-10 |
| FA.004 | Sprachabhängige API-Ausgabe | ST-06 |
| FA.006 | Verlinkung externer Quellen | ST-07, ST-09 |
| FA.009 | Automatisierter Import externer Concept Descriptions per URI | ST-09, ST-10 |
| FA.010 | Überarbeitete Startseite und verbesserte Suchfunktion | ST-01, ST-02, ST-03, ST-04 |
| FA.011 | Quellenspezifische Mapper für QUDT, VEC und KBL auf IEC61360 | ST-09, ST-10 |
| NFA.001 | Verfügbarkeit / Stabilität | ST-01, ST-04, ST-05, ST-08 |
| NFA.002 | Performance / Antwortzeit | ST-05, ST-06, ST-07 |
| NFA.003 | Sicherheit / kontrollierter Schreibzugriff | ST-10 |
| NFA.004 | Benutzerfreundlichkeit | ST-01, ST-02, ST-03, ST-04 |

Die Anforderungen FA.005, FA.007, FA.008 und NFA.005 werden in diesem STP nicht durch eigenständige Systemtestfälle vollständig abgedeckt, da der Fokus dieses Testplans auf der Suchfunktion, der API, den Mappern sowie den sichtbaren Systemreaktionen liegt. Diese Anforderungen können bei Bedarf in ergänzenden Tests oder Reviews betrachtet werden.

---

## 10. Testdurchführung

Die Systemtests werden überwiegend manuell durchgeführt. Für die Benutzeroberfläche werden Browsertests genutzt. Für die API werden Browser, curl oder Postman verwendet.

Die Durchführung erfolgt in folgenden Schritten:

1. Lokale Testumgebung starten.
2. Erreichbarkeit der Startseite prüfen.
3. Suchfunktion mit gültigen, unvollständigen und ungültigen Eingaben testen.
4. API-Endpunkte mit gültigen und ungültigen Requests prüfen.
5. Query-Parameter für Sprache, Sortierung und Filterung testen.
6. Mapping-Ergebnisse aus QUDT, VEC und KBL anhand der JSON-Ausgabe prüfen.
7. Import- und Exportfunktionen anhand strukturierter Testdaten prüfen.
8. Screenshots und Konsolenausgaben als Nachweise sichern.
9. Tatsächliche Ergebnisse und Status im STR dokumentieren.

Da dieses Dokument ein Testplan ist, werden die endgültigen Testergebnisse nicht hier, sondern im Software Test Report dokumentiert.

---

## 11. Erwartete Testergebnisse

Es wird erwartet, dass die grundlegenden Funktionen des Systems erfolgreich überprüft werden können. Dazu gehören insbesondere:

- Erreichbarkeit der Startseite,
- Auffindbarkeit und Nutzbarkeit der Suchfunktion,
- erfolgreiche Suche nach bekannten semanticIds,
- kontrollierte Reaktion bei Suchanfragen ohne Treffer,
- korrekte JSON-Antworten der API,
- korrekte Verarbeitung von Query-Parametern,
- nachvollziehbare Fehlerausgaben bei ungültigen Identifiern,
- erkennbare Mapping-Ergebnisse für QUDT, VEC und KBL,
- nachvollziehbarer Import und Export von semanticIds.

Bei noch nicht vollständig implementierten Funktionen wird erwartet, dass diese im STR als **Offen**, **Teilweise erfolgreich** oder **Fehlgeschlagen** dokumentiert werden.

---

## 12. Risiken und Einschränkungen

| Risiko / Einschränkung | Auswirkung | Umgang im Test |
|-|-|-|
| Funktionen sind noch prototypisch | Nicht alle Testfälle können vollständig durchgeführt werden. | Status im STR als „Offen“ oder „Teilweise erfolgreich“ dokumentieren. |
| API-Endpunkte können von der finalen Spezifikation abweichen | Testdaten oder Requests müssen angepasst werden. | Tatsächlich verfügbare Endpunkte im STR dokumentieren. |
| Externe Quellen können nicht erreichbar sein | Mapper-Tests können fehlschlagen. | Lokale Beispieldaten oder gespeicherte Testdaten verwenden. |
| Datenmodell ist noch nicht final | Mapping-Ergebnisse können sich ändern. | Erwartete Zielstruktur klar dokumentieren. |
| Lokale Umgebung unterscheidet sich von Zielumgebung | Ergebnisse sind nur eingeschränkt übertragbar. | Testumgebung im STR genau beschreiben. |
| Such-Extension oder Startseitenstruktur ist noch nicht final | UI-Tests können sich ändern. | Im STR dokumentieren, welche UI-Version getestet wurde. |

---

## 13. Screenshots und Nachweise

Zur Nachvollziehbarkeit der Testdurchführung werden Screenshots und Ausgaben gesammelt. Geeignete Nachweise sind:

- Startseite mit sichtbarer Suchfunktion,
- Suchergebnis für eine bekannte semanticId,
- Suchergebnis mit Teilbegriff oder Label,
- Suchergebnis ohne Treffer,
- API-Antwort für `GET /semanticIds`,
- API-Antwort für `GET /semanticIds/{identifier}`,
- API-Antwort mit Sprachparameter,
- API-Antwort mit Sortierung oder Filterung,
- Fehlermeldung bei ungültigem Identifier,
- Beispiel einer gemappten QUDT-Ausgabe,
- Beispiel einer VEC- oder KBL-Mapping-Ausgabe,
- Darstellung eines Eintrags in Wikibase/Semantic Hub,
- Repository- oder Ordnerstruktur der Testdaten.

Beispiel für die Einbindung eines Nachweises:

```markdown
![API-Antwort semanticIds](images/stp-api-semanticids.png)

Abbildung 1 zeigt die JSON-Antwort des Endpunkts `GET /semanticIds` während der Testdurchführung.
```

---

## 14. Referenzen und Anhang

### 14.1 Referenzen

- CRS – Lastenheft Semantic Wikibase
- SRS – Pflichtenheft Semantic Wikibase
- SAS – Software Architecture Specification Semantic Wikibase
- SAS_AAS_Wikibase – AAS Concept Description API & Sucherweiterung
- BC – Business Case Semantic Wikibase
- PM – Projektplan Semantic Wikibase
- MOD – Moduldokumentation zur OpenAPI-Spezifikation und Mapping-Zusammenführung
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
curl http://localhost:8000/semanticIds/export
curl "http://localhost:8000/api/v3/search?search=Volt&lang=de&types=unit"
```

### 14.3 Beispielhafte Testdaten

| Quelle | Beispiel | Zweck |
|-|-|-|
| QUDT | `http://qudt.org/vocab/unit/V` | Test einer bekannten Einheit. |
| QUDT | `Volt` | Suche nach Label oder Begriff. |
| VEC | Beispielhafter VEC-Begriff aus Mapping-Datei | Prüfung des VEC-Mappings. |
| KBL | Beispielhafter KBL-Begriff aus Mapping-Datei | Prüfung des KBL-Mappings. |
| Testdaten | `xyzTestEintragNichtVorhanden123` | Negativtest ohne Treffer. |
| API | `nichtVorhanden123` | Negativtest für ungültigen Identifier. |
| API v3 | `/api/v3/search?search=Volt&lang=de&types=unit` | Test des dokumentierten Such-Endpunkts aus MOD und SAS_AAS_Wikibase. |
