from typing import Optional, List, Dict, Any
import requests

from fastapi import FastAPI, Query, HTTPException


app = FastAPI(
    title="Unified Semantic Mapping API",
    description="Zentrale API für QUDT, VEC und KBL Mapping auf IEC61360.",
    version="1.0.0"
)


API_CONFIG = {
    "qudt": {
        "name": "QUDT",
        "url": "http://127.0.0.1:8001/map"
    },
    "vec": {
        "name": "VEC",
        "url": "http://127.0.0.1:8002/map"
    },
    "kbl": {
        "name": "KBL",
        "url": "http://127.0.0.1:8003/map"
    }
}


@app.get("/")
def root():
    return {
        "message": "Unified Semantic Mapping API",
        "description": "Zentrale Schnittstelle für QUDT, VEC und KBL.",
        "sources": list(API_CONFIG.keys()),
        "swagger": "/docs"
    }


def call_mapping_api(
    source: str,
    search: str,
    lang: str,
    types: Optional[List[str]] = None
) -> Dict[str, Any]:

    config = API_CONFIG[source]
    url = config["url"]

    params = {
        "search": search,
        "lang": lang
    }

    # Nur QUDT unterstützt aktuell types
    if source == "qudt" and types:
        params["types"] = types

    try:
        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        return {
            "source": source,
            "sourceName": config["name"],
            "success": True,
            "response": data
        }

    except requests.RequestException as e:
        return {
            "source": source,
            "sourceName": config["name"],
            "success": False,
            "error": str(e)
        }


@app.get("/map")
def map_unified(
    search: str = Query(..., description="Suchbegriff oder Semantic ID"),
    source: str = Query(
        "all",
        description="Datenquelle: qudt, vec, kbl oder all"
    ),
    lang: str = Query("en", description="Sprache, z. B. en oder de"),
    types: Optional[List[str]] = Query(
        default=None,
        description="Nur für QUDT, z. B. unit oder quantitykind"
    ),
    only_found: bool = Query(
        True,
        description="Wenn true, werden nur Treffer mit total > 0 zurückgegeben"
    )
):

    if not search.strip():
        raise HTTPException(
            status_code=400,
            detail="Parameter 'search' darf nicht leer sein."
        )

    source = source.lower().strip()

    if source != "all" and source not in API_CONFIG:
        raise HTTPException(
            status_code=400,
            detail="source muss qudt, vec, kbl oder all sein."
        )

    sources_to_query = list(API_CONFIG.keys()) if source == "all" else [source]

    results = []

    for src in sources_to_query:
        result = call_mapping_api(
            source=src,
            search=search,
            lang=lang,
            types=types
        )

        if only_found:
            if (
                result.get("success")
                and result.get("response", {}).get("total", 0) > 0
            ):
                results.append(result)
        else:
            results.append(result)

    return {
        "query": {
            "search": search,
            "source": source,
            "lang": lang,
            "types": types,
            "onlyFound": only_found
        },
        "total": len(results),
        "results": results
    }


@app.get("/sources")
def get_sources():
    return {
        "sources": [
            {
                "id": key,
                "name": value["name"],
                "url": value["url"]
            }
            for key, value in API_CONFIG.items()
        ]
    }