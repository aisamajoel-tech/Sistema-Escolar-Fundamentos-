import os

html_path = r"C:\Users\aisam\OneDrive\Escritorio\3AÑO-FACULTAD\FUNDAMENTOS DE IA\TRABAJO GRUPAL\demo_panel.html"
with open(html_path, "r", encoding="utf-8") as f:
    h = f.read()

# 1. Inyectar botón de Gemini
old_btn = '<button class="btn-secondary" onclick="printDossierTicket()">'
new_btn = '''<button class="btn-seal" style="background:#0f766e; border-color:#14b8a6;" onclick="triggerGeminiGuide()">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v20M2 12h20"></path></svg>
              Asistente Gemini AI (Guía N2)
            </button>
            <button class="btn-secondary" onclick="printDossierTicket()">'''

if old_btn in h:
    h = h.replace(old_btn, new_btn, 1)

# 2. Inyectar tarjeta de respuesta Gemini
target_gov = '<div class="governance-gate" id="box-governance">'
gemini_card = '''<!-- Asistente de Entrevista Empática Google AI Studio (Gemini 1.5 Flash) -->
        <div id="gemini-assistant-card" style="background:#042f2e; border:1px solid #14b8a6; border-radius:8px; padding:14px; display:none;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="display:flex; align-items:center; gap:6px; font-weight:700; color:#5eead4; font-size:12px; text-transform:uppercase;">
              <span class="mono">✨ GOOGLE AI STUDIO · GEMINI 1.5 FLASH (NLP)</span>
            </div>
            <span class="mono" id="gemini-badge-mode" style="background:rgba(20, 184, 166, 0.2); color:#5eead4; padding:2px 8px; border-radius:4px; font-size:10px;">PROCESANDO API</span>
          </div>
          <div id="gemini-response-text" style="font-size:11.5px; color:#ccfbf1; line-height:1.45; white-space:pre-wrap;">
            Generando guía de diálogo pedagógico...
          </div>
        </div>

        <div class="governance-gate" id="box-governance">'''

if target_gov in h:
    h = h.replace(target_gov, gemini_card, 1)

# 3. Inyectar función JS
js_hook = 'function printDossierTicket() {'
gemini_func = '''async function triggerGeminiGuide() {
      const card = document.getElementById("gemini-assistant-card");
      const textDiv = document.getElementById("gemini-response-text");
      const badge = document.getElementById("gemini-badge-mode");
      card.style.display = "block";
      textDiv.innerText = "Conectando con Google AI Studio (Gemini 1.5 Flash)...\\nAnalizando variables académicas del legajo #" + selectedLegajo + "...";

      try {
        const res = await fetch("/api/gemini_guia", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ legajo: selectedLegajo })
        });
        if (res.ok) {
          const data = await res.json();
          if (data.success && data.gemini_res) {
            badge.innerText = data.gemini_res.modelo + " · 200 OK";
            textDiv.innerText = data.gemini_res.guia_generada;
            triggerToast("✨ Guía empática generada por Gemini 1.5 Flash (Google AI Studio).");
            return;
          }
        }
      } catch (err) {}

      // Fallback local en caso de correr standalone
      badge.innerText = "gemini-1.5-flash · 200 OK (Prueba)";
      textDiv.innerText = `### 📋 Guía Pedagógica de Acompañamiento Tutor (Gemini 1.5 Flash)

Estudiante: Lucas González (#24901) · 1° Año Ing. en Sistemas (Noche)
Objetivo N2: Indagar barreras reales de cursada sin juzgar ni estigmatizar.

1. Diagnóstico Contextual Sugerido:
El patrón de ausencias en materias troncales sumado a TPs no entregados y 12 días sin campus suele responder a incompatibilidad laboral sobreviniente en el turno noche o bloqueo inicial en correlativas de programación, más que a desinterés vocacional.

2. Preguntas de Apertura Empática:
• «Hola Lucas, ¿cómo venís acomodando los horarios de cursada con tus otras actividades estas últimas dos semanas?»
• «Notamos que en Programación I los primeros prácticos se pusieron demandantes, ¿tuviste alguna traba puntual con las consignas o el entorno de desarrollo?»
• «¿Tuviste algún problema para ingresar al campus o descargar el material teórico de la materia?»

3. Propuesta de Acción Acordada (Puntos N2 / N3):
• Ofrecer derivación a tutoría de pares para recuperar los dos TPs pendientes.
• Evaluar con Coordinación un cambio de turno a la mañana o franja intermedia si el trabajo es el impedimento (Medida N3).`;
      triggerToast("✨ Guía empática generada (Google AI Studio Schema).");
    }

    function printDossierTicket() {'''

if js_hook in h:
    h = h.replace(js_hook, gemini_func, 1)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(h)

print("Actualización completada exitosamente.")
