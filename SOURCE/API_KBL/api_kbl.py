# Importiert JSON-Funktionen
import json

# Typdefinitionen
from typing import Any, Dict, List, Optional

# HTTP Requests zum Laden der KBL-XSD-Datei
import requests

# XML Parser für XSD
import xml.etree.ElementTree as ET

# FastAPI Framework für REST API
from fastapi import FastAPI, Query, HTTPException

# Erstellt die FastAPI-Anwendung
app = FastAPI(
    title="KBL to IEC61360 Mapping API",
    description="API zum Abfragen von KBL-XSD-Strukturen und Mapping auf IEC61360.",
    version="1.0.0"
)

# =========================
# KBL XSD Quelle
# =========================

KBL_XSD_URL = "https://ecad-wiki.prostep.org/specifications/kbl/v25-sr1/kbl2.5-sr1.xsd"

# Erlaubte Sprachen
ALLOWED_LANGS = ["en", "de"]

# XML Schema Namespace
XS_NS = {"xs": "http://www.w3.org/2001/XMLSchema"}


# =========================
# Hilfsfunktionen
# =========================

def normalize_lang(lang: str) -> str:
    if not lang:
        return "en"

    return lang if lang in ALLOWED_LANGS else "en"


def create_iec_field(property_number: str, value: Any = None) -> Dict[str, Any]:
    return {
        "property": property_number,
        "value": value
    }


def get_text(elem: Optional[ET.Element]) -> Optional[str]:
    if elem is None or elem.text is None:
        return None

    return elem.text.strip()


def empty_concept_description(identifier: str, id_short: str, lang: str) -> Dict[str, Any]:
    semantic_id = f"{KBL_XSD_URL}#{identifier}"

    return {
        "modelType": "ConceptDescription",
        "id": semantic_id,
        "idShort": id_short,
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
                    "semanticId": create_iec_field("P1", semantic_id),
                    "preferredName": create_iec_field("P35", [
                        {
                            "value": id_short,
                            "lang": lang
                        }
                    ]),
                    "shortName": create_iec_field("P36", id_short),
                    "unit": create_iec_field("P37", None),
                    "sourceOfDefinition": create_iec_field("P40", [
                        {
                            "type": "xsdSource",
                            "value": KBL_XSD_URL
                        }
                    ]),
                    "Symbol": create_iec_field("P41", None),
                    "dataType": create_iec_field("P42", None),
                    "unitId": create_iec_field("P43", None),
                    "Definition": create_iec_field("P44", None),
                    "valueFormat": create_iec_field("P45", None),
                    "valueList": create_iec_field("P46", None),
                    "value": create_iec_field("P47", None),
                    "levelType": create_iec_field("P48", None)
                }
            }
        ],
        "additionalProperties": {}
    }


def detect_xsd_type(elem: ET.Element) -> str:
    tag = elem.tag.split("}")[-1]

    if tag == "complexType":
        return "XSDComplexType"

    if tag == "simpleType":
        return "XSDSimpleType"

    if tag == "element":
        return "XSDElement"

    return tag


def collect_extension_base(type_elem: ET.Element) -> Optional[str]:
    extension = type_elem.find(".//xs:extension", XS_NS)

    if extension is not None:
        return extension.get("base")

    return None


def collect_child_elements(type_elem: ET.Element) -> List[Dict[str, Any]]:
    children = []

    for elem in type_elem.findall(".//xs:element", XS_NS):
        name = elem.get("name")
        typ = elem.get("type")
        min_occurs = elem.get("minOccurs")
        max_occurs = elem.get("maxOccurs")
        documentation = get_text(elem.find(".//xs:documentation", XS_NS))

        if name is not None:
            children.append({
                "name": name,
                "type": typ,
                "minOccurs": min_occurs,
                "maxOccurs": max_occurs,
                "documentation": documentation
            })

    return children


