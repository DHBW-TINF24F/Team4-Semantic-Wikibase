import json
import requests
from typing import Any, Dict, List, Optional

ENDPOINT = "https://qudt.org/fuseki/qudt/query"

ALLOWED_LANGS = ["en", "de"]

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
    },
    "dimensionvector": {
        "classUri": "http://qudt.org/schema/qudt/QuantityKindDimensionVector",
        "vocabPrefix": "http://qudt.org/vocab/dimensionvector/",
        "short": "qudt:QuantityKindDimensionVector"
    },
    "constant": {
        "classUri": "http://qudt.org/schema/qudt/PhysicalConstant",
        "vocabPrefix": "http://qudt.org/vocab/constant/",
        "short": "qudt:PhysicalConstant"
    },
    "sou": {
        "classUri": "http://qudt.org/schema/qudt/SystemOfUnits",
        "vocabPrefix": "http://qudt.org/vocab/sou/",
        "short": "qudt:SystemOfUnits"
    },
    "soqk": {
        "classUri": "http://qudt.org/schema/qudt/SystemOfQuantityKinds",
        "vocabPrefix": "http://qudt.org/vocab/soqk/",
        "short": "qudt:SystemOfQuantityKinds"
    }
}


def normalize_lang(lang: str) -> str:
    if not lang:
        return "en"
    return lang if lang in ALLOWED_LANGS else "en"


def normalize_types(types_list: Optional[List[str]]) -> List[str]:
    if not types_list:
        return list(TYPE_CONFIG.keys())

    parsed = [t.strip().lower() for t in types_list if t.strip().lower() in TYPE_CONFIG]
    return parsed if parsed else list(TYPE_CONFIG.keys())


def detect_search_mode(search: str) -> str:
    if not search:
        return "term"

    s = search.strip()

    if (
        s.startswith("http://qudt.org/")
        or s.startswith("https://qudt.org/")
        or any(s.lower().startswith(prefix + ":") for prefix in [
            "unit", "quantitykind", "qkdv", "dimensionvector", "constant", "sou", "soqk"
        ])
    ):
        return "id"

    return "term"


def expand_curie(search: str) -> str:
    if not search:
        return search

    curie_map = {
        "unit": "http://qudt.org/vocab/unit/",
        "quantitykind": "http://qudt.org/vocab/quantitykind/",
        "qkdv": "http://qudt.org/vocab/dimensionvector/",
        "dimensionvector": "http://qudt.org/vocab/dimensionvector/",
        "constant": "http://qudt.org/vocab/constant/",
        "sou": "http://qudt.org/vocab/sou/",
        "soqk": "http://qudt.org/vocab/soqk/"
    }

    if ":" not in search:
        return search

    prefix, local = search.split(":", 1)
    prefix = prefix.lower()

    if prefix in curie_map:
        return curie_map[prefix] + local

    return search


def to_qname(uri: str) -> str:
    for key, cfg in TYPE_CONFIG.items():
        if uri.startswith(cfg["vocabPrefix"]):
            local = uri[len(cfg["vocabPrefix"]):]
            if key == "dimensionvector":
                return f"qkdv:{local}"
            return f"{key}:{local}"
    return uri


def local_name(uri: str) -> Optional[str]:
    if not uri:
        return None
    return uri.rstrip("/").split("/")[-1]


def predicate_field_name(predicate_uri: str) -> str:
    known = {
        "http://purl.org/dc/terms/description": "dcterms:description",
        "http://www.w3.org/2000/01/rdf-schema#label": "rdfs:label",
        "http://www.w3.org/2000/01/rdf-schema#isDefinedBy": "rdfs:isDefinedBy",
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "a",
        "http://qudt.org/schema/qudt/applicableSystem": "qudt:applicableSystem",
        "http://qudt.org/schema/qudt/conversionMultiplier": "qudt:conversionMultiplier",
        "http://qudt.org/schema/qudt/conversionMultiplierSN": "qudt:conversionMultiplierSN",
        "http://qudt.org/schema/qudt/dbpediaMatch": "qudt:dbpediaMatch",
        "http://qudt.org/schema/qudt/hasDimensionVector": "qudt:hasDimensionVector",
        "http://qudt.org/schema/qudt/hasQuantityKind": "qudt:hasQuantityKind",
        "http://qudt.org/schema/qudt/hasFactorUnit": "qudt:hasFactorUnit",
        "http://qudt.org/schema/qudt/iec61360Code": "qudt:iec61360Code",
        "http://qudt.org/schema/qudt/informativeReference": "qudt:informativeReference",
        "http://qudt.org/schema/qudt/latexDefinition": "qudt:latexDefinition",
        "http://qudt.org/schema/qudt/omUnit": "qudt:omUnit",
        "http://qudt.org/schema/qudt/siExactMatch": "qudt:siExactMatch",
        "http://qudt.org/schema/qudt/siUnitsExpression": "qudt:siUnitsExpression",
        "http://qudt.org/schema/qudt/symbol": "qudt:symbol",
        "http://qudt.org/schema/qudt/ucumCode": "qudt:ucumCode",
        "http://qudt.org/schema/qudt/udunitsCode": "qudt:udunitsCode",
        "http://qudt.org/schema/qudt/uneceCommonCode": "qudt:uneceCommonCode",
        "http://qudt.org/schema/qudt/wikidataMatch": "qudt:wikidataMatch"
    }

    if predicate_uri in known:
        return known[predicate_uri]

    if "#" in predicate_uri:
        return predicate_uri.split("#")[-1]
    return predicate_uri.rstrip("/").split("/")[-1]


