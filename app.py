"""
app.py
Servidor institucional SITA-IA (Punto de entrada del sistema).
Materia: Fundamentos de Inteligencia Artificial (FIA - 3° Año).
Arquitectura: Patrón Modelo-Vista-Controlador (MVC).

Estructura de la aplicación:
- Models:      models/ (agentes A1, A2, A3, generator, gemini_service)
- Views:       views/  (demo_panel.html, assets gráficos)
- Controllers: controllers/ (api_controller, pipeline_controller)
"""

import http.server
import json
import os
import sys
import urllib.parse
import webbrowser

# Configurar path raíz para resolución de módulos MVC
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from controllers.api_controller import SITAController

PORT = 8050
DATA_DIR = os.path.join(BASE_DIR, "data")
VIEWS_DIR = os.path.join(BASE_DIR, "views")

# Instancia central del controlador MVC
controller = SITAController(DATA_DIR)


class SITAEnterpriseHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Servir archivos estáticos desde el directorio de Vistas
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # Endpoint API REST: Obtener datos procesados por el Pipeline (Model -> Controller -> View)
        if parsed.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            datos = controller.obtener_estado_completo()
            self.wfile.write(json.dumps(datos, ensure_ascii=False).encode("utf-8"))
            return

        # Enrutamiento de Vistas
        if parsed.path in ["/", "/index.html", "/demo"]:
            self.path = "/views/demo_panel.html"
        elif parsed.path == "/demo_panel.html":
            self.path = "/views/demo_panel.html"

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            body = {}

        # Endpoint: Generación de Guía Pedagógica con Google AI Studio (Gemini API)
        if parsed.path == "/api/gemini_guia":
            legajo = body.get("legajo", "24901")
            api_key = body.get("api_key")
            res = controller.generar_guia_gemini(legajo=legajo, api_key=api_key)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "gemini_res": res}, ensure_ascii=False).encode("utf-8"))
            return

        # Endpoint: Procesamiento de Mutaciones y Reglas (N1 a N8, F1, F2, F3)
        if parsed.path == "/api/action":
            resp = controller.procesar_accion(body)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def end_headers(self):
        # Deshabilitar cache HTTP para inspección en tiempo real
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


def run_server():
    server_address = ("", PORT)
    httpd = http.server.HTTPServer(server_address, SITAEnterpriseHandler)
    url = f"http://localhost:{PORT}/views/demo_panel.html"
    print("=" * 65)
    print(" 🚀 SISTEMA SITA-IA · SERVICIO INICIADO CON PATRÓN MVC")
    print(f" 🌐 Acceso a la Plataforma: {url}")
    print(" 📂 Arquitectura: Models (src/models) | Views (views/) | Controllers")
    print(" 🔒 Gobernanza Ética: Puntos N1 a N8 y Regla C1 activos")
    print(" ⚡ API Google AI Studio: Gemini 1.5 Flash integrada")
    print(" Presione Ctrl + C para detener el servidor")
    print("=" * 65)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor SITA-IA detenido de forma segura.")


if __name__ == "__main__":
    run_server()
