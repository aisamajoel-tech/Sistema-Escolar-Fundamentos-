# 🏛️ SITA-IA · Sistema Institucional de Tutorías y Alerta Temprana
> **Portal Académico Universitario e Inteligencia Artificial Híbrida para la Prevención Temprana de la Deserción Estudiantil con Gobernanza Ética (*Human-in-the-Loop*).**

[![GitHub Repository](https://img.shields.io/badge/GitHub-aisamajoel--tech%2FSistema--Escolar--Fundamentos---181717?logo=github)](https://github.com/aisamajoel-tech/Sistema-Escolar-Fundamentos-)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-2563eb.svg)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Arquitectura-MVC%20Enterprise-d97706.svg)]()
[![AI Engine](https://img.shields.io/badge/IA%20Híbrida-Regresión%20Logística%20XAI%20%2B%20Gemini%201.5%20Flash-15803d.svg)](https://aistudio.google.com/)
[![Governance](https://img.shields.io/badge/Gobernanza-Puntos%20N1--N8%20%2B%20Regla%20C1-6d28d9.svg)]()

---

## 📌 1. ¿Qué es SITA-IA y Qué Hace?

### ¿Qué es el sistema?
**SITA-IA** (*Sistema Institucional de Tutorías y Alerta Temprana*) es una plataforma web académica diseñada para la **Facultad de Informática de la Universidad Champagnat** (Materia: *Fundamentos de Inteligencia Artificial - 3° Año*). Integra en un único portal universitario la gestión de **cursos, cátedras, asistencia, entregas de trabajos prácticos, claustro docente y el módulo de alerta temprana pedagógica**.

### ¿Qué problema institucional resuelve?
En el primer año universitario, más del 30 % del desgranamiento ocurre durante las primeras 6 a 8 semanas de cursada. Tradicionalmente, la institución detecta el abandono **demasiado tarde** (cuando el estudiante ya reprobó los parciales o dejó de asistir). SITA-IA unifica señales que antes estaban dispersas para anticipar el riesgo de deserción con **al menos 4 semanas de antelación**, permitiendo que el equipo de tutorías acompañe al alumno a tiempo.

### ¿Qué hace exactamente paso a paso? (Flujo Multiagente $A1 \rightarrow A2 \rightarrow A3$ + Gemini API)
1. **Consolidación Semanal de Fuentes (`Agente A1 - Monitoreo`):**
   * Procesa cada semana tres fuentes institucionales: **asistencia presencial** (`asistencia.csv`), **actividad en el Campus Virtual Moodle** (`campus.csv`) y **entregas de TPs / notas de parciales** (`notas.csv`), además de la serie histórica (`historial.csv`).
   * **Salvaguarda de Falla `F1`:** Si el servidor del campus se cae, el sistema **jamás asume que el estudiante abandonó** (*falta de dato $\neq$ inactividad*). Suspende el cálculo y marca el estado como `SIN EVALUAR` hasta que Coordinación restablezca el servicio (`Punto N5`).
2. **Estimación Probabilística y Explicabilidad XAI (`Agente A2 - Evaluación de Riesgo`):**
   * Aplica un modelo supervisado interpretable (**Regresión Logística Calibrada**, $P = \sigma(z)$) que calcula un **Score de Riesgo de 0 a 100** junto con la trayectoria de las últimas 4 semanas.
   * **Explicabilidad Algorítmica (`XAI`):** Desglosa los **3 factores determinantes** que explican el puntaje en puntos aditivos (por ejemplo, en el *Caso Lucas González #24901*: Score `82/100` explicado por `+35 pts` de inasistencias recientes, `+27 pts` por 2 TPs sin entregar y `+20 pts` por 12 días sin ingresar al campus).
3. **Priorización Operativa y Desambiguación (`Agente A3 - Alertas`):**
   * Ordena las alertas respetando un **tope operativo estricto de $\le 15$ casos activos por tutor (`O4`)** para evitar la saturación del equipo humano.
   * **Salvaguarda de Señales Contradictorias (`F3`):** Si un alumno presenta alta asistencia presencial ($\ge 85\%$) pero nula actividad en el campus ($\ge 10$ días, como *Mateo Fernández #24945*), el agente **no promedia ciegamente** ambas variables: asigna el estado `EN REVISIÓN (F3)` para que el tutor verifique con el estudiante.
   * **Protocolo ante Inacción del Tutor (`F2`):** Si un caso crítico no recibe atención en **7 días**, emite un recordatorio al tutor; a los **10 días ($7+3$)**, escala el caso a Coordinación para su **reasignación formal a un Tutor B (`Punto N6`)**.
4. **Asistencia Generativa para Entrevistas Empáticas (`Google AI Studio - Gemini 1.5 Flash API`):**
   * Cuando el tutor prepara la entrevista con un alumno en riesgo (`Punto N2`), SITA-IA consulta la API de **Gemini 1.5 Flash** enviando **únicamente indicadores académicos anonimizados** (sin DNI ni datos sensibles).
   * Gemini devuelve en formato JSON estructurado una **apertura empática no punitiva**, **3 preguntas abiertas** para indagar causas laborales o pedagógicas y una **medida institucional sugerida**.

### 🚫 ¿Qué NO hace el sistema? (Límites Éticos y Puntos No Delegables `N1`–`N8`)
* **No contacta automáticamente al estudiante:** Ningún bot ni correo automático notifica al alumno que "está en riesgo". Todo contacto es humano y empático a través del tutor (`N2`).
* **No sanciona, no da de baja ni altera notas:** El sistema es exclusivamente preventivo y de acompañamiento.
* **No expone el puntaje de riesgo a los docentes de cátedra (`Regla C1`):** Los profesores de materias (*Programación I, Álgebra, etc.*) cargan asistencia y notas, pero tienen la columna de riesgo **bloqueada con candado (`🔒 C1`)** para evitar sesgos de confirmación o efecto Pigmalión al corregir exámenes.
* **No se auto-recalibra sin auditoría humana (`N7`):** Al cierre del cuatrimestre, Coordinación verifica que la diferencia de sensibilidad (*Recall*) entre los turnos Mañana, Tarde y Noche sea $\le 10\text{ puntos porcentuales}$ (`3.8 pts` actuales) antes de autorizar cualquier ajuste de pesos.

---

## 🖥️ 2. Arquitectura del Portal Universitario (4 Módulos y 4 Roles)

La interfaz fue diseñada siguiendo principios de arquitectura de software institucional, separando claramente las vistas según el módulo académico y el rol activo:

| Módulo en Barra Lateral | ¿Qué contiene? | Roles Principales |
| :--- | :--- | :--- |
| **1. 📚 Mis Cursos y Cátedras** | Cursada de 1° año (*Algoritmos y Programación I, Álgebra, Sistemas y Organizaciones, Arquitectura*), horarios, cátedras, planilla docente con **bloqueo C1** y **Espacio de Tutoría Estudiantil**. | **Alumno** (*Lucas González*) y **Docente de Cátedra** (*Prof. Méndez*) |
| **2. 🚨 Alerta Temprana SITA** | KPIs de cohorte (`120 alumnos`), tabla maestra priorizada (`12/15 casos`) y **Expediente Pedagógico Individual** con gráfico de 4 semanas, barras **XAI**, generador **Gemini 1.5 Flash** y formulario de decisión humana (`N1`–`N4`). | **Tutor Pedagógico** (*Prof. Joel Aisama*) |
| **3. 👨‍🏫 Claustro y Tutores** | Directorio del equipo de tutorías (*Tutor A: Joel Aisama*, *Tutor B: Martín Suárez*), balanceo de carga operativa ($\le 15$ casos) y nómina de cátedras sujetas a la Regla C1. | Todos los roles institucionales |
| **4. 🏛️ Administración y N1–N8** | Panel de **Coordinación Académica**: aprobación de derivaciones (`N3`), protocolo de inacción de 10 días y reasignación (`F2 / N6`), auditoría de sesgo inter-turno (`N7`, $\Delta = 3.8\text{ pts}$) y bitácora del protocolo **Prometheus (`Msj 0*` a `Msj 12*`)**. | **Coordinación** (*Bautista Navarro*) |

---

## 📂 3. Estructura del Proyecto (Patrón MVC)

El código fuente respeta estrictamente el patrón **Modelo-Vista-Controlador (MVC)**:

```text
Sistema-Escolar-Fundamentos-/
│
├── models/                           # 🧠 [MODEL]: Lógica de dominio, agentes IA y conexión Gemini
│   ├── agente1_monitoreo.py          # Agente A1: Ingesta de 3 fuentes CSV + historial + Regla F1
│   ├── agente2_riesgo.py             # Agente A2: Regresión logística calibrada (0-100) + XAI
│   ├── agente3_alertas.py            # Agente A3: Tope <=15 por tutor, Regla F3, F2 y sesgo N7
│   ├── gemini_service.py             # Cliente REST para Google AI Studio (Gemini 1.5 Flash) + fallback
│   └── generator.py                  # Generador determinista de la cohorte de 120 estudiantes
│
├── views/                            # 🖥️ [VIEW]: Interfaz gráfica del Portal Académico UCH
│   ├── demo_panel.html               # Aplicación web institucional multirrol y multimódulo
│   └── logo_uch.png                  # Escudo institucional Universidad Champagnat
│
├── controllers/                      # ⚙️ [CONTROLLER]: Orquestación HTTP y trazabilidad Prometheus
│   ├── api_controller.py             # Controlador REST (/api/data, /api/gemini_guia, /api/action)
│   └── pipeline_controller.py        # Ejecución secuencial A1 -> A2 -> A3 y bitácora Prometheus
│
├── data/                             # 📊 Fuentes de datos semanales (120 estudiantes de 1° año)
│   ├── asistencia.csv                # Porcentaje de asistencia y faltas de las últimas 2 semanas
│   ├── campus.csv                    # Días de inactividad en Moodle y recursos descargados
│   ├── notas.csv                     # Trabajos prácticos entregados/exigidos y nota Parcial 1
│   └── historial.csv                 # Evolución longitudinal de puntajes (Semanas 1 a 3)
│
├── docs/                             # 📄 Documentación técnica y anexos de entregas previas
├── screenshots/                      # 📸 Capturas de evidencia del portal y llamadas a Gemini API
├── tools/                            # 🛠️ Scripts de generación de PDF de defensa y auditoría
│
├── app.py                            # 🚀 Servidor principal HTTP/REST (Puerto 8050)
├── demo_panel.html                   # 🌐 Acceso directo autónomo a la vista principal
├── CONSIGNA_PARCIAL_FIA.md           # 📝 Desarrollo completo de los 7 puntos del parcial de FIA
├── Presentacion_Parcial_FIA_SITA.pdf # 📊 Diapositivas ejecutivas para la defensa oral (5 minutos)
└── README.md                         # 📖 Documentación general e instrucciones de despliegue
```

---

## ⚡ 4. Cómo Levantar Todos los Servicios y Correr el Sistema

El sistema fue diseñado con **arquitectura estándar de Python 3 (cero dependencias externas obligatorias)** para garantizar que funcione de inmediato en cualquier computadora de evaluación.

### Requisitos Previos
* **Python 3.10 o superior** instalado (`python --version`).
* **Navegador web moderno** (Google Chrome, Microsoft Edge, Firefox, Brave o Safari).

---

### Opción A: Iniciar el Sistema Completo con Servidor MVC (Recomendado)

#### Paso 1: Clonar el repositorio y entrar a la carpeta
```bash
git clone https://github.com/aisamajoel-tech/Sistema-Escolar-Fundamentos-.git
cd Sistema-Escolar-Fundamentos-
```

#### Paso 2: (Opcional) Configurar la API Key gratuita de Google AI Studio (Gemini)
Si desea realizar consultas en vivo contra la nube de Google AI Studio (`gemini-1.5-flash`), defina la variable de entorno antes de iniciar (o ingrésela directamente desde el botón **`🔎 Ver JSON API Gemini`** dentro de la interfaz web):
* **En Windows (PowerShell):**
  ```powershell
  $env:GEMINI_API_KEY="AIzaSyTuClaveDeGoogleAIStudio..."
  ```
* **En Linux / macOS:**
  ```bash
  export GEMINI_API_KEY="AIzaSyTuClaveDeGoogleAIStudio..."
  ```
*(Si no se define una clave, el servicio utiliza automáticamente su motor de respaldo validado con respuestas estructuradas para que la demostración nunca se interrumpa).*

#### Paso 3: Iniciar el servidor MVC (`app.py`)
```bash
python app.py
```

Verá en la terminal la confirmación de que todos los servicios están activos:
```text
=================================================================
 🚀 SISTEMA SITA-IA · SERVICIO INICIADO CON PATRÓN MVC
 🌐 Acceso a la Plataforma: http://localhost:8050/views/demo_panel.html
 📂 Arquitectura: Models (models/) | Views (views/) | Controllers (controllers/)
 🔒 Gobernanza Ética: Puntos N1 a N8 y Regla C1 activos
 ⚡ API Google AI Studio: Gemini 1.5 Flash integrada
 Presione Ctrl + C para detener el servidor
=================================================================
```
El navegador se abrirá automáticamente en **`http://localhost:8050/views/demo_panel.html`**.

---

### Opción B: Ejecución Instantánea Sin Servidor (*Modo Autónomo Zero-Config*)
Si desea probar la interfaz inmediatamente sin abrir una terminal:
1. Haga **doble clic sobre `views/demo_panel.html`** (o sobre `demo_panel.html` en la raíz del proyecto).
2. El motor autónomo integrado cargará los 120 estudiantes, los 4 módulos académicos, los cambios de rol y los escenarios de defensa directamente en su navegador.

---

## 🎯 5. Guía Rápida para la Defensa Oral (5 Minutos)

En la barra superior del sistema encontrará la botonera **`Guion Defensa 5 Min`** que guía la exposición paso a paso:

1. **`01 · Semana Normal (Cohorte 120)`**: Muestra el flujo normal $A1 \rightarrow A2 \rightarrow A3$ con 100 % de completitud y 12 casos asignados al tutor (respetando el tope $\le 15$).
2. **`02 · Caso Crítico: Lucas González (82/100)`**: Selecciona el legajo `#24901`, grafica su evolución en 4 semanas (`35 → 52 → 68 → 82`) y detalla sus 3 factores XAI.
3. **`✨ Asistente Gemini 1.5 Flash (Guía N2)`**: Genera la guía de entrevista empática con preguntas abiertas para el tutor y permite inspeccionar el payload JSON enviado a Google AI Studio.
4. **`03 · Falla F1: Corte Campus (Sin Evaluar)`**: Simula la caída de Moodle y demuestra que el sistema suspende el puntaje (`SIN EVALUAR`) sin castigar al alumno.
5. **`04 · Falla F3: Señal Contradictoria (Mateo)`**: Muestra el caso `#24945` (92 % asistencia presencial pero 14 días sin usar el campus), clasificado como `EN REVISIÓN (F3)`.
6. **`05 · Falla F2: Inacción 10d + Sesgo N7`**: Cambia al panel de **Coordinación** para mostrar la reasignación al Tutor B (`N6`) y la auditoría de equidad inter-turno ($\Delta = 3.8\text{ pts} \le 10\text{ pts}$, `N7`).
7. **Selector de Roles (esquina superior derecha)**: Conmute entre **`🎓 Alumno`**, **`📘 Docente (C1)`**, **`🛡️ Tutor SITA`** y **`⚖️ Coordinación`** para demostrar cómo la arquitectura adapta las vistas y permisos en tiempo real.

---

## 👥 6. Autores y Cátedra

* **Joel Aisama** — Modelos de IA, Inferencia Logística XAI y Rol Tutor (`joel.aisama@alu.uch.edu.ar`)
* **Bautista Navarro** — Arquitectura de Gobernanza, Métricas de Equidad y Rol Coordinación (`bautista.navarro@alu.uch.edu.ar`)
* **Asignatura:** Fundamentos de Inteligencia Artificial (3° Año) — Universidad Champagnat
* **Repositorio Oficial:** [https://github.com/aisamajoel-tech/Sistema-Escolar-Fundamentos-](https://github.com/aisamajoel-tech/Sistema-Escolar-Fundamentos-) (Acceso compartido con el usuario docente **`ampalmaj`**)
