# Lastenheft

*Dokumentverantwortlicher: Produktmanager, Kristanna Pfeil*

## Versionskontrolle:

| Version | Datum      | Autor       | Kommentar                         |
|-|-|-|-|
| 1.0     | 15.10.2025 | Kristanna Pfeil | Erstellung & erster Entwurf |


<br>

## Inhaltsverzeichnis

1. ...

<br>

---

Das Lastenheft enthält alle gewünschten Anforderungen vom Kunden (Anforderungen, Stakeholder) für das Projekt "Semantic Wikibase".

---

## 1. Stakeholder

- Entwickler
- Datenschutz-/IT-Sicherheitsbeauftragte
- AAS-Plattform-Betreiber (z. B. Eclipse BaSyx)
- Endnutzer
- Externe Datenanbieter


---

## 2. Einzelne Stakeholder-Analyse

Wird noch ergänzt


## 3. Anforderungen

### 3.1 Funktionale Anforderungen


- Auflösbare URIs für Konzepte bereitstellen:  
   - Jeder Begriff hat eine eigene URL, die man im Browser oder per API aufrufen kann.  
   - Akzeptanzkriterium: Aufruf von /concept/{id} liefert die Beschreibung.

- REST‑API zum Abrufen von Concept Descriptions:  
   - GET /concept/{id}?lang=de|en liefert die Daten in IEC61360‑ähnlichem JSON.  
   - Akzeptanzkriterium: API gibt für ein Beispiel‑Item validen JSON‑Output zurück.



- Mehrsprachigkeit:  
   - Labels/Definitionen mindestens in de und en möglich.  
   - Akzeptanzkriterium: ?lang=de liefert deutsche Strings, ?lang=en englische.


- Mapping auf IEC61360‑Datentemplate:  
   - API liefert Felder wie preferredName, definition, dataType, unit, valueFormat.  
   - Akzeptanzkriterium: Beispiel‑Item zeigt alle relevanten IEC61360‑Felder.

- Import/Export / Integration mit AAS:  
   - Import von AASX oder Abgleich mit AAS‑Servern testen.  
   - Akzeptanzkriterium: Ein AASX‑Beispiel kann Daten einlesen / referenzieren.

- Verlinkung zu externen Standards:  
    - Möglichkeit, Referenzen/Redirects zu ECLASS/IEC/QUDT zu speichern.  
    - Akzeptanzkriterium: Item enthält externen Link / IRDI‑Referenz.


- Niedrigschwelliger Zugang / offene Plattform (Wiki‑Ansatz):
    -  Bedeutung: Jeder kann semantische Definitionen erstellen oder finden, ähnlich wie Wikipedia/Wikibase.

- Leichte Spezifikation & Governance:
    - Bedeutung: Eine kurze, klare Anleitung (z. B. „Registry of Semantics“), die festlegt, welche Informationen ein Begriff mindestens enthalten muss (z. B. Name, Kurzdefinition, Sprache, Datentyp, Einheit, Quelle), wie Einträge dokumentiert und versioniert werden.


- Wikibase‑Konfigurationen / Workflow‑Definition:

    - Bedeutung: Technische Umsetzung der Regeln in Wikibase: vordefinierte Eingabeformulare, Properties (z. B. preferredName, definition, dataType, unit), Pflichtfelder und Validierungsregeln.




### 3.2 Nicht-funktionale Anforderungen (NFR)

- Verfügbarkeit / Stabilität  
   - Dienst sollte für Demo/Tests verfügbar sein.

- Performance / Latenz  
   - API‑Antwortzeiten sollten nicht übermäßig lang brauchen.

- Sicherheit  
   - Schreibaktionen geschützt, sensible Daten nicht öffentlich.  

- Datenpersistenz & Versionierung  
   - Änderungen versioniert und nachvollziehbar (z.B. Wer, wann, was).  
   - Akzeptanzkriterium: Historie für Item ist sichtbar.

- Usability  
   - Einfaches Eingabeformular, Pflichtfelder markiert.

- Internationalisierung  
    - UI und Fehlermeldungen mehrsprachig (de/en).  

- Wartbarkeit / Codequalität  
    - klar strukturierter Code, README + Deployment‑Anleitung.

### 3.3 Randbedingungen

Wird noch ergänzt

