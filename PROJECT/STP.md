# STP – Software Test Plan

---

## 1. Einleitung

Der Software Test Plan (STP) beschreibt die Vorgehensweise zur Qualitätssicherung des Projekts Semantic Wikibase. Ziel des Dokuments ist es, nachvollziehbar festzulegen, welche Komponenten getestet werden, welche Testarten eingesetzt werden und wie die Tests durchgeführt werden.

Im Projekt werden semantische Daten aus verschiedenen Quellen verarbeitet, gemappt und über eine API bzw. Wikibase-Struktur bereitgestellt. Dazu gehören unter anderem Daten aus QUDT, VEC und KBL sowie die Verarbeitung von Dateien und Datenstrukturen für den Semantic Hub.

Der STP dient dazu, sicherzustellen, dass die entwickelten Komponenten korrekt funktionieren, die Daten vollständig verarbeitet werden und die Ergebnisse nachvollziehbar überprüft werden können.

---

## 2. Teststrategie

Die Teststrategie beschreibt, wie die Qualität der im Projekt entwickelten Komponenten überprüft wird. Der Fokus liegt auf der korrekten Verarbeitung, Transformation und Bereitstellung von semantischen Daten.

Im Rahmen des Projekts werden folgende Testarten eingesetzt:

- **Funktionale Tests:**  
  Es wird geprüft, ob einzelne Funktionen korrekt arbeiten. Dazu gehört beispielsweise das Laden von QUDT-Daten, das Parsen von TTL-Dateien und das Erzeugen einer JSON-Struktur.

- **Integrationstests:**  
  Es wird überprüft, ob mehrere Komponenten korrekt zusammenarbeiten. Zum Beispiel wird getestet, ob extrahierte Daten korrekt an das Mapping übergeben und anschließend im Semantic Hub genutzt werden können.

- **Systemtests:**  
  Das Gesamtsystem wird als Einheit betrachtet. Dabei wird geprüft, ob der komplette Ablauf von der Datenquelle bis zur Ausgabe über API oder Wikibase funktioniert.

- **Mapping-Tests:**  
  Es wird kontrolliert, ob Begriffe und Strukturen aus Quellen wie VEC und KBL korrekt auf das gemeinsame Datenmodell übertragen werden.

- **API-Tests:**  
  Es wird geprüft, ob die API auf Anfragen korrekt antwortet und die erwarteten Daten zurückliefert.

- **Fehlertests:**  
  Es wird getestet, wie das System auf fehlerhafte Eingaben reagiert, zum Beispiel ungültige URLs, fehlende Datenfelder oder fehlerhafte API-Anfragen.

---

## 3. Testobjekte

Im Projekt werden folgende Komponenten getestet:

| Testobjekt | Beschreibung |
|---|---|
| QUDT-Parser | Lädt und verarbeitet QUDT-Daten aus TTL-Dateien |
| VEC-Mapping | Überführt VEC-Begriffe in das gemeinsame semantische Datenmodell |
| KBL-Mapping | Überführt KBL-Begriffe in das gemeinsame semantische Datenmodell |
| JSON-Ausgabe | Speichert extrahierte und gemappte Daten in strukturierter Form |
| Semantic Hub / Wikibase | Stellt semantische Daten im Zielsystem dar |
| API | Liefert Daten über definierte Schnittstellen zurück |
| Fehlerbehandlung | Reagiert auf fehlerhafte oder unvollständige Eingaben |

---

## 4. Testumgebung

Die Tests werden in einer lokalen Entwicklungsumgebung durchgeführt.

| Komponente | Beschreibung |
|---|---|
| Betriebssystem | Windows |
| Entwicklungsumgebung | Visual Studio Code |
| Programmiersprache | Python |
| API-Testwerkzeug | Browser, curl oder Postman |
| Datenquellen | QUDT, VEC, KBL |
| Zielsystem | Semantic Hub / Wikibase |
| Versionsverwaltung | GitHub |

Die lokale Testumgebung ermöglicht es, Parser, Mapping-Dateien und API-Anfragen unabhängig vom Produktivsystem zu überprüfen.

