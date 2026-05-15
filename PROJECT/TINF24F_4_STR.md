# Software Test Report (STR)

*Dokumentverantwortliche: Testmanager, Marvin Igrec und Technische Redakteure, Lucrezia Trabalza und Marina Hidalgo Burova*

## Versionskontrolle

| Version | Datum | Autor | Kommentar |
|-|-|-|-|
| 0.1 | 14.05.2026 | Marvin Igrec | Erstellung der STR-Ausfüllvorlage auf Basis des STP |
| 0.2 | 15.05.2026 | Marvin Igrec | Anpassung an überarbeitete STP, aktuelle SRS-Anforderungen und vorbereitende Ausfüllstruktur |

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
  - [7. Detaillierte Testergebnisse](#7-detaillierte-testergebnisse)
  - [8. Fehler, Auffälligkeiten und Abweichungen](#8-fehler-auffälligkeiten-und-abweichungen)
  - [9. Bewertung der Anforderungen](#9-bewertung-der-anforderungen)
  - [10. Traceability Matrix](#10-traceability-matrix)
  - [11. Screenshots und Nachweise](#11-screenshots-und-nachweise)
  - [12. Gesamteinschätzung](#12-gesamteinschätzung)
  - [13. Offene Punkte und Empfehlungen](#13-offene-punkte-und-empfehlungen)
  - [14. Referenzen und Anhang](#14-referenzen-und-anhang)

---

## 1. Einführung in den Software Test Report

Der Software Test Report (STR) dokumentiert die Durchführung und Ergebnisse der im Software Test Plan (STP) definierten Systemtests für das Projekt **Semantic Wikibase**.

Während der STP beschreibt, welche Tests geplant sind, hält der STR fest, welche Tests tatsächlich durchgeführt wurden, welche Ergebnisse dabei entstanden sind und welche Fehler, Auffälligkeiten oder offenen Punkte festgestellt wurden.

Der Schwerpunkt dieses STR liegt auf den im STP definierten **Black-Box-Systemtests**. Dabei wird das System aus Sicht eines Nutzers oder API-Clients betrachtet. Interne Implementierungsdetails des Quellcodes stehen nicht im Vordergrund. Entscheidend ist, ob das System bei definierten Eingaben die erwarteten Reaktionen und Ausgaben liefert.

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

---

## 3. Testbasis

Die Testdurchführung basiert auf folgenden Dokumenten und Projektartefakten:

- Software Test Plan (STP) Semantic Wikibase,
- CRS / Lastenheft Semantic Wikibase,
- SRS / Pflichtenheft Semantic Wikibase,
- SAS / Software Architecture Specification Semantic Wikibase,
- SAS_AAS_Wikibase – AAS Concept Description API & Sucherweiterung,
- MOD – Moduldokumentation zur OpenAPI-Spezifikation und Mapping-Zusammenführung,
- BC – Business Case Semantic Wikibase,
- PM – Projektplan Semantic Wikibase,
- Projektbeschreibung „Semantic Wikibase“,
- GitHub-Issue #25 zur verbesserten Suchfunktion,
- GitHub-Issue #26 zur neuen Startseitenstruktur,
- GitHub-Issue #27 zur API gemäß AAS Concept Description Specification,
- Vorlesung „Von der Anforderung zum Testfall“,
- Vorlesung „Analytische Qualitätssicherung“,
- Vorlesung „Requirements Engineering“,
- Vorlesung „Digitaler Zwilling, Verwaltungsschale und AAS“.

Die Testfälle wurden im STP anforderungsbasiert definiert. Die Ergebnisse werden in diesem STR den jeweiligen Anforderungen zugeordnet, um die Nachvollziehbarkeit zwischen Anforderungen, Testfällen und Testergebnissen sicherzustellen.

---

## 4. Testumfang

### 4.1 Durchgeführte Testarten

| Testart | Beschreibung | Durchführung |
|-|-|-|
| Funktionale Tests | Prüfung sichtbarer Funktionen wie Suche, API-Abruf, Import und Export | Geplant |
| Systemtests | Prüfung des Gesamtsystems aus Nutzer- und API-Client-Sicht | Geplant |
| API-Tests | Prüfung von Endpunkten, HTTP-Statuscodes, Query-Parametern und JSON-Strukturen | Geplant |
| Mapping-Tests | Prüfung der sichtbaren Mapping-Ergebnisse aus QUDT, VEC und KBL | Geplant |
| Fehlertests | Prüfung von ungültigen Suchbegriffen, ungültigen Identifiern und nicht vorhandenen Daten | Geplant |
| Usability-orientierte Tests | Prüfung der Auffindbarkeit und Bedienbarkeit der Suchfunktion | Geplant |

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
| Betriebssystem | Windows 11 |
| Entwicklungsumgebung | Visual Studio Code |
| Browser | Google Chrome / Microsoft Edge, genaue Version nach Testdurchführung ergänzen |
| API-Testwerkzeug | Browser, curl und ggf. Postman |
| Programmiersprache | Python |
| API-Framework | FastAPI / Flask, abhängig vom getesteten API-Modul |
| Lokale API-URL | `http://localhost:8000`, falls die lokale API auf diesem Port gestartet wird |
| Wikibase-/Semantic-Hub-URL | [einfügen] |
| Datenquellen | QUDT, VEC, KBL |
| Repository / Branch | `DHBW-TINF24F/Team4-Semantic-Wikibase`, Branch `main`, Commit-ID nach Testdurchführung ergänzen |
| Testdatum | [einfügen] |
| Tester | [einfügen] |

---

## 6. Zusammenfassung der Testergebnisse

| Kennzahl | Anzahl |
|-|-:|
| Geplante Testfälle | 10 |
| Durchgeführte Testfälle | 0 |
| Bestanden | 0 |
| Teilweise bestanden | 0 |
| Fehlgeschlagen | 0 |
| Blockiert / nicht durchführbar | 0 |
| Offen / noch nicht getestet | 10 |

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
| Tatsächliches Ergebnis | Der geplante Endpunkt `GET /semanticIds` wurde über `http://localhost:8000/semanticIds` getestet. Die API war grundsätzlich erreichbar, der Endpunkt selbst lieferte jedoch die Antwort `{"detail": "Not Found"}`. Damit ist der Listen-Endpunkt im aktuellen Projektstand nicht implementiert bzw. nicht verfügbar. |
| Status | Blockiert |
| Nachweis | `images/str-st05-api-semanticids-not-found.png` |
| Bemerkung | Der ursprünglich geplante Endpunkt `/semanticIds` wurde im aktuellen Projektstand nicht separat umgesetzt. Die API-Funktionalität ist stattdessen über den implementierten Gateway-Endpunkt `/map` verfügbar. Der Test kann nach Umsetzung des Listen-Endpunkts erneut durchgeführt werden. |

Beispiel für den Nachweis:

```bash
curl.exe "http://localhost:8000/semanticIds"

Die API antwortete mit `{"detail": "Not Found"}`. Der Endpunkt ist im aktuellen Projektstand nicht verfügbar.
```

```json
{
  "detail": "Not Found"
}
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
| Tatsächliches Ergebnis | Der Sprachparameter wurde über den aktuell implementierten Endpunkt `/map` mit dem Beispiel „Volt“ getestet. Die API war erreichbar und lieferte sowohl für `lang=de` als auch für `lang=en` strukturierte JSON-Antworten. Der Sprachparameter wurde in der Anfrage verarbeitet und in der Antwort bei `query.lang` sowie im Feld `preferredName` sichtbar übernommen. Bei `lang=de` wurde `preferredName` mit `lang: de` zurückgegeben, bei `lang=en` entsprechend mit `lang: en`. |
| Status | Bestanden |
| Nachweis | Screenshots: `images/str-st06-api-lang-de.png`, `images/str-st06-api-lang-en.png` |
| Bemerkung | Der ursprünglich im STP genannte Endpunkt `/semanticIds/{identifier}` wurde im aktuellen Projektstand nicht separat umgesetzt. Die geforderte Funktion zur sprachabhängigen API-Ausgabe konnte jedoch über den implementierten Gateway-Endpunkt `/map` erfolgreich nachgewiesen werden. Da „Volt“ in Deutsch und Englisch gleich benannt ist, unterscheidet sich der Wert des preferredName nicht, der Sprachcode wird jedoch korrekt übernommen. Die vollständigen JSON-Antworten wurden über Screenshots dokumentiert. |

Beispiel für den Nachweis:

```bash
curl.exe "http://localhost:8000/map?search=Volt&source=qudt&lang=de&types=unit&only_found=true"
curl.exe "http://localhost:8000/map?search=Volt&source=qudt&lang=en&types=unit&only_found=true"
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
| Tatsächliches Ergebnis | Die Sortierung und Filterung der semanticIds wurde über die geplanten Endpunkte `GET /semanticIds?sortbyDate=asc`, `GET /semanticIds?sortbyDate=desc` und `GET /semanticIds?filterbyURI=qudt.org` geprüft. Die API war grundsätzlich erreichbar, die angefragten Endpunkte lieferten jedoch jeweils die Antwort `{"detail": "Not Found"}`. Damit konnten Sortierung und Filterung im aktuellen Projektstand nicht durchgeführt werden. |
| Status | Blockiert |
| Nachweis | Sortierung: `images/str-st07-api-sort-not-found.png`<br>Filterung: `images/str-st07-api-filter-not-found.png` |
| Bemerkung | Der geplante `/semanticIds`-Endpunkt sowie die zugehörigen Query-Parameter für Sortierung und Filterung sind im aktuellen Projektstand nicht separat implementiert. Die API-Funktionalität ist stattdessen über den Gateway-Endpunkt `/map` verfügbar. Der Test kann nach Umsetzung der geplanten Listen- und Filter-Endpunkte erneut durchgeführt werden. |

Beispiel für den Nachweis:

```bash
curl.exe "http://localhost:8000/semanticIds?sortbyDate=asc"
curl.exe "http://localhost:8000/semanticIds?sortbyDate=desc"
curl.exe "http://localhost:8000/semanticIds?filterbyURI=qudt.org"

Die API antwortete bei den getesteten `/semanticIds`-Query-Requests jeweils mit `{"detail": "Not Found"}`. Die Query-Parameter konnten daher im aktuellen Projektstand nicht geprüft werden.
```

```json
{
  "detail": "Not Found"
}
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
| Tatsächliches Ergebnis | Die Fehlerbehandlung wurde über den aktuell implementierten Endpunkt `/map` mit dem Suchbegriff `nichtVorhanden123` getestet. Die API war erreichbar und lieferte eine kontrollierte JSON-Antwort mit `total: 0` und `results: []`. Es kam zu keinem Systemabsturz. Anschließend konnte eine gültige Anfrage mit dem Begriff „Volt“ erneut erfolgreich ausgeführt werden. |
| Status | Bestanden |
| Nachweis | Fehlerfall: `images/str-st08-api-error.png`<br>Kontrollanfrage: `images/str-st08-api-after-error.png` |
| Bemerkung | Der ursprünglich geplante Endpunkt `/semanticIds/nichtVorhanden123` wurde im aktuellen Projektstand nicht separat umgesetzt. Die geforderte Fehlerbehandlung konnte jedoch über den implementierten Gateway-Endpunkt `/map` erfolgreich nachgewiesen werden. |

Beispiel für den Nachweis:

```bash
curl.exe "http://localhost:8000/map?search=nichtVorhanden123&source=qudt&lang=de&types=unit&only_found=true"
curl.exe "http://localhost:8000/map?search=Volt&source=qudt&lang=de&types=unit&only_found=true"

Die vollständigen API-Antworten wurden über Screenshots dokumentiert. Der Fehlerfall liefert `total: 0` und `results: []`; eine anschließende gültige Anfrage mit „Volt“ liefert wieder ein Ergebnis.
```

```json
{
  "query": {
    "search": "nichtVorhanden123",
    "source": "qudt",
    "lang": "de",
    "types": [
      "unit"
    ],
    "onlyFound": true
  },
  "total": 0,
  "results": []
}
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
| Tatsächliches Ergebnis | Das QUDT-Mapping konnte anhand des Beispiels „Volt“ über den Endpunkt `/map?search=Volt&source=qudt&lang=de&types=unit&only_found=true` geprüft werden. Die API war erreichbar und lieferte eine strukturierte JSON-Antwort aus der Quelle QUDT. In der Antwort sind unter anderem `modelType: ConceptDescription`, die ID `http://qudt.org/vocab/unit/V`, `idShort: V`, eine `semanticId`, der `preferredName` „Volt“ mit `lang: de`, die Einheit `Volt`, das Symbol `V`, der Datentyp `http://qudt.org/schema/qudt/Unit`, eine `unitId`, Quellenverweise, Definitionen und ein `valueFormat` enthalten. |
| Status | Bestanden |
| Nachweis | `images/str-st09-qudt-mapping.png` |
| Bemerkung | Das QUDT-Mapping ist für das Beispiel „Volt“ nachvollziehbar und liefert die wichtigsten IEC61360-nahen Felder. Einzelne Felder wie `shortName`, `valueList`, `value` und `levelType` sind `null`, da diese Werte aus der QUDT-Quelle nicht direkt ableitbar bzw. für das getestete Einheitenbeispiel nicht relevant sind. |

Beispiel für den Nachweis:

```bash
curl.exe "http://localhost:8000/map?search=Volt&source=qudt&lang=de&types=unit&only_found=true"
```

```json
{
  "query": {
    "search": "Volt",
    "source": "qudt",
    "lang": "de",
    "types": [
      "unit"
    ],
    "onlyFound": true
  },
  "total": 1,
  "results": [
    {
      "source": "qudt",
      "sourceName": "QUDT",
      "success": true,
      "response": {
        "query": {
          "search": "Volt",
          "mode": "term",
          "lang": "de",
          "types": [
            "unit"
          ]
        },
        "total": 1,
        "result": {
          "modelType": "ConceptDescription",
          "id": "http://qudt.org/vocab/unit/V",
          "idShort": "V",
          "embeddedDataSpecifications": [
            {
              "dataSpecificationContent": {
                "modelType": "DataSpecificationIec61360",
                "semanticId": {
                  "property": "P1",
                  "value": "http://qudt.org/vocab/unit/V"
                },
                "preferredName": {
                  "property": "P35",
                  "value": [
                    {
                      "value": "Volt",
                      "lang": "de"
                    }
                  ]
                },
                "shortName": {
                  "property": "P36",
                  "value": null
                },
                "unit": {
                  "property": "P37",
                  "value": "Volt"
                },
                "sourceOfDefinition": {
                  "property": "P40",
                  "value": [
                    "http://qudt.org/3.2.1/vocab/unit",
                    "https://cdd.iec.ch/cdd/iec62720/iec62720.nsf/Units/0112-2---62720%23UAA296",
                    "https://en.wikipedia.org/wiki/Volt?oldid=494812083"
                  ]
                },
                "Symbol": {
                  "property": "P41",
                  "value": "V"
                },
                "dataType": {
                  "property": "P42",
                  "value": "http://qudt.org/schema/qudt/Unit"
                },
                "unitId": {
                  "property": "P43",
                  "value": "0112/2///62720#UAA296"
                },
                "Definition": {
                  "property": "P44",
                  "value": [
                    {
                      "type": "description",
                      "value": "$\\textit{Volt}$ is the SI unit of electric potential.\n  Separating electric charges creates potential energy, which can be measured in energy units such as joules.\n  Electric potential is defined as the amount of potential energy present per unit of charge.\n  Electric potential is measured in volts, with one volt representing a potential of one joule per coulomb of charge.\n  The name of the unit honors the Italian scientist Count Alessandro Volta (1745-1827), the inventor of the first battery.\n  The volt also may be expressed with a variety of other units.\n  For example, a volt is also equal to one watt per ampere ($W/A$) and one joule per ampere per second ($J/A/s$).\n  "
                    },
                    {
                      "type": "latexDefinition",
                      "value": "$\\textit{V}\\ \\equiv\\ \\text{volt}\\ \\equiv\\ \\frac{\\text{J}}{\\text{C}}\\ \\equiv\\ \\frac{\\text{joule}}{\\text{coulomb}}\\ \\equiv\\ \\frac{\\text{W.s}}{\\text{C}}\\ \\equiv\\ \\frac{\\text{watt.second}}{\\text{coulomb}}\\ \\equiv\\ \\frac{\\text{W}}{\\text{A}}\\ \\equiv\\ \\frac{\\text{watt}}{\\text{amp}}$"
                    }
                  ]
                },
                "valueFormat": {
                  "property": "P45",
                  "value": "W/A"
                },
                "valueList": {
                  "property": "P46",
                  "value": null
                },
                "value": {
                  "property": "P47",
                  "value": null
                },
                "levelType": {
                  "property": "P48",
                  "value": null
                }
              }
            }
          ]
        }
      }
    }
  ]
}
```

Beispielhafte Feldprüfung:

| Feld | Erwartung | Tatsächlicher Wert | Bewertung |
|-|-|-|-|
| semanticId | `http://qudt.org/vocab/unit/V` | http://qudt.org/vocab/unit/V | bestanden |
| preferredName | Volt oder sprachabhängiger Name | Volt mit lang: de | bestanden |
| symbol | `V` | V | bestanden |
| dataType | Unit / qudt:Unit | http://qudt.org/schema/qudt/Unit | bestanden |
| source / URI | Quelle nachvollziehbar | QUDT-Quelle, IEC-CDD-Link und Wikipedia-Link vorhanden | bestanden |

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
| Tatsächliches Ergebnis | Das VEC- und KBL-Mapping konnte über den implementierten Gateway-Endpunkt `/map` geprüft werden. Für VEC wurde der Begriff „Volt“ über `/map?search=Volt&source=vec&lang=de&only_found=true` getestet. Die API lieferte eine strukturierte Concept-Description-Ausgabe mit `source: vec`, `sourceName: VEC`, `modelType: ConceptDescription` und dem Ergebnis `NominalVoltage`. Für KBL wurde der Begriff „Wire“ über `/map?search=Wire&source=kbl&lang=de&only_found=true` getestet. Auch hier konnte eine strukturierte Mapping-Ausgabe erzeugt werden. Die geplanten Import- und Exportfunktionen über `/semanticIds` konnten im aktuellen Projektstand jedoch nicht vollständig getestet werden. |
| Tatsächliches Ergebnis | Das VEC- und KBL-Mapping konnte über den implementierten Gateway-Endpunkt `/map` geprüft werden. Für VEC wurde der Begriff „Volt“ über `/map?search=Volt&source=vec&lang=de&only_found=true` getestet. Die API lieferte eine strukturierte Concept-Description-Ausgabe mit `source: vec`, `sourceName: VEC`, `modelType: ConceptDescription` und dem Ergebnis `NominalVoltage`. Für KBL wurde der Begriff „Wire“ über `/map?search=Wire&source=kbl&lang=de&only_found=true` getestet. Auch hier konnte eine strukturierte Mapping-Ausgabe erzeugt werden. Der geplante Export-Endpunkt `/semanticIds/export` wurde ebenfalls geprüft, lieferte jedoch `{"detail": "Not Found"}`. Die Import- und Exportfunktionen über `/semanticIds` konnten daher im aktuellen Projektstand nicht vollständig getestet werden. |
| Status | Teilweise bestanden |
| Nachweis | VEC: `images/str-st10-vec-mapping.png`<br>KBL: `images/str-st10-kbl-mapping.png`<br>Export: `images/str-st10-export-not-found.png` |
| Bemerkung | Die quellenspezifischen Mapper für VEC und KBL sind über den Gateway-Endpunkt `/map` grundsätzlich funktionsfähig. Die geplanten Endpunkte `POST /semanticIds` und `GET /semanticIds/export` sind im aktuellen Projektstand nicht separat umgesetzt bzw. nicht verfügbar. |

Beispiel für den Nachweis:

```bash
curl.exe "http://localhost:8000/map?search=Volt&source=vec&lang=de&only_found=true"
curl.exe "http://localhost:8000/map?search=Wire&source=kbl&lang=de&only_found=true"
curl.exe "http://localhost:8000/semanticIds/export"

Die VEC- und KBL-Mapping-Ausgaben wurden über Screenshots dokumentiert. Der Export-Endpunkt lieferte im aktuellen Projektstand `{"detail": "Not Found"}`.
```
Vec:
```json
{
  "query": {
    "search": "Volt",
    "source": "vec",
    "lang": "de",
    "types": null,
    "onlyFound": true
  },
  "total": 1,
  "results": [
    {
      "source": "vec",
      "sourceName": "VEC",
      "success": true,
      "response": {
        "query": {
          "search": "Volt",
          "mode": "term",
          "lang": "de",
          "source": "https://ecad-wiki.prostep.org/specifications/vec/v220/vec-2.2.0-ontology.ttl"
        },
        "total": 1,
        "result": {
          "modelType": "ConceptDescription",
          "id": "http://www.prostep.org/ontologies/ecad/2024/03/vec#NominalVoltage",
          "idShort": "NominalVoltage",
          "embeddedDataSpecifications": [
            {
              "dataSpecification": {
                "type": "ExternalReference",
                "keys": [
                  {
                    "type": "GlobalReference",
                    "value": "http://admin-shell.io/DataSpecificationTemplates/DataSpecificationIEC61360/3/0"
                  }
                ]
              },
              "dataSpecificationContent": {
                "modelType": "DataSpecificationIec61360",
                "semanticId": {
                  "property": "P1",
                  "value": "http://www.prostep.org/ontologies/ecad/2024/03/vec#NominalVoltage"
                },
                "preferredName": {
                  "property": "P35",
                  "value": [
                    {
                      "value": "NominalVoltage",
                      "lang": "en"
                    }
                  ]
                },
                "shortName": {
                  "property": "P36",
                  "value": "NominalVoltage"
                },
                "unit": {
                  "property": "P37",
                  "value": null
                },
                "sourceOfDefinition": {
                  "property": "P40",
                  "value": [
                    {
                      "type": "ontologySource",
                      "value": "https://ecad-wiki.prostep.org/specifications/vec/v220/vec-2.2.0-ontology.ttl"
                    }
                  ]
                },
                "Symbol": {
                  "property": "P41",
                  "value": null
                },
                "dataType": {
                  "property": "P42",
                  "value": "Class"
                },
                "unitId": {
                  "property": "P43",
                  "value": null
                },
                "Definition": {
                  "property": "P44",
                  "value": [
                    {
                      "type": "comment",
                      "value": " OpenEnumeration defines the nominal voltage levels currently known and used in vehicles.\n"
                    }
                  ]
                },
                "valueFormat": {
                  "property": "P45",
                  "value": null
                },
                "valueList": {
                  "property": "P46",
                  "value": null
                },
                "value": {
                  "property": "P47",
                  "value": null
                },
                "levelType": {
                  "property": "P48",
                  "value": null
                }
              }
            }
          ],
          "additionalProperties": {
            "rdfs:subClassOf": "http://www.prostep.org/ontologies/ecad/2024/03/vec#OpenEnumeration"
          }
        }
      }
    }
  ]
}
```
Kbl:
```json
{
  "query": {
    "search": "Wire",
    "source": "kbl",
    "lang": "de",
    "types": null,
    "onlyFound": true
  },
  "total": 1,
  "results": [
    {
      "source": "kbl",
      "sourceName": "KBL",
      "success": true,
      "response": {
        "query": {
          "search": "Wire",
          "mode": "xsd-term",
          "lang": "de",
          "source": "https://ecad-wiki.prostep.org/specifications/kbl/v25-sr1/kbl2.5-sr1.xsd"
        },
        "total": 1,
        "result": {
          "modelType": "ConceptDescription",
          "id": "https://ecad-wiki.prostep.org/specifications/kbl/v25-sr1/kbl2.5-sr1.xsd#Wire",
          "idShort": "Wire",
          "embeddedDataSpecifications": [
            {
              "dataSpecification": {
                "type": "ExternalReference",
                "keys": [
                  {
                    "type": "GlobalReference",
                    "value": "http://admin-shell.io/DataSpecificationTemplates/DataSpecificationIEC61360/3/0"
                  }
                ]
              },
              "dataSpecificationContent": {
                "modelType": "DataSpecificationIec61360",
                "semanticId": {
                  "property": "P1",
                  "value": "https://ecad-wiki.prostep.org/specifications/kbl/v25-sr1/kbl2.5-sr1.xsd#Wire"
                },
                "preferredName": {
                  "property": "P35",
                  "value": [
                    {
                      "value": "Wire",
                      "lang": "de"
                    }
                  ]
                },
                "shortName": {
                  "property": "P36",
                  "value": "Wire"
                },
                "unit": {
                  "property": "P37",
                  "value": null
                },
                "sourceOfDefinition": {
                  "property": "P40",
                  "value": [
                    {
                      "type": "xsdSource",
                      "value": "https://ecad-wiki.prostep.org/specifications/kbl/v25-sr1/kbl2.5-sr1.xsd"
                    }
                  ]
                },
                "Symbol": {
                  "property": "P41",
                  "value": null
                },
                "dataType": {
                  "property": "P42",
                  "value": "XSDElement"
                },
                "unitId": {
                  "property": "P43",
                  "value": null
                },
                "Definition": {
                  "property": "P44",
                  "value": [
                    {
                      "type": "documentation",
                      "value": "ref to Core_occurrence, Wire_occurrence"
                    }
                  ]
                },
                "valueFormat": {
                  "property": "P45",
                  "value": null
                },
                "valueList": {
                  "property": "P46",
                  "value": null
                },
                "value": {
                  "property": "P47",
                  "value": null
                },
                "levelType": {
                  "property": "P48",
                  "value": null
                }
              }
            }
          ],
          "additionalProperties": {
            "xsdType": "XSDElement",
            "extensionBase": null,
            "children": [],
            "attributes": []
          }
        }
      }
    }
  ]
}
```
---

## 8. Fehler, Auffälligkeiten und Abweichungen

### 8.1 Übersicht erkannter Fehler

Zum Zeitpunkt der Erstellung dieser STR-Vorlage wurden noch keine Systemtests durchgeführt. Daher sind noch keine Fehler oder Auffälligkeiten dokumentiert.

| Fehler-ID | Zugehöriger Testfall | Beschreibung | Schweregrad | Status | Verantwortlich |
|-|-|-|-|-|-|
| - | - | Noch keine Fehler dokumentiert | - | - | - |

### 8.2 Detailbeschreibung der Fehler

Die Detailbeschreibung wird ergänzt, sobald bei der Testdurchführung ein Fehler festgestellt wurde.

#### ERR-001: [Titel nach Testdurchführung einfügen]

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

Die folgende Tabelle dient zur späteren Bewertung der Anforderungen nach der Testdurchführung. Da die Tests noch nicht ausgeführt wurden, stehen alle Anforderungen zunächst auf **Offen**.

| Anforderung | Beschreibung | Zugeordnete Testfälle | Bewertung nach Testdurchführung |
|-|-|-|-|
| FA.001 | Auflösbare URIs / Detailseiten | ST-01, ST-03, ST-06 | Offen |
| FA.002 | REST-API zum Abrufen von Concept Descriptions | ST-05, ST-06, ST-07, ST-08, ST-10 | Offen |
| FA.003 | Mapping auf IEC-61360-Datentemplate | ST-06, ST-09, ST-10 | Offen |
| FA.004 | Sprachabhängige API-Ausgabe | ST-06 | Offen |
| FA.006 | Verlinkung externer Quellen | ST-07, ST-09 | Offen |
| FA.009 | Automatisierter Import externer Concept Descriptions per URI | ST-09, ST-10 | Offen |
| FA.010 | Überarbeitete Startseite und verbesserte Suchfunktion | ST-01, ST-02, ST-03, ST-04 | Offen |
| FA.011 | Quellenspezifische Mapper für QUDT, VEC und KBL auf IEC61360 | ST-09, ST-10 | Offen |
| NFA.001 | Verfügbarkeit / Stabilität | ST-01, ST-04, ST-05, ST-08 | Offen |
| NFA.002 | Performance / Antwortzeit | ST-05, ST-06, ST-07 | Offen |
| NFA.003 | Sicherheit / kontrollierter Schreibzugriff | ST-10 | Offen |
| NFA.004 | Benutzerfreundlichkeit | ST-01, ST-02, ST-03, ST-04 | Offen |

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

Beispiel für die Einbindung eines Screenshots:

```markdown
![API-Antwort semanticIds](images/str-st05-api-semanticids.png)

Abbildung 1 zeigt die JSON-Antwort des Endpunkts `GET /semanticIds` während der Testdurchführung.
```

---

## 12. Gesamteinschätzung

Da die Systemtests zum Zeitpunkt der Erstellung dieser STR-Vorlage noch nicht durchgeführt wurden, kann noch keine abschließende Bewertung der Systemqualität erfolgen.

Die Gesamteinschätzung wird nach Durchführung der Testfälle ST-01 bis ST-10 ergänzt. Bewertet werden insbesondere:

- Erreichbarkeit der Startseite und grundlegende Stabilität,
- Auffindbarkeit und Nutzbarkeit der Suchfunktion,
- REST-API und Query-Parameter,
- Fehlerbehandlung bei ungültigen Eingaben,
- QUDT-, VEC- und KBL-Mapping,
- Import- und Exportfunktionen,
- erkennbare Abweichungen zwischen Planung und tatsächlichem Systemverhalten.

### 12.1 Zusammenfassung

[nach Testdurchführung ergänzen]

### 12.2 Testfazit

| Bereich | Bewertung |
|-|-|
| Startseite / UI | Offen |
| Suchfunktion | Offen |
| REST-API | Offen |
| Query-Parameter | Offen |
| Fehlerbehandlung | Offen |
| QUDT-Mapping | Offen |
| VEC-/KBL-Mapping | Offen |
| Import / Export | Offen |
| Gesamtbewertung | Offen |

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
- Rechteverwaltung für Schreibzugriffe ist noch nicht umgesetzt.

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
- Projektbeschreibung „Semantic Wikibase“
- Vorlesung Software Engineering I: „Von der Anforderung zum Testfall“
- Vorlesung Software Engineering I: „Analytische Qualitätssicherung“
- Vorlesung Software Engineering I: „Requirements Engineering“
- Vorlesung Software Engineering I: „Digitaler Zwilling, Verwaltungsschale und AAS“
- GitHub-Issue #25: Implementierung verbesserter Suchfunktion
- GitHub-Issue #26: Neue Startseitenstruktur mit den vorgegebenen Inhalten
- GitHub-Issue #27: API gemäß AAS Concept Description Specification

### 14.2 Beispielhafte API-Requests

```bash
curl http://localhost:8000/semanticIds
curl "http://localhost:8000/api/v3/search?search=Volt&lang=de&types=unit"
curl http://localhost:8000/semanticIds/volt
curl "http://localhost:8000/semanticIds/volt?lang=de"
curl "http://localhost:8000/semanticIds/volt?lang=en"
curl "http://localhost:8000/semanticIds?filterbyURI=qudt.org"
curl "http://localhost:8000/semanticIds?sortbyDate=asc"
curl "http://localhost:8000/semanticIds?sortbyDate=desc"
curl -i http://localhost:8000/semanticIds/nichtVorhanden123
curl http://localhost:8000/semanticIds/export
```

### 14.3 Beispielhafte Testdaten

| Quelle | Beispiel | Zweck |
|-|-|-|
| QUDT | `http://qudt.org/vocab/unit/V` | Test einer bekannten Einheit. |
| QUDT | `Volt` | Suche nach Label oder Begriff. |
| QUDT | `V` | Suche nach Symbol / Kurzbegriff. |
| VEC | Beispielhafter VEC-Begriff aus Mapping-Datei | Prüfung des VEC-Mappings. |
| KBL | Beispielhafter KBL-Begriff aus Mapping-Datei | Prüfung des KBL-Mappings. |
| Testdaten | `xyzTestEintragNichtVorhanden123` | Negativtest ohne Treffer. |
| API | `nichtVorhanden123` | Negativtest für ungültigen Identifier. |
| API | `/api/v3/search?search=Volt&lang=de&types=unit` | Test des dokumentierten Such-Endpunkts aus MOD/SAS_AAS. |

### 14.4 Statusdefinitionen

| Status | Bedeutung |
|-|-|
| Bestanden | Erwartetes Ergebnis wurde vollständig erreicht. |
| Teilweise bestanden | Kernfunktion funktioniert, aber es gibt Einschränkungen oder Abweichungen. |
| Fehlgeschlagen | Erwartetes Ergebnis wurde nicht erreicht. |
| Blockiert | Test konnte wegen fehlender Voraussetzung nicht durchgeführt werden. |
| Noch nicht durchgeführt | Test wurde zum Zeitpunkt der STR-Erstellung noch nicht ausgeführt. |

