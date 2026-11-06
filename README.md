# SITA-IA · Sistema Institucional de Tutorías y Alerta Temprana
**Materia:** Fundamentos de Inteligencia Artificial (3° Año)  
**Integrantes:** Joel Aisama · Bautista Navarro  
**Institución:** Universidad Champagnat — Facultad de Informática  

---

## 🏛️ Arquitectura del Sistema y Cadena de Agentes

El sistema implementa una arquitectura desacoplada de **tres agentes de software (IA débil)** y **cuatro actores humanos**, respetando el principio rector del Canvas: **«Un asistente que alerta y prioriza, no que decide»**.

```
  [ Fuentes Semanales CSV ]
 (asistencia, campus, notas)
             │
             ▼
┌────────────────────────────┐
│   Agente A1: Monitoreo     │  ==> Msj 1-2: Ingesta, completitud e integridad (Regla F1)
└────────────┬───────────────┘
             ▼
┌────────────────────────────┐
│   Agente A2: Evaluación    │  ==> Msj 3: Inferencia Logística (0-100) + XAI (Top 3 factores)
└────────────┬───────────────┘
             ▼
┌────────────────────────────┐
│   Agente A3: Alertas       │  ==> Msj 4: Priorización (tope 15) y contingencias (F2 / F3)
└────────────┬───────────────┘
             ▼
┌────────────────────────────┐
│  COMPUERTA HUMANA N1 - N4  │  ==> Msj 5-10: Decisión, contacto y derivación humana
└────────────────────────────┘
```

---

## 👥 Matriz de Roles y Reglas de Permisos

* **Tutor (Joel Aisama):**
  * Accede a la bandeja semanal priorizada (tope $\le 15$ casos).
  * Examina la explicabilidad matemática de los 3 factores de riesgo ($A2$).
  * Decide de forma humana si acepta el caso ($N1$), contacta al alumno ($N2$), propone una derivación ($N3$) o lo mantiene en seguimiento ($N4$).
* **Coordinación / Secretaría Académica (Bautista Navarro):**
  * Supervisa el padrón global de 120 estudiantes.
  * Aprueba medidas institucionales elevadas por tutores ($N3$).
  * Gestiona contingencias por corte de fuentes ($N5$).
  * Reasigna casos ante inacción prolongada de 10 días ($N6$).
  * Audita el sesgo inter-turno ($\Delta \text{recall} \le 10\text{ pts}$) y aprueba la recalibración cuatrimestral ($N7$).
  * Habilita fuentes con consentimiento registrado ($N8$, mensaje 0\*).
* **Docente de Cátedra (Regla de Diseño C1):**
  * Carga asistencia y notas de parciales/TPs.
  * **Regla C1:** La columna de score/nivel de riesgo de IA está **estrictamente oculta** para evitar sesgos de expectativa que influyan en cómo califica al estudiante.
* **Estudiante (Afectado):**
  * Decide si acepta o rechaza la entrevista de acompañamiento (mensaje 7).
  * Tiene derecho a conocer qué datos suyos utiliza el sistema.

---

## 📜 Trazabilidad de Mensajes Prometheus (Diagrama de Secuencia)

| # Código | Emisor $\rightarrow$ Receptor | Tipo | Contenido y Punto No Delegable |
| :---: | :--- | :---: | :--- |
| **P msj. 0\*** | Coordinación $\rightarrow$ A1 | `ACEPTAR` | Habilita fuentes con consentimientos registrados (**N8**). |
| **P msj. 1** | Docente $\rightarrow$ A1 | `INFORMAR` | Carga asistencia y notas (sin ver puntajes **C1**). |
| **P msj. 2** | A1 $\rightarrow$ A2 | `INFORMAR` | Transmite 120 perfiles consolidados semanales. |
| **P msj. 3** | A2 $\rightarrow$ A3 | `PROPONER` | Propone riesgo 82/100 para Caso X + 3 factores XAI. |
| **P msj. 4** | A3 $\rightarrow$ Tutor | `PROPONER` | Caso X en prioridad 1 de bandeja semanal (tope 15). |
| **P msj. 5** | Tutor $\rightarrow$ A3 | `ACEPTAR` | Tutor toma el caso (**N1**). |
| **P msj. 6** | Tutor $\rightarrow$ Estudiante | `PEDIR` | Tutor solicita charla de acompañamiento presencial (**N2**). |
| **P msj. 7** | Estudiante $\rightarrow$ Tutor | `ACEPTAR` | Estudiante acepta y cuenta dificultad laboral/horaria. |
| **P msj. 8** | Tutor $\rightarrow$ Coordinación | `PROPONER` | Tutor propone cambio de comisión/turno (**N3**). |
| **P msj. 9** | Coordinación $\rightarrow$ Tutor | `ACEPTAR` | Coordinación aprueba formalmente la medida institucional (**N3**). |
| **P msj. 10** | Tutor $\rightarrow$ A3 | `INFORMAR` | Caso registrado en seguimiento activo (**N4**). |
| **P msj. 11** | A3 $\rightarrow$ A2 | `INFORMAR` | Resultado etiquetado guardado para fin de cuatrimestre. |
| **P msj. 12\*** | Coordinación $\rightarrow$ A2 | `ACEPTAR` | Aprueba recalibración cuatrimestral tras auditar sesgo $\le 10$ pts (**N7**). |

---

## 🚨 Contingencias y Caminos de Falla

* **F1 (Corte de Campus):** La falta de telemetría **no se interpreta como inactividad** ($O8$). El scoring pasa a *«Sin Evaluar»* y Coordinación gestiona el restablecimiento ($N5$).
* **F2 (Inacción del Tutor):** A los **7 días** A3 envía recordatorio formal. A los **10 días** escala a Coordinación, quien reasigna al Tutor B ($N6$). **A3 nunca cubre al tutor escribiéndole al alumno.**
* **F3 (Señales Discordantes):** Alumno con 92% presencial pero campus inactivo $\ge 10$ días. A3 **no promedia**: marca *«En Revisión»* ($O9$). Si el tutor lo desestima, cuenta como **Falso Positivo** para el control de precisión ($\ge 50\%$).

---

## 🚀 Cómo Ejecutar la Demostración

1. **Modo Servidor Python:**
   ```bash
   python app.py
   ```
   *Abre automáticamente el navegador en `http://localhost:8050` con sincronización de estado y API REST.*

2. **Modo Autónomo:**
   Hacer doble clic en `demo_panel.html` en cualquier computadora (Chrome o Edge).
