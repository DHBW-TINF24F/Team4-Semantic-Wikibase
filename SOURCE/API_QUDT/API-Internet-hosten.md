# FastAPI öffentlich über Cloudflare Tunnel hosten (kostenlos)

Diese Anleitung beschreibt, wie eine lokal laufende FastAPI-Anwendung inklusive Swagger UI (`/docs`) kostenlos und sicher über das Internet erreichbar gemacht werden kann, ohne Portfreigaben im Router.

---

# Voraussetzungen

Installiert sein müssen:

* Python
* FastAPI
* Uvicorn
* cloudflared

---

# 1. FastAPI und Uvicorn installieren

```bash
pip install fastapi uvicorn
```

---

# 2. Cloudflared installieren

Download:

https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/

Danach testen:

```bash
cloudflared --version
```

---

# 3. FastAPI lokal starten


API starten:

```bash
uvicorn api_qudt:app --host 127.0.0.1 --port 8000 --proxy-headers
```

---

# 4. Lokal testen

Swagger UI öffnen:

```text
http://127.0.0.1:8000/docs
```

Wenn Swagger angezeigt wird, funktioniert die API lokal korrekt.

---

# 5. Cloudflare Tunnel starten

Neues Terminal öffnen:

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

---

# 6. Öffentlichen Link erhalten

Nach dem Start erscheint ein Link im Terminal wie:

```text
https://random-name.trycloudflare.com
```

Beispiel:

```text
https://updating-donated-afford-diagnostic.trycloudflare.com
```

---

# 7. Swagger öffentlich öffnen

Swagger UI:

```text
https://random-name.trycloudflare.com/docs
```

Beispiel:

```text
https://updating-donated-afford-diagnostic.trycloudflare.com/docs
```

---

# Sicherheit

## Vorteile dieser Methode

* Keine Router-Portfreigabe notwendig
* Keine direkte öffentliche IP
* Verschlüsselter Tunnel
* API bleibt lokal auf dem eigenen Rechner

## Wichtig

Die API funktioniert nur solange:

### Terminal 1 läuft

```bash
uvicorn test_api:app --host 127.0.0.1 --port 8000 --proxy-headers
```

### Terminal 2 läuft

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

Wenn eines der beiden Programme beendet wird, ist die API nicht mehr öffentlich erreichbar.

---

# Tunnel beenden

In beiden Terminals:

```text
CTRL + C
```

Danach ist die API wieder vollständig offline.

---

# Hinweise

* Der generierte `trycloudflare.com` Link ist temporär.
* Bei jedem Neustart wird ein neuer Link erzeugt.
* Für dauerhafte eigene Domains wird ein Cloudflare-Account mit eigener Domain benötigt.
