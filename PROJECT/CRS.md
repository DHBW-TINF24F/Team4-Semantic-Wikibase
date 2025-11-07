# Lastenheft

*Dokumentverantwortlicher: Produktmanager, Kristanna Pfeil*

## Versionskontrolle:

| Version | Datum      | Autor       | Kommentar                         |
|-|-|-|-|
| 1.0     | 15.10.2025 | Kristanna Pfeil | Erstellung & erster Entwurf |
| 2.0     | 23.10.2025 | Kristanna Pfeil | Überarbeitung & Ergänzung   |


<br>

## Inhaltsverzeichnis

-  [Konventionen](#konventionen)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [1. Stakeholder](#1-stakeholder)
  - [2. Das Inhaltsverzeichnis](#2-das-inhaltsverzeichnis)
  - [2. Die Versionskontrolle](#2-die-versionskontrolle)
  - [3. Nachtragen von Inhalten](#3-nachtragen-von-inhalten)
  - [4. Der Issue-Tracker](#4-der-issue-tracker)
  - [5. Die Quellenangabe](#5-die-quellenangabe)

<br>

---

Das Lastenheft enthält alle gewünschten Anforderungen vom Kunden (Anforderungen, Stakeholder) für das Projekt "Semantic Wikibase".

---
## 1. Ausgangssituation

In der Asset Administration Shell (AAS) werden Eigenschaften von Submodellen über **Concept Descriptions** beschrieben. Diese verweisen oft auf Inhalte aus **IEC 61360**, **ECLASS** oder anderen Katalogen. Heute sind solche Beschreibungen häufig lokal im AAS-Repository gespeichert, schwer über das Web aufzulösen und nicht einheitlich per API abfragbar. Dadurch ist die Wiederverwendbarkeit begrenzt und Integrationen sind umständlich.

## Projektziel

Es soll ein **webbasierter Prototyp** gebaut werden, der:

- für AAS-Concept Descriptions **auflösbare URIs** bereitstellt,

- eine **einheitliche REST-API** liefert (sprachabhängige Antworten, kompaktes IEC‑61360‑nahes JSON),

- auf **Wikibase** (ähnlich wie Wikidata) als Backend aufsetzt,

- **niedrigschwellig** ist (offene Plattform, einfache Pflege),

- perspektivisch eine **Weiterleitung/Migration** auf etablierte Quellen (IEC‑CDD, ECLASS, QUDT, …) erlaubt.



## 1. Stakeholder


- **Datenschutz-/IT-Sicherheitsbeauftragte**:

- **Externe Datenanbieter**:

- **Studierenden-Team - Entwickler**: möchte ein umsetzbares Projekt mit klaren Anforderungen.

- **Dozenten**: erwarten ein lauffähiges Demo-System, Dokumentation und Präsentation.

- **AAS-Tool-Anwender** (z.B. mit AASX-Explorer): will stabile URIs und einfache API-Antworten für Submodel-Elemente.

- **Domänen-Experten** (z. B. aus Elektrotechnik): wollen korrekte, verständliche Definitionen und Einheiten.

- **Systemintegratoren**: wollen eine **einfache REST-Integration** in bestehende AAS-Server/Services.

- **Community/Offene Daten-Interessierte**: wünscht sich niedrige Einstiegshürden und Governance-Regeln.


---

## 2. Einzelne Stakeholder-Analyse

Wird noch ergänzt


## Anwendungsfälle - Use Cases

**URI-Dereferenzierung**  
Das AAS-Tool nutzt die URI einer Eigenschaft (z.B. Nennspannung) und bekommt direkt alle Basisinfos maschinenlesbar.

**Sprachspezifische Anzeige**  
Der Nutzer kann in der UI „DE“ oder „EN“ auswählen und bekommt das Label/Definition in der jeweiligen Sprache.

**Suche & Detailansicht**  
Der Nutzer sucht nach dem Namen und öffnet eine Detailseite mit Einheit, Datentyp und weiteren Informationen (und Quellenlinks).

**REST‑Abfrage für AAS**  
Ein AAS-Server oder ein Skript fragt `/api/v1/iec61360/{id}?lang=de` ab und bekommt ein schlankes JSON.

**Quellenverweis - vielleicht optional - muss überprüft werden**  
Der Nutzer sieht Links zu IEC‑CDD/ECLASS/QUDT, um die Herkunft zu prüfen.

**Pflege der Datensätze**  
Der Editor kann Beispiel‑Properties anlegen (Label, Definition, Einheit, Datentyp).

## 3. Anforderungen

### 3.1 Funktionale Anforderungen

- **Auflösbare URIs für Konzepte bereitstellen**  
   - Jede Eigenschaft bekommt eine eigene Web-Adresse (URI).
   Wenn diese URL im Browser oder über eine API aufgerufen wird, wird die Beschreibung, der Eigenschaft, angezeigt.

- **REST‑API zum Abrufen von Concept Descriptions**  
   - Es gibt eine Programmierschnittstelle (API), über die man Konzepte abrufen, anlegen, ändern oder löschen kann.
    - Aufruf der URI im Browser zeigt eine kompakte Detailseite; per REST gibt es JSON.


- **Sprachumschaltung**  
    - UI und API liefern Label/Definition abhängig von `lang` (mind. `de`, `en`).  
    - z.B. qudt.org/vocab/unit/V?lang=de
    - Man kann in der UI angeben, in welcher Sprache die Beschreibung gefordert werden soll.


- **Mapping auf IEC61360‑Datentemplate**  
    - Die gespeicherten Konzepte sollen nach dem internationalen Standard IEC 61360 aufgebaut sein.
    - Es gibt feste Felder wie Name, Definition, Datentyp, Einheit usw., damit alles einheitlich beschrieben ist. 
    - `preferredName`, `definition`, `unit`, `datatype`, `identifiers(IRDI)`

- **REST‑API**  
    - `GET /api/v1/iec61360/{id}?lang=xx` liefert kompaktes JSON wie:
        ```json
        {
        "id": "AFD116",
        "preferredName": {"de": "Nennspannung", "en": "rated voltage"},
        "definition": {"de": "Spannung, für die das Gerät ausgelegt ist."},
        "unit": {"id": "QUDT:V", "label": {"de":"Volt","en":"volt"}},
        "datatype": "float",
        "identifiers": {"IRDI": "0112/2///61360_4#AFD116"},
        "seeAlso": ["https://beispiel.org/quelle/AFD116"]
        }
        ```
        genaueres siehe in Projekt 1 abgebildete JSON-Datei.

- **Admin‑/Edit‑Workflow**  
    - Einfaches Erfassen/Anpassen von Beispiel‑Einträgen in Wikibase (kein komplexes Rechtesystem im MVP).
    -  Die Plattform soll offen und leicht nutzbar sein – ähnlich wie Wikipedia.
    - Jeder soll Konzepte suchen und eintragen können, ohne komplizierte Hürden oder teure Lizenzen.
    

- **Verlinkung externen Quellen**  
    - Detailansicht zeigt klickbare Links (z. B. IEC‑CDD, ECLASS, QUDT), ohne deren Inhalte zu kopieren.
    - So bleibt die Verbindung zu bestehenden Normen erhalten, auch wenn das Konzept in der Wikibase gespeichert ist.

- **Import/Export / Integration mit AAS**  
    - Die Wikibase soll mit der Asset Administration Shell (AAS) zusammenarbeiten.
    - Das heißt: AAS-Daten (z.B. aus einer AASX-Datei) können importiert oder verknüpft werden.
    - Damit können AAS-Tools direkt auf die semantischen Konzepte zugreifen.
    

- **Leichte Spezifikation & Governance**
    - Es soll einfache Regeln und Vorgaben geben, wie ein Konzept aufgebaut sein muss.
    - Zum Beispiel: Jedes Konzept braucht einen Namen, eine kurze Definition, eine Sprache, einen Datentyp und eine Quelle.
    So bleibt alles übersichtlich und nachvollziehbar.



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

- Open‑Source‑kompatible Komponenten (Wikibase).

- Datenschutz: keine personenbezogenen Daten.

- Nur Inhalte nutzen, die wir modellieren/entscheiden dürfen (Beispieldaten selbst erstellt oder auf frei nutzbare Quellen verlinken).

## Skizzen der UI
 
 


## Geschäftsvorfälle, ...