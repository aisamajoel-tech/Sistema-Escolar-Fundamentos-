"""
agente2_riesgo.py
Agente A2: Evaluación Probabilística de Riesgo y Explicabilidad (XAI).
Responsabilidad:
- Recibe perfiles consolidados de A1.
- Aplica función logística multivariable calibrada para predecir propensión al abandono.
- Si la Regla F1 está activa (fuente caída), NO inventa puntaje: cataloga como 'SIN EVALUAR'.
- Extrae los 3 factores determinantes con mayor peso explicativo para el tutor (O3).
"""

import math
from typing import Dict, Any, List, Tuple


class AgenteEvaluadorRiesgo:
    def __init__(self):
        # Coeficientes beta calibrados del modelo logístico
        # z = beta_0 + sum(beta_i * x_i)
        self.beta_0 = -2.10
        self.w_asistencia = 0.055      # Cada punto porcentual que cae respecto al 100%
        self.w_faltas = 0.52          # Faltas en las últimas 2 semanas
        self.w_inactivo_campus = 0.18 # Días corridos sin login
        self.w_tps_adeudados = 0.75   # TPs no entregados
        self.w_nota_baja = 0.35       # Brecha negativa respecto a la nota mínima de aprobación (6.0)

    def _sigmoide(self, z: float) -> float:
        try:
            return 1.0 / (1.0 + math.exp(-z))
        except OverflowError:
            return 0.0 if z < 0 else 1.0

    def evaluar(self, perfiles: List[Dict[str, Any]], regla_f1: bool = False) -> List[Dict[str, Any]]:
        evaluados = []

        for p in perfiles:
            item = dict(p)

            # Si la fuente del campus se cayó (Regla F1)
            if regla_f1 or not p.get("fuente_campus_activa", True) or p.get("dias_inactivo_campus") is None:
                item["score_riesgo"] = None
                item["nivel_riesgo"] = "SIN EVALUAR"
                item["estado_sistema"] = "Sin evaluar (Falla F1: Corte en Campus)"
                item["factores_explicativos"] = [
                    "Corte detectado en la fuente de Campus Virtual.",
                    "Regla F1: La falta de datos no se interpreta como inactividad del estudiante.",
                    "Calificación preventiva suspendida para evitar falsos positivos."
                ]
                evaluados.append(item)
                continue

            # Cálculo de variables de riesgo
            caida_asistencia = max(0.0, 100.0 - p["asistencia_pct"])
            faltas_recientes = p["faltas_ult_2sem"]
            dias_inactivo = p["dias_inactivo_campus"]
            tps_debe = max(0, p["tps_exigidos"] - p["tps_entregados"])
            gap_nota = max(0.0, 6.0 - p["nota_parcial"])

            # Cálculo de logit z
            c_asistencia = self.w_asistencia * caida_asistencia
            c_faltas = self.w_faltas * faltas_recientes
            c_inactivo = self.w_inactivo_campus * dias_inactivo
            c_tps = self.w_tps_adeudados * tps_debe
            c_nota = self.w_nota_baja * gap_nota

            z = self.beta_0 + c_asistencia + c_faltas + c_inactivo + c_tps + c_nota
            probabilidad = self._sigmoide(z)
            score = int(round(probabilidad * 100))
            score = max(5, min(98, score)) # Acotar a rango realista

            # Explicabilidad (Top 3 Factores con mayor aporte al logit)
            aportes = [
                (
                    c_asistencia + c_faltas,
                    f"Inasistencias acumuladas: asistencia al {p['asistencia_pct']}% con {faltas_recientes} faltas en las últimas dos semanas."
                ),
                (
                    c_tps,
                    f"Trabajos Prácticos adeudados: {tps_debe} de {p['tps_exigidos']} entregas sin registrar."
                ),
                (
                    c_inactivo,
                    f"Inactividad digital: {dias_inactivo} días consecutivos sin acceso a los recursos del Campus."
                ),
                (
                    c_nota,
                    f"Rendimiento inicial: nota en Parcial 1 ({p['nota_parcial']}) por debajo de la media esperada."
                )
            ]

            # Ordenar por mayor contribución
            aportes.sort(key=lambda x: x[0], reverse=True)
            top_3 = [desc for _, desc in aportes[:3]]

            # Asignar nivel
            if score >= 70:
                nivel = "ALTO"
            elif score >= 40:
                nivel = "MEDIO"
            else:
                nivel = "BAJO"

            item["score_riesgo"] = score
            item["nivel_riesgo"] = nivel
            item["factores_explicativos"] = top_3
            evaluados.append(item)

        return evaluados
