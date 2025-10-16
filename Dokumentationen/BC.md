# Business Case

*Dokumentverantwortlicher: Projektleiter, Yvonne Wagner*

## Versionskontrolle:

| Version | Datum      | Autor       | Kommentar                         |
|-|-|-|-|
| 1.0     | 10.10.2025 | Yvonne Wagner | Erstellung & erster Überblick |
| 1.1 | 16.10.2025 | Yvonne Wagner | Entwurf für Zeitplan, Ressorucenplan, Kostenplan, Aufteilung der Arbeitsstunden, Vorgehensmodell, Meilensteine hinzugefügt & kleinere Änderungen |


<br>

## Inhaltsverzeichnis

1. Einleitung
2. Ausgangssituation
   1.  Problemstellung
3. Projektziel und Lösungsansätze
   1. Projektziel
   2. Lösungsansätze 
4. Wirtschaftlicher Nutzen und Bewertung
5. Zielgruppen und Marktpotenzial
6. Kosten und Ressourcen
   1. Kostenplan
   2. Ressourcenplan
7. Vorgehensmodell - Wasserfallmodell
8. GANTT - Diagramm
9.  Risikoanalyse
10. Aufteilung der Arbeitsstunden
11. Quellenverzeichnis

<br>

## 1. Einführung
Es wird im folgenden eine Analyse des Geschäftsszenarios im Hinblick auf die Rentabilität, sowie die Darstellung und Abwägung der erwarteten finanziellen und organisatorischen Umfängen des Projekts beschrieben.

Hierbei wird der Ist-Zustand zu Beginn des Projekts beschrieben, die angestrebten Ziele und Anforderungen ebenso wie mögliche Lösungsansätze. Abschließend werden die wirtschaftlichen Aspekte genannt, genauso wie eine Risikoanalyse.

<br><br>

## 2. Ausgangssituation

### 2.1 Analyse des Ist-Zustandes

Bestehende Datenbanken, die sich mit diesem Themenfeld befassen, sind häufig schwer auffindbar und zudem nicht uneingeschränkt zugänglich. Die enthaltenen Begriffsdefinitionen sind in der Regel nicht standardisiert, wodurch identische Sachverhalte unterschiedlich benannt und Inhalte mehrfach angelegt werden. In der Industrie 4.0 entstehen durch den Einsatz digitaler Zwillinge (Asset Administration Shell, AAS) enorme Datenmengen. Begriffe und Merkmale wie Maßeinheiten oder Materialeigenschaften sollten daher eindeutig und maschinenlesbar definiert sein. Bestehende Lösungen wie IEC-CDD oder ECLASS sind jedoch oft geschlossen, schwer zugänglich und teuer in der Integration.

Das IEC-CDD (Common Data Dictionary) ist ein Allgemeines Datenwörterbuch, dass von der Internationalen Elektronischen Kommission (IEC) verwaltet wird. Dabei umfasst das Repository alle ISO- und IEC-technischen Bereiche. Es werden standardisierte Definitionen für Messgrößen bereitstellt und somit eine gemeinsame Semantik ermöglicht. <sup>[1]</sup>

ECLASS ist hingegen ein branchenübergreifendes Klassifikationssystem zur eindeutigen Beschreibung von Produkten und Dienstleistungen. Es dient als globaler Referenzdatenstandard und ist ISO/IEC-normenkonform, was bedeutet, dass es weltweit angewendet wird. <sup>[2]</sup> ECLASS ermöglicht den digitalen Austausch von Produktstammdaten über verschiedene Branchen, Länder und Sprachen hinweg, was die Effizienz in Einkauf, Warenwirtschaft und Vertrieb steigert. <sup>[3]</sup>

Abschließend lässt sich zusammenfassen, das IEC-CDD und ECLASS  etablierte, aber geschlossene und teilweise kostenpflichtige Standardsysteme für technische und Produktdaten, während das Projekt der Semantischen Wikibase eine offene und frei zugängliche Wissensbasis für Industriebegriffe schaffen soll, die direkt und unkompliziert von Programmen, Maschinen und Anwendern genutzt werden kann.

