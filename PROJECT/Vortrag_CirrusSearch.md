# Vortrag: Verbesserte Suche mit CirrusSearch

Kurztext für eine Präsentation von ca. 3 Minuten.

## Folie 1 – Problem & Ziel

**Titel:** Verbesserte Suche mit CirrusSearch

**Inhalt:**
- Alte Suche war schwer auffindbar und wenig intuitiv
- Ziel: Begriffe, Labels, URIs und Semantic IDs schnell finden
- Fokus auf einfache Nutzung direkt über die Startseite

**Sprechtext:**
„Ich habe die Suchfunktion in der Semantic Wikibase verbessert, damit Nutzer schneller und einfacher passende Concept Descriptions finden. Wichtig war dabei, dass man nicht nur nach Begriffen sucht, sondern auch nach Semantic IDs oder URIs. Damit wird die Plattform deutlich zugänglicher, gerade für Nutzer ohne tiefes Wikibase-Wissen.“

## Folie 2 – Lösung: CirrusSearch + Semantic-ID-Suche

**Inhalt:**
- CirrusSearch als Hauptsuche
- Basierend auf Elasticsearch
- Unterstützt Volltext-, Fuzzy-, Phrase- und Wildcard-Suche
- Ergänzung durch direkte Semantic-ID-Auflösung (`Special:GoBySemanticId`)
- Autocomplete über `wbsearchentities`

**Sprechtext:**
„Technisch habe ich CirrusSearch als zentrale Suchmaschine genutzt, weil sie gut in MediaWiki und Wikibase integriert ist und starke Volltextsuche bietet. Zusätzlich gibt es eine direkte Suche über Semantic IDs, sodass ein Eintrag auch per URI direkt aufgelöst werden kann. Für die Bedienung habe ich außerdem Autocomplete vorgesehen, damit Nutzer schneller zum richtigen Treffer kommen.“

## Folie 3 – Ergebnis & Nutzen

**Inhalt:**
- Suchfunktion ist schneller und benutzerfreundlicher
- Bessere Auffindbarkeit von Concept Descriptions
- Mehrsprachige Suche möglich
- Skalierbar und gut in die Wikibase-Architektur integrierbar

**Sprechtext:**
„Der große Vorteil ist, dass die Suche jetzt näher an dem ist, was Nutzer wirklich brauchen: schnell, verständlich und flexibel. CirrusSearch verbessert die Volltextsuche, während die Semantic-ID-Suche den direkten Zugriff auf eindeutige Einträge ermöglicht. Insgesamt wird die Semantic Wikibase dadurch deutlich benutzerfreundlicher und technisch besser skalierbar.“

## Kurzabschluss

„Zusammengefasst: Mit CirrusSearch haben wir die Suche in der Wikibase so erweitert, dass sowohl klassische Begriffe als auch semantische IDs gefunden werden können. Das verbessert die Usability und unterstützt die zentrale Idee des Projekts: semantische Inhalte einfach auffindbar zu machen.“
