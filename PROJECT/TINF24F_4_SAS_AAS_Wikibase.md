# Software Architecture Specification (SAS)
## Semantic Wikibase – AAS Concept Description API & Sucherweiterung

---

| Dokument-ID   | SAS_AAS_Wikibase                                  |
|---------------|---------------------------------------------------|
| Version       | 1.1                                               |
| Datum         | 08.05.2026                                        |
| Autor         | GitHub Copilot Agent (Senior Software Architekt)  |
| Basis         | IEEE 1471-2000 / ISO/IEC/IEEE 42010               |
| Repository    | DHBW-TINF24F/Team4-Semantic-Wikibase              |

---

## Versionskontrolle

| Version | Datum      | Autor                              | Kommentar                |
|---------|------------|------------------------------------|--------------------------|
| 1.0     | 08.05.2026 | GitHub Copilot (Architekturanalyse) | Erstversion auf Basis der Repository-Analyse |
| 1.1     | 15.05.2026 | Team 4 | Überarbeitung der API-Architektur, Kürzung doppelter Mapper-Beschreibungen und Verweis auf die Moduldokumentation |

---

## Inhaltsverzeichnis

1. [Einleitung & Vision](#1-einleitung--vision)
2. [Systemübersicht](#2-systemübersicht)
3. [API-Architektur und Gateway-Konzept](#3-api-architektur-und-gateway-konzept)
   - 3.1 [Rolle der API-Architektur](#31-rolle-der-api-architektur)
   - 3.2 [API-Gateway und Einzel-APIs](#32-api-gateway-und-einzel-apis)
   - 3.3 [Datenfluss der API](#33-datenfluss-der-api)
   - 3.4 [Abgrenzung zur Moduldokumentation](#34-abgrenzung-zur-moduldokumentation)
   - 3.5 [Zugriffskontrolle und Sicherheit auf API-Ebene](#35-zugriffskontrolle-und-sicherheit-auf-api-ebene)
4. [Such-Architektur](#4-such-architektur)
   - 4.1 [CirrusSearch vs. FacettedSearch](#41-cirrussearch-vs-facettedsearch)
   - 4.2 [Begründung der Wahl](#42-begründung-der-wahl)
   - 4.3 [UX-Optimierungen auf der Startseite](#43-ux-optimierungen-auf-der-startseite)
5. [Datenmodell](#5-datenmodell)
   - 5.1 [Interner Speicher in Wikibase](#51-interner-speicher-in-wikibase)
   - 5.2 [Externe Repräsentation als AAS Concept Description](#52-externe-repräsentation-als-aas-concept-description)
   - 5.3 [Datenquellen und Source-Mapping](#53-datenquellen-und-source-mapping)
6. [Nicht-funktionale Anforderungen](#6-nicht-funktionale-anforderungen)
   - 6.1 [Skalierbarkeit der Suche](#61-skalierbarkeit-der-suche)
   - 6.2 [Sicherheit der API](#62-sicherheit-der-api)
7. [Zusammenfassung und Ausblick](#7-zusammenfassung-und-ausblick)

---

## 1. Einleitung & Vision

### 1.1 Hintergrund und Problemstellung

Im Kontext der Industrie 4.0 und des Industrial Internet of Things (IIoT) werden physische Assets zunehmend durch digitale Zwillinge beschrieben. Die **Asset Administration Shell (AAS)** ist das standardisierte digitale Äquivalent eines Industrie-Assets gemäß der IDTA-Spezifikation. In jedem AAS-Submodell werden Eigenschaften (Submodel Elements) durch **Concept Descriptions (CDs)** semantisch beschrieben. Eine CD verweist dabei auf eine externe Semantikquelle – typischerweise eine URI, die auf einen Eintrag in Registern wie IEC CDD, ECLASS oder QUDT zeigt.

Die aktuell verfügbaren Systeme für Concept Descriptions leiden unter erheblichen Einschränkungen:

- **IEC CDD** und **ECLASS** sind geschlossene, kostenpflichtige Systeme mit komplexen Lizenzmodellen
- Concept Descriptions sind oft lokal in AAS-Repositories gespeichert und damit nicht universell auflösbar
- Bestehende Plattformen bieten keine nutzerfreundliche Oberfläche für die Pflege von Einträgen
- REST-APIs für die maschinenlesbare Abfrage von IEC 61360-konformen Daten fehlen oder sind unzureichend standardisiert

### 1.2 Vision des Projekts

Das Projekt **Semantic Wikibase** verfolgt die Vision, eine offene, kollaborative Wissensdatenbank für industrielle Semantic IDs und Concept Descriptions zu schaffen. Angelehnt an das Wikidata/Wikibase-Ökosystem entsteht eine Plattform, die:

- **Auflösbare, persistente URIs** für jede Concept Description bereitstellt (z. B. `https://semanticid.aas-connect.com/id/Q21`)
- Eine **REST-API** anbietet, die semantische Definitionen in IEC 61360-konformer JSON-Struktur zurückgibt
- **Mehrsprachigkeit** nativ unterstützt (deutsch, englisch und weitere Sprachen)
- **Offen und kollaborativ** ist – jeder kann Einträge erstellen, prüfen und verbessern
- Als **Brücke zu externen Ontologien** dient, insbesondere zu QUDT (Quantities, Units, Dimensions and Types), VEC (Vehicle Electric Container) und KBL (Kabelbaumleitung)
- Eine **AAS-konforme Schnittstelle** bietet, sodass AAS-Tools wie der AASX-Explorer Concept Descriptions direkt auflösen können

### 1.3 Zweck dieses Dokuments

Diese Software Architecture Specification (SAS) beschreibt auf Basis von IEEE 1471-2000 die übergeordnete Softwarearchitektur der Semantic Wikibase Plattform. Der Fokus liegt dabei auf dem Zusammenspiel der zentralen Systemkomponenten, der API-Gateway-Struktur, der Wikibase-Integration sowie den nicht-funktionalen Anforderungen.

Die detaillierte Beschreibung einzelner APIs, Mapper und Mapping-Regeln wird bewusst nicht vollständig im SAS wiederholt, sondern in der Moduldokumentation (MOD) beschrieben. Dadurch bleibt das SAS auf die Gesamtarchitektur fokussiert, während das MOD die konkrete Modul- und Implementierungsebene dokumentiert.

Dieses Dokument beschreibt insbesondere:

1. Die Gesamtarchitektur der Semantic Wikibase
2. Das Zusammenspiel zwischen API-Gateway, Einzel-APIs, Mappern und Wikibase
3. Die Such-Architektur der Wikibase-Erweiterung
4. Das interne und externe Datenmodell auf Architekturebene
5. Nicht-funktionale Anforderungen bezüglich Sicherheit, Skalierbarkeit und Betrieb

---

## 2. Systemübersicht

### 2.1 High-Level-Architektur

Das System besteht aus vier logischen Schichten, die miteinander interagieren:

```
┌─────────────────────────────────────────────────────────────────┐
│                        EXTERNE CLIENTS                          │
│   AASX-Explorer │ AAS-Backends │ Entwickler │ Browser-Nutzer   │
└──────────┬──────────────┬──────────────┬──────────────┬────────┘
           │ REST-API     │ OpenAPI      │ Wikibase UI  │ SPARQL
           ▼              ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   API-GATEWAY / FACADE                          │
│                                                                 │
│  ┌──────────────────────┐   ┌──────────────────────────────┐   │
│  │  FastAPI / Flask     │   │  Wikibase MediaWiki REST API │   │
│  │  (api_qudt.py /      │   │  (Wikibase Extension)        │   │
│  │   api_v3_blueprint)  │   │                              │   │
│  └──────────┬───────────┘   └──────────────┬───────────────┘   │
└─────────────┼──────────────────────────────┼────────────────────┘
              │                              │
              ▼                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   TRANSFORMATIONSSCHICHT                         │
│                                                                 │
│  ┌───────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ QUDT Service  │  │ KBL Mapper   │  │ VEC Mapper         │   │
│  │ (qudt_service)│  │(kbl_xsd_     │  │(vec_var_API.py)    │   │
│  │               │  │  mapper.py)  │  │                    │   │
│  └───────┬───────┘  └──────┬───────┘  └────────┬───────────┘   │
└──────────┼────────────────┼──────────────────┼─────────────────┘
           │                │                  │
           ▼                ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                   EXTERNE DATENQUELLEN                           │
│                                                                 │
│  ┌─────────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  QUDT Fuseki    │  │  KBL XSD     │  │  VEC Ontologie   │   │
│  │  SPARQL Endpoint│  │  (prostep.io)│  │  (TTL/RDF/OWL)   │   │
│  │  (qudt.org)     │  │              │  │                  │   │
│  └─────────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WIKIBASE (PERSISTENZ)                         │
│                                                                 │
│   MediaWiki + Wikibase Extension + Blazegraph/WDQS SPARQL      │
│   Concept Description Items (QIDs), Properties, Statements      │
│   Pretty URIs: https://semanticid.aas-connect.com/id/Q{n}       │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Komponentenbeschreibung

Die folgende Tabelle beschreibt die zentralen Architekturkomponenten der Semantic Wikibase. Während das SAS die Rolle der Komponenten im Gesamtsystem beschreibt, werden die einzelnen Mapper, APIs und Mapping-Regeln in der Moduldokumentation detailliert erläutert.

| Komponente | Technologie | Zweck | Detailbeschreibung |
|---|---|---|---|
| **API-Gateway / Facade** | Python, FastAPI / Flask | Zentrale Schnittstelle für externe Clients. Nimmt Anfragen entgegen und leitet diese an die passende Einzel-API bzw. den passenden Mapper weiter. | [MOD Kapitel 3.2](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#32-abgrenzung-zwischen-api-gateway-und-einzel-apis) |
| **QUDT-API** | Python 3, FastAPI / Flask | Stellt REST-Endpunkte für QUDT-Abfragen bereit und ermöglicht das Mapping von QUDT-Daten auf das gemeinsame Zielmodell. | [MOD Kapitel 1](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#1-openapi-spezifikation), [MOD Kapitel 4.1](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#41-qudt) |
| **QUDT-Mapper** | Python 3, `rdflib`, SPARQL | Verarbeitet QUDT-Daten aus RDF-, TTL- oder SPARQL-Quellen und überführt sie in das IEC61360-nahe Zielmodell. | [MOD Kapitel 4.1](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#41-qudt) |
| **VEC-Mapper** | Python 3, `rdflib` | Verarbeitet die VEC-Ontologie auf Basis von RDF/OWL/TTL und erstellt daraus ConceptDescriptions. | [MOD Kapitel 4.2](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#42-vec) |
| **KBL-Mapper** | Python 3, `requests`, XML/XSD | Analysiert KBL-XSD-Strukturen und bildet Elemente, Typen, Attribute und Enumerationen auf das Zielmodell ab. | [MOD Kapitel 4.3](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#43-kbl) |
| **Gemeinsames Zielmodell** | JSON, IEC61360-nahes Datenmodell | Vereinheitlicht die Ausgaben aller angebundenen Datenquellen. | [MOD Kapitel 5](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#5-gemeinsames-mapping-über-alle-quellen), [MOD Kapitel 6](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#6-gemeinsames-zielmodell) |
| **Wikibase** | MediaWiki, Wikibase Extension | Dient als zentrale Plattform zur Verwaltung und Bereitstellung semantischer Definitionen. | [MOD Kapitel 7](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#7-wikibase-datenstruktur-und-ablage-der-gemappten-informationen), [MOD Kapitel 9](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#9-wikibase-integration) |
| **SPARQL Endpoint** | Blazegraph / WDQS | Ermöglicht RDF-Abfragen auf Wikibase-Daten und unterstützt semantische Such- und Integrationsszenarien. | [MOD Kapitel 9](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#9-wikibase-integration) |
| **Reverse Proxy / Routing** | Nginx / Traefik | Zuständig für Pretty URIs, Routing und perspektivisch SSL-Terminierung. | [MOD Kapitel 9](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#9-wikibase-integration) |

---

## 3. API-Architektur und Gateway-Konzept

### 3.1 Rolle der API-Architektur

Die API-Architektur der Semantic Wikibase dient als Vermittlungsschicht zwischen externen Clients, den angebundenen Datenquellen und der Wikibase. Externe Systeme wie AAS-Clients, Entwicklerwerkzeuge oder Benutzeroberflächen sollen semantische Definitionen über REST-Endpunkte abrufen können, ohne die internen Datenquellen direkt ansprechen zu müssen.

Im aktuellen Projektstand stehen vor allem folgende Aufgaben im Fokus:

- Entgegennahme von Suchanfragen über REST-Endpunkte
- Weiterleitung an passende Einzel-APIs bzw. Mapper
- Verarbeitung externer Datenquellen wie QUDT, VEC und KBL
- Transformation der Quelldaten in ein gemeinsames IEC61360-nahes JSON-Zielmodell
- Bereitstellung der Ergebnisse für API-Clients und perspektivisch für die Ablage in Wikibase

Die detaillierte Beschreibung der einzelnen APIs, Mapper und Mapping-Regeln befindet sich in der Moduldokumentation.

Siehe hierzu:
- [MOD Kapitel 3: Architektur der API](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#3-architektur-der-api)
- [MOD Kapitel 4: Datenquellen und Mappings](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#4-datenquellen-und-mappings)
- [MOD Kapitel 5: Gemeinsames Mapping über alle Quellen](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#5-gemeinsames-mapping-über-alle-quellen)

---

### 3.2 API-Gateway und Einzel-APIs

Die Architektur unterscheidet zwischen einer zentralen Gateway-API und mehreren fachlichen Einzel-APIs bzw. Mappern.

Das API-Gateway fungiert als zentrale Einstiegsschicht. Es nimmt Anfragen von externen Clients entgegen und entscheidet anhand der Anfrageparameter, welche Datenquelle bzw. welches Mapping-Modul verwendet werden soll. Dadurch müssen externe Systeme nicht wissen, ob die angefragten Informationen aus QUDT, VEC oder KBL stammen.

Die Einzel-APIs und Mapper übernehmen die konkrete Verarbeitung der jeweiligen Quelle:

| Komponente | Aufgabe |
|---|---|
| API-Gateway | Zentrale Annahme und Weiterleitung von Anfragen |
| QUDT-API / QUDT-Mapper | Verarbeitung von QUDT-Daten wie Einheiten, Symbolen und QuantityKinds |
| VEC-API / VEC-Mapper | Verarbeitung der VEC-Ontologie auf Basis von RDF/OWL/TTL |
| KBL-API / KBL-Mapper | Verarbeitung von KBL-XSD-Strukturen |
| Gemeinsames Zielmodell | Vereinheitlichung der Ergebnisse im IEC61360-nahen JSON-Format |
| Wikibase | Persistente Verwaltung und Bereitstellung semantischer Definitionen |

Diese Trennung unterstützt eine modulare Erweiterung der Plattform. Neue Datenquellen können ergänzt werden, ohne die gesamte API-Struktur neu aufzubauen.

---

### 3.3 Datenfluss der API

Der grundlegende Datenfluss sieht wie folgt aus:

```
Externer Client
      |
      v
API-Gateway
      |
      v
Auswahl der passenden Einzel-API / des passenden Mappers
      |
      v
Abruf und Analyse der externen Datenquelle
      |
      v
Transformation in das gemeinsame IEC61360-nahe Zielmodell
      |
      v
JSON-Antwort an Client / perspektivische Ablage in Wikibase
```

Beispielhaft kann eine Anfrage nach einer Einheit wie `Volt` über das Gateway verarbeitet und an die QUDT-API weitergeleitet werden. Der QUDT-Mapper extrahiert relevante RDF-Properties und erzeugt daraus eine ConceptDescription im gemeinsamen Zielmodell.

Für VEC und KBL erfolgt derselbe Ablauf, jedoch mit anderen Quellformaten. VEC basiert auf RDF/OWL/TTL, während KBL auf XML/XSD-Strukturen basiert.

---

### 3.4 Abgrenzung zur Moduldokumentation

Dieses SAS beschreibt die übergeordnete Architektur, die beteiligten Komponenten und deren Zusammenspiel. Die konkrete technische Umsetzung einzelner Mapper, die detaillierten Mapping-Tabellen und die Behandlung einzelner IEC61360-Felder werden nicht im SAS wiederholt, sondern in der Moduldokumentation beschrieben.

Dadurch wird eine klare Trennung erreicht:

| Dokument | Fokus |
|---|---|
| SAS | Gesamtarchitektur, Komponenten, Datenfluss, Schnittstellen, Qualitätsaspekte |
| MOD | Einzelmodule, Mapper, Mapping-Regeln, Zielmodell, Modultests |

Die detaillierten Modulbeschreibungen befinden sich in:

- [MOD Kapitel 4.1 QUDT](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#41-qudt)
- [MOD Kapitel 4.2 VEC](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#42-vec)
- [MOD Kapitel 4.3 KBL](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#43-kbl)
- [MOD Kapitel 12 Tests der Module](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#12-tests-der-module)

---

### 3.5 Zugriffskontrolle und Sicherheit auf API-Ebene

Die aktuelle API-Implementierung ist primär für Entwicklungs- und Demonstrationszwecke vorgesehen. Für einen produktiven Betrieb ist ein rollenbasiertes Zugriffskonzept geplant.

Grundsätzlich werden folgende Rollen betrachtet:

| Rolle | Rechte | Beschreibung |
|---|---|---|
| Anonymer Nutzer | Lesen | Kann veröffentlichte ConceptDescriptions abrufen |
| Angemeldeter Nutzer | Lesen und Erstellen | Kann neue Einträge anlegen |
| Editor / Kurator | Lesen, Schreiben und Pflegen | Kann Einträge bearbeiten und kuratieren |
| Administrator | Vollzugriff | Verwaltet System, Benutzer und Rechte |
| API-Dienst | Maschineller Zugriff | Greift über Token oder API-Key auf REST-Endpunkte zu |

Für die produktive Nutzung sind zusätzlich Authentifizierung, Autorisierung, Rate Limiting, CORS-Einschränkungen und TLS-Absicherung vorzusehen.

---

## 4. Such-Architektur

### 4.1 CirrusSearch vs. FacettedSearch

Die Wikibase-Erweiterung unterstützt mehrere Suchmechanismen, die sich in ihrer technischen Grundlage und ihren Anwendungsfällen unterscheiden.

#### 4.1.1 CirrusSearch

**CirrusSearch** ist die Standard-Suchmaschine von MediaWiki/Wikibase, basierend auf **Elasticsearch**. Sie ermöglicht Volltextsuche über alle Wiki-Seiten und Wikibase-Items.

| Merkmal | Beschreibung |
|---------|--------------|
| **Technologie** | Elasticsearch (über MediaWiki-Extension) |
| **Indexierung** | Automatische Volltext-Indizierung aller Item-Labels und Beschreibungen |
| **Suche** | Fuzzy-Suche, Phrase-Suche, Wildcard-Suche |
| **Sprachunterstützung** | Mehrsprachige Analyzer via Elasticsearch |
| **Integration** | Native MediaWiki-Integration, wird von Wikibase-Suche verwendet |
| **Skalierbarkeit** | Horizontal skalierbar über Elasticsearch-Cluster |
| **Stärken** | Robuste Volltextsuche, bewährt in Wikidata-Produktion |
| **Schwächen** | Konfigurationsaufwand, kein natives Facettenfiltering für Wikibase-Properties |

**Konfigurationsbeispiel** (MediaWiki `LocalSettings.php`):
```php
wfLoadExtension( 'CirrusSearch' );
wfLoadExtension( 'Elastica' );
$wgSearchType = 'CirrusSearch';
$wgCirrusSearchServers = [ 'elasticsearch' ];
```

#### 4.1.2 FacettedSearch

**FacettedSearch** (auch als `Special:Search` mit Filtererweiterungen oder dedizierte MediaWiki-Erweiterungen wie `SemanticMediaWiki`) erlaubt die Suche mit strukturierten Filtern basierend auf Wikibase-Properties.

| Merkmal | Beschreibung |
|---------|--------------|
| **Technologie** | MediaWiki-Extension oder SPARQL-basiertes Filtering |
| **Filterung** | Nach Wikibase-Properties (z. B. `dataType = unit`, `sourceSystem = QUDT`) |
| **Suche** | Strukturierte Suche über Property-Werte |
| **Sprachunterstützung** | Über Property-Werte konfigurierbar |
| **Integration** | Erfordert separate Extension-Konfiguration |
| **Skalierbarkeit** | Abhängig von SPARQL-Endpunkt-Performance |
| **Stärken** | Semantisches Filtering, für strukturierte Daten ideal |
| **Schwächen** | Höhere Implementierungskomplexität, SPARQL-Kenntnisse notwendig |

### 4.2 Begründung der Wahl

Für das Semantic Wikibase-Projekt wird **CirrusSearch in Kombination mit einer spezifischen Wikibase-Property-Suche** empfohlen. Die Entscheidung basiert auf folgenden Kriterien:

| Kriterium | CirrusSearch | FacettedSearch | Gewichtung |
|-----------|:---:|:---:|:---:|
| Volltext über Labels & Beschreibungen | ✅ | ⚠️ | Hoch |
| Mehrsprachige Suche | ✅ | ✅ | Hoch |
| Semantic ID (URI-Suche) | ⚠️ | ✅ | Sehr hoch |
| Property-basiertes Filtern | ⚠️ | ✅ | Mittel |
| Wikibase-native Integration | ✅ | ⚠️ | Hoch |
| Deploymentaufwand | Gering | Mittel-Hoch | Mittel |
| Community-Support | Sehr hoch | Mittel | Mittel |

**Empfohlener Ansatz**: CirrusSearch für die primäre Volltext-Suche, ergänzt um die `Special:GoBySemanticId`-Suche für direkte URI-Auflösung. Für fortgeschrittene Property-Filter wird der SPARQL-Endpunkt von Wikibase direkt genutzt.

#### 4.2.1 `Special:GoBySemanticId` Integration

Eine geplante Spezialseite `Special:GoBySemanticId` ermöglicht die direkte Auflösung einer Semantic ID zur entsprechenden Wikibase-Item-Seite:

```
GET /wiki/Special:GoBySemanticId?id=http://qudt.org/vocab/unit/V
→ Redirect zu: /wiki/Item:Q21
```

**Implementierungskonzept** (MediaWiki PHP-Extension):
```php
class SpecialGoBySemanticId extends SpecialPage {
    public function execute( $subPage ) {
        $semanticId = $this->getRequest()->getVal( 'id' );
        // SPARQL-Abfrage gegen lokalen Wikibase SPARQL-Endpunkt
        $item = $this->findItemBySemanticId( $semanticId );
        if ( $item ) {
            $this->getOutput()->redirect(
                Title::makeTitle( NS_ITEM, $item )->getFullURL()
            );
        } else {
            $this->getOutput()->addHTML( '<p>Keine Concept Description gefunden.</p>' );
        }
    }
}
```

### 4.3 UX-Optimierungen auf der Startseite

Die UX-Verbesserungen der Semantic Wikibase Hauptseite zielen darauf ab, die Einstiegshürde für Nutzer ohne technisches Wikibase-Wissen zu senken.

#### 4.3.1 Geplante Suchfeld-Integration

Die Hauptseite (`Main_Page`) soll ein prominentes Suchfeld erhalten, das direkt Concept Descriptions nach Begriff oder URI sucht:

```html
<!-- Geplantes Suchfeld auf Main_Page -->
<div id="semantic-search-widget">
  <h2>Semantic ID Suche</h2>
  <form action="/wiki/Special:GoBySemanticId" method="get">
    <input type="text"
           name="id"
           placeholder="Begriff eingeben, z. B. 'Volt' oder URI..."
           class="semantic-search-input" />
    <select name="lang">
      <option value="en">Englisch</option>
      <option value="de">Deutsch</option>
    </select>
    <button type="submit">Suchen</button>
  </form>
</div>
```

#### 4.3.2 Automatische Vervollständigung (Typeahead)

Über die bestehende Wikibase Action API (`action=wbsearchentities`) wird eine Autocomplete-Funktion bereitgestellt:

```
GET /api.php?action=wbsearchentities&search=Volt&language=de&type=item&format=json
```

Diese gibt eine Liste von Wikibase-Items zurück, die den Suchbegriff im Label enthalten, und kann für clientseitige Autocomplete-Widgets genutzt werden.

---

## 5. Datenmodell

### 5.1 Interner Speicher in Wikibase

#### 5.1.1 Wikibase-Entitäten (Items)

Jede Concept Description wird als ein **Wikibase Item** (QID) gespeichert. Die Items haben folgende Struktur:

```
Item: Q21
├── Label[de]:       "Nennspannung"
├── Label[en]:       "Rated Voltage"
├── Description[de]: "Spannung, für die ein Gerät ausgelegt ist"
├── Description[en]: "Voltage for which a device is designed"
├── Alias[de]:       ["Bemessungsspannung"]
└── Statements:
    ├── P1  (semanticId):         "https://semanticid.aas-connect.com/id/Q21"
    ├── P35 (preferredName):      "Nennspannung" [de], "Rated Voltage" [en]
    ├── P36 (shortName):          "U_N" [en]
    ├── P37 (unit):               Item:Q174789 (Volt)
    ├── P40 (sourceOfDefinition): "0112-2---61360_4#AAA123#001"
    ├── P41 (symbol):             "U"
    ├── P42 (dataType):           "REAL_MEASURE"
    └── P44 (definition):         "..." [de], "..." [en]
```

#### 5.1.2 Wikibase-Properties

Die Wikibase-Instanz enthält dedizierte Properties, die die IEC 61360-Felder abbilden:

| Property-ID | Name | Datentyp | IEC 61360-Entsprechung |
|-------------|------|----------|------------------------|
| P1 | semanticId | URL | Globale Semantic ID |
| P35 | preferredName | Monolingual text | Bevorzugter Name |
| P36 | shortName | Monolingual text | Kurzname |
| P37 | unit | Item | Einheit (Verweis auf Einheits-Item) |
| P40 | sourceOfDefinition | String | Quellverweis |
| P41 | symbol | String | Symbol (z. B. V, Ω) |
| P42 | dataType | Item | Datentyp (STRING, REAL, etc.) |
| P43 | unitId | External ID | Einheiten-Kennung (IEC Code) |
| P44 | definition | Monolingual text | Definition |
| P45 | valueFormat | String | Werteformat |
| P46 | valueList | Item | Werteliste (Enum) |
| P47 | value | Quantity | Nominalwert |
| P48 | levelType | Item | Wertebereich-Typ |

#### 5.1.3 RDF/Turtle-Repräsentation

Intern speichert Wikibase alle Aussagen als RDF-Tripel im Blazegraph-Triplestore. Beispiel für `Q21`:

```turtle
@prefix wd:  <https://semanticid.aas-connect.com/entity/> .
@prefix wdt: <https://semanticid.aas-connect.com/prop/direct/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

wd:Q21
    rdfs:label "Nennspannung"@de, "Rated Voltage"@en ;
    wdt:P1  "https://semanticid.aas-connect.com/id/Q21" ;
    wdt:P35 "Nennspannung"@de, "Rated Voltage"@en ;
    wdt:P37 wd:Q174789 ;
    wdt:P41 "U" ;
    wdt:P42 wd:Q_REAL_MEASURE ;
    wdt:P44 "Spannung, für die ein Gerät ausgelegt ist"@de .
```

### 5.2 Externe Repräsentation als AAS Concept Description

Die externe JSON-Darstellung, wie sie die API zurückgibt, folgt dem AAS-Metamodell Part 3a (IEC 61360 Data Specification). Das vollständig befüllte Beispiel für „Volt" aus der `qudt_mapper.py`-Ausgabe (`SOURCE/source_mapping/QUDT/Volt.json`):

```json
{
  "query": {
    "search": "Volt",
    "mode": "term",
    "lang": "en",
    "source": "QUDT"
  },
  "total": 1,
  "result": {
    "modelType": "ConceptDescription",
    "id": "http://qudt.org/vocab/unit/V",
    "idShort": "V",
    "category": "REFERENCE",
    "embeddedDataSpecifications": [
      {
        "dataSpecification": {
          "type": "ExternalReference",
          "keys": [{
            "type": "GlobalReference",
            "value": "https://admin-shell.io/DataSpecificationTemplates/DataSpecificationIec61360/3"
          }]
        },
        "dataSpecificationContent": {
          "modelType": "DataSpecificationIec61360",
          "semanticId": "http://qudt.org/vocab/unit/V",
          "preferredName": [
            {"language": "de", "text": "Volt"},
            {"language": "en", "text": "Volt"},
            {"language": "zh", "text": "伏特"},
            {"language": "ar", "text": "فولت"}
          ],
          "shortName": [{"language": "en", "text": "V"}],
          "unit": "V",
          "unitId": {
            "type": "ExternalReference",
            "keys": [{"type": "GlobalReference", "value": "http://qudt.org/vocab/unit/V"}]
          },
          "symbol": "V",
          "dataType": "IRI",
          "definition": [{
            "language": "en",
            "text": "Volt is the SI unit of electric potential..."
          }]
        }
      }
    ]
  }
}
```

### 5.3 Datenquellen und Source-Mapping

Die Semantic Wikibase bindet im aktuellen Projektstand drei externe Datenquellen an:

- QUDT
- VEC
- KBL

Diese Quellen unterscheiden sich in ihrer technischen Struktur. QUDT und VEC basieren auf RDF-, TTL- bzw. OWL-Strukturen, während KBL auf XML/XSD basiert. Aus architektonischer Sicht werden diese Unterschiede durch separate Mapper gekapselt. Jeder Mapper übernimmt die Verarbeitung seiner jeweiligen Quelle und überführt die Daten anschließend in das gemeinsame IEC61360-nahe Zielmodell.

| Datenquelle | Quellformat | Verarbeitung | Ergebnis |
|---|---|---|---|
| QUDT | RDF / TTL / SPARQL | QUDT-API und QUDT-Mapper | ConceptDescriptions für Einheiten, Größen und Symbole |
| VEC | RDF / OWL / TTL | VEC-Mapper | ConceptDescriptions für VEC-Konzepte |
| KBL | XML / XSD | KBL-Mapper | ConceptDescriptions für KBL-Elemente, Typen und Enumerationen |

Die detaillierten Mapping-Regeln, Feldzuordnungen und Besonderheiten der einzelnen Quellen sind in der Moduldokumentation beschrieben:

- [MOD Kapitel 4.1 QUDT](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#41-qudt)
- [MOD Kapitel 4.2 VEC](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#42-vec)
- [MOD Kapitel 4.3 KBL](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#43-kbl)
- [MOD Kapitel 5 Gemeinsames Mapping über alle Quellen](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#5-gemeinsames-mapping-über-alle-quellen)

---

## 6. Nicht-funktionale Anforderungen

### 6.1 Skalierbarkeit der Suche

#### 6.1.1 API-Latenz-Anforderungen

Gemäß CRS und den Projektanforderungen gelten folgende Performance-Ziele:

| Anforderung | Zielwert | Aktueller Status |
|------------|----------|-----------------|
| API-Antwortzeit (gecacht) | < 300 ms | Abhängig von QUDT-Endpunkt |
| API-Antwortzeit (ungecacht) | < 3000 ms | SPARQL-Timeout: 30 s konfiguriert |
| SPARQL-Kandidatenabfrage | < 2000 ms | `LIMIT 1` sichert Performance |
| SPARQL-Detailabfrage | < 2000 ms | Sprachfilter reduziert Ergebnismenge |

#### 6.1.2 Caching-Strategie

Die aktuelle Implementierung enthält **kein Caching**. Die empfohlene Architektur für Produktivbetrieb:

1. **HTTP-Level-Cache** (Nginx): `Cache-Control: public, max-age=3600` für GET-Anfragen
2. **Application-Level-Cache** (Redis): Gecachte ConceptDescription-Objekte nach URI, TTL: 1 Stunde
3. **SPARQL-Result-Cache**: Blazegraph interner Query-Cache (konfigurierbar via `queryCache.maxSize`)

#### 6.1.3 Skalierungsmodell

```
                    Load Balancer (Nginx)
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
      API-Instanz 1              API-Instanz 2
      (FastAPI/Uvicorn)          (FastAPI/Uvicorn)
              │                         │
              └────────────┬────────────┘
                           ▼
                  Redis Cache Cluster
                           │
                           ▼
                  QUDT Fuseki (extern)
                  Wikibase Blazegraph (intern)
```

Containerisierung via Docker Compose (Entwicklung) / Kubernetes (Produktion) ermöglicht horizontale Skalierung der API-Schicht.

#### 6.1.4 Wikibase SPARQL-Skalierbarkeit

Für den Wikibase-internen SPARQL-Endpunkt (Blazegraph) gelten:
- Empfohlene JVM-Heap-Größe: mindestens 8 GB (`-Xmx8g`)
- Query-Timeout-Konfiguration: 60 Sekunden
- Für Produktionslast: Blazegraph-Replikation oder Wechsel zu Apache Jena TDB2

### 6.2 Sicherheit der API

#### 6.2.1 Aktuelle Sicherheitslage

Die aktuelle API-Implementierung ist für Entwicklungs- und Demo-Zwecke ausgelegt:
- **Kein TLS**: Nur HTTP, kein HTTPS in der lokalen Entwicklungsumgebung
- **Keine Authentifizierung**: Alle Endpunkte sind ohne Token erreichbar
- **CORS**: Flask-CORS ist aktiviert (`CORS(app)`), erlaubt alle Origins

#### 6.2.2 Sicherheitsmaßnahmen für Produktionsbetrieb

**Pflichtmaßnahmen vor Produktivgang:**

| Bereich | Maßnahme | Implementierung |
|---------|----------|-----------------|
| **Transport** | TLS 1.3 erzwingen | Nginx: `ssl_protocols TLSv1.3;` |
| **Authentifizierung** | OAuth2 / JWT | FastAPI: `python-jose`, `passlib` |
| **CORS** | Einschränken auf bekannte Origins | `CORSMiddleware` mit `allow_origins=["https://..."]` |
| **Input-Validierung** | Parameter-Sanitierung | FastAPI Pydantic-Validierung bereits integriert |
| **Rate Limiting** | Anfragen pro IP begrenzen | Nginx `limit_req_zone` oder API-Gateway |
| **SPARQL-Injection** | Suchbegriff escapen | `safe_search = search.replace('"', '\\"')` ✅ bereits implementiert |
| **Secrets Management** | Keine Credentials im Code | Environment Variables, `.env`-Dateien |

#### 6.2.3 SPARQL-Injection-Schutz

Die Implementierung enthält bereits grundlegende Schutzmaßnahmen:

```python
# In build_candidate_query():
safe_search = search.replace('"', '\\"')
safe_expanded = expanded.replace('"', '\\"')
```

Für Produktionsumgebungen wird zusätzlich empfohlen:
- Whitelisting erlaubter URI-Präfixe
- Maximale Länge des `search`-Parameters (z. B. 512 Zeichen)
- Parametrisierte SPARQL-Abfragen (wo vom Endpunkt unterstützt)

#### 6.2.4 Wikibase-Berechtigungsmodell

MediaWiki bietet eine differenzierte Zugriffssteuerung:

```php
// LocalSettings.php – Nur angemeldete Nutzer können Edits vornehmen
$wgGroupPermissions['*']['edit'] = false;
$wgGroupPermissions['user']['edit'] = true;
$wgGroupPermissions['sysop']['deleterevision'] = true;

// API-Zugriff für maschinelle Clients
$wgGroupPermissions['bot']['edit'] = true;
$wgGroupPermissions['bot']['apihighlimits'] = true;
```

---

## 7. Zusammenfassung und Ausblick

### 7.1 Zusammenfassung der Architektur

Die Semantic Wikibase Architektur realisiert eine offene Plattform zur Verwaltung und Bereitstellung industrieller Concept Descriptions gemäß IEC61360-nahem Zielmodell und AAS-Kontext. Die wesentlichen Architekturentscheidungen sind:

1. **Wikibase als zentrale semantische Plattform**: Die Wikibase dient als zentrale Umgebung zur Verwaltung, Pflege und Bereitstellung semantischer Definitionen. ConceptDescriptions können dort als strukturierte Items mit Properties und Statements abgebildet werden.

2. **API-Gateway als zentrale Zugriffsschicht**: Externe Clients greifen nicht direkt auf einzelne Datenquellen zu, sondern über eine zentrale API-Schicht. Diese nimmt Anfragen entgegen und leitet sie abhängig von Quelle oder Suchkontext an die passenden Einzel-APIs bzw. Mapper weiter.

3. **Modulare Mapper-Struktur**: Die Datenquellen QUDT, VEC und KBL werden über getrennte Mapper verarbeitet. Dadurch bleiben Unterschiede zwischen RDF/TTL/OWL-Quellen und XML/XSD-Quellen innerhalb der jeweiligen Module gekapselt.

4. **Gemeinsames Zielmodell**: Alle Mapper führen ihre Ergebnisse in ein einheitliches IEC61360-nahes JSON-Zielmodell über. Dadurch können externe Clients unabhängig von der ursprünglichen Datenquelle eine konsistente Antwortstruktur verwenden.

5. **Erweiterbarkeit der Architektur**: Durch die Trennung von Gateway, Einzel-APIs, Mapping-Schicht und Wikibase können weitere Datenquellen oder zusätzliche Schnittstellen später ergänzt werden, ohne die gesamte Architektur neu aufzubauen.

Die detaillierten Mapping-Regeln und konkreten Feldzuordnungen sind in der Moduldokumentation beschrieben.

### 7.2 Bekannte Einschränkungen und offene Punkte

| Thema | Aktueller Stand | Handlungsbedarf |
|-------|-----------------|-----------------|
| **Authentifizierung** | Nicht implementiert | OAuth2/JWT-Integration notwendig |
| **Caching** | Nicht implementiert | Redis-Cache für Produktivbetrieb |
| **Batch-Import** | Noch nicht implementiert | POST `/semanticIds` (Batch) ist geplant |
| **Export-Endpunkt** | Noch nicht implementiert | GET `/semanticIds/export` (CSV/JSON) geplant |
| **`Special:GoBySemanticId`** | Konzept vorhanden | MediaWiki-PHP-Extension muss implementiert werden |
| **AASX-Import** (FA.007) | Im CRS spezifiziert | Parsing und Mapping von AASX-Paketen |
| **FoP Consult GmbH** | Im SAS erwähnt | Identity-Provider-Integration offen |
| **Wikibase-Deployment** | Docker-Compose-Konzept vorhanden | Konfiguration der Wikibase-Properties muss finalisiert werden |

### 7.3 Technische Schulden

- Einzelne API- und Mapping-Komponenten enthalten teilweise ähnliche Logik zur Datenabfrage, Transformation und Fehlerbehandlung. Perspektivisch sollte gemeinsame Logik in eine gemeinsame Library oder ein gemeinsames Package ausgelagert werden.
- Für externe Datenquellen fehlt teilweise eine robuste Retry- und Timeout-Strategie. Für einen produktiven Betrieb sollten Wiederholungsmechanismen und klar definierte Fehlerfälle ergänzt werden.
- Das Error-Handling sollte vereinheitlicht werden, damit Fehler aus externen Quellen, Mappern und API-Endpunkten strukturiert und konsistent zurückgegeben werden.

### 7.4 Roadmap und nächste Schritte

**Sprint 1 (sofort umzusetzen):**
- [ ] Wikibase-Instanz mit konfigurierten Properties (P1–P48) aufsetzen
- [ ] Pretty-URI-Konfiguration in Nginx aktivieren
- [ ] Docker-Compose-Stack für Entwicklungsumgebung fertigstellen

**Sprint 2:**
- [ ] `Special:GoBySemanticId` als MediaWiki-Extension implementieren
- [ ] QUDT-Bulk-Import-Script: automatisches Befüllen der Wikibase mit QUDT-Einheiten
- [ ] API-Authentifizierung mit OAuth2 implementieren

**Sprint 3:**
- [ ] Suchfeld-Widget auf Main_Page integrieren
- [ ] CirrusSearch konfigurieren und testen
- [ ] `POST /semanticIds` (Einzelimport und Batch) implementieren
- [ ] `GET /semanticIds/export` implementieren

**Mittelfristig:**
- [ ] AASX-Import (FA.007 aus CRS)
- [ ] Federated Query zu Catena-X Semantic Hub
- [ ] Automatisierter Abgleich mit IEC CDD und ECLASS (Verlinkung, kein Datenkopie)
- [ ] FoP Consult GmbH Identity-Provider Integration

---

## Anhang: Konfigurationsdateien und Referenzen

### A.1 Abhängigkeiten (Python)

**FastAPI-Stack** (`SOURCE/API_QUDT/`):
```
fastapi
uvicorn
requests
```

**Flask-Stack** (`SOURCE/Wikibase_API/`):
```
flask
flask-cors
requests
```

**Lokaler Mapper** (`SOURCE/source_mapping/QUDT/requirements.txt`):
```
rdflib
```

### A.2 Hinweise zu Mapper-Konfigurationen

Die konkreten Konfigurationen der einzelnen Mapper, beispielsweise erlaubte QUDT-Typen, Quell-URIs, Namespace-Präfixe oder Mapping-spezifische Einstellungen, sind Bestandteil der jeweiligen Implementierung.

Im SAS werden diese Details nicht vollständig aufgeführt, da sie zur Modulebene gehören und in der Moduldokumentation bzw. im Quellcode nachvollziehbar sind.

Weitere Informationen befinden sich in:

- [MOD Kapitel 4.1 QUDT](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#41-qudt)
- [MOD Kapitel 4.2 VEC](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#42-vec)
- [MOD Kapitel 4.3 KBL](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#43-kbl)
- [MOD Kapitel 5 Gemeinsames Mapping über alle Quellen](TINF24F_4-MOD-Semantic-Wikibase-0v1.md#5-gemeinsames-mapping-über-alle-quellen)

### A.3 Referenzen

| Dokument / Artefakt | Pfad im Repository | Beschreibung |
|---|---|---|
| Moduldokumentation (MOD) | `PROJECT/TINF24F_4-MOD-Semantic-Wikibase-0v1.md` | Detailbeschreibung der APIs, Mapper, Mapping-Regeln, Zielmodelle und Modultests |
| OpenAPI-Spezifikation | `SOURCE/API_QUDT/Source_Code/openapi.yaml` | Maschinenlesbare Beschreibung der QUDT-API |
| QUDT API | `SOURCE/API_QUDT/Source_Code/api_qudt.py` | Implementierung der QUDT-API |
| Wikibase API | `SOURCE/Wikibase_API/app.py` | Flask-App-Einstiegspunkt für die Wikibase-API |
| QUDT Service | `SOURCE/Wikibase_API/api_v3/qudt_service.py` | Service-Schicht für QUDT-Abfragen |
| QUDT Mapper | `SOURCE/source_mapping/QUDT/qudt_mapper.py` | Mapping von QUDT-Daten auf das gemeinsame Zielmodell |
| KBL Mapper | `SOURCE/source_mapping/KBL/kbl_xsd_mapper.py` | Mapping von KBL-XSD-Strukturen auf das gemeinsame Zielmodell |
| VEC Mapper | `SOURCE/source_mapping/VEC/vec_var_API.py` | Mapping der VEC-Ontologie auf das gemeinsame Zielmodell |
| Lastenheft (CRS) | `PROJECT/CRS.md` | Kundenanforderungen |
| Pflichtenheft (SRS) | `PROJECT/SRS.md` | Technische und funktionale Systemspezifikation |
| Business Case | `PROJECT/BC.md` | Wirtschaftliche Begründung |
| Projektplan | `PROJECT/PM.md` | Zeitplanung, Organisation und Projektstruktur |

---

*Dieses Dokument beschreibt die übergeordnete Softwarearchitektur des Projekts `DHBW-TINF24F/Team4-Semantic-Wikibase`. Detaillierte Beschreibungen einzelner APIs, Mapper, Mapping-Regeln und Modultests sind in der Moduldokumentation (MOD) enthalten.*