<br>

### 2.2 Analyse der Problemstellung
Analyse der vorhandenen Probleme:

* Hoher Aufwand für Standardisierung neuer Begriffe
* Fehlende offene, durchsuchbare und verlinkbare Plattform
* Komplexe Lizenzmodelle und eingeschränkte Schnittstellen
* Mangelnde Interoperabilität zwischen Systemen

Diese Faktoren verursachen zusätzliche Integrationskosten, verlängern Entwicklungszeiten und behindern Innovation in datengetriebenen Prozessen.

<br><br>

## 3. Projektziel und Lösungsansätze

### 3.1 Projektziel

Entwicklung einer offenen, kollaborativen und semantisch klaren Wissensbasis („Semantic Wikibase“) zur Beschreibung industrieller Begriffe mit eindeutigen, webbasierten URIs. Ziel ist eine frei nutzbare semantische Infrastruktur für die AAS.


### 3.2 Lösungsansätze

-wird nachgetragen-


<br><br>

## 4. Wirtschaftlicher Nutzen und Bewertung

Direkte Effekte:

* Reduktion des Aufwands für Datenmodellierung und Begriffspflege (geschätzt 20–40 % weniger Zeitbedarf)
* Geringere Lizenz- und Integrationskosten durch offene Plattform
* Schnellere Implementierung neuer digitaler Zwillinge

<br>

Indirekte Effekte:

* Beschleunigung von Standardisierungsprozessen
* Bessere Datenqualität und Rückverfolgbarkeit

<br><br>

## 5. Zielgruppen und Marktpotenzial

* Industrieunternehmen mit AAS-basierten Digitalisierungsstrategien
* Forschungs- und Standardisierungsorganisationen
* Anbieter von Industrie-Software und Plattformen
* Mittelständische Unternehmen, die offene Standards bevorzugen

Ein offenes semantisches Repository kann zum zentralen Infrastrukturbaustein für Industrie 4.0-Ökosysteme werden, ähnlich wie Wikidata für Wissensmanagement im Web.


Bewertung:
Bei Nutzung durch mehrere Unternehmen und Förderprojekten ist der ROI (Return on Investment) bereits innerhalb von 2–3 Jahren realistisch, vor allem durch Wiederverwendung von Begriffen, offene Schnittstellen und Wegfall redundanter Datenpflege.

<br><br>

## 6. Kosten und Ressourcen

### 6.1 Kostenplan


1. **Personalkosten**  
   6 Personen * 80 € pro Stunde * 180 std (für 31 Wochen) = 86.400 € 

2. **Software & Infrastruktur**  
   - Wikibase Installation und Hosting: ca. 5.000 €  
   - Testumgebungen, Server: ca. 3.000 €

3. **Sonstiges (Dokumentation, Puffer)**  
   - ca. 20.000 €

**Gesamtkosten:** ca. **106.408 €**



*Der Plan berücksichtigt den Zeitraum KW 39 bis KW 22 im nächsten Jahr, inklusive der Pause von KW 44 bis KW 47 und dem Meilenstein des ersten Prototyps in KW 48.*


<br>

### 6.2 Ressourcenplan

#### Personal Ressourcen

| Rolle | Anzahl | Aufgaben und Anmerkungen |
|-|-|-|
| Projektleiter | 1 | Projektkoordination, Fortschrittskontrolle |
| Produktmanager | 1 | Anforderungsmanagement, Abnahme, User-Orientierung |
| Testmanager | 1 | Testplanung, Testdurchführung, Qualitätssicherung |
| Systemarchitekt | 1 | Technische Architektur, Infrastrukturplanung |
| Technische Redakteure | 2 | Erstellung technischer Dokumentationen, Nutzeranleitungen |
| Entwickler | alle | Implementierung, Prototypenentwicklung, Tests |

*Alle Teammitglieder sind gleichzeitig in der Rolle des Entwickles. Durch die eingeschränkte Erfahrung im Projektgebiet, werden zeitliche Puffer eingeplant.*

