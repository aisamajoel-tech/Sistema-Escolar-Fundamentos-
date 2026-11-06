import subprocess, os

html_src = r"C:\Users\aisam\OneDrive\Escritorio\3AÑO-FACULTAD\FUNDAMENTOS DE IA\TRABAJO GRUPAL\demo_panel.html"
with open(html_src, "r", encoding="utf-8") as f:
    content = f.read()

# Crear vista activa de Gemini
c_gemini = content.replace('style="background:#042f2e; border:1px solid #14b8a6; border-radius:8px; padding:14px; display:none;"', 'style="background:#042f2e; border:1px solid #14b8a6; border-radius:8px; padding:14px; display:block;"')

sample_output = """### 📋 Guía Pedagógica de Acompañamiento Tutor (Google AI Studio - Gemini 1.5 Flash)

Estudiante: Lucas González (#24901) · 1° Año Ing. en Sistemas (Noche)
Objetivo N2: Indagar barreras reales de cursada sin juzgar ni estigmatizar.

1. Diagnóstico Contextual Sugerido:
El patrón de ausencias en materias troncales sumado a TPs no entregados y 12 días sin campus suele responder a incompatibilidad laboral sobreviniente en el turno noche o bloqueo inicial en correlativas de programación, más que a desinterés vocacional.

2. Preguntas de Apertura Empática:
• «Hola Lucas, ¿cómo venís acomodando los horarios de cursada con tus otras actividades estas últimas dos semanas?»
• «Notamos que en Programación I los primeros prácticos se pusieron demandantes, ¿tuviste alguna traba puntual con las consignas o el entorno de desarrollo?»
• «¿Tuviste algún problema para ingresar al campus o descargar el material teórico de la materia?»

3. Propuesta de Acción Acordada (Punto N3):
• Ofrecer derivación a tutoría de pares para recuperar los dos TPs pendientes.
• Evaluar con Coordinación un cambio de turno a la mañana o franja intermedia si el trabajo es el impedimento (Medida N3)."""

c_gemini = c_gemini.replace("Generando guía de diálogo pedagógico...", sample_output)

temp_html = r"C:\Users\aisam\demo_sc_gemini.html"
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(c_gemini)

out_png = r"C:\Users\aisam\OneDrive\Escritorio\3AÑO-FACULTAD\FUNDAMENTOS DE IA\TRABAJO GRUPAL\screenshots\sc8_gemini_api.png"
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

subprocess.run([edge, "--headless", "--window-size=1400,900", f"--screenshot={out_png}", f"file:///{temp_html}"], check=True)
print(f"Captura Gemini guardada en: {out_png}")
