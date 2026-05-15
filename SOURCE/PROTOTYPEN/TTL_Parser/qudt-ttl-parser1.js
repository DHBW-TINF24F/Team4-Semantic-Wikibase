// file: qudt-ttl-parser.js

//import { Parser } from "n3";
const { Parser } = require("n3");

const URL = "https://qudt.org/vocab/unit/V";

async function main() {
  try {
    // ✅ WICHTIG: KEIN JSON HEADER
    const response = await fetch(URL);

    if (!response.ok) {
      throw new Error(`HTTP Fehler: ${response.status}`);
    }

    // ✅ IMMER TEXT LESEN (nicht .json!)
    const ttl = await response.text();

    console.log("=== TTL geladen ===\n");

    // ✅ Parser initialisieren
    const parser = new Parser();

    // ✅ TTL parsen
    const quads = parser.parse(ttl);

    console.log(`Gefundene Triples: ${quads.length}\n`);

    // ✅ Daten extrahieren
    let type = null;
    let symbol = null;

    for (const quad of quads) {
      const predicate = quad.predicate.value;

      if (predicate.includes("type")) {
        type = quad.object.value;
      }

      if (predicate.includes("symbol")) {
        symbol = quad.object.value;
      }
    }

    console.log("=== ERGEBNIS ===");
    console.log("Type:", type);
    console.log("Symbol:", symbol);

  } catch (err) {
    console.error("Fehler:", err);
  }
}

main();