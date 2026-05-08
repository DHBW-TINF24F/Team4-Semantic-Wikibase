import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, DCTERMS, SKOS, OWL

sys.stdout.reconfigure(encoding="utf-8")

# =========================
# Konfigurierbare Variablen
# =========================
QUDT_TTL_FILES = [
    "volt.ttl",
    "qudt-units.ttl",
    # "qudt-quantitykinds.ttl",
]

SEARCH = "Volt"              # ← Hier deinen Suchbegriff eintragen (z.B. "Kilogram", "Ampere", "Second"...)
LANG = "en"
ALLOWED_LANGS = ["en", "de"]

PREFER_SI_UNIT_ID = False

IEC61360_DATA_SPEC_IRI = "https://admin-shell.io/DataSpecificationTemplates/DataSpecificationIec61360/3"

QUDT = Namespace("http://qudt.org/schema/qudt/")


# =========================
# Hilfsfunktionen
# =========================

def local_name(uri: Union[str, URIRef]) -> str:
    """Extrahiert den lokalen Namen (letzter Teil) aus einer IRI."""
    iri = str(uri)
    if "#" in iri:
        return iri.rsplit("#", 1)[1]
    return iri.rstrip("/").rsplit("/", 1)[-1]


def clean_id_short(value: str) -> str:
    """Bereinigt einen String, sodass er als gültige AAS idShort verwendet werden kann."""
    import re
    value = re.sub(r"[^A-Za-z0-9_]", "_", value.strip())
    value = re.sub(r"_+", "_", value).strip("_")
    if not value:
        return "QudtConcept"
    if value[0].isdigit():
        return f"Q_{value}"
    return value