def parse_literal(value: str, datatype: str) -> Any:
    if not datatype:
        return value

    datatype = datatype.lower()

    if "integer" in datatype:
        try:
            return int(value)
        except ValueError:
            return value

    if "decimal" in datatype or "double" in datatype or "float" in datatype:
        try:
            num = float(value)
            if num.is_integer():
                return int(num)
            return num
        except ValueError:
            return value

    if "boolean" in datatype:
        return value.lower() == "true"

    return value


def object_to_compact_value(obj_type: str, value: str, lang: str = "", datatype: str = "") -> Any:
    if obj_type == "uri":
        qname = to_qname(value)
        return value if qname.startswith("http") else qname

    parsed = parse_literal(value, datatype)

    if lang:
        return {"value": parsed, "lang": lang}

    return parsed


def push_unique(arr: List[Any], value: Any) -> None:
    if value is None:
        return
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)
    if not any(json.dumps(item, ensure_ascii=False, sort_keys=True) == serialized for item in arr):
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
        "additionalProperties": {}
    }


def ensure_additional_property(target: Dict[str, Any], field_name: str, value: Any) -> None:
    additional = target["additionalProperties"]

    if field_name not in additional:
        additional[field_name] = []

    if not isinstance(additional[field_name], list):
        additional[field_name] = [additional[field_name]]

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
    mapped_predicates = {
        "http://www.w3.org/2000/01/rdf-schema#label",
        "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",
        "http://qudt.org/schema/qudt/informativeReference",
        "http://qudt.org/schema/qudt/symbol",
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
        "http://qudt.org/schema/qudt/iec61360Code",
        "http://purl.org/dc/terms/description",
        "http://qudt.org/schema/qudt/latexDefinition",
        "http://qudt.org/schema/qudt/siUnitsExpression",
    }
    return predicate_uri in mapped_predicates


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


def build_detail_query(entity_uri: str, lang: str) -> str:
    return f"""
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?p ?o ?lang ?datatype
WHERE {{
  BIND(<{entity_uri}> AS ?s)

  ?s ?p ?o .

  BIND(LANG(?o) AS ?lang)
  BIND(DATATYPE(?o) AS ?datatype)

  FILTER(
    !isLiteral(?o) ||
    LANG(?o) = "{lang}" ||
    LANG(?o) = "" ||
    LANG(?o) = "en" ||
    ?p = rdfs:label ||
    ?p = dcterms:description
  )
}}
"""


def run_sparql(query: str) -> Dict[str, Any]:
    response = requests.get(
        ENDPOINT,
        params={"query": query},
        headers={
            "Accept": "application/sparql-results+json",
            "User-Agent": "QUDT-SemanticHub-IEC61360-Bridge/1.0"
        },
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def map_rows_to_semantichub(entity_uri: str, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
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

        if not is_mapped_predicate(predicate_uri):
            ensure_additional_property(result, field_name, compact_value)

        if predicate_uri == "http://www.w3.org/2000/01/rdf-schema#label":
            push_unique(iec["preferredName"]["value"], compact_value)

            if iec["unit"]["value"] is None:
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

    if not iec["preferredName"]["value"]:
        iec["preferredName"]["value"] = None

    if not iec["sourceOfDefinition"]["value"]:
        iec["sourceOfDefinition"]["value"] = None

    if not iec["Definition"]["value"]:
        iec["Definition"]["value"] = None

    finalize_additional_properties(result)
    return result


def search_qudt(search: str, lang: str = "en", types: Optional[List[str]] = None) -> Dict[str, Any]:
    lang = normalize_lang(lang)
    selected_types = normalize_types(types)

    if not search.strip():
        return {
            "query": {
                "search": search,
                "mode": "term",
                "lang": lang,
                "types": selected_types
            },
            "total": 0,
            "result": None,
            "error": "SEARCH darf nicht leer sein."
        }

    mode = detect_search_mode(search)

    candidate_query = build_candidate_query(
        search=search,
        mode=mode,
        lang=lang,
        selected_types=selected_types
    )

    candidate_data = run_sparql(candidate_query)
    candidates = candidate_data.get("results", {}).get("bindings", [])

    if not candidates:
        return {
            "query": {
                "search": search,
                "mode": mode,
                "lang": lang,
                "types": selected_types
            },
            "total": 0,
            "result": None
        }

    entity_uri = candidates[0]["entity"]["value"]

    detail_query = build_detail_query(entity_uri, lang)
    detail_data = run_sparql(detail_query)
    detail_rows = detail_data.get("results", {}).get("bindings", [])

    mapped = map_rows_to_semantichub(entity_uri, detail_rows)

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