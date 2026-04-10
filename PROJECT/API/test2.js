const ENDPOINT = "https://qudt.org/fuseki/qudt/query";

// Filterung von Sprachen
const languages = ["en", "de"];
const language = "en";
//const langValues = languages.map(l => `"${l}"`).join(" ");

const query = `
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX unit: <http://qudt.org/vocab/unit/>
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
}
`; 
// den Filter noch anpassen, das er eine Sprache übergeben bekommt und nicht hartkodiert ist
// FILTER(LANG(?label) IN ("en", "de")) -> alter Filter



async function run() {
  const url = ENDPOINT + "?query=" + encodeURIComponent(query);

  // Änderung:
  const res = await fetch(url, {
  headers: {
    "Accept": "application/sparql-results+json",
    "User-Agent": "MyApp/1.0"
  }
});

  const data = await res.json();

  // Änderung: Ausgabe als JSON-String
  console.log("=== SPARQL RESULT ===\n");

  const results = [];
  for (const row of data.results.bindings) {
    results.push({
      unit: row.unit?.value,
      label: row.label?.value,
      symbol: row.symbol?.value,
      type: row.type?.value,
      description: row.description?.value,
      lang: row.lang?.value
    });
  }

  console.log(JSON.stringify(results, null, 2));
}

run();