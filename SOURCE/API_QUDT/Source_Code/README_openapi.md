# QUDT to IEC61360 Mapping API

Diese Anwendung stellt eine REST-API bereit, mit der semantische Begriffe aus QUDT abgefragt und in eine IEC61360-nahe `ConceptDescription`-JSON-Struktur umgewandelt werden können.

Die API basiert auf **FastAPI**. Dadurch wird automatisch eine **Swagger UI** erzeugt, über die die API direkt im Browser getestet werden kann.

---

## 1. Ziel der API

Die API soll Begriffe wie zum Beispiel:

- `Volt`
- `unit:V`
- `http://qudt.org/vocab/unit/V`

entgegennehmen, über den QUDT-SPARQL-Endpunkt abfragen und anschließend die gefundenen RDF-Daten auf eine IEC61360-nahe Struktur mappen.

Beispiel:

```http
GET /map?search=Volt&lang=en&types=unit
```

liefert eine JSON-Antwort mit einer `ConceptDescription`.

---

## 2. Ordnerdateien

Empfohlene Struktur:

```text
projektordner/
│
├── api_qudt.py
├── openapi.yaml
└── README.md
```

- `api_qudt.py` enthält den FastAPI-Code.
- `openapi.yaml` enthält die manuell dokumentierte OpenAPI-Spezifikation.
- `README.md` erklärt Installation, Start und Test der API.

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
uvicorn api_qudt:app --reload
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

### Suche nach Begriff

```http
GET http://127.0.0.1:8000/map?search=Volt&lang=en&types=unit
```


### Suche nach vollständiger QUDT-URI

```http
GET http://127.0.0.1:8000/map?search=http://qudt.org/vocab/unit/V&lang=en&types=unit
```

### Suche nach QuantityKind

```http
GET http://127.0.0.1:8000/map?search=Voltage&lang=en&types=quantitykind
```

---

## 8. Unterstützte Query-Parameter

| Parameter | Pflicht | Beispiel | Beschreibung |
|---|---:|---|---|
| `search` | ja | `Volt` | Suchbegriff, QUDT-URI oder CURIE |
| `lang` | nein | `en` | Sprache der Labels/Beschreibungen, z. B. `en` oder `de` |
| `types` | nein | `unit` | QUDT-Typen, die durchsucht werden sollen |

Unterstützte `types`:

```text
unit
quantitykind
dimensionvector
constant
sou
soqk
```

---

## 9. Beispielantwort

Vereinfachte Beispielantwort:

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
        "dataSpecificationContent": {
          "modelType": "DataSpecificationIec61360",
          "semanticId": {
            "property": "P1",
            "value": "http://qudt.org/vocab/unit/V"
          },
          "preferredName": {
            "property": "P35",
            "value": [
              {
                "value": "Volt",
                "lang": "en"
              }
            ]
          },
          "Symbol": {
            "property": "P41",
            "value": "V"
          }
        }
      }
    ],
    
  }
}
```

---

## 10. Was macht die API intern?

Die API führt intern folgende Schritte aus:

1. Query-Parameter auslesen  
2. Sprache und Typen validieren  
3. Suchmodus erkennen:
   - Begriffsuche
   - Semantic-ID-Suche
   - CURIE-Suche
4. SPARQL-Kandidatenabfrage an QUDT senden  
5. Erstes passendes QUDT-Objekt bestimmen  
6. Detaildaten per SPARQL laden  
7. RDF-Properties auf IEC61360-nahe Felder mappen  
8. JSON-Antwort zurückgeben  

---


