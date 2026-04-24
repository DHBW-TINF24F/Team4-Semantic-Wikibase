import fetch from "node-fetch";
import express from "express";

const app = express();
const PORT = 3000;

const ENDPOINT = "https://qudt.org/fuseki/qudt/query";
const ALLOWED_LANGS = ["en", "de"];

const TYPE_CONFIG = {
  unit: {
    classUri: "http://qudt.org/schema/qudt/Unit",
    vocabPrefix: "http://qudt.org/vocab/unit/",
    short: "qudt:Unit"
  },
  quantitykind: {
    classUri: "http://qudt.org/schema/qudt/QuantityKind",
    vocabPrefix: "http://qudt.org/vocab/quantitykind/",
    short: "qudt:QuantityKind"
  },
  dimensionvector: {
    classUri: "http://qudt.org/schema/qudt/QuantityKindDimensionVector",
    vocabPrefix: "http://qudt.org/vocab/dimensionvector/",
    short: "qudt:QuantityKindDimensionVector"
  },
  constant: {
    classUri: "http://qudt.org/schema/qudt/PhysicalConstant",
    vocabPrefix: "http://qudt.org/vocab/constant/",
    short: "qudt:PhysicalConstant"
  },
  sou: {
    classUri: "http://qudt.org/schema/qudt/SystemOfUnits",
    vocabPrefix: "http://qudt.org/vocab/sou/",
    short: "qudt:SystemOfUnits"
  },
  soqk: {
    classUri: "http://qudt.org/schema/qudt/SystemOfQuantityKinds",
    vocabPrefix: "http://qudt.org/vocab/soqk/",
    short: "qudt:SystemOfQuantityKinds"
  }
};

function normalizeLang(lang) {
  if (!lang) return "en";
  return ALLOWED_LANGS.includes(lang) ? lang : "en";
}

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

function detectSearchMode(search) {
  if (!search) return "term";
  const s = search.trim();

  if (
    s.startsWith("http://qudt.org/") ||
    s.startsWith("https://qudt.org/") ||
    /^(unit|quantitykind|qkdv|dimensionvector|constant|sou|soqk):.+$/i.test(s)
  ) {
    return "id";
  }

  return "term";
}

function isMappedPredicate(predicateUri) {
  const mappedPredicates = new Set([
    "http://www.w3.org/2000/01/rdf-schema#label",
    "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",
    "http://qudt.org/schema/qudt/informativeReference",
    "http://qudt.org/schema/qudt/symbol",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
    "http://qudt.org/schema/qudt/iec61360Code",
    "http://purl.org/dc/terms/description",
    "http://qudt.org/schema/qudt/latexDefinition",
    "http://qudt.org/schema/qudt/siUnitsExpression"
  ]);

  return mappedPredicates.has(predicateUri);
}

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

function localName(uri) {
  if (!uri) return null;
  const parts = uri.split("/");
  return parts[parts.length - 1] || uri;
}

function predicateFieldName(predicateUri) {
  const known = {
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
  };

  if (known[predicateUri]) return known[predicateUri];

  const hashIndex = predicateUri.lastIndexOf("#");
  const slashIndex = predicateUri.lastIndexOf("/");
  const idx = Math.max(hashIndex, slashIndex);
  return idx >= 0 ? predicateUri.slice(idx + 1) : predicateUri;
}

function parseLiteral(value, datatype) {
  if (datatype?.includes("integer")) return Number.parseInt(value, 10);
  if (
    datatype?.includes("decimal") ||
    datatype?.includes("double") ||
    datatype?.includes("float")
  ) {
    return Number(value);
  }
  return value;
}

function objectToCompactValue(obj) {
  if (!obj) return null;

  if (obj.type === "uri") {
    return toQname(obj.value).startsWith("http") ? obj.value : toQname(obj.value);
  }

  const parsed = parseLiteral(obj.value, obj.datatype);

  if (obj.lang) {
    return { value: parsed, lang: obj.lang };
  }

  return parsed;
}

function pushUnique(arr, value) {
  if (value === null || value === undefined) return;

  const serialized = JSON.stringify(value);
  const exists = arr.some((item) => JSON.stringify(item) === serialized);

  if (!exists) arr.push(value);
}

function finalizeValue(arr) {
  if (!arr || arr.length === 0) return null;
  if (arr.length === 1) return arr[0];
  return arr;
}

