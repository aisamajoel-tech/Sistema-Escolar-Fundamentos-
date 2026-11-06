"""
models/agente2_riesgo.py
Agente A2: Evaluación de riesgo y explicabilidad (XAI).

Responsabilidades:
- Recibir los perfiles semanales consolidados por A1.
- Estimar la probabilidad de abandono con una regresión logística calibrada.
- Regla F1: si falta la fuente del campus, NO estima (estado "SIN EVALUAR").
- Explicar cada puntaje con los 3 factores que más aportaron (en puntos).

Calibración (cohorte de referencia):
- Perfil regular (asistencia 90 %, campus al día, TPs completos, parcial 8) -> ~10 puntos.
- Perfil Caso X (asistencia 40 %, 4 faltas, 12 días sin campus, 2 TPs, parcial 3.5) -> ~82 puntos.
"""

import math
from typing import Any, Dict, List


class AgenteEvaluadorRiesgo:
    BETA_0 = -2.50
    PESOS = {
        "asistencia": 0.0222,   # por cada punto porcentual por debajo del 100 %
        "faltas": 0.21,         # por falta en las últimas dos semanas
        "campus": 0.073,        # por día corrido sin ingresar al campus
        "entregas": 0.30,       # por trabajo práctico adeudado
        "parcial": 0.14,        # por punto por debajo de la nota de aprobación (6)
    }
    NOTA_APROBACION = 6.0
    UMBRAL_ALTO = 70
    UMBRAL_MEDIO = 40

    @staticmethod
    def _sigmoide(z: float) -> float:
        try:
            return 1.0 / (1.0 + math.exp(-z))
        except OverflowError:
            return 0.0 if z < 0 else 1.0

    def _nivel(self, score: int) -> str:
        if score >= self.UMBRAL_ALTO:
            return "ALTO"
        if score >= self.UMBRAL_MEDIO:
            return "MEDIO"
        return "BAJO"

    def evaluar(self, perfiles: List[Dict[str, Any]], regla_f1: bool = False) -> List[Dict[str, Any]]:
        evaluados = []
        w = self.PESOS

        for p in perfiles:
            item = dict(p)

            # Regla F1: falta de dato != inactividad
            if regla_f1 or not p.get("fuente_campus_activa", True) or p.get("dias_inactivo_campus") is None:
                item["score_riesgo"] = None
                item["nivel_riesgo"] = "SIN EVALUAR"
                item["factores_explicativos"] = [
                    "La fuente del campus virtual no envió datos esta semana.",
                    "Regla F1: la falta de datos no se interpreta como inactividad del estudiante.",
                    "El puntaje queda suspendido hasta que se restablezca la fuente.",
                ]
                item["factores_detalle"] = []
                item["historial"] = list(p.get("historial_previo", [20, 25, 30])) + [None]
                evaluados.append(item)
                continue

            asistencia = float(p["asistencia_pct"])
            faltas = int(p["faltas_ult_2sem"])
            dias = int(p["dias_inactivo_campus"])
            exigidos = int(p["tps_exigidos"])
            adeudados = max(0, exigidos - int(p["tps_entregados"]))
            nota = float(p["nota_parcial"])
            brecha = max(0.0, self.NOTA_APROBACION - nota)

            contribuciones = [
                ("asistencia",
                 w["asistencia"] * (100.0 - asistencia) + w["faltas"] * faltas,
                 f"Asistencia del {asistencia:.0f} % con {faltas} faltas en las últimas dos semanas"),
                ("entregas",
                 w["entregas"] * adeudados,
                 f"{adeudados} de {exigidos} trabajos prácticos sin entregar"),
                ("campus",
                 w["campus"] * dias,
                 f"{dias} días sin ingresar al campus virtual"),
                ("parcial",
                 w["parcial"] * brecha,
                 f"Primer parcial con nota {nota:.1f} (se aprueba con {self.NOTA_APROBACION:.0f})"),
            ]

            z = self.BETA_0 + sum(c for _, c, _ in contribuciones)
            score = max(1, min(99, int(round(self._sigmoide(z) * 100))))

            # Explicabilidad: reparte el puntaje según el aporte de cada factor
            positivas = [(k, c, t) for k, c, t in contribuciones if c > 0.05]
            total = sum(c for _, c, _ in positivas)
            positivas.sort(key=lambda x: x[1], reverse=True)
            detalle = [
                {"clave": k, "texto": t, "aporte": int(round(c / total * score)) if total else 0}
                for k, c, t in positivas[:3]
            ]

            item["score_riesgo"] = score
            item["nivel_riesgo"] = self._nivel(score)
            item["factores_detalle"] = detalle
            item["factores_explicativos"] = [d["texto"] for d in detalle]
            item["historial"] = list(p.get("historial_previo", [20, 25, 30])) + [score]
            evaluados.append(item)

        return evaluados
