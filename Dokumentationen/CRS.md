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
   - Jedes Konzept (also z. B. ein Merkmal oder eine Eigenschaft) bekommt eine eigene Web-Adresse (URL).
   Wenn man diese URL im Browser oder über eine API aufruft, sieht man die Beschreibung des Konzepts.

- REST‑API zum Abrufen von Concept Descriptions:  
   - Es gibt eine Programmierschnittstelle (API), über die man Konzepte abrufen, anlegen, ändern oder löschen kann.
    - Die Daten werden als JSON geliefert, damit andere Systeme sie leicht nutzen können. (Vermutlich - bin ich mir noch nicht sicher)



- Mehrsprachigkeit:  
   - Alle Konzepte sollen mindestens auf Deutsch und Englisch verfügbar sein.
    - Man kann also in der API angeben, in welcher Sprache die Beschreibung geliefert werden soll.


- Mapping auf IEC61360‑Datentemplate:  
    - Die gespeicherten Konzepte sollen nach dem internationalen Standard IEC 61360 aufgebaut sein. (wird nochmnal genau überprüft welches Standard)
    - Das bedeutet: Es gibt feste Felder wie Name, Definition, Datentyp, Einheit usw., damit alles einheitlich beschrieben ist.

- Import/Export / Integration mit AAS:  
    - Die Wikibase soll mit der Asset Administration Shell (AAS) zusammenarbeiten.
    - Das heißt: AAS-Daten (z. B. aus einer AASX-Datei) können importiert oder verknüpft werden.
    - Damit können AAS-Tools direkt auf die semantischen Konzepte zugreifen.

- Verlinkung zu externen Standards:  
    - Ein Konzept kann auf andere Standards verweisen, zum Beispiel auf ECLASS, IEC-CDD oder QUDT.
    - So bleibt die Verbindung zu bestehenden Normen erhalten, auch wenn das Konzept in der Wikibase gespeichert ist.


- Niedrigschwelliger Zugang / offene Plattform (Wiki‑Ansatz):
    -  Die Plattform soll offen und leicht nutzbar sein – ähnlich wie Wikipedia.
    - Jeder soll Konzepte suchen und eintragen können, ohne komplizierte Hürden oder teure Lizenzen.

- Leichte Spezifikation & Governance:
    - Es soll einfache Regeln und Vorgaben geben, wie ein Konzept aufgebaut sein muss.
    - Zum Beispiel: Jedes Konzept braucht einen Namen, eine kurze Definition, eine Sprache, einen Datentyp und eine Quelle.
    So bleibt alles übersichtlich und nachvollziehbar.


- Wikibase‑Konfigurationen / Workflow‑Definition:

    - Die Wikibase wird technisch so eingerichtet, dass sie diesen Ablauf unterstützt:
    z. B. bestimmte Eingabefelder, Pflichtangaben, Validierungen und Workflows (z. B. Entwurf → Review → Freigabe).




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

