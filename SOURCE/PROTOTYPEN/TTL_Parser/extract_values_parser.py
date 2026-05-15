import json
import os
import requests
import sys
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDFS, DCTERMS, RDF, XSD, OWL, PROV, SKOS

sys.stdout.reconfigure(encoding='utf-8')


# Definiere QUDT-Namespace für Abkürzungen
# QUDT = Namespace("http://qudt.org/schema/qudt/")
# PREFIX = Namespace("http://qudt.org/vocab/prefix/")
# QKDV = Namespace("http://qudt.org/vocab/dimensionvector/")
# QUANTITYKIND = Namespace("http://qudt.org/vocab/quantitykind/")
# SIUNIT = Namespace("https://si-digital-framework.org/SI/units/")
# SOU = Namespace("http://qudt.org/vocab/sou/")
# UNIT = Namespace("http://qudt.org/vocab/unit/")
# VAEM = Namespace("http://www.linkedmodel.org/schema/vaem#")
# VOAG = Namespace("http://voag.linkedmodel.org/schema/voag#")



def fetch_url(url: str) -> str:
    """
    Lädt den Inhalt einer URL.
    
    Args:
        url: Die URL, von der Daten heruntergeladen werden sollen
    
    Returns:
        Der Textinhalt der angeforderten URL
    """
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.text


def parse_ttl(ttl_text: str) -> Graph:
    """
    Parst TTL-Text (Turtle-Format) in einen RDF-Graph.
    
    Args:
        ttl_text: Ein String im Turtle-RDF-Format
    
    Returns:
        Ein rdflib Graph mit den geparsten RDF-Tripeln
    """
    graph = Graph()
    graph.parse(data=ttl_text, format="turtle")
    return graph


def remove_prefix(uri_string: str) -> str:
    """
    Entfernt den Namespace-Präfix aus einer URI und gibt nur den lokalen Namen zurück.
    
    Args:
        uri_string: Eine vollständige URI (z.B. "http://www.w3.org/2000/01/rdf-schema#label")
    
    Returns:
        Der lokale Teil der URI (z.B. "label")
    """
    if not uri_string:
        return ""
    
    uri_str = str(uri_string)
    # Versuche nach # zu teilen
    if "#" in uri_str:
        return uri_str.split("#")[-1]
    # Falls kein #, versuche nach letztem /
    return uri_str.split("/")[-1]


def serialize_value(obj) -> any:
    """
    Konvertiert RDF-Objekte in JSON-serialisierbare Werte.
    """
    if obj is None:
        return None
    if isinstance(obj, URIRef):
        return str(obj)
    return str(obj)


def extract_qudt_entry(graph: Graph, subject_uri: str) -> dict:
    """
    Extrahiert ALLE Informationen für eine QUDT-Unit aus dem RDF-Graph.
    Das Prädikat wird ohne Präfix gespeichert.
    
    Args:
        graph: Der RDF-Graph mit den QUDT-Daten
        subject_uri: Die URI der Einheit (z.B. "https://qudt.org/vocab/unit/V")
    
    Returns:
        Ein Dictionary mit allen Triple-Prädikaten (ohne Präfixe) als Keys
    """
    
    # Konvertiert die String-URI in ein rdflib URIRef-Objekt
    subject = URIRef(subject_uri)
    
    # Sammle alle Triple für dieses Subjekt
    result = {
        "identifier": subject_uri.rstrip("/").split("/")[-1].lower(),
        "uri": subject_uri,
        "properties": {}
    }
    
    # Iteriere über alle Triple mit diesem Subjekt
    for predicate, obj in graph.predicate_objects(subject):
        # Entferne den Präfix aus dem Prädikat
        predicate_name = remove_prefix(predicate)
        
        # Konvertiere das Objekt in einen serialisierbaren Wert
        value = serialize_value(obj)
        
        # Wenn das Prädikat bereits existiert, mache es zu einer Liste
        if predicate_name in result["properties"]:
            if not isinstance(result["properties"][predicate_name], list):
                result["properties"][predicate_name] = [result["properties"][predicate_name]]
            result["properties"][predicate_name].append(value)
        else:
            result["properties"][predicate_name] = value
    
    return result


def save_json(path: str, data: dict) -> None:
    """
    Speichert ein Dictionary als JSON-Datei.
    
    Args:
        path: Der Pfad, wo die Datei gespeichert werden soll
        data: Das Dictionary, das als JSON gespeichert wird
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # Definiere die URL der QUDT-Unit (Volt) und die entsprechende URI
    url = "https://qudt.org/vocab/unit/V.ttl"
    
    # MUSS HTTP und NICHT HTTPS sein, da die RDF-Graphen mit HTTP-URIs arbeiten
    subject_uri = "http://qudt.org/vocab/unit/V"  # Ändere zu "http://" wenn nötig

    # Lade und Parse die TTL-Datei
    ttl_text = fetch_url(url)
    graph = parse_ttl(ttl_text)

    # Debug: Prüfe Graph-Größe und ob URI existiert
    print(f"Graph hat {len(graph)} Tripel.")
    subject = URIRef(subject_uri)
    print(f"URI {subject_uri} im Graph? {subject in graph.subjects()}")

    # Debug: Zeige alle Prädikate für das Subjekt
    predicates = set(graph.predicates(subject))
    print(f"Anzahl Prädikate für {subject_uri}: {len(predicates)}")
    print(f"Prädikate: {[remove_prefix(p) for p in predicates]}\n")

    # Extrahiere die Daten für Volt aus dem Graph (jetzt mit ALLEN Triple)
    entry = extract_qudt_entry(graph, subject_uri)
    
    print(f"Extrahierte Eigenschaften: {len(entry['properties'])}\n")
    
    # Speichere die Daten als JSON
    output_path = os.path.join(os.getcwd(), "output", "qudt_volt.json")
    save_json(output_path, entry)

    # Gib die Ergebnisse in der Konsole aus
    print("Gespeicherte JSON:")
    print(json.dumps(entry, ensure_ascii=False, indent=2))