function buildCandidateQuery({ search, mode, lang, selectedTypes }) {
  const safeSearch = search.replace(/"/g, '\\"');
  const typeValues = selectedTypes
    .map((t) => `<${TYPE_CONFIG[t].classUri}>`)
    .join(" ");

  const prefixFilters = selectedTypes
    .map((t) => `STRSTARTS(STR(?entity), "${TYPE_CONFIG[t].vocabPrefix}")`)
    .join(" || ");

  const expanded = expandCurie(search);
  const safeExpanded = expanded.replace(/"/g, '\\"');

  let rankingBlock = "";
  let filterBlock = "";

  if (mode === "id") {
    filterBlock = `
      FILTER(STR(?entity) = "${safeExpanded}")
      BIND(0 AS ?rank)
    `;
  } else {
    filterBlock = `
      FILTER(
        (BOUND(?label) && LCASE(STR(?label)) = LCASE("${safeSearch}")) ||
        LCASE(REPLACE(STR(?entity), "^.+[/#]", "")) = LCASE("${safeSearch}") ||
        (BOUND(?symbol) && LCASE(STR(?symbol)) = LCASE("${safeSearch}")) ||
        (BOUND(?label) && CONTAINS(LCASE(STR(?label)), LCASE("${safeSearch}")))
      )
    `;

    rankingBlock = `
      BIND(
        IF(BOUND(?label) && LCASE(STR(?label)) = LCASE("${safeSearch}"), 0,
          IF(LCASE(REPLACE(STR(?entity), "^.+[/#]", "")) = LCASE("${safeSearch}"), 1,
            IF(BOUND(?symbol) && LCASE(STR(?symbol)) = LCASE("${safeSearch}"), 2, 3)
          )
        ) AS ?rank
      )
    `;
  }

  return `
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?entity ?entityType ?label ?symbol ?rank
WHERE {
  VALUES ?entityType { ${typeValues} }

  ?entity a ?entityType .
  FILTER(${prefixFilters})

  OPTIONAL {
    ?entity rdfs:label ?label .
    FILTER(LANG(?label) = "${lang}" || LANG(?label) = "" || LANG(?label) = "en")
  }

  OPTIONAL { ?entity qudt:symbol ?symbol . }

  ${filterBlock}
  ${rankingBlock}
}
ORDER BY ?rank STRLEN(STR(?label)) ?entity
LIMIT 1
`;
}

function buildDetailQuery(entityUri, lang) {
  const safeEntity = entityUri.replace(/"/g, '\\"');

  return `
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?p ?o ?lang ?datatype
WHERE {
  BIND(<${safeEntity}> AS ?s)

  ?s ?p ?o .

  BIND(LANG(?o) AS ?lang)
  BIND(DATATYPE(?o) AS ?datatype)

  FILTER(
    !isLiteral(?o) ||
    LANG(?o) = "${lang}" ||
    LANG(?o) = "" ||
    LANG(?o) = "en" ||
    ?p = rdfs:label ||
    ?p = dcterms:description
  )
}
`;
}

async function runSparql(query) {
  const url = ENDPOINT + "?query=" + encodeURIComponent(query);

  const response = await fetch(url, {
    headers: {
      Accept: "application/sparql-results+json",
      "User-Agent": "QUDT-SemanticHub-IEC61360-Bridge/1.0"
    }
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`SPARQL endpoint error: ${response.status} ${text}`);
  }

  return response.json();
}

function emptySemanticHubRecord(uri) {
  return {
    P1: uri,
    P35: [],
    P36: null,
    P37: null,
    P43: null,
    P40: [],
    P41: null,
    P42: null,
    P44: [],
    P45: null,
    P46: null,
    P47: null,
    P48: null
  };
}


function createIecField(propertyNumber, value = null) {
  return {
    property: propertyNumber,
    value: value
  };
}

function emptyConceptDescription(uri) {
  return {
    modelType: "ConceptDescription",
    id: uri,
    idShort: localName(uri),
    embeddedDataSpecifications: [
      {
        dataSpecification: {
          type: "ExternalReference",
          keys: [
            {
              type: "GlobalReference",
              value: "http://admin-shell.io/DataSpecificationTemplates/DataSpecificationIEC61360/3/0"
            }
          ]
        },
        dataSpecificationContent: {
          modelType: "DataSpecificationIec61360",

          semanticId: createIecField("P1", uri),
          preferredName: createIecField("P35", []),
          shortName: createIecField("P36", null),
          unit: createIecField("P37", null),
          sourceOfDefinition: createIecField("P40", []),
          Symbol: createIecField("P41", null),
          dataType: createIecField("P42", null),
          unitId: createIecField("P43", null),
          Definition: createIecField("P44", []),
          valueFormat: createIecField("P45", null),
          valueList: createIecField("P46", null),
          value: createIecField("P47", null),
          levelType: createIecField("P48", null)
        }
      }
    ],
    additionalProperties: {}
  };
}

function ensureAdditionalProperty(target, fieldName, value) {
  if (!Object.prototype.hasOwnProperty.call(target.additionalProperties, fieldName)) {
    target.additionalProperties[fieldName] = [];
  }

  if (!Array.isArray(target.additionalProperties[fieldName])) {
    target.additionalProperties[fieldName] = [target.additionalProperties[fieldName]];
  }

  pushUnique(target.additionalProperties[fieldName], value);
}

function finalizeAdditionalProperties(obj) {
  for (const key of Object.keys(obj.additionalProperties)) {
    const val = obj.additionalProperties[key];
    if (Array.isArray(val) && val.length === 1) {
      obj.additionalProperties[key] = val[0];
    }
    if (Array.isArray(val) && val.length === 0) {
      obj.additionalProperties[key] = null;
    }
  }
}

function mapRowsToSemanticHub(entityUri, rows) {
  const result = emptyConceptDescription(entityUri);
  const iec = result.embeddedDataSpecifications[0].dataSpecificationContent;

  for (const row of rows) {
    const predicateUri = row.p?.value;
    const object = row.o;

    if (!predicateUri || !object) continue;

    const fieldName = predicateFieldName(predicateUri);
    const compactValue = objectToCompactValue({
      type: object.type,
      value: object.value,
      lang: row.lang?.value || "",
      datatype: row.datatype?.value || ""
    });

    // Nur zusätzliche, nicht bereits gemappte Properties in additionalProperties aufnehmen
    if (!isMappedPredicate(predicateUri)) {
      ensureAdditionalProperty(result, fieldName, compactValue);
    }

    switch (predicateUri) {
      case "http://www.w3.org/2000/01/rdf-schema#label":
        pushUnique(iec.preferredName.value, compactValue);

        if (iec.unit.value == null) {
          if (typeof compactValue === "string") {
            iec.unit.value = compactValue;
          } else if (compactValue && typeof compactValue === "object" && "value" in compactValue) {
            iec.unit.value = compactValue.value;
          }
        }
        break;

      case "http://www.w3.org/2000/01/rdf-schema#isDefinedBy":
      case "http://qudt.org/schema/qudt/informativeReference":
        pushUnique(iec.sourceOfDefinition.value, compactValue);
        break;

      case "http://qudt.org/schema/qudt/symbol":
        if (iec.Symbol.value == null) {
          iec.Symbol.value = compactValue;
        }
        break;

      case "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
        if (iec.dataType.value == null) {
          iec.dataType.value = compactValue;
        }
        break;

      case "http://qudt.org/schema/qudt/iec61360Code":
        if (iec.unitId.value == null) {
          iec.unitId.value = compactValue;
        }
        break;

      case "http://purl.org/dc/terms/description":
        pushUnique(iec.Definition.value, {
          type: "description",
          value: object.value
        });
        break;

      case "http://qudt.org/schema/qudt/latexDefinition":
        pushUnique(iec.Definition.value, {
          type: "latexDefinition",
          value: object.value
        });
        break;

      case "http://qudt.org/schema/qudt/siUnitsExpression":
        if (iec.valueFormat.value == null) {
          iec.valueFormat.value = compactValue;
        }
        break;

      default:
        break;
    }
  }

  // PreferredName leer -> null
  if (iec.preferredName.value.length === 0) {
    iec.preferredName.value = null;
  }

  // SourceOfDefinition leer -> null
  if (iec.sourceOfDefinition.value.length === 0) {
    iec.sourceOfDefinition.value = null;
  }

  // Definition leer -> null
  if (iec.Definition.value.length === 0) {
    iec.Definition.value = null;
  }

  finalizeAdditionalProperties(result);

  return result;
}

app.get("/api/concept-description", async (req, res) => {
  try {
    const search = (req.query.search || "").trim();
    const lang = normalizeLang(req.query.lang);
    const selectedTypes = normalizeTypes(req.query.types);

    if (!search) {
      return res.status(400).json({
        error: "Missing required query parameter: search"
      });
    }

    const mode = detectSearchMode(search);

    // 1) Erst genau einen Kandidaten bestimmen
    const candidateQuery = buildCandidateQuery({
      search,
      mode,
      lang,
      selectedTypes
    });

    const candidateData = await runSparql(candidateQuery);
    const candidates = candidateData.results.bindings;

    if (!candidates.length) {
      return res.status(404).json({
        query: { search, mode, lang, types: selectedTypes },
        total: 0,
        result: null
      });
    }

    const entityUri = candidates[0].entity.value;

    // 2) Dann genau dieses eine Objekt vollständig laden
    const detailQuery = buildDetailQuery(entityUri, lang);
    const detailData = await runSparql(detailQuery);

    const mapped = mapRowsToSemanticHub(entityUri, detailData.results.bindings);

    return res.json({
      query: {
        search,
        mode,
        lang,
        types: selectedTypes
      },
      total: 1,
      result: mapped
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