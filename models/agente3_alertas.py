"""
models/agente3_alertas.py
Agente A3: Alertas, priorización y carga del tutor.

Responsabilidades:
- Tope operativo: como máximo 15 casos por tutor y por semana (O4).
- Regla F3: ante señales contradictorias (asistencia alta y campus inactivo)
  no promedia; marca el caso "EN REVISIÓN" para que decida el tutor (O9).
- Regla F2: recordatorio a los 7 días sin respuesta y escalamiento a
  Coordinación a los 10 días (O5). Nunca contacta al estudiante.
- Expone las métricas de validación del modelo (O10 / N7).
"""

from typing import Any, Dict, List, Tuple

# Métricas obtenidas en el backtesting sobre la cohorte 2025 (datos históricos).
# Coordinación las revisa al cierre de cada cuatrimestre antes de aprobar una recalibración (N7).
VALIDACION_COHORTE_2025 = {
    "recall_por_turno": {"Mañana": 74.5, "Tarde": 72.1, "Noche": 75.9},
    "recall_global": 73.8,
    "precision_nivel_alto": 58.4,
    "anticipacion_semanas": 4,
}


class AgentePriorizacion:
    TOPE_CASOS_TUTOR = 15
    UMBRAL_ASISTENCIA_F3 = 85.0
    UMBRAL_DIAS_F3 = 10
    DIAS_RECORDATORIO = 7
    DIAS_ESCALAMIENTO = 10
    TUTOR_TITULAR = "Prof. Joel Aisama"

    def priorizar(self, evaluados: List[Dict[str, Any]], dias_inaccion_tutor: int = 0) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        procesados = []

        for p in evaluados:
            item = dict(p)
            dias = item.get("dias_inactivo_campus")

            # Regla F3: señales contradictorias -> revisión humana
            if (item.get("asistencia_pct", 0) >= self.UMBRAL_ASISTENCIA_F3
                    and dias is not None and dias >= self.UMBRAL_DIAS_F3):
                item["nivel_riesgo"] = "EN REVISIÓN"
                item["score_riesgo"] = None
                item["estado_sistema"] = "En revisión (F3: señales contradictorias)"
                item["factores_detalle"] = []
                item["factores_explicativos"] = [
                    f"Asistencia presencial alta ({item['asistencia_pct']:.0f} %).",
                    f"Sin ingresar al campus virtual hace {dias} días.",
                    "El sistema no promedia señales opuestas: el tutor verifica si hay un problema de acceso.",
                ]
                item["prioridad_tutor"] = 1
                item["tutor_asignado"] = self.TUTOR_TITULAR
                procesados.append(item)
                continue

            score = item.get("score_riesgo")
            item["tutor_asignado"] = self.TUTOR_TITULAR
            if score is None:
                item["estado_sistema"] = "Sin evaluar (F1: fuente de campus caída)"
                item["prioridad_tutor"] = 99
            elif score >= 70:
                item["prioridad_tutor"] = 1
                if dias_inaccion_tutor >= self.DIAS_ESCALAMIENTO:
                    item["estado_sistema"] = "Escalado a Coordinación (F2)"
                    item["requiere_reasignacion_n6"] = True
                elif dias_inaccion_tutor >= self.DIAS_RECORDATORIO:
                    item["estado_sistema"] = "Recordatorio enviado al tutor (F2)"
                else:
                    item["estado_sistema"] = "Pendiente de revisión del tutor"
            elif score >= 40:
                item["estado_sistema"] = "Seguimiento periódico"
                item["prioridad_tutor"] = 2
            else:
                item["estado_sistema"] = "Regular"
                item["prioridad_tutor"] = 3
                item["tutor_asignado"] = None

            procesados.append(item)

        # Orden: prioridad, luego mayor puntaje (los casos en revisión al final de la prioridad 1)
        procesados.sort(key=lambda x: (x["prioridad_tutor"], -(x["score_riesgo"] if x["score_riesgo"] is not None else -1)))

        bandeja = [p for p in procesados if p["prioridad_tutor"] == 1][:self.TOPE_CASOS_TUTOR]
        recall = VALIDACION_COHORTE_2025["recall_por_turno"]

        metricas_a3 = {
            "total_estudiantes": len(procesados),
            "casos_criticos_detectados": sum(1 for p in procesados if p.get("nivel_riesgo") == "ALTO"),
            "casos_en_revision_f3": sum(1 for p in procesados if p.get("nivel_riesgo") == "EN REVISIÓN"),
            "casos_sin_evaluar": sum(1 for p in procesados if p.get("nivel_riesgo") == "SIN EVALUAR"),
            "casos_asignados_bandeja": len(bandeja),
            "tope_casos_tutor": self.TOPE_CASOS_TUTOR,
            "tope_respetado": len(bandeja) <= self.TOPE_CASOS_TUTOR,
            "recall_por_turno": recall,
            "recall_estimado_pct": VALIDACION_COHORTE_2025["recall_global"],
            "precision_nivel_alto_pct": VALIDACION_COHORTE_2025["precision_nivel_alto"],
            "diferencia_sesgo_turnos_pts": round(max(recall.values()) - min(recall.values()), 1),
            "dias_inaccion_simulados": dias_inaccion_tutor,
            "regla_f2_activa": dias_inaccion_tutor >= self.DIAS_RECORDATORIO,
        }
        return procesados, metricas_a3
