# Importiert JSON-Funktionen
import json

# Importiert Systemfunktionen
import sys

# Typdefinitionen für bessere Lesbarkeit und Swagger-Dokumentation
from typing import Any, Dict, List, Optional

# HTTP Requests für SPARQL-Abfragen
import requests

# FastAPI Framework für REST API
from fastapi import FastAPI, Query, HTTPException

# UTF-8 Ausgabe aktivieren
sys.stdout.reconfigure(encoding="utf-8")

# Erstellt die FastAPI-Anwendung
app = FastAPI(
    title="QUDT to IEC61360 Mapping API",
    description="API zum Abfragen von QUDT-Daten und Mapping auf IEC61360.",
    version="1.0.0"
)

# SPARQL Endpoint von QUDT
ENDPOINT = "https://qudt.org/fuseki/qudt/query"

# Erlaubte Sprachen
ALLOWED_LANGS = ["en", "de"]

# Konfiguration der unterstützten QUDT-Typen
TYPE_CONFIG = {
    "unit": {
        "classUri": "http://qudt.org/schema/qudt/Unit",
        "vocabPrefix": "http://qudt.org/vocab/unit/",
        "short": "qudt:Unit"
    },
    "quantitykind": {
        "classUri": "http://qudt.org/schema/qudt/QuantityKind",
        "vocabPrefix": "http://qudt.org/vocab/quantitykind/",
        "short": "qudt:QuantityKind"
    }
}


# Normalisiert die Sprache auf erlaubte Werte
def normalize_lang(lang: str) -> str:
    if not lang:
        return "en"

    return lang if lang in ALLOWED_LANGS else "en"


# Validiert und normalisiert die übergebenen Typen
def normalize_types(types_list: Optional[List[str]]) -> List[str]:
    if not types_list:
        return list(TYPE_CONFIG.keys())

    parsed = [
        t.strip().lower()
        for t in types_list
        if t.strip().lower() in TYPE_CONFIG
    ]

    return parsed if parsed else list(TYPE_CONFIG.keys())


# Erkennt ob nach Begriff oder Semantic-ID gesucht wird
def detect_search_mode(search: str) -> str:
    if not search:
        return "term"

    s = search.strip()

    if (
        s.startswith("http://qudt.org/")
        or s.startswith("https://qudt.org/")
        or s.lower().startswith("unit:")
    ):
        return "id"

    return "term"


# Wandelt CURIEs wie unit:V in vollständige URIs um
def expand_curie(search: str) -> str:
    curie_map = {
        "unit": "http://qudt.org/vocab/unit/"
    }

    if ":" not in search:
        return search

    prefix, local = search.split(":", 1)

    if prefix in curie_map:
        return curie_map[prefix] + local

    return search


# Wandelt eine URI in eine kompakte QNAME-Schreibweise um
def to_qname(uri: str) -> str:
    for key, cfg in TYPE_CONFIG.items():
        if uri.startswith(cfg["vocabPrefix"]):
            local = uri[len(cfg["vocabPrefix"]):]
            return f"{key}:{local}"

    return uri


# Extrahiert den letzten Teil einer URI
def local_name(uri: str) -> Optional[str]:
    if not uri:
        return None

    return uri.rstrip("/").split("/")[-1]


# Wandelt bekannte Predicate-URIs in lesbare Feldnamen um
def predicate_field_name(predicate_uri: str) -> str:
    known = {
        "http://www.w3.org/2000/01/rdf-schema#label": "rdfs:label",
        "http://purl.org/dc/terms/description": "dcterms:description",
        "http://qudt.org/schema/qudt/symbol": "qudt:symbol"
    }

    if predicate_uri in known:
        return known[predicate_uri]

    if "#" in predicate_uri:
        return predicate_uri.split("#")[-1]

    return predicate_uri.rstrip("/").split("/")[-1]


# Konvertiert RDF-Literale in passende Python-Datentypen
def parse_literal(value: str, datatype: str) -> Any:
    if not datatype:
        return value

    datatype = datatype.lower()

    if "integer" in datatype:
        try:
            return int(value)
        except ValueError:
            return value

    if "decimal" in datatype or "double" in datatype:
        try:
            return float(value)
        except ValueError:
            return value

    return value


# Konvertiert RDF-Objekte in kompakte JSON-Werte
def object_to_compact_value(
    obj_type: str,
    value: str,
    lang: str = "",
    datatype: str = ""
) -> Any:

    if obj_type == "uri":
        return to_qname(value)

    parsed = parse_literal(value, datatype)

    if lang:
        return {
            "value": parsed,
            "lang": lang
        }

    return parsed


# Fügt Werte nur hinzu wenn sie noch nicht existieren
def push_unique(arr: List[Any], value: Any) -> None:
    if value is None:
        return

    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)

    if not any(
        json.dumps(item, ensure_ascii=False, sort_keys=True) == serialized
        for item in arr
    ):
        arr.append(value)


