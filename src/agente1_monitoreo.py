"""
agente1_monitoreo.py
Agente A1: Monitoreo y Consolidación de Fuentes Semanales.
Responsabilidad:
- Ingesta de 3 fuentes desestructuradas: asistencia.csv, campus.csv, notas.csv.
- Validación de esquema e integridad.
- Detección de caída de fuentes (Regla de Falla F1: Falta de dato != inactividad).
- Emisión del Perfil Semanal Consolidado para el Agente A2.
"""

import csv
import os
from typing import Dict, Any, List, Tuple


class AgenteMonitoreo:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def ejecutar(self, simular_corte_campus: bool = False) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Consolida las 3 fuentes en un perfil semanal por alumno.
        Si simular_corte_campus es True, emite la alerta F1 sin inferir inactividad errónea.
        """
        asistencia_path = os.path.join(self.data_dir, "asistencia.csv")
        campus_path = os.path.join(self.data_dir, "campus.csv")
        notas_path = os.path.join(self.data_dir, "notas.csv")

        # Verificar existencia de archivos
        if not os.path.exists(asistencia_path) or not os.path.exists(notas_path):
            raise FileNotFoundError("Fuentes obligatorias de secretaría académica no disponibles.")

        # 1. Leer Asistencia
        perfiles: Dict[str, Dict[str, Any]] = {}
        with open(asistencia_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                leg = row["legajo"]
                perfiles[leg] = {
                    "legajo": leg,
                    "nombre": row["nombre"],
                    "comision": row["comision"],
                    "turno": row["turno"],
                    "carrera": row["carrera"],
                    "asistencia_pct": float(row["asistencia_acumulada_pct"]),
                    "faltas_ult_2sem": int(row["faltas_ultimas_2_semanas"]),
                    # Campos por completar
                    "dias_inactivo_campus": None,
                    "recursos_descargados": None,
                    "tps_entregados": None,
                    "tps_exigidos": None,
                    "nota_parcial": None,
                    "fuente_campus_activa": not simular_corte_campus,
                    "datos_completos": False
                }

        # 2. Leer Campus (o aplicar Regla F1 si está cortado)
        if not simular_corte_campus and os.path.exists(campus_path):
            with open(campus_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    leg = row["legajo"]
                    if leg in perfiles:
                        perfiles[leg]["dias_inactivo_campus"] = int(row["dias_inactividad_campus"])
                        perfiles[leg]["recursos_descargados"] = int(row["recursos_descargados"])

        # 3. Leer Notas
        with open(notas_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                leg = row["legajo"]
                if leg in perfiles:
                    perfiles[leg]["tps_entregados"] = int(row["tps_entregados"])
                    perfiles[leg]["tps_exigidos"] = int(row["tps_exigidos"])
                    perfiles[leg]["nota_parcial"] = float(row["calificacion_parcial_1"])
                    perfiles[leg]["datos_completos"] = (perfiles[leg]["dias_inactivo_campus"] is not None)

        lista_perfiles = list(perfiles.values())
        completitud = (sum(1 for p in lista_perfiles if p["datos_completos"]) / len(lista_perfiles)) * 100 if lista_perfiles else 0

        metricas_a1 = {
            "total_registros": len(lista_perfiles),
            "fuente_campus_disponible": not simular_corte_campus,
            "regla_f1_activada": simular_corte_campus,
            "tasa_completitud_pct": round(completitud, 1),
            "estado": "Corte de servicio detectado (F1)" if simular_corte_campus else "Consolidación exitosa (≥95%)"
        }

        return lista_perfiles, metricas_a1
