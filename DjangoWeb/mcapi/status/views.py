from django.http import JsonResponse
from django.views.decorators.http import require_GET
from mcstatus import JavaServer, BedrockServer
from django.shortcuts import render

def index(request):
    return render(request, "index.html")

@require_GET
def mc_status(request):
    host = (request.GET.get("host") or "localhost").strip()
    port_q = request.GET.get("port")
    edition = (request.GET.get("edition") or "java").lower()  # "java" | "bedrock"
    timeout = float(request.GET.get("timeout") or 3.0)

    # Validación de puerto (opcional)
    port = None
    if port_q:
        try:
            port = int(port_q)
            if not (1 <= port <= 65535):
                raise ValueError()
        except ValueError:
            return JsonResponse({"error": "port inválido"}, status=400)

    # Direcciones por defecto
    default_port = 25565 if edition == "java" else 19132
    address = f"{host}:{port or default_port}"

    try:
        if edition == "java":
            # lookup resuelve SRV y acepta timeout
            server = JavaServer.lookup(address, timeout=timeout)
            status = server.status()  # 1.7+ -> players, latency, version, description
            motd_text = str(getattr(status, "description", "")) if hasattr(status, "description") else None
            sample = None
            try:
                sample = [p.name for p in (status.players.sample or [])]
            except Exception:
                sample = None

            data = {
                "online": True,
                "edition": "java",
                "host": host,
                "port": port or default_port,
                "latency_ms": getattr(status, "latency", None),
                "version": getattr(getattr(status, "version", None), "name", None),
                "protocol": getattr(getattr(status, "version", None), "protocol", None),
                "motd": motd_text,
                "players": {
                    "online": getattr(getattr(status, "players", None), "online", None),
                    "max":    getattr(getattr(status, "players", None), "max", None),
                    "sample": sample,
                },
            }

        elif edition == "bedrock":
            # Bedrock también soporta lookup() y status()
            server = BedrockServer.lookup(address, timeout=timeout)
            status = server.status()  # motd, map, gamemode, players, latency
            players_obj = getattr(status, "players", None)
            data = {
                "online": True,
                "edition": "bedrock",
                "host": host,
                "port": port or default_port,
                "latency_ms": getattr(status, "latency", None),
                "motd": getattr(status, "motd", None),
                "map": getattr(status, "map", None),
                "gamemode": getattr(status, "gamemode", None),
                "players": {
                    "online": getattr(players_obj, "online", None) if players_obj else None,
                    "max": getattr(players_obj, "max", None) if players_obj else None,
                },
            }

        else:
            return JsonResponse({"error": "edition debe ser 'java' o 'bedrock'."}, status=400)

        return JsonResponse(data)

    except Exception as e:
        # Errores típicos: host inválido, timeout, server offline, etc.
        return JsonResponse({"online": False, "error": str(e)}, status=503)
