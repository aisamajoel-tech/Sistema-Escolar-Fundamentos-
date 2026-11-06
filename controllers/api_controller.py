"""
controllers/api_controller.py
Controlador de API y orquestación de solicitudes HTTP.
Patrón MVC: Gestiona el flujo entre las Vistas (Web/Panel) y los Modelos (Agentes IA y Gemini API).
"""

from typing import Dict, Any
from controllers.pipeline_controller import ejecutar_pipeline
from models.gemini_service import generar_guia_tutor_gemini


class SITAController:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.estado_sesion: Dict[str, Any] = {
            "corte_campus": False,
            "dias_inaccion": 0,
            "intervenciones": {},
            "derivaciones_pendientes": {},
            "recalibracion_aprobada": False,
            "fuentes_habilitadas_n8": True,
            "tutor_reasignado": None,
            "guias_gemini": {}
        }

    def obtener_estado_completo(self) -> Dict[str, Any]:
        """Ejecuta el pipeline de modelos y combina con el estado transaccional."""
        datos = ejecutar_pipeline(
            self.data_dir,
            simular_corte_campus=self.estado_sesion["corte_campus"],
            dias_inaccion_tutor=self.estado_sesion["dias_inaccion"]
        )

        for e in datos["estudiantes"]:
            leg = e["legajo"]
            if leg in self.estado_sesion["intervenciones"]:
                e["intervencion_tutor"] = self.estado_sesion["intervenciones"][leg]
            if leg in self.estado_sesion["derivaciones_pendientes"]:
                e["derivacion_institucional"] = self.estado_sesion["derivaciones_pendientes"][leg]
            if leg in self.estado_sesion["guias_gemini"]:
                e["guia_gemini_api"] = self.estado_sesion["guias_gemini"][leg]
            if self.estado_sesion["tutor_reasignado"] and e.get("requiere_reasignacion_n6"):
                e["tutor_asignado"] = self.estado_sesion["tutor_reasignado"]
                e["estado_sistema"] = "Reasignado formalmente (N6)"

        datos["estado_sesion"] = self.estado_sesion
        return datos

    def generar_guia_gemini(self, legajo: str, api_key: str = None) -> Dict[str, Any]:
        """Invoca el Modelo de Lenguaje Gemini para generar la guía empática del tutor."""
        datos = self.obtener_estado_completo()
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

        res = generar_guia_tutor_gemini(target, api_key=api_key)
        self.estado_sesion["guias_gemini"][legajo] = res
        return res

    def procesar_accion(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa mutaciones del estado transaccional (Puntos N1 a N8 y contingencias)."""
        tipo = body.get("action")

        if tipo == "toggle_campus":
            self.estado_sesion["corte_campus"] = not self.estado_sesion["corte_campus"]
            msg = "Regla F1 conmutada (Corte/Restablecimiento de Campus)."
        elif tipo == "reset_normal":
            self.estado_sesion["corte_campus"] = False
            self.estado_sesion["dias_inaccion"] = 0
            msg = "Sesión restablecida a semana normal de cursada."
        elif tipo == "intervencion":
            leg = body.get("legajo")
            opt = body.get("tipo_accion")
            notas = body.get("notas", "")
            self.estado_sesion["intervenciones"][leg] = {
                "accion": opt,
                "notas": notas,
                "registrado_por": "Prof. Joel Aisama"
            }
            if opt in ["comision", "beca", "gabinete"]:
                self.estado_sesion["derivaciones_pendientes"][leg] = {
                    "tipo": opt,
                    "motivo": notas,
                    "aprobada": False
                }
            msg = f"Decisión humana de tutor registrada para #{leg} (N1/N2)."
        elif tipo == "aprobar_derivacion":
            leg = body.get("legajo")
            if leg in self.estado_sesion["derivaciones_pendientes"]:
                self.estado_sesion["derivaciones_pendientes"][leg]["aprobada"] = True
            msg = f"Coordinación aprobó formalmente la medida institucional para #{leg} (N3)."
        elif tipo == "simular_f2_10d":
            self.estado_sesion["dias_inaccion"] = 10
            msg = "Simulación F2: Pasaron 10 días sin respuesta del tutor. Escalamiento N6 activo."
        elif tipo == "reasignar_tutor":
            self.estado_sesion["tutor_reasignado"] = "Prof. Martín Suárez (Tutor B)"
            msg = "Coordinación reasignó formalmente el caso al Tutor B (N6)."
        elif tipo == "aprobar_recalibracion":
            self.estado_sesion["recalibracion_aprobada"] = True
            msg = "Coordinación aprobó la recalibración tras verificar sesgo <= 10 pts (N7)."
        else:
            msg = "Acción procesada."

        return {"success": True, "message": msg, "estado_sesion": self.estado_sesion}
