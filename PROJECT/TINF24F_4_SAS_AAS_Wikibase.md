# Software Architecture Specification (SAS)
## Semantic Wikibase – AAS Concept Description API & Sucherweiterung

---

| Dokument-ID   | SAS_AAS_Wikibase                                  |
|---------------|---------------------------------------------------|
| Version       | 1.0                                               |
| Datum         | 08.05.2026                                        |
| Autor         | GitHub Copilot Agent (Senior Software Architekt)  |
| Basis         | IEEE 1471-2000 / ISO/IEC/IEEE 42010               |
| Repository    | DHBW-TINF24F/Team4-Semantic-Wikibase              |

---

## Versionskontrolle

| Version | Datum      | Autor                              | Kommentar                |
|---------|------------|------------------------------------|--------------------------|
| 1.0     | 08.05.2026 | GitHub Copilot (Architekturanalyse) | Erstversion auf Basis der Repository-Analyse |

---

## Inhaltsverzeichnis

1. [Einleitung & Vision](#1-einleitung--vision)
2. [Systemübersicht](#2-systemübersicht)
3. [Detaillierte API-Architektur](#3-detaillierte-api-architektur)
   - 3.1 [OpenAPI-Spezifikation](#31-openapi-spezifikation)
   - 3.2 [AAS-CD Daten-Mapping (Transformationsschicht)](#32-aas-cd-daten-mapping-transformationsschicht)
   - 3.3 [Filter- und Sortierlogik](#33-filter--und-sortierlogik)
   - 3.4 [Konzept für rollenbasierte Zugriffskontrolle](#34-konzept-für-rollenbasierte-zugriffskontrolle)
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

Diese Software Architecture Specification (SAS) beschreibt auf Basis von IEEE 1471-2000 die vollständige Softwarearchitektur der Semantic Wikibase Plattform. Sie dokumentiert:

1. Die implementierten API-Endpunkte und deren OpenAPI-Spezifikation
2. Die Transformationsschicht zwischen externen Ontologien (QUDT, VEC, KBL) und dem AAS-CD-Metamodell nach IEC 61360
3. Die Such-Architektur der Wikibase-Erweiterung
4. Das interne und externe Datenmodell
5. Nicht-funktionale Anforderungen bezüglich Sicherheit und Skalierbarkeit

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

| Komponente | Technologie | Zweck |
|---|---|---|
| **FastAPI QUDT-API** | Python 3, FastAPI, Uvicorn | Standalone REST-Endpunkt für QUDT-zu-IEC61360-Mapping |
| **Flask Wikibase-API** | Python 3, Flask, Blueprints | Erweiterbare API-Schicht über der Wikibase-Instanz |
| **QUDT Service** | Python 3, `requests`, SPARQL | Abfrage des QUDT Fuseki-Endpunkts, 2-Schritt SPARQL-Auflösung |
| **QUDT Mapper** | Python 3, `rdflib` | Lokales TTL-basiertes Mapping ohne Netzwerkzugriff |
| **KBL Mapper** | Python 3, `requests`, XML/XSD | Mapping von KBL-XSD-Strukturen auf IEC 61360 |
| **VEC Mapper** | Python 3, `rdflib` | Mapping der VEC-Ontologie (OWL/TTL) auf IEC 61360 |
| **Wikibase** | MediaWiki, Wikibase Extension | Persistente Wissensdatenbank für Concept Descriptions |
| **SPARQL Endpoint** | Blazegraph / WDQS | RDF-Abfrageendpunkt für Wikibase-Daten |
| **Nginx Reverse Proxy** | Nginx | Pretty URIs, SSL-Terminierung, Routing |

---

## 3. Detaillierte API-Architektur

### 3.1 OpenAPI-Spezifikation

Die API-Spezifikation ist im Repository unter `SOURCE/API_QUDT/Source_Code/openapi.yaml` abgelegt und wurde nach OpenAPI 3.0.3 erstellt. Die Spezifikation beschreibt eine **QUDT-zu-IEC61360-Mapping-API** mit zwei Haupt-Endpunkten.

#### 3.1.1 Endpunkt: `GET /`

```
GET /
```

**Beschreibung:** Root-Endpunkt mit Basisinformationen zur API.

**Antwort (HTTP 200):**
```json
{
  "message": "QUDT to IEC61360 Mapping API",
  "swagger": "/docs",
  "endpoint": "/map"
}
```

#### 3.1.2 Endpunkt: `GET /map`

```
GET /map?search={begriff}&lang={sprache}&types={typen}
```

Dies ist der zentrale Endpunkt der API. Er nimmt einen Suchbegriff, eine optionale Sprache und optionale QUDT-Typ-Filter entgegen, führt eine SPARQL-Abfrage gegen den QUDT-Endpunkt durch und gibt eine IEC 61360-konforme ConceptDescription zurück.

**Query-Parameter:**

| Parameter | Typ | Pflicht | Standardwert | Beschreibung |
|-----------|-----|---------|--------------|--------------|
| `search` | string | ja | – | Suchbegriff, vollständige QUDT-URI oder CURIE (z. B. `unit:V`) |
| `lang` | enum (`en`, `de`) | nein | `en` | Sprache für Labels und Beschreibungen |
| `types` | array[enum] | nein | alle Typen | QUDT-Typen: `unit`, `quantitykind`, `dimensionvector`, `constant`, `sou`, `soqk` |

**Suchmodi:**
- **term**: Der Suchbegriff ist ein Klarbegriff wie `Volt` oder `Ampere`
- **id**: Der Suchbegriff ist eine vollständige QUDT-URI (`http://qudt.org/vocab/unit/V`) oder eine CURIE (`unit:V`)

**Antwortstruktur (HTTP 200 – Treffer gefunden):**

```json
{
  "query": {
    "search": "Volt",
    "mode": "term",
    "lang": "en",
    "types": ["unit"]
  },
  "total": 1,
  "result": {
    "modelType": "ConceptDescription",
    "id": "http://qudt.org/vocab/unit/V",
    "idShort": "V",
    "embeddedDataSpecifications": [
      {
        "dataSpecification": {
          "type": "ExternalReference",
          "keys": [
            {
              "type": "GlobalReference",
              "value": "http://admin-shell.io/DataSpecificationTemplates/DataSpecificationIEC61360/3/0"
            }
          ]
        },
        "dataSpecificationContent": {
          "modelType": "DataSpecificationIec61360",
          "semanticId":        { "property": "P1",  "value": "http://qudt.org/vocab/unit/V" },
          "preferredName":     { "property": "P35", "value": [{"value": "Volt", "lang": "en"}] },
          "shortName":         { "property": "P36", "value": null },
          "unit":              { "property": "P37", "value": "Volt" },
          "sourceOfDefinition":{ "property": "P40", "value": null },
          "Symbol":            { "property": "P41", "value": "V" },
          "dataType":          { "property": "P42", "value": "qudt:Unit" },
          "unitId":            { "property": "P43", "value": null },
          "Definition":        { "property": "P44", "value": null },
          "valueFormat":       { "property": "P45", "value": null },
          "valueList":         { "property": "P46", "value": null },
          "value":             { "property": "P47", "value": null },
          "levelType":         { "property": "P48", "value": null }
        }
      }
    ],
    "additionalProperties": {}
  }
}
```

**Fehler-Antworten:**

| HTTP-Code | Ursache | Antwort-Body |
|-----------|---------|--------------|
| 400 | Leerer `search`-Parameter | `{"detail": "Parameter 'search' darf nicht leer sein."}` |
| 500 | QUDT-Endpunkt nicht erreichbar | `{"detail": "Fehler beim Zugriff auf QUDT."}` |

#### 3.1.3 Flask-Blueprint-Endpunkt: `GET /api/v3/search`

Neben der FastAPI-Implementierung existiert eine Flask-basierte Architektur unter `SOURCE/Wikibase_API/`. Die `app.py` registriert den Blueprint `api_v3` auf dem Pfad `/api/v3`:

```python
app.register_blueprint(api_v3, url_prefix="/api/v3")
```

Der Blueprint definiert:
```
GET /api/v3/info     → Gibt API-Name und Version zurück
GET /api/v3/search   → Suche: ?search=Volt&lang=en&types=unit,quantitykind
```

Der `/api/v3/search`-Endpunkt delegiert an den `search_qudt()`-Service in `qudt_service.py` und gibt eine identische JSON-Struktur zurück wie der FastAPI-Endpunkt.

### 3.2 AAS-CD Daten-Mapping (Transformationsschicht)

#### 3.2.1 Überblick des Mapping-Prozesses

Die Transformationsschicht ist das Kernstück der API. Sie konvertiert RDF-Tripel aus QUDT (oder anderen Quellen) in AAS-konforme `ConceptDescription`-JSON-Objekte nach IEC 61360. Der Prozess umfasst sechs Schritte:

```
[1] Eingabe validieren          (normalize_lang, normalize_types)
       │
       ▼
[2] Suchmodus erkennen          (detect_search_mode)
       │
       ▼
[3] SPARQL Kandidatenabfrage    (build_candidate_query → run_sparql)
       │
       ▼
[4] Beste URI ermitteln         (candidates[0]["entity"]["value"])
       │
       ▼
[5] SPARQL Detailabfrage        (build_detail_query → run_sparql)
       │
       ▼
[6] RDF → IEC61360 mappen       (map_rows_to_semantichub)
       │
       ▼
[7] JSON-Antwort zurückgeben
```

#### 3.2.2 Mapping-Tabelle: QUDT-Prädikate auf IEC 61360-Felder

Die zentrale Funktion `map_rows_to_semantichub()` in `qudt_service.py` iteriert über alle RDF-Tripel des gefundenen Objekts und ordnet jeden Prädikat einem IEC 61360-Feld zu:

| IEC 61360-Feld | Property-Nr. | QUDT RDF-Prädikat | Bemerkung |
|----------------|--------------|-------------------|-----------|
| `semanticId` | P1 | Subject-URI (direkt) | Globale eindeutige ID des Konzepts |
| `preferredName` | P35 | `rdfs:label` | Mehrsprachige Liste von `{value, lang}` |
| `shortName` | P36 | lokaler URI-Name | Aus URI extrahiert, max. 64 Zeichen |
| `unit` | P37 | `rdfs:label` (erster Treffer) | Fallback: erstes Label als Einheitenname |
| `sourceOfDefinition` | P40 | `rdfs:isDefinedBy`, `qudt:informativeReference` | Liste von Quell-URIs |
| `Symbol` | P41 | `qudt:symbol` | Einheitensymbol (z. B. `V` für Volt) |
| `dataType` | P42 | `rdf:type` | QUDT-Klasse (z. B. `qudt:Unit`) |
| `unitId` | P43 | `qudt:iec61360Code` | IEC 61360-Einheiten-Code |
| `Definition` | P44 | `dcterms:description`, `qudt:latexDefinition` | Textuelle und LaTeX-Definitionen |
| `valueFormat` | P45 | `qudt:siUnitsExpression` | SI-Einheitenausdruck |
| `valueList` | P46 | – | Nicht aus QUDT ableitbar, `null` |
| `value` | P47 | – | Nicht für Einheiten, `null` |
| `levelType` | P48 | – | MIN/NOM/TYP/MAX, `null` bei Einheiten |

**Nicht gemappte Prädikate** werden in `additionalProperties` gesammelt, z. B.:
- `qudt:conversionMultiplier`
- `qudt:hasDimensionVector`
- `qudt:hasQuantityKind`
- `qudt:ucumCode`
- `qudt:wikidataMatch`

#### 3.2.3 CURIE-Expansion

Vor der SPARQL-Abfrage werden CURIEs (Compact URIs) in vollständige URIs expandiert:

```python
curie_map = {
    "unit":           "http://qudt.org/vocab/unit/",
    "quantitykind":   "http://qudt.org/vocab/quantitykind/",
    "qkdv":           "http://qudt.org/vocab/dimensionvector/",
    "dimensionvector":"http://qudt.org/vocab/dimensionvector/",
    "constant":       "http://qudt.org/vocab/constant/",
    "sou":            "http://qudt.org/vocab/sou/",
    "soqk":           "http://qudt.org/vocab/soqk/"
}
```

Beispiel: `unit:V` → `http://qudt.org/vocab/unit/V`

#### 3.2.4 Klassenstruktur: `empty_concept_description()`

Die Funktion `empty_concept_description(uri: str)` erzeugt das Grundgerüst jeder ConceptDescription. Jedes IEC-Feld ist als Objekt `{"property": "P{n}", "value": ...}` strukturiert:

```python
def empty_concept_description(uri: str) -> Dict[str, Any]:
    return {
        "modelType": "ConceptDescription",
        "id": uri,
        "idShort": local_name(uri),
        "embeddedDataSpecifications": [
            {
                "dataSpecification": {
                    "type": "ExternalReference",
                    "keys": [{
                        "type": "GlobalReference",
                        "value": "http://admin-shell.io/DataSpecificationTemplates/DataSpecificationIEC61360/3/0"
                    }]
                },
                "dataSpecificationContent": {
                    "modelType": "DataSpecificationIec61360",
                    "semanticId":         {"property": "P1",  "value": uri},
                    "preferredName":      {"property": "P35", "value": []},
                    "shortName":          {"property": "P36", "value": None},
                    "unit":               {"property": "P37", "value": None},
                    "sourceOfDefinition": {"property": "P40", "value": []},
                    "Symbol":             {"property": "P41", "value": None},
                    "dataType":           {"property": "P42", "value": None},
                    "unitId":             {"property": "P43", "value": None},
                    "Definition":         {"property": "P44", "value": []},
                    "valueFormat":        {"property": "P45", "value": None},
                    "valueList":          {"property": "P46", "value": None},
                    "value":              {"property": "P47", "value": None},
                    "levelType":          {"property": "P48", "value": None}
                }
            }
        ],
        "additionalProperties": {}
    }
```

### 3.3 Filter- und Sortierlogik

#### 3.3.1 SPARQL-Kandidatenabfrage mit Ranking

Die Funktion `build_candidate_query()` baut eine SPARQL-Abfrage mit einem mehrstufigen Ranking. Der begriffs-basierte Suchmodus wendet vier Prioritätsstufen an:

```sparql
BIND(
  IF(BOUND(?label) && LCASE(STR(?label)) = LCASE("Volt"), 0,
    IF(LCASE(REPLACE(STR(?entity), "^.+[/#]", "")) = LCASE("Volt"), 1,
      IF(BOUND(?symbol) && LCASE(STR(?symbol)) = LCASE("Volt"), 2, 3)
    )
  ) AS ?rank
)
ORDER BY ?rank STRLEN(STR(?label)) ?entity
LIMIT 1
```

| Rang | Priorität | Kriterium |
|------|-----------|-----------|
| 0 | Höchste | Exakter Match auf `rdfs:label` (case-insensitive) |
| 1 | Hoch | Exakter Match auf lokalen URI-Namen |
| 2 | Mittel | Exakter Match auf `qudt:symbol` |
| 3 | Niedrig | Teilstring-Match auf `rdfs:label` |

Bei gleichem Rang wird nach Labellänge und dann nach URI alphabetisch sortiert, um deterministische Ergebnisse zu gewährleisten.

#### 3.3.2 Typ-Filter

Die Query verwendet `VALUES ?entityType { ... }` um die Suche auf ausgewählte QUDT-Typen zu beschränken. Zusätzlich gibt es einen URI-Präfix-Filter (`STRSTARTS`), der verhindert, dass Ressourcen aus unerwarteten QUDT-Namespaces zurückgegeben werden:

```sparql
VALUES ?entityType {
  <http://qudt.org/schema/qudt/Unit>
}

?entity a ?entityType .

FILTER(
  STRSTARTS(STR(?entity), "http://qudt.org/vocab/unit/")
)
```

#### 3.3.3 Sprachfilter in der Detailabfrage

Die Detailabfrage (`build_detail_query`) filtert Literale nach Sprache, gibt aber immer englische Labels und Nicht-Literale (URIs) zurück:

```sparql
FILTER(
  !isLiteral(?o) ||
  LANG(?o) = "de"  ||
  LANG(?o) = ""    ||
  LANG(?o) = "en"  ||
  ?p = rdfs:label  ||
  ?p = dcterms:description
)
```

### 3.4 Konzept für rollenbasierte Zugriffskontrolle

Die API-Implementierung enthält aktuell keinen direkten Authentifizierungs- oder Autorisierungsmechanismus. Die bestehende SAS v1.1 und das CRS beschreiben das geplante Rechtemanagement jedoch ausführlich.

#### 3.4.1 Geplante Rollen

| Rolle | Rechte | Beschreibung |
|-------|--------|--------------|
| **Anonymer Nutzer** | Lesen (GET) | Kann alle veröffentlichten Concept Descriptions abfragen |
| **Angemeldeter Nutzer** | Lesen + Erstellen | Kann neue Einträge in Wikibase anlegen |
| **Editor / Kurator** | Lesen + Schreiben + Löschen | Kann Einträge bearbeiten und pflegen |
| **Administrator** | Vollzugriff | Systemverwaltung, Benutzerverwaltung |
| **API-Dienst (M2M)** | Lesen via Token | Maschineller Zugriff über API-Token (OAuth2) |

#### 3.4.2 Architekturkonzept

Die geplante Implementierung sieht folgende Schichten vor:

1. **Wikibase-native Rechteverwaltung**: MediaWiki bietet ein differenziertes Rechtesystem (`$wgGroupPermissions`), das für Lese-/Schreibzugriffe auf Items genutzt wird.

2. **API-Gateway-Authentifizierung**: Die Semantic Facade validiert API-Tokens (Bearer Token / OAuth2 Client Credentials) für programmatischen Zugriff. Nur validierte Token erhalten Schreibrechte (`POST`, `PUT`).

3. **FoP Consult GmbH Integration** (geplant): Für den produktiven Einsatz ist die Integration eines externen Identity-Providers vorgesehen. Die REST-API soll OAuth2 mit JWT-Tokens verwenden, wobei Claims wie `role: editor` die Zugriffsstufe bestimmen.

4. **Audit-Log**: Jede Änderung an Wikibase-Items wird durch das MediaWiki-Revisionssystem versioniert und ist nachvollziehbar.

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

Das Repository implementiert Mapper für drei externe Quellen, die alle auf das gemeinsame IEC 61360-Ausgabeformat abbilden:

#### 5.3.1 QUDT-Mapper

- **Quelle**: QUDT Fuseki SPARQL-Endpunkt (`https://qudt.org/fuseki/qudt/query`)
- **Typen**: Unit, QuantityKind, DimensionVector, PhysicalConstant, SystemOfUnits, SystemOfQuantityKinds
- **Mapping**: RDF-Prädikate → IEC 61360 Felder (vollständig, siehe Abschnitt 3.2.2)
- **Besonderheit**: Zwei-Schritt SPARQL (Kandidatensuche + Detailabfrage), Ranking-Algorithmus

#### 5.3.2 KBL-Mapper (`kbl_xsd_mapper.py`)

- **Quelle**: KBL 2.5 XSD-Schema (`ecad-wiki.prostep.org`)
- **Typen**: `xs:complexType`, `xs:simpleType`, `xs:element`
- **Mapping-Tabelle** (KBL → IEC 61360):

| IEC-Feld | Property | Quelle |
|----------|----------|--------|
| `semanticId` | P1 | XSD-URL + `#Typname` |
| `preferredName` | P35 | XSD-Typname |
| `shortName` | P36 | XSD-Typname |
| `sourceOfDefinition` | P40 | XSD-URL |
| `dataType` | P42 | XSDComplexType / XSDSimpleType |
| `definition` | P44 | Generiert |

- **Einschränkung**: KBL ist keine Ontologie, enthält keine Labels, Definitionen oder Einheiten → viele Felder bleiben `null`

#### 5.3.3 VEC-Mapper (`vec_var_API.py`)

- **Quelle**: VEC 2.2.0 Ontologie (`ecad-wiki.prostep.org`, TTL/OWL)
- **Typen**: OWL-Klassen, RDF-Ressourcen
- **Mapping**: Analog zu QUDT, nutzt `rdflib` zum Parsen der lokalen TTL-Datei
- **Stärke**: VEC ist eine echte Ontologie (OWL/RDF), daher können `rdfs:label`, `rdfs:comment` und Vererbungsbeziehungen direkt gemappt werden

---

## 6. Nicht-funktionale Anforderungen

### 6.1 Skalierbarkeit der Suche

#### 6.1.1 API-Latenz-Anforderungen

Gemäß CRS und SAS v1.1 gelten folgende Performance-Ziele:

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

Die Semantic Wikibase Architektur realisiert eine moderne, offene Plattform für industrielle Concept Descriptions gemäß IEC 61360 und AAS-Standard. Die wesentlichen Architekturentscheidungen sind:

1. **Wikibase als Single Source of Truth**: Alle Concept Descriptions werden einmalig in Wikibase persistiert. AAS-Backends und externe Clients greifen lesend über REST-API und SPARQL zu.

2. **Zustandslose API-Facade**: Die API-Schicht (FastAPI / Flask) transformiert Anfragen zwischen AAS-Clients und Wikibase bzw. externen Ontologien. Es findet keine Datenhaltung in der Facade statt.

3. **Multi-Source-Mapping**: Das Repository implementiert Mapper für drei externe Quellen (QUDT, KBL, VEC), die alle auf die gleiche IEC 61360-JSON-Ausgabestruktur abbilden.

4. **Zweistufige SPARQL-Suche**: Die QUDT-Integration verwendet einen robusten Zwei-Schritt-Ansatz (Kandidatenauswahl mit Ranking → Detailabfrage), der sowohl Begriffssuche als auch URI/CURIE-Suche unterstützt.

5. **Erweiterbare Architektur**: Das Blueprint-Muster in Flask und die klare Trennung von Service-Layer (`qudt_service.py`) und API-Layer (`api_v3_blueprint.py`) erlauben die einfache Ergänzung neuer Datenquellen und Endpunkte.

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

- Die aktuelle `api_qudt.py` (FastAPI) und `qudt_service.py` (Flask) enthalten duplizierte Logik (SPARQL-Bau, Mapping-Funktionen). Eine gemeinsame Library oder ein gemeinsames Package sollte extrahiert werden.
- Der QUDT-Mapper verwendet direkte HTTP-Requests ohne Retry-Logik. Für Produktionsbetrieb sollte `tenacity` oder ein ähnliches Retry-Framework integriert werden.
- Fehler aus dem QUDT-Endpunkt werden in `qudt_service.py` als rohe HTTP-Fehler weitergeleitet; strukturiertes Error-Handling mit dedizierten Fehlerklassen fehlt.

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

### A.2 QUDT Typ-Konfiguration

```python
TYPE_CONFIG = {
    "unit": {
        "classUri":    "http://qudt.org/schema/qudt/Unit",
        "vocabPrefix": "http://qudt.org/vocab/unit/",
        "short":       "qudt:Unit"
    },
    "quantitykind": {
        "classUri":    "http://qudt.org/schema/qudt/QuantityKind",
        "vocabPrefix": "http://qudt.org/vocab/quantitykind/",
        "short":       "qudt:QuantityKind"
    },
    "dimensionvector": {
        "classUri":    "http://qudt.org/schema/qudt/QuantityKindDimensionVector",
        "vocabPrefix": "http://qudt.org/vocab/dimensionvector/",
        "short":       "qudt:QuantityKindDimensionVector"
    },
    "constant": {
        "classUri":    "http://qudt.org/schema/qudt/PhysicalConstant",
        "vocabPrefix": "http://qudt.org/vocab/constant/",
        "short":       "qudt:PhysicalConstant"
    },
    "sou": {
        "classUri":    "http://qudt.org/schema/qudt/SystemOfUnits",
        "vocabPrefix": "http://qudt.org/vocab/sou/",
        "short":       "qudt:SystemOfUnits"
    },
    "soqk": {
        "classUri":    "http://qudt.org/schema/qudt/SystemOfQuantityKinds",
        "vocabPrefix": "http://qudt.org/vocab/soqk/",
        "short":       "qudt:SystemOfQuantityKinds"
    }
}
```

### A.3 Referenzen

| Dokument | Pfad im Repository | Beschreibung |
|----------|--------------------|--------------|
| OpenAPI-Spezifikation | `SOURCE/API_QUDT/Source_Code/openapi.yaml` | REST-API Spec |
| QUDT API (FastAPI) | `SOURCE/API_QUDT/Source_Code/api_qudt.py` | FastAPI-Implementierung |
| Wikibase API (Flask) | `SOURCE/Wikibase_API/app.py` | Flask-App-Einstiegspunkt |
| QUDT Service | `SOURCE/Wikibase_API/api_v3/qudt_service.py` | SPARQL-Service-Layer |
| QUDT Mapper (lokal) | `SOURCE/source_mapping/QUDT/qudt_mapper.py` | TTL-basierter Mapper |
| KBL Mapper | `SOURCE/source_mapping/KBL/kbl_xsd_mapper.py` | XSD-Mapper |
| VEC API | `SOURCE/source_mapping/VEC/vec_var_API.py` | VEC-Ontologie-Mapper |
| Volt-Beispiel-JSON | `SOURCE/source_mapping/QUDT/Volt.json` | Beispielausgabe |
| Lastenheft (CRS) | `PROJECT/CRS.md` | Kundenanforderungen |
| Business Case | `PROJECT/BC.md` | Wirtschaftliche Begründung |
| SAS v1.1 | `PROJECT/SAS.md` | Erste SAS-Version |
| Begriffserklärungen | `Erklaerungen.md` | Glossar |

---

*Dieses Dokument wurde auf Basis einer vollständigen Analyse des Repositories `DHBW-TINF24F/Team4-Semantic-Wikibase` erstellt und dokumentiert den aktuellen Implementierungsstand sowie die geplante Zielarchitektur des Semantic Wikibase Projekts.*