def clean_text(value: str) -> str:
    """Entfernt HTML- und LaTeX-Fragmente aus Texten und bereinigt Leerzeichen."""
    import re
    value = re.sub(r"<[^>]+>", " ", value.strip())
    replacements = {
        "\\textit{": "", "\\text{": "", "\\mathrm{": "", "\\frac{": "",
        "\\equiv": "≡", "\\cdot": "·", "\\times": "×", "\\ ": " ",
        "$": "", "{": "", "}": "",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return re.sub(r"\s+", " ", value).strip()


def lang_values(graph: Graph, subject: URIRef, predicates: list, default_lang: str = "en") -> list:
    """Sammelt mehrsprachige Labels oder Definitionen für ein Subjekt und gibt sie als Liste von Sprach-Text-Paaren zurück."""
    result = {}
    for pred in predicates:
        for obj in graph.objects(subject, pred):
            if isinstance(obj, Literal):
                lang = obj.language or default_lang
                result.setdefault(lang.lower(), clean_text(str(obj)))
    return [
        {"language": lang, "text": text}
        for lang, text in sorted(result.items()) if text
    ]


def first_literal(graph: Graph, subject: URIRef, predicates: list) -> Optional[str]:
    """Gibt den ersten gefundenen Literal-Wert für eines der angegebenen Prädikate zurück."""
    for pred in predicates:
        for obj in graph.objects(subject, pred):
            if isinstance(obj, Literal):
                return str(obj)
    return None


def first_uri(graph: Graph, subject: URIRef, predicates: list) -> Optional[str]:
    """Gibt die erste gefundene URI für eines der angegebenen Prädikate zurück."""
    for pred in predicates:
        for obj in graph.objects(subject, pred):
            if isinstance(obj, URIRef):
                return str(obj)
    return None


def external_ref(iri: str) -> Dict[str, Any]:
    """Erzeugt eine AAS-konforme ExternalReference für eine IRI."""
    return {
        "type": "ExternalReference",
        "keys": [{"type": "GlobalReference", "value": iri}]
    }


def detect_search_mode(search: str) -> str:
    """Erkennt, ob die Suche nach einem Begriff oder einer URI erfolgt."""
    if not search:
        return "all"
    if search.startswith(("http://", "https://")):
        return "id"
    return "term"


# =========================
# Mapping
# =========================

def empty_concept_description(uri: str) -> Dict[str, Any]:
    """Erstellt eine leere Grundstruktur für eine IEC 61360 ConceptDescription."""
    return {
        "modelType": "ConceptDescription",
        "id": uri,
        "idShort": clean_id_short(local_name(uri)),
        "embeddedDataSpecifications": [
            {
                "dataSpecification": external_ref(IEC61360_DATA_SPEC_IRI),
                "dataSpecificationContent": {
                    "modelType": "DataSpecificationIec61360",
                    "semanticId": uri,
                    "preferredName": [],
                    "shortName": [],
                    "unit": None,
                    "unitId": None,
                    "sourceOfDefinition": [],
                    "symbol": None,
                    "dataType": "STRING",
                    "definition": [],
                    "valueFormat": None,
                    "valueList": None,
                    "value": None,
                    "levelType": None,
                    #"x-qudt": {}
                }
            }
        ]
    }


def map_qudt_resource(graph: Graph, subject: URIRef, default_lang: str, prefer_si: bool) -> Dict[str, Any]:
    """Mappt eine einzelne QUDT-Ressource auf eine vollständige AAS IEC61360 ConceptDescription."""
    entity_uri = str(subject)
    result = empty_concept_description(entity_uri)
    iec = result["embeddedDataSpecifications"][0]["dataSpecificationContent"]

    iec["preferredName"] = lang_values(graph, subject, [RDFS.label, SKOS.prefLabel], default_lang)
    if not iec["preferredName"]:
        iec["preferredName"] = [{"language": default_lang, "text": local_name(subject)}]

    symbol = first_literal(graph, subject, [QUDT.symbol])
    iec["shortName"] = [{"language": default_lang, "text": clean_text(symbol or local_name(subject))[:64]}]
    iec["symbol"] = symbol

    defs = lang_values(graph, subject, [DCTERMS.description, SKOS.definition, RDFS.comment], default_lang)
    iec["definition"] = defs or [{"language": default_lang, "text": f"QUDT concept {local_name(subject)}."}]

    # Unit Handling
    if (subject, RDF.type, QUDT.Unit) in graph:
        unit_symbol = first_literal(graph, subject, [QUDT.symbol])
        unit_id = str(subject)
        if prefer_si:
            si = first_uri(graph, subject, [QUDT.siExactMatch])
            if si:
                unit_id = si
        iec["unit"] = unit_symbol
        iec["unitId"] = external_ref(unit_id) if unit_id else None

    # Category & DataType
    types = set(graph.objects(subject, RDF.type))
    if QUDT.QuantityKind in types or QUDT.PhysicalConstant in types:
        iec["dataType"] = "REAL_MEASURE"
        result["category"] = "PROPERTY"
    else:
        result["category"] = "REFERENCE"
        if QUDT.Unit in types:
            iec["dataType"] = "IRI"
        elif QUDT.Prefix in types:
            iec["dataType"] = "STRING"

    # x-qudt Felder
    # x_qudt = {}
    # x_fields = {
    #     "quantityKinds": QUDT.hasQuantityKind,
    #     "ucumCode": QUDT.ucumCode,
    #     "conversionMultiplier": QUDT.conversionMultiplier,
    #     "iec61360Code": QUDT.iec61360Code,
    # }
    # for name, pred in x_fields.items():
    #     values = [str(o) for o in graph.objects(subject, pred) if isinstance(o, (URIRef, Literal))]
    #     if values:
    #         x_qudt[name] = values[0] if len(values) == 1 else values

    # iec["x-qudt"] = x_qudt
    return result


# =========================
# TTL Laden
# =========================

def load_qudt_graph() -> Graph:
    """Lädt alle konfigurierten QUDT Turtle-Dateien in einen gemeinsamen RDF-Graphen."""
    graph = Graph()
    for file in QUDT_TTL_FILES:
        path = Path(file)
        if path.exists():
            graph.parse(str(path), format="turtle")
        else:
            print(f"Warnung: Datei nicht gefunden: {file}", file=sys.stderr)
    return graph


# =========================
# Suche
# =========================

def find_candidate(graph: Graph, search: str) -> Optional[str]:
    """Sucht nach einer QUDT-Ressource und gibt die beste Treffer-URI zurück."""
    if not search:
        return None

    if search.startswith(("http://", "https://")):
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

        if subject_local and subject_local.lower() == search_lower:
            candidates.append((0, subject_uri))
            continue

        labels = list(graph.objects(subject, RDFS.label))
        for label in labels:
            if isinstance(label, Literal) and str(label).lower() == search_lower:
                candidates.append((1, subject_uri))
                break

        if subject_local and search_lower in subject_local.lower():
            candidates.append((2, subject_uri))
            continue

        for label in labels:
            if isinstance(label, Literal) and search_lower in str(label).lower():
                candidates.append((3, subject_uri))
                break

    if not candidates:
        return None

    candidates.sort(key=lambda x: (x[0], len(x[1]), x[1]))
    return candidates[0][1]


# =========================
# Main
# =========================

def main() -> None:
    """Führt die Suche mit den im Code definierten Variablen SEARCH und LANG aus und gibt das JSON-Ergebnis aus."""
    lang = LANG if LANG in ALLOWED_LANGS else "en"
    graph = load_qudt_graph()

    if not SEARCH.strip():
        print(json.dumps({"error": "SEARCH Variable ist leer. Bitte einen Suchbegriff im Code eintragen."}, 
                        ensure_ascii=False, indent=2))
        return

    entity_uri = find_candidate(graph, SEARCH)

    if not entity_uri:
        output = {
            "query": {
                "search": SEARCH,
                "mode": detect_search_mode(SEARCH),
                "lang": lang,
                "source": "QUDT"
            },
            "total": 0,
            "result": None
        }
    else:
        mapped = map_qudt_resource(graph, URIRef(entity_uri), lang, PREFER_SI_UNIT_ID)
        output = {
            "query": {
                "search": SEARCH,
                "mode": detect_search_mode(SEARCH),
                "lang": lang,
                "source": "QUDT"
            },
            "total": 1,
            "result": mapped
        }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()