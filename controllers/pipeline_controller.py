"""
controllers/pipeline_controller.py
Controlador de Orquestación del Pipeline Multiagente.
Patrón MVC: Coordina la ejecución secuencial de los Modelos (A1 -> A2 -> A3)
y genera la bitácora formal de Mensajería Prometheus (Mensajes 0 al 12).
"""

import os
import sys
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.generator import generar_datos
from models.agente1_monitoreo import AgenteMonitoreo
from models.agente2_riesgo import AgenteEvaluadorRiesgo
from models.agente3_alertas import AgentePriorizacion


def ejecutar_pipeline(
    data_dir: str,
    simular_corte_campus: bool = False,
    dias_inaccion_tutor: int = 0
) -> Dict[str, Any]:
    """Orquesta la inferencia de modelos y emite la trazabilidad Prometheus."""
    if not os.path.exists(os.path.join(data_dir, "asistencia.csv")) or not os.path.exists(os.path.join(data_dir, "historial.csv")):
        generar_datos(data_dir)

    mensajes: List[Dict[str, str]] = []

    # Msj 0* (N8)
    mensajes.append({
        "codigo": "P msj. 0*",
        "origen": "Coordinación",
        "destino": "A1 Monitoreo",
        "tipo": "ACEPTAR",
        "contenido": "Habilita fuentes del cuatrimestre con consentimientos estudiantiles registrados (N8).",
        "no_delegable": "N8"
    })

    # Msj 1
    mensajes.append({
        "codigo": "P msj. 1",
        "origen": "Docente",
        "destino": "A1 Monitoreo",
        "tipo": "INFORMAR",
        "contenido": "Carga de asistencia y notas de la semana (Docente no accede a scores C1).",
        "no_delegable": None
    })

    # 1. Ejecutar Modelo A1 (Monitoreo)
    a1 = AgenteMonitoreo(data_dir)
    perfiles, metricas_a1 = a1.ejecutar(simular_corte_campus=simular_corte_campus)

    if simular_corte_campus:
        mensajes.append({
            "codigo": "F1 msj. 2",
            "origen": "A1 Monitoreo",
            "destino": "A2 Eval. Riesgo",
            "tipo": "INFORMAR",
            "contenido": "Alerta F1: Corte detectado en telemetría de Campus Virtual. Perfiles incompletos.",
            "no_delegable": None
        })
        mensajes.append({
            "codigo": "F1 msj. 4",
            "origen": "A2 Eval. Riesgo",
            "destino": "A3 Alertas",
            "tipo": "INFORMAR",
            "contenido": "Riesgo 'sin evaluar' asignado a los afectados. No se inventa inactividad.",
            "no_delegable": None
        })
        mensajes.append({
            "codigo": "F1 msj. 6",
            "origen": "A3 Alertas",
            "destino": "Coordinación",
            "tipo": "PEDIR",
            "contenido": "Coordinación gestiona contingencia con Sistemas e instruye a tutores (N5).",
            "no_delegable": "N5"
        })
    else:
        mensajes.append({
            "codigo": "P msj. 2",
            "origen": "A1 Monitoreo",
            "destino": "A2 Eval. Riesgo",
            "tipo": "INFORMAR",
            "contenido": f"Transmisión de {len(perfiles)} perfiles semanales consolidados (Completitud: {metricas_a1['tasa_completitud_pct']}%).",
            "no_delegable": None
        })

    # 2. Ejecutar Modelo A2 (Evaluación de Riesgo / XAI)
    a2 = AgenteEvaluadorRiesgo()
    evaluados = a2.evaluar(perfiles, regla_f1=simular_corte_campus)

    if not simular_corte_campus:
        mensajes.append({
            "codigo": "P msj. 3",
            "origen": "A2 Eval. Riesgo",
            "destino": "A3 Alertas",
            "tipo": "PROPONER",
            "contenido": "Riesgo alto estimado para Caso X (#24901, 82/100) + 3 factores determinantes (XAI).",
            "no_delegable": None
        })

    # 3. Ejecutar Modelo A3 (Priorización y Carga Operativa)
    a3 = AgentePriorizacion()
    procesados, metricas_a3 = a3.priorizar(evaluados, dias_inaccion_tutor=dias_inaccion_tutor)

    if not simular_corte_campus:
        mensajes.append({
            "codigo": "P msj. 4",
            "origen": "A3 Alertas",
            "destino": "Tutor (Joel Aisama)",
            "tipo": "PROPONER",
            "contenido": f"Bandeja semanal asignada ({metricas_a3['casos_asignados_bandeja']} casos, respetando tope de 15).",
            "no_delegable": None
        })

    # Mensajes de Escalamiento F2
    if dias_inaccion_tutor >= 10:
        mensajes.append({
            "codigo": "F2 msj. 3",
            "origen": "A3 Alertas",
            "destino": "Tutor A",
            "tipo": "PEDIR",
            "contenido": "Recordatorio formal: Caso crítico pendiente hace 7 días.",
            "no_delegable": None
        })
        mensajes.append({
            "codigo": "F2 msj. 5",
            "origen": "A3 Alertas",
            "destino": "Coordinación",
            "tipo": "PEDIR",
            "contenido": "Escalamiento a los 10 días: se solicita reasignación por inacción prolongada.",
            "no_delegable": None
        })
        mensajes.append({
            "codigo": "F2 msj. 6",
            "origen": "Coordinación",
            "destino": "Tutor B",
            "tipo": "PEDIR",
            "contenido": "Coordinación reasigna el caso de riesgo al Tutor B (N6).",
            "no_delegable": "N6"
        })

    return {
        "metricas": {
            **metricas_a1,
            **metricas_a3
        },
        "mensajes_prometheus": mensajes,
        "estudiantes": procesados
    }
