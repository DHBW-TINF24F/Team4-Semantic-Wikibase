# Importiert JSON-Funktionen
import json

# Importiert Systemfunktionen
import sys

# Typdefinitionen
from typing import Any, Dict, List, Optional

# HTTP Requests zum Laden der VEC-TTL-Datei
import requests

# FastAPI Framework für REST API
from fastapi import FastAPI, Query, HTTPException

# RDF Parser
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL

# UTF-8 Ausgabe aktivieren
sys.stdout.reconfigure(encoding="utf-8")

# Erstellt die FastAPI-Anwendung
app = FastAPI(
    title="VEC to IEC61360 Mapping API",
    description="API zum Abfragen von VEC-Daten aus einer TTL-Datei und Mapping auf IEC61360.",
    version="1.0.0"
)

# =========================
# VEC TTL Quelle
# =========================

VEC_TTL_URL = "https://ecad-wiki.prostep.org/specifications/vec/v220/vec-2.2.0-ontology.ttl"

# Erlaubte Sprachen
ALLOWED_LANGS = ["en", "de"]


# =========================
# Hilfsfunktionen
# =========================

def normalize_lang(lang: str) -> str:
    if not lang:
        return "en"

    return lang if lang in ALLOWED_LANGS else "en"


def local_name(uri: str) -> Optional[str]:
    if not uri:
        return None

    if "#" in uri:
        return uri.split("#")[-1]

    return uri.rstrip("/").split("/")[-1]


def detect_search_mode(search: str) -> str:
    if not search:
        return "term"

    s = search.strip()

    if s.startswith("http://") or s.startswith("https://"):
        return "id"

    return "term"


def parse_literal(value: Any) -> Any:
    if isinstance(value, Literal):
        if value.datatype:
            datatype = str(value.datatype).lower()

            if "integer" in datatype:
                try:
                    return int(value)
                except ValueError:
                    return str(value)

            if "decimal" in datatype or "double" in datatype or "float" in datatype:
                try:
                    num = float(value)
                    if num.is_integer():
                        return int(num)
                    return num
                except ValueError:
                    return str(value)

            if "boolean" in datatype:
                return str(value).lower() == "true"

        if value.language:
            return {
                "value": str(value),
                "lang": value.language
            }

        return str(value)

    return str(value)


def predicate_field_name(predicate_uri: str) -> str:
    known = {
        str(RDF.type): "a",
        str(RDFS.label): "rdfs:label",
        str(RDFS.comment): "rdfs:comment",
        str(RDFS.isDefinedBy): "rdfs:isDefinedBy",
        str(RDFS.domain): "rdfs:domain",
        str(RDFS.range): "rdfs:range",
        str(RDFS.subClassOf): "rdfs:subClassOf",
        str(OWL.versionInfo): "owl:versionInfo",
    }

    if predicate_uri in known:
        return known[predicate_uri]

    if "#" in predicate_uri:
        return predicate_uri.split("#")[-1]

    return predicate_uri.rstrip("/").split("/")[-1]


def compact_value(obj: Any) -> Any:
    if isinstance(obj, URIRef):
        return str(obj)

    if isinstance(obj, Literal):
        return parse_literal(obj)

    return str(obj)


def push_unique(arr: List[Any], value: Any) -> None:
    if value is None:
        return

    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)

    if not any(
        json.dumps(item, ensure_ascii=False, sort_keys=True) == serialized
        for item in arr
    ):
        arr.append(value)


def create_iec_field(property_number: str, value: Any = None) -> Dict[str, Any]:
    return {
        "property": property_number,
        "value": value
    }


def empty_concept_description(uri: str) -> Dict[str, Any]:
    return {
        "modelType": "ConceptDescription",
        "id": uri,
        "idShort": local_name(uri),
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
                    "semanticId": create_iec_field("P1", uri),
                    "preferredName": create_iec_field("P35", []),
                    "shortName": create_iec_field("P36", local_name(uri)),
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
        "additionalProperties": {}
    }


def ensure_additional_property(
    target: Dict[str, Any],
    field_name: str,
    value: Any
) -> None:
    additional = target["additionalProperties"]

    if field_name not in additional:
        additional[field_name] = []

    push_unique(additional[field_name], value)


def finalize_additional_properties(obj: Dict[str, Any]) -> None:
    additional = obj["additionalProperties"]

    for key in list(additional.keys()):
        val = additional[key]

        if isinstance(val, list) and len(val) == 1:
            additional[key] = val[0]
        elif isinstance(val, list) and len(val) == 0:
            additional[key] = None


def is_mapped_predicate(predicate_uri: str) -> bool:
    mapped = {
        str(RDF.type),
        str(RDFS.label),
        str(RDFS.comment),
        str(RDFS.isDefinedBy),
        str(OWL.versionInfo),
    }

    return predicate_uri in mapped


# =========================
# TTL laden
# =========================

def load_vec_graph() -> Graph:
    try:
        response = requests.get(
            VEC_TTL_URL,
            headers={
                "Accept": "text/turtle",
                "User-Agent": "VEC-SemanticHub-IEC61360-Bridge/1.0"
            },
            timeout=30
        )

        response.raise_for_status()

        graph = Graph()
        graph.parse(data=response.text, format="turtle")

        return graph

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"VEC TTL konnte nicht geladen werden: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"VEC TTL konnte nicht geparst werden: {str(e)}"
        )