# Erstellt ein IEC61360 Property-Feld
def create_iec_field(property_number: str, value: Any = None) -> Dict[str, Any]:
    return {
        "property": property_number,
        "value": value
    }


# Erstellt eine leere IEC61360 ConceptDescription-Struktur
def empty_concept_description(uri: str) -> Dict[str, Any]:
    return {
        "modelType": "ConceptDescription",
        "id": uri,
        "idShort": local_name(uri),
        "embeddedDataSpecifications": [
            {
                "dataSpecificationContent": {
                    "modelType": "DataSpecificationIec61360",
                    "semanticId": create_iec_field("P1", uri),
                    "preferredName": create_iec_field("P35", []),
                    "shortName": create_iec_field("P36", None),
                    "unit": create_iec_field("P37", None),
                    "sourceOfDefinition": create_iec_field("P40", []),
                    "Symbol": create_iec_field("P41", None),
                    "dataType": create_iec_field("P42", None),
                    "unitId": create_iec_field("P43", None),
                    "Definition": create_iec_field("P44", []),
                    "valueFormat": create_iec_field("P45", None),
                    "valueList": create_iec_field("P46", None),
                    "value": create_iec_field("P47", None),
                    "levelType": create_iec_field("P48", None)
                }
            }
        ],
        #"additionalProperties": {}
    }


# Fügt zusätzliche nicht gemappte Properties hinzu
def ensure_additional_property(
    target: Dict[str, Any],
    field_name: str,
    value: Any
) -> None:

    additional = target["additionalProperties"]

    if field_name not in additional:
        additional[field_name] = []

    push_unique(additional[field_name], value)


# Vereinfacht Listen mit nur einem Element
def finalize_additional_properties(obj: Dict[str, Any]) -> None:
    additional = obj["additionalProperties"]

    for key in list(additional.keys()):
        val = additional[key]

        if isinstance(val, list) and len(val) == 1:
            additional[key] = val[0]


# Prüft ob ein Predicate bereits auf IEC61360 gemappt wird
def is_mapped_predicate(predicate_uri: str) -> bool:
    mapped_predicates = {
        "http://www.w3.org/2000/01/rdf-schema#label",
        "http://purl.org/dc/terms/description"
    }

    return predicate_uri in mapped_predicates


# Baut die SPARQL-Abfrage zur Suche eines passenden Kandidaten
def build_candidate_query(search: str, mode: str, lang: str, selected_types: List[str]) -> str:
    safe_search = search.replace('"', '\\"')
    type_values = " ".join(f"<{TYPE_CONFIG[t]['classUri']}>" for t in selected_types)
    prefix_filters = " || ".join(
        f'STRSTARTS(STR(?entity), "{TYPE_CONFIG[t]["vocabPrefix"]}")' for t in selected_types
    )

    expanded = expand_curie(search)
    safe_expanded = expanded.replace('"', '\\"')

    if mode == "id":
        filter_block = f'''
      FILTER(STR(?entity) = "{safe_expanded}")
      BIND(0 AS ?rank)
'''
        ranking_block = ""
    else:
        filter_block = f'''
      FILTER(
        (BOUND(?label) && LCASE(STR(?label)) = LCASE("{safe_search}")) ||
        LCASE(REPLACE(STR(?entity), "^.+[/#]", "")) = LCASE("{safe_search}") ||
        (BOUND(?symbol) && LCASE(STR(?symbol)) = LCASE("{safe_search}")) ||
        (BOUND(?label) && CONTAINS(LCASE(STR(?label)), LCASE("{safe_search}")))
      )
'''
        ranking_block = f'''
      BIND(
        IF(BOUND(?label) && LCASE(STR(?label)) = LCASE("{safe_search}"), 0,
          IF(LCASE(REPLACE(STR(?entity), "^.+[/#]", "")) = LCASE("{safe_search}"), 1,
            IF(BOUND(?symbol) && LCASE(STR(?symbol)) = LCASE("{safe_search}"), 2, 3)
          )
        ) AS ?rank
      )
'''

    return f"""
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?entity ?entityType ?label ?symbol ?rank
WHERE {{
  VALUES ?entityType {{ {type_values} }}

  ?entity a ?entityType .
  FILTER({prefix_filters})

  OPTIONAL {{
    ?entity rdfs:label ?label .
    FILTER(LANG(?label) = "{lang}" || LANG(?label) = "" || LANG(?label) = "en")
  }}

  OPTIONAL {{ ?entity qudt:symbol ?symbol . }}

  {filter_block}
  {ranking_block}
}}
ORDER BY ?rank STRLEN(STR(?label)) ?entity
LIMIT 1
"""



# Baut die SPARQL-Abfrage für alle Properties eines Objekts
def build_detail_query(entity_uri: str, lang: str) -> str:
    return f"""
SELECT ?p ?o ?lang ?datatype
WHERE {{
  BIND(<{entity_uri}> AS ?s)

  ?s ?p ?o .

  BIND(LANG(?o) AS ?lang)
  BIND(DATATYPE(?o) AS ?datatype)
}}
"""


