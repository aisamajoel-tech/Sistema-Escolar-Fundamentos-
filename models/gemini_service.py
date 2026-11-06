"""
models/gemini_service.py
Asistente pedagógico con Google AI Studio (Gemini API).

Capacidad de IA: procesamiento de lenguaje natural (LLM).
Rol: a partir de los factores que explicaron la alerta, redacta una guía
para que el tutor prepare la entrevista (punto N2). La guía es para el
tutor: nunca se envía al estudiante.

Privacidad: el prompt NO incluye nombre, legajo, DNI ni correo. Solo
variables académicas (carrera, turno, puntaje y factores).

Configuración por variables de entorno:
- GEMINI_API_KEY : clave gratuita de https://aistudio.google.com/app/apikey
- GEMINI_MODEL   : modelo a usar (por defecto "gemini-1.5-flash"). Si Google
                   retira ese modelo, cambiarlo por uno vigente del catálogo.
Sin clave, o si la API falla, se devuelve una plantilla local equivalente.
"""

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List

DEFAULT_MODEL = "gemini-1.5-flash"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"


def construir_prompt(est: Dict[str, Any]) -> str:
    factores = est.get("factores_explicativos") or []
    puntaje = est.get("score_riesgo")
    puntaje_txt = f"{puntaje}/100" if puntaje is not None else "no calculado (señales contradictorias)"
    lista = "\n".join(f"- {f}" for f in factores) or "- Sin factores disponibles"
    return f"""Sos orientador pedagógico de una facultad de informática y ayudás a un tutor a preparar una entrevista.

Datos (anonimizados) de un estudiante de 1.er año:
- Carrera: {est.get('carrera', 'sin dato')}
- Turno: {est.get('turno', 'sin dato')}
- Índice de riesgo de abandono estimado: {puntaje_txt}
- Factores que explican la alerta:
{lista}

Redactá en español rioplatense, en formato markdown breve (máximo 220 palabras):
1. Posibles causas a explorar (2 o 3, sin afirmar nada como hecho).
2. Tres preguntas abiertas para iniciar la charla, en tono cálido y sin reproches.
3. Dos o tres acuerdos posibles (por ejemplo: plan de entregas, tutoría de pares, cambio de comisión a evaluar con Coordinación).

Reglas: no menciones el puntaje ni la palabra "riesgo" en las preguntas; no inventes datos personales."""


def _plantilla_local(est: Dict[str, Any]) -> str:
    claves = {d.get("clave") for d in (est.get("factores_detalle") or [])}
    factores: List[str] = est.get("factores_explicativos") or []

    preguntas = ["¿Cómo te estás sintiendo con la cursada en estas primeras semanas?"]
    if "asistencia" in claves:
        preguntas.append("¿Cómo venís acomodando los horarios de cursada con tus otras actividades?")
    if "entregas" in claves or "parcial" in claves:
        preguntas.append("¿Hay alguna materia o trabajo práctico que se te esté complicando más que el resto?")
    if "campus" in claves or not claves:
        preguntas.append("¿Pudiste entrar sin problemas al campus virtual y al material de las materias?")
    preguntas = preguntas[:3]

    lineas = ["### Guía para la entrevista",
              "**Objetivo:** entender cómo está viviendo la cursada y acordar próximos pasos, sin juzgar.",
              "",
              "#### Lo que muestran los datos"]
    lineas += [f"- {f}" for f in factores] or ["- Sin factores disponibles"]
    lineas += ["",
               "#### Posibles causas a explorar",
               "- Superposición con horarios laborales o familiares.",
               "- Dificultades con los contenidos o con el ritmo de alguna materia.",
               "- Problemas de acceso al campus virtual o a una computadora.",
               "",
               "#### Preguntas para abrir la conversación"]
    lineas += [f"{i}. {p}" for i, p in enumerate(preguntas, 1)]
    lineas += ["",
               "#### Acuerdos posibles",
               "- Un plan concreto para ponerse al día con las entregas, con fechas.",
               "- Tutoría de pares en la materia que más cuesta.",
               "- Si el horario es el problema, evaluar con Coordinación un cambio de comisión (N3).",
               "",
               "*Durante la charla no menciones puntajes ni etiquetas de riesgo.*"]
    return "\n".join(lineas)


def generar_guia_tutor_gemini(est: Dict[str, Any], api_key: str = None) -> Dict[str, Any]:
    prompt = construir_prompt(est)
    key = api_key or os.environ.get("GEMINI_API_KEY")
    modelo = os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)

    if not key:
        return {"modo": "sin_clave", "modelo": "plantilla local", "prompt_utilizado": prompt,
                "guia_generada": _plantilla_local(est)}

    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"temperature": 0.4, "maxOutputTokens": 700}}
    try:
        req = urllib.request.Request(API_URL.format(model=modelo, key=key),
                                     data=json.dumps(payload).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        texto = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"modo": "en_vivo", "modelo": modelo, "prompt_utilizado": prompt, "guia_generada": texto,
                "consumo_tokens": data.get("usageMetadata", {})}
    except (urllib.error.URLError, KeyError, IndexError, ValueError, TimeoutError) as e:
        return {"modo": "error_api", "modelo": modelo, "detalle": str(e)[:200], "prompt_utilizado": prompt,
                "guia_generada": _plantilla_local(est)}


if __name__ == "__main__":
    ejemplo = {
        "carrera": "Ing. en Sistemas de Información", "turno": "Noche", "score_riesgo": 82,
        "factores_detalle": [{"clave": "asistencia"}, {"clave": "campus"}, {"clave": "entregas"}],
        "factores_explicativos": ["Asistencia del 40 % con 4 faltas en las últimas dos semanas",
                                  "12 días sin ingresar al campus virtual",
                                  "2 de 3 trabajos prácticos sin entregar"],
    }
    r = generar_guia_tutor_gemini(ejemplo)
    print(f"Modo: {r['modo']} · Modelo: {r['modelo']}\n")
    print(r["guia_generada"])
