// Wandelt die TTL-Daten von QUDT in ein lesbares Format um und extrahiert wichtige Informationen wie den Typ
// im JSON-Format

const { Parser } = require("n3");

const URL = "https://qudt.org/vocab/unit/V";



async function ttlToJson(url) {
  const res = await fetch(url);
  const ttl = await res.text();

  const parser = new Parser();
  const quads = parser.parse(ttl);

  const graph = {};

  for (const q of quads) {
    const s = q.subject.value;
    const p = q.predicate.value;
    const o = q.object.value;

    if (!graph[s]) {
      graph[s] = {};
    }

    if (!graph[s][p]) {
      graph[s][p] = [];
    }

    graph[s][p].push(o);
  }

  // 👉 optional: schöner machen (Arrays reduzieren)
  const cleaned = {};

  for (const [subject, props] of Object.entries(graph)) {
    cleaned[subject] = {};

    for (const [predicate, values] of Object.entries(props)) {
      cleaned[subject][predicate] =
        values.length === 1 ? values[0] : values;
    }
  }

  return cleaned;
}


function simplify(json) {
  const result = {};

  for (const [subject, props] of Object.entries(json)) {
    const unit = {};

    for (const [predicate, value] of Object.entries(props)) {
      const key = predicate.split("#").pop() || predicate.split("/").pop();

      // RDF-Struktur entfernen (wichtig!)
      if (key === "type") continue;
      if (key === "hasUnit") continue;
      if (key === "exponent") continue;

      unit[key] = value;
    }

    result.unit = unit;
  }

  return result;
}



async function main() {
  try {
    const rawJson = await ttlToJson(URL);

    const niceJson = simplify(rawJson);

    console.log("=== JSON OUTPUT ===\n");
    console.log(JSON.stringify(niceJson, null, 2));
  } catch (err) {
    console.error(err);
  }
}

main();