---

## 5. Testfälle

### Testfall 1: Laden von QUDT-Daten

| Feld | Beschreibung |
|---|---|
| Ziel | Prüfen, ob QUDT-Daten korrekt geladen werden können |
| Eingabe | QUDT-URL, z. B. eine Unit wie Volt |
| Erwartetes Ergebnis | Die TTL-Datei wird erfolgreich geladen |
| Tatsächliches Ergebnis | Die Daten konnten geladen werden |
| Status | Erfolgreich |

---

### Testfall 2: Parsen einer TTL-Datei

| Feld | Beschreibung |
|---|---|
| Ziel | Prüfen, ob TTL-Daten korrekt verarbeitet werden |
| Eingabe | TTL-Daten aus QUDT |
| Erwartetes Ergebnis | Die Datei wird geparst und relevante Tripel werden erkannt |
| Tatsächliches Ergebnis | Die Tripel konnten ausgelesen werden |
| Status | Erfolgreich |

---

### Testfall 3: Extraktion relevanter Eigenschaften

| Feld | Beschreibung |
|---|---|
| Ziel | Prüfen, ob wichtige Eigenschaften aus den Daten extrahiert werden |
| Eingabe | Geparste QUDT-Daten |
| Erwartetes Ergebnis | Eigenschaften wie Label, Symbol, Typ und Beschreibung werden erkannt |
| Tatsächliches Ergebnis | Die relevanten Eigenschaften wurden extrahiert |
| Status | Erfolgreich |

---

### Testfall 4: Erstellung einer JSON-Struktur

| Feld | Beschreibung |
|---|---|
| Ziel | Prüfen, ob die extrahierten Daten korrekt als JSON gespeichert werden |
| Eingabe | Extrahierte Eigenschaften |
| Erwartetes Ergebnis | Eine strukturierte JSON-Ausgabe wird erzeugt |
| Tatsächliches Ergebnis | Die JSON-Struktur wurde erstellt |
| Status | Erfolgreich |

---

### Testfall 5: VEC-Mapping

| Feld | Beschreibung |
|---|---|
| Ziel | Prüfen, ob VEC-Begriffe korrekt auf das gemeinsame Modell übertragen werden |
| Eingabe | Begriffe und Strukturen aus der VEC-Quelle |
| Erwartetes Ergebnis | Die Daten werden einem einheitlichen Mapping-Schema zugeordnet |
| Tatsächliches Ergebnis | Das Mapping konnte erstellt und dokumentiert werden |
| Status | Erfolgreich / Teilweise erfolgreich |

---

### Testfall 6: KBL-Mapping

| Feld | Beschreibung |
|---|---|
| Ziel | Prüfen, ob KBL-Begriffe korrekt auf das gemeinsame Modell übertragen werden |
| Eingabe | Begriffe und Strukturen aus der KBL-Quelle |
| Erwartetes Ergebnis | Die Daten werden einem einheitlichen Mapping-Schema zugeordnet |
| Tatsächliches Ergebnis | Das Mapping konnte erstellt und dokumentiert werden |
| Status | Erfolgreich / Teilweise erfolgreich |

---

### Testfall 7: API-Abfrage

| Feld | Beschreibung |
|---|---|
| Ziel | Prüfen, ob die API korrekt auf Anfragen reagiert |
| Eingabe | API-Anfrage über Browser, curl oder Postman |
| Erwartetes Ergebnis | Die API liefert eine gültige Antwort im JSON-Format |
| Tatsächliches Ergebnis | Die Antwort konnte empfangen und geprüft werden |
| Status | Erfolgreich |

---

### Testfall 8: Darstellung im Semantic Hub / Wikibase

| Feld | Beschreibung |
|---|---|
| Ziel | Prüfen, ob Daten im Semantic Hub bzw. in Wikibase sichtbar sind |
| Eingabe | Importierte oder manuell übernommene Daten |
| Erwartetes Ergebnis | Die Daten erscheinen korrekt im Zielsystem |
| Tatsächliches Ergebnis | Die Darstellung konnte überprüft werden |
| Status | Erfolgreich / Teilweise erfolgreich |

