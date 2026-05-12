# Business Case

|Dokumentverantwortlicher|Rolle|
|-|-|
|Yvonne Wagner|Projektleiterin|

## Versionskontrolle

| Version | Datum      | Autor       | Kommentar                         |
|-|-|-|-|
| 1.0     | 10.10.2025 | Yvonne Wagner | Erstellung & erster Überblick |
| 1.1 | 16.10.2025 | Yvonne Wagner | Entwurf für Zeitplan, Ressourcenplan, Kostenplan, Aufteilung der Arbeitsstunden, Vorgehensmodell, Meilensteine hinzugefügt & kleinere Änderungen |
|1.2|23.10.2025|Yvonne Wagner|Überarbeitung der Ressourcen- & Kostenplanung|
|1.3|28.10.2025|Yvonne Wagner|Anpassung des Zeitplans, kleine Änderungen & Anpassung der IEC Beschreibung|
|1.4|15.11.2025|Yvonne Wagner|Korrektur des BC nach Absprache mit dem Kunden|


<br>

## Inhaltsverzeichnis

- [Business Case](#business-case)
  - [Versionskontrolle](#versionskontrolle)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [1. Einführung](#1-einführung)
  - [2. Ausgangssituation](#2-ausgangssituation)
  - [3. Projektziel und Lösungsansätze](#3-projektziel-und-lösungsansätze)
  - [4. Wirtschaftlicher Nutzen und Bewertung](#4-wirtschaftlicher-nutzen-und-bewertung)
  - [5. Zielgruppen und Marktpotenzial](#5-zielgruppen-und-marktpotenzial)
  - [6. Ressourcen und Kosten](#6-ressourcen-und-kosten)
    - [6.1 Ressourcenplan](#61-ressourcenplan)
      - [Personal Ressourcen](#personal-ressourcen)
      - [Hardware Ressorcen](#hardware-ressorcen)
      - [Software Ressourcen](#software-ressourcen)
      - [Räumliche Ressourcen](#räumliche-ressourcen)
    - [6.2 Kostenplan](#62-kostenplan)
  - [7. Risikoanalyse](#7-risikoanalyse)
  - [Quellenverzeichnis](#quellenverzeichnis)

<br>

## 1. Einführung
Das Projekt zur Entwicklung einer „Semantic Wikibase“ verfolgt das Ziel, eine einheitliche und optimierte Plattform für die industrielle Nutzung von Begriffen zu schaffen. Durch die Nutzung einer an Wikipedia orientierten Wikibase, werden sowohl Benutzerfreundlichkeit als auch Flexibilität in den Mittelpunkt gestellt. Die Besonderheit liegt in der standardisierten und automatisierten Integration von technischen Maschinenbegriffen nach IEC 61360, wodurch eine eindeutige und digitale Beschreibung industrieller Objekte ermöglicht wird. So entsteht ein offenes, leicht zugängliches Online-Nachschlagewerk, das weltweit die digitale Kommunikation und Zusammenarbeit zwischen Unternehmen und Maschinen erleichtern soll.

Im Folgenden wird der aktuelle Ist-Zustand erläutert, ergänzt durch Kontext- und Begriffserklärungen zur besseren Einordnung des Projekts.

<br><br>

## 2. Ausgangssituation

Bestehende Datenbanken, die sich mit diesem Themenfeld befassen, sind häufig schwer auffindbar und zudem nicht uneingeschränkt zugänglich. Die enthaltenen Begriffsdefinitionen sind in der Regel nicht standardisiert, wodurch identische Sachverhalte unterschiedlich benannt und Inhalte mehrfach angelegt werden. In der Industrie 4.0 entstehen durch den Einsatz digitaler Zwillinge (Asset Administration Shell, AAS) enorme Datenmengen. Begriffe und Merkmale wie Maßeinheiten oder Materialeigenschaften sollten daher eindeutig und maschinenlesbar definiert sein. Bestehende Lösungen wie IEC-CDD oder ECLASS sind jedoch oft geschlossen, schwer zugänglich und teuer in der Integration.

Das IEC-CDD (Common Data Dictionary) ist ein Allgemeines Datenwörterbuch, dass von der Internationalen Elektronischen Kommission (IEC) verwaltet wird. Dabei umfasst das Repository alle ISO- und IEC-technischen Bereiche. Es werden standardisierte Definitionen für Messgrößen bereitstellt und somit eine gemeinsame Semantik ermöglicht.<sup>[1]</sup>

In diesem Kontext ist der Standard IEC-61360 zu betrachten.<sup>[2]</sup> 

ECLASS ist hingegen ein branchenübergreifendes Klassifikationssystem zur eindeutigen Beschreibung von Produkten und Dienstleistungen. Es dient als globaler Referenzdatenstandard und ist ISO/IEC-normenkonform, was bedeutet, dass es weltweit angewendet wird.<sup>[3]</sup> ECLASS ermöglicht den digitalen Austausch von Produktstammdaten über verschiedene Branchen, Länder und Sprachen hinweg, was die Effizienz in Einkauf, Warenwirtschaft und Vertrieb steigert.<sup>[4]</sup>

Abschließend lässt sich zusammenfassen, das IEC-CDD und ECLASS  etablierte, aber geschlossene und teilweise kostenpflichtige Standardsysteme für technische und Produktdaten, während das Projekt der Semantischen Wikibase eine offene und frei zugängliche Wissensbasis für Industriebegriffe schaffen soll, die direkt und unkompliziert von Programmen, Maschinen und Anwendern genutzt werden kann.

Zusammenfassend lassen sich folgende Probleme identifizieren:

* Hoher Aufwand für Standardisierung neuer Begriffe
* Fehlende offene, durchsuchbare und verlinkbare Plattform
* Komplexe Lizenzmodelle und eingeschränkte Schnittstellen
* Mangelnde Interoperabilität zwischen Systemen

Diese Faktoren verursachen zusätzliche Integrationskosten, verlängern Entwicklungszeiten und behindern Innovation in datengetriebenen Prozessen.

<br><br>

## 3. Projektziel und Lösungsansätze

Das Ziel des Projektes wird die Entwicklung einer offenen, kollaborativen und semantisch klaren Wissensbasis („Semantic Wikibase“) zur Beschreibung industrieller Begriffe mit eindeutigen, webbasierten URIs. Ziel ist eine frei nutzbare semantische Infrastruktur für die AAS.

Aufbauend auf die Open-Source Lösung Wikibase, soll die Semantische Wissensdatenbank nach dem Standard IEC-61360 entwickelt werden. Darüber hinaus soll die Lösung "auflösbare URIs", für das AAS-Concept bereitstellen und die automatische Erfassung von neuen Datensätzen aus der AAS Umgebung unterstützen.

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

Ein offenes semantisches Repository kann zum zentralen Infrastrukturbaustein für Industrie 4.0-Ökosystemen werden, ähnlich wie Wikidata für Wissensmanagement im Web. Ebenfalls könnte die Anzahl an potentiellen Kunden steigen durch die erhöhte Nachfrage in der Digitalisierung und Automatisierung von der Produktion.

Bewertung:
Bei Nutzung durch mehrere Unternehmen und Förderprojekten ist der ROI (Return on Investment) bereits innerhalb von 2–3 Jahren realistisch, vor allem durch Wiederverwendung von Begriffen, offene Schnittstellen und Wegfall redundanter Datenpflege.

<br><br>

## 6. Ressourcen und Kosten

Das Projekt der Semantischen Wikibase braucht hauptsächlich Software-Ressorcen, hier werde auf die Open-Source Lösungen wie zum Beispiel die Plattformen Wikibase oder MediaWiki. Die Personelle Kapazität ist für 6 Mitarbeitern angesetzt.

### 6.1 Ressourcenplan

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

Es werden mit den vorhandenen Ressourcen gearbeitet, mit der Voraussetzung, das jeder Mitarbeiter einen Computer besitzt, mit dem an dem Projekt aktiv mitentwickelt werden kann.

* Server & deren Wartung (bestehende Möglichkeit zur Nutzung der kostenlosen Wikibase Cloud)

<br>

#### Software Ressourcen

Es wird ausschließlich mit Open Source Software gearbeitet.

* Wikibase-Software als Kernsystem (open source)
* API-Entwicklungswerkzeuge zur Schnittstellenprogrammierung
* Datenbank- und Webserver-Software
* Werkzeuge zur Entwicklung und zum Testen neuer Funktionen

<br>

#### Räumliche Ressourcen

Es werden lediglich Büroräume für die Entwicklung und anstehende wöchentliche Meetings benötigt.

<br>


### 6.2 Kostenplan



| Kostenbereich                     | Details                           | Betrag (€) |
| --------------------------------- | --------------------------------- | ---------- |
| Personalkosten                    | 6 Personen ×80 €/Stunde ×180 Std. | 86.400     |
| Software & Infrastruktur          | Wikibase Installation und Hosting | 5.000      |
|                                   | Testumgebungen, Server            | 3.000      |
| Sonstiges                         | Arbeitsaufwand für Dokumentation  | 2.000      |
|                                   | Weiterbildungen (pro Person)      | 1.000      |
|                                   | Kosten für zeitlichen Puffer      | 10.000     |
| Büroräume für den Projektzeitraum |                                   | 30.000     |
| Gesamtkosten                      |                                   | 142.400    |


*Der Plan berücksichtigt den Zeitraum KW 39 bis KW 22 im nächsten Jahr, inklusive der Pause von KW 45 bis KW 47 und dem Meilenstein des ersten Prototyps in KW 47.*

Ein Überblick über das Projekt wird in dem Dokument "Projektplan"/PM näher erläutert sowie die Darstellung eines GANTT-Diagramms.

<br><br>


## 7. Risikoanalyse

Im folgenden werden mögliche identifizierte Risiken aufgezählt:

* Abhängigkeit von Open-Source Lösungen, statt eine eigene zu entwickeln
* Systemperformance und Skalierbarkeit
* Datenintegrität
* Schnittstellenprobleme (API)
* Möglicher Missbrauch bei Open Source und frei zugänglichen Daten
* Probleme durch die mangelnde Kommunikation im Team
* Budgetüberschreitung
* Verlust von Open-Source-Lösungen
* Uneinheitliche Terminologien der Begriffe

Die Risiken können im allgemeinen durch genügend Puffer in Arbeitszeit und Budgetkalkulationen minimiert werden.

<br><br>


## Quellenverzeichnis

| Nummer | Link zur Quelle | Datum |
|-|-|-|
|[1]|https://cdd.iec.ch/|28.10.2025|
|[2]|https://cdd.iec.ch/CDD/iec61360/iec61360.nsf/TreeFrameset?OpenFrameSet|28.10.2025|
|[3]|https://nexoma.de/eclass/|16.10.2025|
|[4]|https://eclass.eu/eclass-standard/einfuehrung|16.10.2025|