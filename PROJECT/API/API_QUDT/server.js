import fetch from "node-fetch";
import express from "express";

const app = express();
const PORT = 3000;

const ENDPOINT = "https://qudt.org/fuseki/qudt/query";

// Welche Sprachen du zulassen willst
const ALLOWED_LANGS = ["en", "de"];

// QUDT-Typen, die wir durchsuchen wollen
const TYPE_CONFIG = {
  unit: {
    classUri: "http://qudt.org/schema/qudt/Unit",
    vocabPrefix: "http://qudt.org/vocab/unit/",
    short: "Unit"
  },
  quantitykind: {
    classUri: "http://qudt.org/schema/qudt/QuantityKind",
    vocabPrefix: "http://qudt.org/vocab/quantitykind/",
    short: "QuantityKind"
  },
  dimensionvector: {
    classUri: "http://qudt.org/schema/qudt/QuantityKindDimensionVector",
    vocabPrefix: "http://qudt.org/vocab/dimensionvector/",
    short: "DimensionVector"
  },
  constant: {
    classUri: "http://qudt.org/schema/qudt/PhysicalConstant",
    vocabPrefix: "http://qudt.org/vocab/constant/",
    short: "PhysicalConstant"
  },
  sou: {
    classUri: "http://qudt.org/schema/qudt/SystemOfUnits",
    vocabPrefix: "http://qudt.org/vocab/sou/",
    short: "SystemOfUnits"
  },
  soqk: {
    classUri: "http://qudt.org/schema/qudt/SystemOfQuantityKinds",
    vocabPrefix: "http://qudt.org/vocab/soqk/",
    short: "SystemOfQuantityKinds"
  }
};

// Hilfsfunktion: Sprache validieren
function normalizeLang(lang) {
  if (!lang) return "en";
  return ALLOWED_LANGS.includes(lang) ? lang : "en";
}

// Hilfsfunktion: gewünschte Typen auswählen
function normalizeTypes(typesParam) {
  if (!typesParam) {
    return Object.keys(TYPE_CONFIG);
  }

  const parsed = typesParam
    .split(",")
    .map((t) => t.trim().toLowerCase())
    .filter((t) => TYPE_CONFIG[t]);

  return parsed.length ? parsed : Object.keys(TYPE_CONFIG);
}

// Erkennung: ist das eher eine Semantic-ID?
function detectSearchMode(search) {
  if (!search) return "term";

  const s = search.trim();

  if (
    s.startsWith("http://qudt.org/") ||
    s.startsWith("https://qudt.org/") ||
    /^[a-z]+:[A-Za-z0-9_\-./]+$/i.test(s)
  ) {
    return "id";
  }

  return "term";
}

// CURIE -> URI
function expandCurie(search) {
  if (!search) return search;

  const curieMap = {
    unit: "http://qudt.org/vocab/unit/",
    quantitykind: "http://qudt.org/vocab/quantitykind/",
    qkdv: "http://qudt.org/vocab/dimensionvector/",
    dimensionvector: "http://qudt.org/vocab/dimensionvector/",
    constant: "http://qudt.org/vocab/constant/",
    sou: "http://qudt.org/vocab/sou/",
    soqk: "http://qudt.org/vocab/soqk/"
  };

  const match = search.match(/^([a-z]+):(.+)$/i);
  if (!match) return search;

  const prefix = match[1].toLowerCase();
  const local = match[2];

  if (curieMap[prefix]) {
    return curieMap[prefix] + local;
  }

  return search;
}

// URI -> QNAME-artige Kurzform
function toQname(uri) {
  for (const [key, cfg] of Object.entries(TYPE_CONFIG)) {
    if (uri.startsWith(cfg.vocabPrefix)) {
      const local = uri.slice(cfg.vocabPrefix.length);
      if (key === "dimensionvector") return `qkdv:${local}`;
      return `${key}:${local}`;
    }
  }
  return uri;
}

// URI -> lokaler Name
function localName(uri) {
  const parts = uri.split("/");
  return parts[parts.length - 1] || uri;
}