<br>

#### Hardware Ressorcen

Es werden mit den vorhandenen Ressourcen gearbeitet, mit der Voraussetzung, das jeder einen Computer besitzt, mit dem an dem Projekt aktiv mitentwickelt werden kann.

<br>

#### Software Ressourcen

Es wird ausschließlich mit Open Source Software gearbeitet.

* Wikibase-Software als Kernsystem (open source)
* API-Entwicklungswerkzeuge zur Schnittstellenprogrammierung
* Datenbank- und Webserver-Software
* Werkzeuge zur Entwicklung und zum Testen neuer Funktionen

<br>

#### Räumliche Ressourcen

-wird nachgetragen -


<br><br>

## 7. Vorgehensmodell - Wasserfallmodell


| Phase                  | Aufgaben                                   | Zeitraum             | Meilenstein                  |
|------------------------|--------------------------------------------|----------------------|------------------------------|
| Analyse, Planung & Prototypentwicklung | Analyse bestehender Beschreibungen, Projektplanung & Detaildefinition | KW 39 - KW 42 | Abschluss Analyse, Planung &  (KW 42) |
| Designphase | Theoretischer Prototyp fertigen | KW 42 - 43 | Prototypentwicklung (KW 43) |
| Pause | - | KW 44 - KW 47 | - |
| Präsentation des Zwischenstands | - | KW 48 | Präsentation (KW 48) |
| Designphase 2.0 | Ggf. Feedback in Design übernehmen | KW 49 - 51 | Verbessertes Design (KW 51) |
| Entwicklungsphase | Erweiterung API, Implementierung, UI, Entwicklung von Tests für kleinere Module | KW 51 - KW 13 | Prototyp-Erweiterung abgeschlossen (KW 10) |
| Testphase | API- und Systemtests, Bugfixing | KW 13 - KW 16 | Abschluss Tests (KW 16) |
| Abschluss | Dokumentation, Anwenderdokumentation & Abschlusspräsentation | KW 17 - KW 22 | Projektabschluss & Präsentation (KW 22) |

<br><br>

## 8. GANTT - Diagramm

-wird nachgetragen-

<br><br>

## 9. Risikoanalyse

-wird nachgetragen-

<br><br>

## 10. Aufteilung der Arbeitsstunden

Jeder der Mitarbeiter muss ein Soll-Stunden-Konto von insgesamt 180 Stunden absolvieren. Dabei sind die Rollen zu gleichen Teilen aufgeteilt, jeweils 90 Stunden für die spezialisierte Rolle und jeweils 90 Stunden als Entwickler.

||Yvonne Wagner|Kristanna Pfeil|Mariv Igrec|Colin Dietschman|Lucrezia Trabalza|Marina Hidalgo Burova|
|-|-|-|-|-|-|-|
|Anforderungsanalyse|5|15|5|5|5|5|
|Organisation & Kommunikation|15|5|5|5|10|10|
|Projektleitung|20|0|0|0|0|0|
|Recherche|5|15|10|15|10|10|
|Dokumentation|15|15|15|10|35|35|
|Systemarchitektur|0|0|0|25|0|0|
|Programmieren|90|90|90|90|90|90|
|Testen|5|5|30|5|5|5|
|Meetings|10|10|10|10|10|10|
|GitHub Management|10|10|10|10|10|10|
|Präsentation|5|5|5|5|5|5|


## Quellenverzeichnis

| Nummer | Link zur Quelle | Datum |
|-|-|-|
|[1]|https://www.bing.com/search?q=was%20ist%20IEC-CDD&qs=n&form=QBRE&sp=-1&lq=0&pq=was%20ist%20iec-cdd&sc=0-15&sk=&cvid=5F22EEE0E137469FB93BBCE16BE35D02|16.10.2025|
|[2]|https://nexoma.de/eclass/|16.10.2025|
|[3]|https://eclass.eu/eclass-standard/einfuehrung|16.10.2025|