# =========================
# Suche
# =========================

def find_candidate(graph: Graph, search: str, lang: str) -> Optional[str]:
    mode = detect_search_mode(search)

    if mode == "id":
        uri = URIRef(search.strip())

        if (uri, None, None) in graph:
            return str(uri)

        return None

    search_lower = search.lower().strip()
    candidates = []

    for subject in set(graph.subjects()):
        if not isinstance(subject, URIRef):
            continue

        subject_uri = str(subject)
        subject_local = local_name(subject_uri)

        labels = list(graph.objects(subject, RDFS.label))

        # 1. Exakter LocalName Treffer
        if subject_local and subject_local.lower() == search_lower:
            candidates.append((0, subject_uri))
            continue

        # 2. Exakter Label Treffer
        for label in labels:
            if isinstance(label, Literal):
                label_text = str(label)

                if label.language and label.language not in [lang, "en"]:
                    continue

                if label_text.lower() == search_lower:
                    candidates.append((1, subject_uri))
                    break

        # 3. Enthält LocalName
        if subject_local and search_lower in subject_local.lower():
            candidates.append((2, subject_uri))
            continue

        # 4. Enthält Label
        for label in labels:
            if isinstance(label, Literal):
                label_text = str(label)

                if search_lower in label_text.lower():
                    candidates.append((3, subject_uri))
                    break

    if not candidates:
        return None

    candidates.sort(key=lambda x: (x[0], len(x[1]), x[1]))

    return candidates[0][1]


# =========================
# Mapping
# =========================

def map_resource_to_semantichub(
    graph: Graph,
    entity_uri: str,
    lang: str
) -> Dict[str, Any]:

    entity = URIRef(entity_uri)
    result = empty_concept_description(entity_uri)
    iec = result["embeddedDataSpecifications"][0]["dataSpecificationContent"]

    for predicate, obj in graph.predicate_objects(entity):
        predicate_uri = str(predicate)
        field_name = predicate_field_name(predicate_uri)
        value = compact_value(obj)

        # additionalProperties nur für nicht gemappte Felder
        if not is_mapped_predicate(predicate_uri):
            ensure_additional_property(result, field_name, value)

        # rdfs:label → preferredName
        if predicate == RDFS.label:
            if isinstance(obj, Literal):
                if obj.language in [lang, "en", None]:
                    push_unique(iec["preferredName"]["value"], value)

        # rdfs:comment → Definition
        elif predicate == RDFS.comment:
            if isinstance(obj, Literal):
                if obj.language in [lang, "en", None]:
                    push_unique(iec["Definition"]["value"], {
                        "type": "comment",
                        "value": str(obj)
                    })

        # rdfs:isDefinedBy → sourceOfDefinition
        elif predicate == RDFS.isDefinedBy:
            push_unique(iec["sourceOfDefinition"]["value"], value)

        # owl:versionInfo → sourceOfDefinition
        elif predicate == OWL.versionInfo:
            push_unique(iec["sourceOfDefinition"]["value"], {
                "type": "versionInfo",
                "value": value
            })

        # rdf:type → dataType
        elif predicate == RDF.type:
            type_local = local_name(str(obj))

            if type_local in ["Class", "ObjectProperty", "DatatypeProperty"]:
                iec["dataType"]["value"] = type_local
            elif iec["dataType"]["value"] is None:
                iec["dataType"]["value"] = value

    # Leere Listen behandeln
    if not iec["preferredName"]["value"]:
        iec["preferredName"]["value"] = None

    if not iec["sourceOfDefinition"]["value"]:
        iec["sourceOfDefinition"]["value"] = [
            {
                "type": "ontologySource",
                "value": VEC_TTL_URL
            }
        ]

    if not iec["Definition"]["value"]:
        iec["Definition"]["value"] = None

    finalize_additional_properties(result)

    return result


# =========================
# API Endpunkte
# =========================

@app.get("/")
def root():
    return {
        "message": "VEC to IEC61360 Mapping API",
        "swagger": "/docs"
    }


@app.get("/map")
def map_vec_to_iec61360(
    search: str = Query(..., description="Suchbegriff oder vollständige VEC-URI"),
    lang: str = Query("en", description="Sprache, z. B. en oder de")
):
    lang = normalize_lang(lang)

    if not search.strip():
        raise HTTPException(
            status_code=400,
            detail="Parameter 'search' darf nicht leer sein."
        )

    mode = detect_search_mode(search)

    graph = load_vec_graph()

    entity_uri = find_candidate(graph, search, lang)

    if not entity_uri:
        return {
            "query": {
                "search": search,
                "mode": mode,
                "lang": lang,
                "source": VEC_TTL_URL
            },
            "total": 0,
            "result": None
        }

    mapped = map_resource_to_semantichub(graph, entity_uri, lang)

    return {
        "query": {
            "search": search,
            "mode": mode,
            "lang": lang,
            "source": VEC_TTL_URL
        },
        "total": 1,
        "result": mapped
    }