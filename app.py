"""
app.py
Servidor local institucional para la demostración de SITA-IA.
Materia: Fundamentos de Inteligencia Artificial (FIA - 3° Año).
Soporta multirrol, trazabilidad Prometheus, simulación de fallas F1, F2, F3 y Google AI Studio (Gemini API).
"""

import http.server
import json
import os
import sys
import urllib.parse
import webbrowser
from typing import Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from pipeline import ejecutar_pipeline
from gemini_service import generar_guia_tutor_gemini

PORT = 8050
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))

ESTADO_SESION: Dict[str, Any] = {
    "corte_campus": False,
    "dias_inaccion": 0,
    "intervenciones": {},        # legajo -> {accion, notas, fecha, estado}
    "derivaciones_pendientes": {},# legajo -> {tipo, motivo, aprobada}
    "recalibracion_aprobada": False,
    "fuentes_habilitadas_n8": True,
    "tutor_reasignado": None,
    "guias_gemini": {}           # legajo -> resultado API Gemini
}


class SITAHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            datos = ejecutar_pipeline(
                DATA_DIR,
                simular_corte_campus=ESTADO_SESION["corte_campus"],
                dias_inaccion_tutor=ESTADO_SESION["dias_inaccion"]
            )
            
            # Anexar intervenciones, derivaciones y guías de Gemini
            for e in datos["estudiantes"]:
                leg = e["legajo"]
                if leg in ESTADO_SESION["intervenciones"]:
                    e["intervencion_tutor"] = ESTADO_SESION["intervenciones"][leg]
                if leg in ESTADO_SESION["derivaciones_pendientes"]:
                    e["derivacion_institucional"] = ESTADO_SESION["derivaciones_pendientes"][leg]
                if leg in ESTADO_SESION["guias_gemini"]:
                    e["guia_gemini_api"] = ESTADO_SESION["guias_gemini"][leg]
                if ESTADO_SESION["tutor_reasignado"] and e.get("requiere_reasignacion_n6"):
                    e["tutor_asignado"] = ESTADO_SESION["tutor_reasignado"]
                    e["estado_sistema"] = "Reasignado formalmente (N6)"

            datos["estado_sesion"] = ESTADO_SESION
            self.wfile.write(json.dumps(datos, ensure_ascii=False).encode("utf-8"))
            return

        if parsed.path == "/" or parsed.path == "/index.html":
            self.path = "/demo_panel.html"

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            body = {}

        if parsed.path == "/api/gemini_guia":
            # Endpoint para invocar Google AI Studio (Gemini 1.5 Flash)
            legajo = body.get("legajo", "24901")
            api_key = body.get("api_key")
            
            # Obtener datos del alumno
            datos = ejecutar_pipeline(DATA_DIR, simular_corte_campus=ESTADO_SESION["corte_campus"])
            target = next((s for s in datos["estudiantes"] if s["legajo"] == legajo), None)
            
            if not target:
                target = {
                    "nombre": "González, Lucas (Caso X)",
                    "carrera": "Ingeniería en Sistemas de Información",
                    "comision": "Comisión 1 (Noche)",
                    "score_riesgo": 82,
                    "factores_explicativos": [
                        "Inasistencias continuas (40% acumulado en últimas 2 semanas)",
                        "Trabajos Prácticos adeudados (TP 2 y 3 sin entregar)",
                        "Inactividad digital prolongada en campus (12 días sin login)"
                    ]
                }

            gemini_res = generar_guia_tutor_gemini(target, api_key=api_key)
            ESTADO_SESION["guias_gemini"][legajo] = gemini_res

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "gemini_res": gemini_res}, ensure_ascii=False).encode("utf-8"))
            return

        if parsed.path == "/api/action":
            tipo = body.get("action")

            if tipo == "toggle_campus":
                ESTADO_SESION["corte_campus"] = not ESTADO_SESION["corte_campus"]
                msg = "Regla F1 conmutada."
            elif tipo == "reset_normal":
                ESTADO_SESION["corte_campus"] = False
                ESTADO_SESION["dias_inaccion"] = 0
                msg = "Sesión restablecida a semana normal."
            elif tipo == "intervencion":
                leg = body.get("legajo")
                opt = body.get("tipo_accion")
                notas = body.get("notas", "")
                ESTADO_SESION["intervenciones"][leg] = {
                    "accion": opt,
                    "notas": notas,
                    "registrado_por": "Prof. Joel Aisama"
                }
                if opt in ["comision", "beca", "gabinete"]:
                    ESTADO_SESION["derivaciones_pendientes"][leg] = {
                        "tipo": opt,
                        "motivo": notas,
                        "aprobada": False
                    }
                msg = f"Decisión de tutor registrada para #{leg}."
            elif tipo == "aprobar_derivacion":
                leg = body.get("legajo")
                if leg in ESTADO_SESION["derivaciones_pendientes"]:
                    ESTADO_SESION["derivaciones_pendientes"][leg]["aprobada"] = True
                msg = f"Coordinación aprobó la medida institucional para #{leg} (N3)."
            elif tipo == "simular_f2_10d":
                ESTADO_SESION["dias_inaccion"] = 10
                msg = "Simulación F2: Pasaron 10 días sin respuesta del tutor. Escalamiento activo."
            elif tipo == "reasignar_tutor":
                ESTADO_SESION["tutor_reasignado"] = "Prof. Martín Suárez (Tutor B)"
                msg = "Coordinación reasignó formalmente el caso al Tutor B (N6)."
            elif tipo == "aprobar_recalibracion":
                ESTADO_SESION["recalibracion_aprobada"] = True
                msg = "Coordinación aprobó la recalibración cuatrimestral tras verificar sesgo <= 10 pts (N7)."
            else:
                msg = "Acción procesada."

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": msg, "estado_sesion": ESTADO_SESION}, ensure_ascii=False).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


def run_server():
    server_address = ("", PORT)
    httpd = http.server.HTTPServer(server_address, SITAHandler)
    url = f"http://localhost:{PORT}/demo_panel.html"
    print(f"SITA-IA Server iniciado en {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")


if __name__ == "__main__":
    run_server()