# Führt eine SPARQL-Abfrage gegen QUDT aus
def run_sparql(query: str) -> Dict[str, Any]:

    try:
        response = requests.get(
            ENDPOINT,
            params={"query": query},
            headers={
                "Accept": "application/sparql-results+json"
            },
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"QUDT Fehler: {str(e)}"
        )


# Mappt RDF-Properties auf IEC61360 Felder

def map_rows_to_semantichub(entity_uri: str, rows: List[Dict[str, Any]], selected_lang: str) -> Dict[str, Any]:
    result = empty_concept_description(entity_uri)
    iec = result["embeddedDataSpecifications"][0]["dataSpecificationContent"]

    for row in rows:
        predicate_uri = row.get("p", {}).get("value")
        obj = row.get("o")

        if not predicate_uri or not obj:
            continue

        field_name = predicate_field_name(predicate_uri)
        compact_value = object_to_compact_value(
            obj_type=obj.get("type", ""),
            value=obj.get("value", ""),
            lang=row.get("lang", {}).get("value", ""),
            datatype=row.get("datatype", {}).get("value", "")
        )

        # Nur nicht bereits gemappte Properties zusätzlich aufnehmen
        #if not is_mapped_predicate(predicate_uri):
            #ensure_additional_property(result, field_name, compact_value)

        # Mapping auf IEC61360-Felder
        if predicate_uri == "http://www.w3.org/2000/01/rdf-schema#label":
            label_lang = row.get("lang", {}).get("value", "")

            # Nur gewählte Sprache oder Englisch als Fallback speichern
            if label_lang == selected_lang:
                iec["preferredName"]["value"] = [compact_value]

            elif label_lang == "en" and not iec["preferredName"]["value"]:
                iec["preferredName"]["value"] = [compact_value]

            # unit nur setzen, wenn Label zur gewählten Sprache passt
            if iec["unit"]["value"] is None and label_lang in [selected_lang, "en"]:
                if isinstance(compact_value, str):
                    iec["unit"]["value"] = compact_value
                elif isinstance(compact_value, dict) and "value" in compact_value:
                    iec["unit"]["value"] = compact_value["value"]

        elif predicate_uri in {
            "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",
            "http://qudt.org/schema/qudt/informativeReference"
        }:
            push_unique(iec["sourceOfDefinition"]["value"], compact_value)

        elif predicate_uri == "http://qudt.org/schema/qudt/symbol":
            if iec["Symbol"]["value"] is None:
                iec["Symbol"]["value"] = compact_value

        elif predicate_uri == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
            if iec["dataType"]["value"] is None:
                iec["dataType"]["value"] = compact_value

        elif predicate_uri == "http://qudt.org/schema/qudt/iec61360Code":
            if iec["unitId"]["value"] is None:
                iec["unitId"]["value"] = compact_value

        elif predicate_uri == "http://purl.org/dc/terms/description":
            push_unique(iec["Definition"]["value"], {
                "type": "description",
                "value": obj.get("value")
            })

        elif predicate_uri == "http://qudt.org/schema/qudt/latexDefinition":
            push_unique(iec["Definition"]["value"], {
                "type": "latexDefinition",
                "value": obj.get("value")
            })

        elif predicate_uri == "http://qudt.org/schema/qudt/siUnitsExpression":
            if iec["valueFormat"]["value"] is None:
                iec["valueFormat"]["value"] = compact_value

    # Falls preferredName leer, dann null
    if not iec["preferredName"]["value"]:
        iec["preferredName"]["value"] = None

    if not iec["sourceOfDefinition"]["value"]:
        iec["sourceOfDefinition"]["value"] = None

    if not iec["Definition"]["value"]:
        iec["Definition"]["value"] = None

    #finalize_additional_properties(result)
    return result


# Root-Endpunkt der API
@app.get("/")
def root():
    return {
        "message": "QUDT to IEC61360 Mapping API",
        "swagger": "/docs"
    }


# Haupt-Endpunkt zum Mapping von QUDT auf IEC61360
@app.get("/map")
def map_qudt_to_iec61360(
    search: str = Query(...),
    lang: str = Query("en"),
    types: Optional[List[str]] = Query(default=None)
):

    lang = normalize_lang(lang)

    selected_types = normalize_types(types)

    mode = detect_search_mode(search)

    candidate_query = build_candidate_query(
        search,
        mode,
        lang,
        selected_types
    )

    candidate_data = run_sparql(candidate_query)

    candidates = candidate_data.get("results", {}).get("bindings", [])

    if not candidates:
        return {
            "total": 0,
            "result": None
        }

    entity_uri = candidates[0]["entity"]["value"]

    detail_query = build_detail_query(entity_uri, lang)

    detail_data = run_sparql(detail_query)

    detail_rows = detail_data.get("results", {}).get("bindings", [])

    mapped = map_rows_to_semantichub(entity_uri, detail_rows, lang)

    return {
        "query": {
            "search": search,
            "mode": mode,
            "lang": lang,
            "types": selected_types
        },
        "total": 1,
        "result": mapped
    }