// SPARQL-Query bauen
function buildQuery({ search, mode, lang, selectedTypes, limit }) {
  const safeSearch = search.replace(/"/g, '\\"');
  const typeValues = selectedTypes
    .map((t) => `<${TYPE_CONFIG[t].classUri}>`)
    .join(" ");

  const prefixFilters = selectedTypes
    .map((t) => `STRSTARTS(STR(?entity), "${TYPE_CONFIG[t].vocabPrefix}")`)
    .join(" || ");

  const expanded = expandCurie(search);

  let searchFilter = "";
  if (mode === "id") {
    const safeExpanded = expanded.replace(/"/g, '\\"');
    searchFilter = `
      FILTER(
        STR(?entity) = "${safeExpanded}" ||
        LCASE(STR(?entity)) = LCASE("${safeExpanded}") ||
        LCASE(REPLACE(STR(?entity), "^.+[/#]", "")) = LCASE("${safeSearch}") ||
        LCASE("${toQname(expanded)}") = LCASE("${safeSearch}")
      )
    `;
  } else {
    searchFilter = `
      FILTER(
        CONTAINS(LCASE(STR(?label)), LCASE("${safeSearch}")) ||
        CONTAINS(LCASE(COALESCE(STR(?symbol), "")), LCASE("${safeSearch}")) ||
        CONTAINS(LCASE(REPLACE(STR(?entity), "^.+[/#]", "")), LCASE("${safeSearch}"))
      )
    `;
  }

  return `
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT DISTINCT
  ?entity
  ?entityType
  ?label
  ?description
  ?symbol
  ?plainCode
  ?ucumCode
  ?applicableUnit
  ?hasQuantityKind
  (LANG(?label) AS ?labelLang)
  (LANG(?description) AS ?descLang)
WHERE {
  VALUES ?entityType { ${typeValues} }

  ?entity a ?entityType .
  FILTER(${prefixFilters})

  OPTIONAL {
    ?entity rdfs:label ?label .
    FILTER(LANG(?label) = "${lang}" || LANG(?label) = "")
  }

  OPTIONAL {
    ?entity dcterms:description ?description .
    FILTER(LANG(?description) = "${lang}" || LANG(?description) = "")
  }

  OPTIONAL { ?entity qudt:description ?description . }

  OPTIONAL { ?entity qudt:symbol ?symbol . }
  OPTIONAL { ?entity qudt:plainTextDescription ?plainCode . }
  OPTIONAL { ?entity qudt:ucumCode ?ucumCode . }
  OPTIONAL { ?entity qudt:applicableUnit ?applicableUnit . }
  OPTIONAL { ?entity qudt:hasQuantityKind ?hasQuantityKind . }

  ${searchFilter}
}
LIMIT ${Number(limit) || 25}
`;
}

// SPARQL row -> IEC61360-artige Struktur
function mapToIec61360(row, lang) {
  const uri = row.entity?.value || null;
  const label = row.label?.value || localName(uri);
  const description = row.description?.value || null;
  const symbol = row.symbol?.value || null;
  const ucumCode = row.ucumCode?.value || null;
  const entityTypeUri = row.entityType?.value || "";
  const entityType =
    Object.values(TYPE_CONFIG).find((t) => t.classUri === entityTypeUri)?.short ||
    entityTypeUri;

  // IEC61360 ist hier absichtlich "gemappt", nicht 1:1 aus QUDT übernommen.
  return {
    modelType: "ConceptDescription",
    idShort: localName(uri),
    category: entityType,
    semanticId: {
      type: "ExternalReference",
      keys: [
        {
          type: "GlobalReference",
          value: uri
        }
      ]
    },
    dataSpecification: {
      modelType: "DataSpecificationIec61360",
      preferredName: [
        {
          language: lang,
          text: label
        }
      ],
      shortName: [
        {
          language: lang,
          text: localName(uri)
        }
      ],
      definition: description
        ? [
            {
              language: lang,
              text: description
            }
          ]
        : [],
      unit: entityType === "Unit" ? label : null,
      unitSymbol: symbol || ucumCode || null,
      dataType: "STRING",
      sourceOfDefinition: "QUDT"
    },
    qudt: {
      uri,
      qname: toQname(uri),
      type: entityType,
      label,
      description,
      symbol,
      ucumCode,
      applicableUnit: row.applicableUnit?.value || null,
      hasQuantityKind: row.hasQuantityKind?.value || null
    }
  };
}

// Gleiche Ressourcen zusammenführen
function mergeRows(rows, lang) {
  const grouped = new Map();

  for (const row of rows) {
    const uri = row.entity?.value;
    if (!uri) continue;

    if (!grouped.has(uri)) {
      grouped.set(uri, mapToIec61360(row, lang));
      continue;
    }

    const item = grouped.get(uri);

    // Beschreibung ergänzen, falls bisher leer
    if (!item.dataSpecification.definition.length && row.description?.value) {
      item.dataSpecification.definition = [
        {
          language: lang,
          text: row.description.value
        }
      ];
      item.qudt.description = row.description.value;
    }

    // Symbol ergänzen
    if (!item.dataSpecification.unitSymbol && (row.symbol?.value || row.ucumCode?.value)) {
      item.dataSpecification.unitSymbol = row.symbol?.value || row.ucumCode?.value;
      item.qudt.symbol = row.symbol?.value || item.qudt.symbol;
      item.qudt.ucumCode = row.ucumCode?.value || item.qudt.ucumCode;
    }

    // QUDT-Links ergänzen
    if (!item.qudt.applicableUnit && row.applicableUnit?.value) {
      item.qudt.applicableUnit = row.applicableUnit.value;
    }
    if (!item.qudt.hasQuantityKind && row.hasQuantityKind?.value) {
      item.qudt.hasQuantityKind = row.hasQuantityKind.value;
    }
  }

  return Array.from(grouped.values());
}

app.get("/api/concept-description", async (req, res) => {
  try {
    const search = (req.query.search || "").trim();
    const lang = normalizeLang(req.query.lang);
    const limit = req.query.limit || 25;
    const selectedTypes = normalizeTypes(req.query.types);

    if (!search) {
      return res.status(400).json({
        error: "Missing required query parameter: search"
      });
    }

    const mode = detectSearchMode(search);
    const query = buildQuery({
      search,
      mode,
      lang,
      selectedTypes,
      limit
    });

    const url = ENDPOINT + "?query=" + encodeURIComponent(query);

    const response = await fetch(url, {
      headers: {
        Accept: "application/sparql-results+json",
        "User-Agent": "QUDT-IEC61360-Bridge/1.0"
      }
    });

    if (!response.ok) {
      const text = await response.text();
      return res.status(response.status).json({
        error: "SPARQL endpoint error",
        details: text
      });
    }

    const data = await response.json();
    const items = mergeRows(data.results.bindings, lang);

    return res.json({
      query: {
        search,
        mode,   // "term" oder "id"
        lang,
        types: selectedTypes,
        limit: Number(limit)
      },
      total: items.length,
      result: items
    });
  } catch (error) {
    console.error(error);
    return res.status(500).json({
      error: "Internal server error",
      details: error.message
    });
  }
});

app.listen(PORT, () => {
  console.log(`Server läuft auf http://localhost:${PORT}`);
});