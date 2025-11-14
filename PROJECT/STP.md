# STP – Software Test Plan

---

## 1. Einleitung
Dieser Software Test Plan (STP) definiert die Teststrategie, den Testumfang, die Testumgebung sowie die Testfälle für das Projekt *Semantic Wikibase*. Ziel ist es, die Qualität der Semantic Facade API, des Wikibase-Datenmodells und des AASX-Importers sicherzustellen.

---

## 2. Teststrategie
- Funktionale Tests (REST-API)
- Integrationstests (Wikibase ↔ Semantic Facade API)
- Systemtests (Docker-Deployment)
- AASX-Importtests (CD/EDS-Verarbeitung)
- Performance-Tests (< 500 ms Antwortzeit)
- Fehlertests (404, 500, invalid input)
