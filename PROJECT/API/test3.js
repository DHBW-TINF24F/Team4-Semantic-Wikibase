const ENDPOINT = "https://qudt.org/fuseki/qudt/query";

const languages = ["en", "de"];

function escapeSparqlString(str) {
  return str.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
}

async function run(searchTerm, language = "en") {
  if (!languages.includes(language)) {
    throw new Error(`Ungültige Sprache: ${language}`);
  }

  const query = `
  PREFIX qudt: <http://qudt.org/schema/qudt/>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX dcterms: <http://purl.org/dc/terms/>

  SELECT ?unit ?label ?symbol ?type ?description (LANG(?label) AS ?lang)
  WHERE {
      ?unit a qudt:Unit .
      ?unit rdfs:label ?label .

      OPTIONAL { ?unit qudt:symbol ?symbol . }
      OPTIONAL { ?unit a ?type . }
      OPTIONAL { ?unit dcterms:description ?description . }
      OPTIONAL { ?unit qudt:description ?description . }

      FILTER(LANG(?label) = "${language}")
      FILTER(CONTAINS(LCASE(STR(?label)), LCASE("${escapeSparqlString(searchTerm)}")))
      # Kommentar
      # FILTER(LCASE(STR(?label)) = LCASE("${escapeSparqlString(searchTerm)}")) 
  }
  `;

  const url = ENDPOINT + "?query=" + encodeURIComponent(query);

  const res = await fetch(url, {
    headers: {
      "Accept": "application/sparql-results+json",
      "User-Agent": "MyApp/1.0"
    }
  });

  const data = await res.json();

  const results = data.results.bindings.map(row => ({
    unit: row.unit?.value,
    label: row.label?.value,
    symbol: row.symbol?.value,
    type: row.type?.value,
    description: row.description?.value,
    lang: row.lang?.value
  }));

  console.log(JSON.stringify(results, null, 2));
}

run("ampere", "de");