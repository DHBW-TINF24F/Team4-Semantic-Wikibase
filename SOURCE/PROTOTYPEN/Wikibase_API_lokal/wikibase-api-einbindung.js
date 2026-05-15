// Code einfügen in Common.js in der Wikibase
// API fügt Werte in das Item:Q5 (Test) ein
// --> Fügt nur die Daten ein, nicht in die Vorhandene Tabelle

mw.loader.using(["mediawiki.util"]).then(function () {
  if (
    mw.config.get("wgPageName") !== "Item:Q5" ||
    mw.config.get("wgAction") !== "view"
  ) {
    return;
  }

  // Lokale Adresse der Test-API, ggf. anpassen
  const apiUrl =
    "http://127.0.0.1:5000/api/v3/search?search=Volt&lang=en&types=unit";

  function normalizeText(text) {
    return (text || "").replace(/\s+/g, " ").trim().toLowerCase();
  }

  function extractValues(data) {
    const result = data?.result || {};
    const embedded = (result.embeddedDataSpecifications || [])[0] || {};
    const content = embedded.dataSpecificationContent || {};

    const preferredNameRaw = content.preferredName?.value;
    const symbolRaw = content.Symbol?.value;

    let preferredName = "—";
    if (Array.isArray(preferredNameRaw)) {
      preferredName = preferredNameRaw
        .map((v) =>
          typeof v === "object" && v !== null
            ? v.value || JSON.stringify(v)
            : String(v),
        )
        .join(", ");
    } else if (preferredNameRaw) {
      preferredName =
        typeof preferredNameRaw === "object"
          ? preferredNameRaw.value || JSON.stringify(preferredNameRaw)
          : String(preferredNameRaw);
    }

    let symbol = "—";
    if (symbolRaw) {
      symbol =
        typeof symbolRaw === "object"
          ? symbolRaw.value || JSON.stringify(symbolRaw)
          : String(symbolRaw);
    }

    return {
      id: result.id || "—",
      idshort: result.idShort || "—",
      "preferred name": preferredName,
      preferredname: preferredName,
      symbol: symbol,
    };
  }

  function setCellValue(row, value) {
    if (!row) return false;

    let valueCell =
      row.querySelector("td") ||
      row.querySelector(".wikibase-statementview-mainsnak-container") ||
      row.querySelector(".wikibase-snakview-value") ||
      row.querySelector(".wikibase-statementview-mainsnak");

    if (!valueCell) return false;

    const target =
      valueCell.querySelector(".wikibase-snakview-value") || valueCell;

    target.textContent = value;
    return true;
  }

  function fillExistingTable(values) {
    const rows = document.querySelectorAll("tr, .wikibase-statementview");

    let filled = 0;

    rows.forEach(function (row) {
      const headerText = normalizeText(row.textContent);

      if (!headerText) return;

      if (headerText.includes("idshort")) {
        if (setCellValue(row, values["idshort"])) filled++;
      } else if (
        headerText.includes("preferred name") ||
        headerText.includes("preferredname")
      ) {
        if (setCellValue(row, values["preferredname"])) filled++;
      } else if (headerText.includes("symbol")) {
        if (setCellValue(row, values["symbol"])) filled++;
      } else if (headerText === "id" || headerText.includes(" id ")) {
        if (setCellValue(row, values["id"])) filled++;
      }
    });

    return filled;
  }

  function showDebugFallback(values, errorText) {
    const target = document.querySelector("#mw-content-text") || document.body;
    if (!target) return;

    const box = document.createElement("div");
    box.style.border = "1px solid #c8ccd1";
    box.style.background = "#fff8e1";
    box.style.padding = "12px";
    box.style.margin = "12px 0";
    box.innerHTML = `
            <strong>QUDT-Testdaten</strong><br>
            ${errorText ? '<div style="color:#a33; margin-top:6px;">' + errorText + "</div>" : ""}
            <pre style="white-space:pre-wrap; margin-top:8px;"></pre>
        `;
    box.querySelector("pre").textContent = JSON.stringify(values, null, 2);
    target.prepend(box);
  }

  fetch(apiUrl)
    .then(function (response) {
      if (!response.ok) {
        throw new Error("HTTP " + response.status);
      }
      return response.json();
    })
    .then(function (data) {
      const values = extractValues(data);
      const filled = fillExistingTable(values);

      if (filled === 0) {
        showDebugFallback(
          values,
          "Keine passende Property-Tabelle bzw. Zeile gefunden.",
        );
      }
    })
    .catch(function (error) {
      showDebugFallback({}, "Fehler beim Laden: " + error.message);
    });
});
