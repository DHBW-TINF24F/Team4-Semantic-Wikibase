# QUDT IEC61360 SemanticHub Mapper (Python)

Dieses Python-Skript fragt Daten aus QUDT über den SPARQL-Endpunkt ab, mappt sie auf ein IEC61360-orientiertes JSON-Format und gibt genau einen passenden Eintrag zurück.

Es unterscheidet zwischen:

- **Begriffssuche**, z. B. `Volt`
- **Semantic-ID-Suche**, z. B. `http://qudt.org/vocab/unit/V` oder `unit:V`

Die Ausgabe enthält:

- die gemappten IEC61360-Felder
- die zugehörigen Property-Nummern wie `P1`, `P35`, `P43`
- zusätzliche, nicht gemappte Properties unter `additionalProperties`

## Installation

Benötigtes Paket installieren:

```bash
pip install requests
```

## Konfiguration

Die Suchparameter werden direkt im Python-Code über Variablen gesetzt:

```python
SEARCH = "Volt"
LANG = "en"
TYPES = ["unit"]
```

### Beispiele

#### Begriffssuche

```python
SEARCH = "Volt"
LANG = "en"
TYPES = ["unit"]
```

#### Semantic-ID-Suche mit vollständiger URI

```python
SEARCH = "http://qudt.org/vocab/unit/V"
LANG = "en"
TYPES = ["unit"]
```

#### Semantic-ID-Suche mit Kurzform

```python
SEARCH = "unit:V"
LANG = "en"
TYPES = ["unit"]
```

#### QuantityKind-Suche

```python
SEARCH = "http://qudt.org/vocab/quantitykind/ElectricCurrent"
LANG = "en"
TYPES = ["quantitykind"]
```

## Starten

```bash
python script.py
```

Falls dein Dateiname anders ist, entsprechend ersetzen, zum Beispiel:

```bash
python qudt_mapper.py
```

## Verhalten der Suche

Das Skript unterscheidet automatisch zwischen:

- **Begriff**
- **Semantic ID**

Bei einer Begriffssuche wird der beste exakte Treffer ausgewählt, damit nicht mehrere ähnliche Ergebnisse wie `Volt per meter` zurückgegeben werden.

Bei einer Semantic-ID-Suche wird genau diese Ressource geladen.

## Ausgabe

Das Skript gibt das Ergebnis als JSON in der Konsole aus.

Die Ausgabe enthält:

- `query`
- `total`
- `result`

## Inhalt von `result`

Der Datensatz enthält unter anderem:

- `modelType`
- `id`
- `idShort`
- `embeddedDataSpecifications`
- `dataSpecificationContent`
- `additionalProperties`

## Gemappte IEC61360-Felder

Im Block `dataSpecificationContent` werden wichtige Felder gemappt, z. B.:

- `semanticId` (`P1`)
- `preferredName` (`P35`)
- `shortName` (`P36`)
- `unit` (`P37`)
- `sourceOfDefinition` (`P40`)
- `Symbol` (`P41`)
- `dataType` (`P42`)
- `unitId` (`P43`)
- `Definition` (`P44`)
- `valueFormat` (`P45`)
- `valueList` (`P46`)
- `value` (`P47`)
- `levelType` (`P48`)

Falls ein Feld nicht vorhanden ist, wird es mit `null` zurückgegeben.

## Zusätzliche Properties

Alle weiteren, nicht gemappten QUDT-/RDF-Properties werden unter `additionalProperties` zurückgegeben.

Bereits gemappte Properties wie `rdfs:label`, `qudt:symbol` oder `dcterms:description` erscheinen dort nicht noch einmal doppelt.

## Hinweise

- Für `unit` müssen auch Unit-URIs verwendet werden, z. B. `http://qudt.org/vocab/unit/V`
- Für `quantitykind` müssen QuantityKind-URIs verwendet werden, z. B. `http://qudt.org/vocab/quantitykind/ElectricCurrent`
- Wenn `TYPES` nicht zur Semantic ID passt, wird kein Treffer gefunden
- Das Skript liefert im Normalfall genau **einen** Eintrag zurück