---

### Testfall 9: Fehlerhafte API-Anfrage

| Feld | Beschreibung |
|---|---|
| Ziel | Prüfen, wie das System auf ungültige Anfragen reagiert |
| Eingabe | Ungültige oder unvollständige API-Anfrage |
| Erwartetes Ergebnis | Das System gibt eine verständliche Fehlermeldung zurück |
| Tatsächliches Ergebnis | Fehlerhafte Anfragen wurden erkannt |
| Status | Erfolgreich |

---

### Testfall 10: Fehlende Datenfelder

| Feld | Beschreibung |
|---|---|
| Ziel | Prüfen, wie das System mit unvollständigen Daten umgeht |
| Eingabe | Datensatz mit fehlenden Eigenschaften |
| Erwartetes Ergebnis | Das System verarbeitet vorhandene Daten und bricht nicht unkontrolliert ab |
| Tatsächliches Ergebnis | Fehlende Felder konnten erkannt werden |
| Status | Erfolgreich / Teilweise erfolgreich |

---

## 6. Testdurchführung

Die Tests wurden manuell in der lokalen Entwicklungsumgebung durchgeführt. Dabei wurden einzelne Komponenten zunächst separat geprüft und anschließend im Zusammenspiel betrachtet.

Der QUDT-Parser wurde über ein Python-Skript ausgeführt. Dabei wurde geprüft, ob die Datenquelle erreichbar ist, ob die TTL-Daten korrekt geladen werden und ob daraus eine strukturierte Ausgabe erzeugt werden kann.

Die Mapping-Dateien für VEC und KBL wurden auf Konsistenz überprüft. Dabei wurde kontrolliert, ob die jeweiligen Begriffe sinnvoll auf das gemeinsame Datenmodell übertragen wurden.

Die API wurde mit Browser, curl oder Postman getestet. Dabei wurde geprüft, ob die Schnittstelle erreichbar ist und ob gültige JSON-Antworten zurückgegeben werden.

Die Darstellung im Semantic Hub bzw. in Wikibase wurde visuell geprüft. Dabei wurde kontrolliert, ob die Daten korrekt angezeigt werden und ob die semantischen Informationen nachvollziehbar sind.

---

## 7. Testergebnisse

Die wichtigsten Tests konnten erfolgreich durchgeführt werden. Besonders die Verarbeitung von QUDT-Daten, das Parsen der TTL-Struktur und die Erstellung einer JSON-Ausgabe konnten nachvollziehbar geprüft werden.

Auch die Mapping-Arbeiten für VEC und KBL konnten dokumentiert und überprüft werden. Dabei wurde deutlich, dass die einzelnen Datenquellen unterschiedliche Strukturen besitzen und deshalb eine manuelle Anpassung an ein gemeinsames Schema notwendig ist.

Die API konnte grundsätzlich getestet werden. Erfolgreiche API-Anfragen liefern strukturierte Daten zurück. Fehlerhafte Anfragen konnten erkannt werden und dienen als Grundlage für die weitere Verbesserung der Fehlerbehandlung.

Die Integration in den Semantic Hub bzw. in Wikibase konnte teilweise überprüft werden. Einige Funktionen befinden sich noch in einem prototypischen Zustand, weshalb nicht alle geplanten Funktionen vollständig automatisiert getestet werden konnten.

---

## 8. Screenshots und Nachweise

Zur besseren Nachvollziehbarkeit können dem Dokument Screenshots hinzugefügt werden.

Geeignete Screenshots sind:

- Ausgabe des QUDT-Parsers in der Konsole
- Beispiel einer erzeugten JSON-Datei
- API-Antwort im Browser, in curl oder Postman
- Darstellung eines Eintrags im Semantic Hub / Wikibase
- Ordnerstruktur des Projekts im Repository

Jeder Screenshot sollte kurz beschrieben werden.

Beispiel:

```markdown
![Beispiel JSON-Ausgabe](./screenshots/json-output.png)

Abbildung 1 zeigt eine erzeugte JSON-Ausgabe nach dem Parsen einer QUDT-Unit.