# API de Estado de Minecraft (Django)

Proyecto Django mínimo que expone **un endpoint GET** para consultar el estado de un servidor de **Minecraft** (Java o Bedrock) usando la librería `mcstatus`.

- **Endpoint:** `GET /api/mc/status`
- **Casos de uso:** health checks, paneles, bots, “¿está arriba el server?”, mostrar jugadores conectados, etc.

---

## TL;DR (instalación y arranque rápido)

```bash
# 1) Entorno y dependencias
python -m venv venv
source venv/bin/activate         # Windows: venv\Scripts\activate
pip install "Django>=5.0,<6.0" "mcstatus>=12.0.0"

# 2) Proyecto + app
django-admin startproject mcapi
cd mcapi
python manage.py startapp status

# 3) Conectar la vista y URL (ver /status/views.py y mcapi/urls.py)
python manage.py runserver 0.0.0.0:8000

# 4) Probar
curl "http://localhost:8000/api/mc/status?host=play.hypixel.net"
```

**Respuesta ejemplo**

```bash
#json
{
  "online": true,
  "edition": "java",
  "host": "play.hypixel.net",
  "port": 25565,
  "latency_ms": 123.4,
  "version": "1.21.1",
  "protocol": 767,
  "motd": "Hypixel Network ...",
  "players": {
    "online": 50000,
    "max": 65000,
    "sample": ["PlayerOne", "PlayerTwo"]
  }
}
```
