# Benutzeranleitung - Semantic Wikibase

*Dokumentverantwortliche: Technische Redakteure, Lucrezia Trabalza, Marina Hidalgo Burova und Produktmanager, Kristanna Pfeil*

---

## Versionskontrolle 

| Version | Datum | Autor | Kommentar |
|---------|-------|-------|-----------|
| 1.0     | 27.04.2026 | Lucrezia Trabalza | Erstellung & erster Entwurf |


---

## 1. Einleitung

Diese Benutzeranleitung beschreibt die geplante Funktionsweise der Semantic Wikibase sowie die Nutzung und das Testen der API.

Die Plattform dient als zentrale, webbasierte Umgebung zur Verwaltung und Bereitstellung semantischer Definitionen (Concept Descriptions) für die Asset Administration Shell (AAS).

---

## 2. Geplante Funktionsweise der Wikibase 

### 2.1 Ziel der Plattform

Die Semantic Wikibase soll eine offene Plattform bereitstellen, auf der Nutzer semantische Begriffe und Eigenschaften definieren und veröffentlichen können. 

Jeder Begriff erhält eine eindeutige, auflösbare URI, über die er von externen Systemen referenziert werden kann. 

---

### 2.2 Erstellung von Concept Descriptions

Ein Benutzer kann in der Wikibase: 

- neue Begriffe (Concept Descriptions) anlegen
- bestehende Begriffe bearbeiten
- Eigenschaften hinzufügen (z.B. Name, Beschreibung, Einheit)

Jede Concept Description enthält typischerweise:

- **ID / URI**
- **Name (mehrsprachig)**
- **Definition**
- **Datentyp (valueFormat)**
- **Einheit (optional)**
- **Referenzen zu externen Standards (z.B. IEC, ECLASS, QUDT)**

---

### 2.3 Nutzung der Daten

Die gespeicherten Daten können:

- über die Benutzeroberfläche eingesehen werden
- über eine API abgerufen werden
- von AAS-Systemen als semantische Referenz genutzt werden

---

### 2.4 Geplanter Workflow

1. Benutzer erstellt eine Concept Description in der Wikibase
2. Die Wikibase vergibt eine eindeutige ID
3. Diese ID wird als URI veröffentlicht
4. Externe Systeme können die URI verwenden
5. Über die API werden die zugehörigen Daten abgerufen

---

### 2.5 Hinweis zum Projektstand

Im Rahmen des Projekts konnte die vollständige Umsetzung der Plattform nicht realisiert werden.

Die oben beschriebene Funktionsweise stellt das geplante Zielsystem dar und dient als konzeptionelle Grundlage für eine zukünftige Umsetzung.

---

## 3. Lokales Testen der API

### 3.1 Voraussetzungen

Für das lokale Testen der API wird benötigt:

---

### ...

---

## 4. Zusammenfassung

Die Semantic Wikibase bietet eine Grundlage für die Verwaltung und Bereitstellung semantischer Definitionen über das Web. 

...

