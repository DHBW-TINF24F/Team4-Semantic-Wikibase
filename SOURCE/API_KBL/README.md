# KBL to IEC61360 Mapping API

Diese Anwendung stellt eine REST-API bereit, mit der Begriffe aus der KBL-XSD-Datei abgefragt und in eine IEC61360-nahe `ConceptDescription`-JSON-Struktur umgewandelt werden können.

Die API basiert auf **FastAPI**. Dadurch wird automatisch eine **Swagger UI** erzeugt, über die die API direkt im Browser getestet werden kann.

---

## 1. Ziel der API

Die API soll XSD-Begriffe wie zum Beispiel:

- `Wire_occurrence`
- `Harness`
- `Unit`
- `Harness_content`

entgegennehmen, die KBL-XSD-Datei laden und anschließend die gefundenen XML-Schema-Informationen auf eine IEC61360-nahe Struktur mappen.

Beispiel:

```http
GET /map?search=Wire_occurrence&lang=en
```

liefert eine JSON-Antwort mit einer `ConceptDescription`.

---

## 2. Ordnerdateien

Empfohlene Struktur:

```text
projektordner/
│
├── api_kbl.py
├── openapi_kbl.yaml
└── README_openapi_kbl.md
```

- `api_kbl.py` enthält den FastAPI-Code.
- `openapi_kbl.yaml` enthält die manuell dokumentierte OpenAPI-Spezifikation.
- `README_openapi_kbl.md` erklärt Installation, Start und Test der API.

---

Prüfen, ob Python installiert ist:

```bash
python --version
```

oder:

```bash
py --version
```

---

## 3. Virtuelle Umgebung erstellen

Optional, aber empfohlen:

```bash
python -m venv .venv
```

Aktivieren unter Windows:

```bash
.venv\Scripts\activate
```

Aktivieren unter macOS/Linux:

```bash
source .venv/bin/activate
```

---

## 4. Abhängigkeiten installieren

Installiere die benötigten Python-Pakete:

```bash
pip install fastapi uvicorn requests
```

---

## 5. API starten

Die API wird mit Uvicorn gestartet:

```bash
uvicorn api_kbl:app --reload
```

Nach dem Start sollte im Terminal ungefähr Folgendes erscheinen:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

## 6. API im Browser öffnen

Root-Endpunkt:

```text
http://127.0.0.1:8000/
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## 7. Beispielanfragen

### Suche nach ComplexType

```http
GET http://127.0.0.1:8000/map?search=Wire_occurrence&lang=en
```

### Suche nach Harness

```http
GET http://127.0.0.1:8000/map?search=Harness&lang=en
```

### Suche nach Enumeration / SimpleType

```http
GET http://127.0.0.1:8000/map?search=Harness_content&lang=en
```

---

## 8. Unterstützte Query-Parameter

| Parameter | Pflicht | Beispiel | Beschreibung |
|---|---:|---|---|
| `search` | ja | `Wire_occurrence` | XSD-Begriff, z. B. `xs:complexType`, `xs:simpleType` oder `xs:element` |
| `lang` | nein | `en` | Sprache für generierte Labels, z. B. `en` oder `de` |

---

## 9. Beispielantwort

Vereinfachte Beispielantwort:

```json
{
  "query": {
    "search": "Wire_occurrence",
    "mode": "xsd-term",
    "lang": "en",
    "source": "https://ecad-wiki.prostep.org/specifications/kbl/v25-sr1/kbl2.5-sr1.xsd"
  },
  "total": 1,
  "result": {
    "modelType": "ConceptDescription",
    "id": "https://ecad-wiki.prostep.org/specifications/kbl/v25-sr1/kbl2.5-sr1.xsd#Wire_occurrence",
    "idShort": "Wire_occurrence",
    "embeddedDataSpecifications": [
      {
        "dataSpecificationContent": {
          "modelType": "DataSpecificationIec61360",
          "semanticId": {
            "property": "P1",
            "value": "https://ecad-wiki.prostep.org/specifications/kbl/v25-sr1/kbl2.5-sr1.xsd#Wire_occurrence"
          },
          "preferredName": {
            "property": "P35",
            "value": [
              {
                "value": "Wire_occurrence",
                "lang": "en"
              }
            ]
          },
          "dataType": {
            "property": "P42",
            "value": "XSDComplexType"
          }
        }
      }
    ],
    "additionalProperties": {
      "xsdType": "XSDComplexType",
      "extensionBase": "kbl:General_wire_occurrence",
      "children": [
        {
          "name": "Wire_number",
          "type": "xs:string"
        }
      ],
      "attributes": []
    }
  }
}
```

---

## 10. Was macht die API intern?

Die API führt intern folgende Schritte aus:

1. Query-Parameter auslesen  
2. Sprache validieren  
3. KBL-XSD-Datei herunterladen  
4. XSD-Datei als XML parsen  
5. Gesuchten Begriff in `xs:complexType`, `xs:simpleType` oder `xs:element` suchen  
6. XSD-Informationen extrahieren:
   - Typ
   - Vererbung
   - Kind-Elemente
   - Attribute
   - Enumerationen
7. XSD-Informationen auf IEC61360-nahe Felder mappen  
8. JSON-Antwort zurückgeben  

---
