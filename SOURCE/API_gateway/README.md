# API Gateway lokal & im Internet starten

Diese Anleitung ist für das schnelle lokale Starten der drei Mapping-APIs und des API Gateways.

Wichtig: Die Pfade sind allgemein gehalten. Jeder muss zuerst in den lokalen Projektordner wechseln, in dem die Ordner `API_QUDT`, `API_VEC`, `API_KBL` und die Datei `api_gateway.py` liegen.

Beispielhafte Struktur:

```text
Mapper+API/
├── API_QUDT/
│   └── api_qudt.py
├── API_VEC/
│   └── api_vec.py
├── API_KBL/
│   └── api_kbl.py
└── api_gateway.py
```

---

## API Gateway lokal starten

### 1. Pakete installieren

Einmalig ausführen:

```bash
python -m pip install fastapi uvicorn requests rdflib
```

---

### 2. Vier Terminals öffnen

Es müssen alle drei APIs und danach das Gateway gestartet werden. 
<br>

####  Terminal 1: QUDT API

In den lokalen QUDT-Ordner wechseln:

```bash
cd <PFAD_ZUM_PROJEKT>/API_QUDT
```

API starten:

```bash
uvicorn api_qudt:app --port 8001 --reload
```


#### Terminal 2: VEC API

In den lokalen VEC-Ordner wechseln:

```bash
cd <PFAD_ZUM_PROJEKT>/API_VEC
```

API starten:

```bash
uvicorn api_vec:app --port 8002 --reload
```


#### Terminal 3: KBL API

In den lokalen KBL-Ordner wechseln:

```bash
cd <PFAD_ZUM_PROJEKT>/API_KBL
```

API starten:

```bash
uvicorn api_kbl:app --port 8003 --reload
```

#### Terminal 4: API Gateway

In den lokalen Hauptordner wechseln, in dem `api_gateway.py` liegt:

```bash
cd <PFAD_ZUM_PROJEKT>
```

Gateway starten:

```bash
uvicorn api_gateway:app --port 8000 --reload
```

Falls `uvicorn` nicht erkannt wird, stattdessen verwenden:

```bash
python -m uvicorn api_gateway:app --port 8000 --reload
```

---

### 3. Gateway öffnen

Im Browser öffnen:

```text
http://127.0.0.1:8000/docs
```

---

### 4. Beispielabfragen

#### QUDT

```text
http://127.0.0.1:8000/map?source=qudt&search=Volt&lang=en&types=unit
```

#### VEC

```text
http://127.0.0.1:8000/map?source=vec&search=WireElement&lang=en
```

#### KBL

```text
http://127.0.0.1:8000/map?source=kbl&search=Wire_occurrence&lang=en
```

#### Alle Quellen

```text
http://127.0.0.1:8000/map?source=all&search=Wire&lang=en
```

---

### 5. Ports

| API | Port |
|---|---:|
| Gateway | 8000 |
| QUDT | 8001 |
| VEC | 8002 |
| KBL | 8003 |

---

### 6. Stoppen

Jede API kann im jeweiligen Terminal mit `CTRL + C` gestoppt werden.

## Gateway über das Internet veröffentlichen (Cloudflare Tunnel)

Damit die Swagger-Oberfläche (`/docs`) öffentlich erreichbar ist, kann ein kostenloser Cloudflare Tunnel verwendet werden.

Vorteile:
- Keine Router-Portfreigabe notwendig
- Keine öffentliche IP-Adresse
- Verschlüsselter Tunnel
- API bleibt lokal auf dem eigenen Rechner


### 1. Cloudflared installieren

Download:

https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/

Danach testen:

```bash
cloudflared --version
```


### 2. Alle APIs aktivieren

Starten sie alle einzelnen APIs in seperaten Terminals mit den jeweiligen Befehlen die in den Links hinterlegt sind.

- [API QUDT](#terminal-1-qudt-api)
- [API VEC](#terminal-2-vec-api)
- [API KBL](#terminal-3-kbl-api)
- [API Gateway](#terminal-4-api-gateway)


### 3. Cloudflare Tunnel starten

Neues zusätzliches Terminal öffnen.

Folgenden Befehl ausführen:

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```


### 4. Öffentlichen Link erhalten

Nach dem Start erscheint eine Ausgabe im Terminal, in dem der Cloudflare Tunnel gestartet wurde. Ähnlich wie:

```text
Your quick Tunnel has been created!
https://random-name.trycloudflare.com
```

Beispiel:

```text
https://updating-donated-afford-diagnostic.trycloudflare.com
```


### 5. Swagger öffentlich öffnen

Die Swagger UI ist anschließend erreichbar unter:

```text
https://random-name.trycloudflare.com/docs
```

Beispiel:

```text
https://updating-donated-afford-diagnostic.trycloudflare.com/docs
```

### Wichtig

Der öffentliche Zugriff funktioniert nur solange:
- das API Gateway läuft
- der Cloudflare Tunnel läuft
- der lokale Rechner eingeschaltet ist

Zum Beenden:

```text
CTRL + C
```

im jeweiligen Terminal drücken.