def collect_attributes(type_elem: ET.Element) -> List[Dict[str, Any]]:
    attributes = []

    for attr in type_elem.findall(".//xs:attribute", XS_NS):
        attributes.append({
            "name": attr.get("name"),
            "type": attr.get("type"),
            "use": attr.get("use")
        })

    return attributes


def collect_enumerations(type_elem: ET.Element) -> List[str]:
    values = []

    for enum in type_elem.findall(".//xs:enumeration", XS_NS):
        value = enum.get("value")

        if value:
            values.append(value)

    return values


def load_xsd_root() -> ET.Element:
    try:
        response = requests.get(
            KBL_XSD_URL,
            headers={
                "Accept": "application/xml,text/xml,*/*",
                "User-Agent": "KBL-SemanticHub-IEC61360-Bridge/1.0"
            },
            timeout=30
        )

        response.raise_for_status()

        return ET.fromstring(response.text)

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"KBL XSD konnte nicht geladen werden: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"KBL XSD konnte nicht geparst werden: {str(e)}"
        )


def find_candidate(root: ET.Element, search: str) -> Optional[ET.Element]:
    for elem in root.findall(".//xs:complexType", XS_NS):
        if elem.get("name") == search:
            return elem

    for elem in root.findall(".//xs:simpleType", XS_NS):
        if elem.get("name") == search:
            return elem

    for elem in root.findall(".//xs:element", XS_NS):
        if elem.get("name") == search:
            return elem

    return None


def map_xsd_element_to_semantichub(elem: ET.Element, lang: str) -> Dict[str, Any]:
    name = elem.get("name")

    if not name:
        raise HTTPException(
            status_code=500,
            detail="XSD-Element hat keinen Namen."
        )

    xsd_type = detect_xsd_type(elem)

    result = empty_concept_description(name, name, lang)
    iec = result["embeddedDataSpecifications"][0]["dataSpecificationContent"]

    iec["dataType"]["value"] = xsd_type

    documentation = get_text(elem.find(".//xs:documentation", XS_NS))

    if documentation:
        iec["Definition"]["value"] = [
            {
                "type": "documentation",
                "value": documentation
            }
        ]
    else:
        iec["Definition"]["value"] = [
            {
                "type": "generatedDefinition",
                "value": f"{name} is defined in the KBL 2.5 SR-1 XML schema as {xsd_type}."
            }
        ]

    child_elements = collect_child_elements(elem)
    attributes = collect_attributes(elem)
    enumerations = collect_enumerations(elem)
    extension_base = collect_extension_base(elem)

    if enumerations:
        iec["valueList"]["value"] = enumerations

    result["additionalProperties"] = {
        "xsdType": xsd_type,
        "extensionBase": extension_base,
        "children": child_elements,
        "attributes": attributes
    }

    if enumerations:
        result["additionalProperties"]["enumerations"] = enumerations

    return result


# =========================
# API Endpunkte
# =========================

@app.get("/")
def root():
    return {
        "message": "KBL to IEC61360 Mapping API",
        "swagger": "/docs"
    }


@app.get("/map")
def map_kbl_to_iec61360(
    search: str = Query(..., description="XSD-Begriff, z. B. Wire_occurrence, Harness oder Unit"),
    lang: str = Query("en", description="Sprache, z. B. en oder de")
):
    lang = normalize_lang(lang)

    if not search.strip():
        raise HTTPException(
            status_code=400,
            detail="Parameter 'search' darf nicht leer sein."
        )

    root_xml = load_xsd_root()

    candidate = find_candidate(root_xml, search)

    if candidate is None:
        return {
            "query": {
                "search": search,
                "mode": "xsd-term",
                "lang": lang,
                "source": KBL_XSD_URL
            },
            "total": 0,
            "result": None
        }

    mapped = map_xsd_element_to_semantichub(candidate, lang)

    return {
        "query": {
            "search": search,
            "mode": "xsd-term",
            "lang": lang,
            "source": KBL_XSD_URL
        },
        "total": 1,
        "result": mapped
    }