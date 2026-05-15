# Begriffs Erklärungen

Dieses Dokument dient dazu Fachspezifische Begriffe, Methoden und Technologien zu erläutern.


## AAS

**AAS** steht für **Asset Administration Shell** („Verwaltungsschale“):

- Das ist das digitale „Datenblatt“ oder der „Steckbrief“ eines physischen Objekts (z.B. Maschine, Bauteil).
- Die AAS sammelt und verwaltet alle Daten über ein Asset, damit Computer diese Informationen automatisch nutzen können.
- Sie ist ein zentrales Konzept in der Industrie 4.0 und macht aus jedem Ding einen digitalen Zwilling.

Die Asset Administration Shell (AAS) ist sozusagen der digitale Zwilling eines physischen oder virtuellen Assets. Also z. B. einer Maschine, eines Motors, eines Sensors oder sogar einer Software.

---

## Asset

Ein "Asset" ist alles, was einen Wert hat:
- eine Maschine, ein Sensor, ein Produkt,
- aber auch Software, Daten, Dienstleistungen oder Materialien.

Die AAS beschreibt dieses Asset vollständig in digitaler Form, mit Daten, Funktionen und Bedeutung (Semantik).

## Submodell

Damit man die Informationen über ein Asset strukturiert darstellen kann, wird die AAS in mehrere Submodelle aufgeteilt, die bestimmte Themenbereiche beschreiben, z. B.:

| **Beispiel-Submodell** | **Beschreibung** |
|--------------------------|------------------|
| Technische Daten | Spannung, Leistung, Gewicht usw. |
| Wartung | Wartungszyklen, Servicehistorie |
| Zustandsüberwachung | Temperatur, Laufzeit, Fehlercodes |
| Verwaltung | Seriennummer, Hersteller, Lebenszyklus |

Jedes Submodell enthält mehrere Submodel Elements.
Die Idee ist, dass nicht jedes System alle Daten braucht, sondern nur bestimmte Submodelle.

Beispiel:

- Ein Wartungssystem ruft nur das Wartungs-Submodell ab.

- Ein Monitoring-System interessiert sich nur für das Zustands-Submodell.

- Ein Einkaufs- oder ERP-System nutzt das Verwaltungs-Submodell.

Dadurch ist die AAS modular, erweiterbar und interoperabel – also perfekt für Industrie 4.0.

## Submodel Elements

Ein Submodel Element ist das kleinste Informations- oder Funktionsbaustein in einem Submodell.
Es stellt eine konkrete Eigenschaft, Messung, Datei, Beziehung oder Funktion dar.


Beispiel:
Submodell: „Technische Daten“
→ Submodel Elements:

- Nennspannung = 230 V

- Leistung = 2 kW

- Seriennummer = „MTR-2025-07“

- Hersteller = „Siemens AG“

Jedes dieser Dinge ist ein Submodel Element.


Damit Maschinen wissen, was ein Submodel Element bedeutet (nicht nur wie es heißt), wird es semantisch beschrieben – und da kommen Concept Descriptions ins Spiel.

## Concept Description (CD)

Eine Concept Description beschreibt die Bedeutung eines Submodel Elements.
Sie legt also fest, was genau z. B. „Leistung“ oder „Nennspannung“ heißt, in welcher Einheit sie angegeben wird usw.

Jede Concept Description verweist auf eine Data Specification — meist nach IEC 61360.

## IEC 61360 – Data Specification

Die **IEC 61360** ist eine internationale Norm, die beschreibt, wie technische Eigenschaften **standardisiert definiert** werden.

**Beispiel:**  
Eigenschaft: *Nennspannung*

| **Feld** | **Bedeutung** | **Beispiel** |
|-----------|----------------|---------------|
| Preferred Name | Bezeichnung | Nennspannung |
| Definition | Beschreibung | Spannung, für die ein Gerät ausgelegt ist |
| Einheit | Einheit | Volt (V) |
| Datentyp | Datentyp | Float |
| ID | Eindeutige Kennung | 0112/2///61360_4#AAA123#001 |

## URI

Eine URI steht für Uniform Resource Identifier und ist ein eindeutiger Bezeichner für eine Ressource im Internet oder in einem Informationssystem.
Sie dient also dazu, etwas eindeutig zu identifizieren oder zu adressieren, egal ob es sich um eine Webseite, ein Dokument, ein Datenelement oder z. B. eine semantische Definition handelt.

URL und URN sind Unterarten einer URI.