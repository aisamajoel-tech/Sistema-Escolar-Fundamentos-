# SITA-IA · Sistema Institucional de Tutorías y Alerta Temprana
> **Plataforma Enterprise de Detección Temprana del Abandono Universitario con Gobernanza Ética e Inteligencia Artificial Híbrida.**

[![GitHub Repository](https://img.shields.io/badge/GitHub-aisamajoel--tech%2FSistema--Escolar--Fundamentos---181717?logo=github)](https://github.com/aisamajoel-tech/Sistema-Escolar-Fundamentos-)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/architecture-MVC%20Enterprise-orange.svg)]()
[![AI Engine](https://img.shields.io/badge/AI-Scoring%20ML%20%2B%20Gemini%201.5%20Flash-green.svg)](https://aistudio.google.com/)
[![Governance](https://img.shields.io/badge/governance-Human--in--the--Loop%20(N1--N8)-purple.svg)]()

---

## 🏛️ 1. Descripción del Sistema

**SITA-IA** es una solución de software orientada a instituciones de educación superior para mitigar la **deserción estudiantil en el primer año universitario**.

A diferencia de los enfoques tradicionales y reactivos, SITA-IA procesa semanalmente rastros digitales heterogéneos (asistencia presencial, notas de cátedra y telemetría de Moodle) para estimar la probabilidad de abandono con **al menos 4 semanas de anticipación**, permitiendo intervenciones personalizadas antes del cierre del primer cuatrimestre.

### 🌟 Pilares Tecnológicos y Éticos
* **Arquitectura de IA Híbrida:** Clasificación supervisada probabilística ($ML$) combinada con un Asistente Pedagógico Generativo impulsado por la API de **Google AI Studio (Gemini 1.5 Flash)**.
* **Gobernanza Ética (*Human-in-the-Loop*):** Implementación estricta de las salvaguardas **N1 a N8**. La IA **nunca** envía correos directos al estudiante, no sanciona, no da de baja ni publica calificaciones.
* **Aislamiento Anti-Sesgo Docente (Regla C1):** Los profesores de cátedra cargan datos pero tienen **los puntajes de riesgo estrictamente bloqueados con candado** para evitar sesgos de expectativa en sus exámenes.
* **Tolerancia a Fallas Institucionales (F1, F2, F3):** Protocolos que impiden calificar con datos rotos (F1), gestionan la inacción del tutor escalando a Coordinación (F2 / N6) y aíslan señales contradictorias en estado de revisión (F3).

---

## 📂 2. Estructura del Proyecto (Patrón MVC)

El repositorio está organizado bajo el patrón arquitectónico **Modelo-Vista-Controlador (MVC)**:

```
Sistema-Escolar-Fundamentos-/
│
├── models/                           # 🧠 [MODEL]: Lógica de negocio, inferencia y agentes de IA
│   ├── agente1_monitoreo.py          # Ingesta, validación y detección de cortes de sensor (F1)
│   ├── agente2_riesgo.py             # Modelo probabilístico multivariable (0-100) + Explicabilidad XAI
│   ├── agente3_alertas.py            # Priorización con tope (<=15), balanceo de tutores y regla F3
│   ├── gemini_service.py             # Integración con Google AI Studio (Gemini 1.5 Flash API)
│   └── generator.py                  # Generador determinista de la cohorte sintética (120 alumnos)
│
├── views/                            # 🖥️ [VIEW]: Interfaz de usuario y presentación gráfica
│   ├── demo_panel.html               # Panel Web Institucional multirrol (Tutor, Coordinación, Docente)
│   └── logo_uch.png                  # Identidad visual institucional (Universidad Champagnat)
│
├── controllers/                      # ⚙️ [CONTROLLER]: Orquestación, flujo y API REST
│   ├── api_controller.py             # Controlador REST: gestiona mutaciones, gobernanza N1-N8 y Gemini
│   └── pipeline_controller.py        # Orquestador del ciclo semanal y matriz Prometheus (Msj 0 al 12)
│
├── data/                             # 📊 Fuentes de datos semanales simuladas (CSVs)
│   ├── asistencia.csv                # Asistencias y ausencias recientes por turno/comisión
│   ├── campus.csv                    # Logs de plataforma Moodle (inactividad, descargas, sesiones)
│   └── notas.csv                     # Calificaciones de parciales y entregas de TPs
│
├── docs/                             # 📄 Documentación académica y actas de auditoría
├── screenshots/                      # 📸 Evidencias visuales de la API de Gemini y métricas de sesgo
├── tools/                            # 🛠️ Utilidades auxiliares y generadores de reportes
│
├── CONSIGNA_PARCIAL_FIA.md           # 📝 Resolución exhaustiva de los 7 puntos de la consigna de FIA
├── Presentacion_Parcial_FIA_SITA.pdf # 📊 Presentación ejecutiva en 9 diapositivas para la defensa oral
├── README.md                         # 🌟 Manual técnico y guía de despliegue del sistema
└── app.py                            # 🚀 Punto de entrada principal y servidor HTTP
```

---

## ⚡ 3. Guía de Inicio Rápido (Cómo Levantar los Servicios)

El sistema está desarrollado con **cero dependencias externas complejas** (utiliza librerías estándar nativas de Python).

### Requisitos Previos
* Python 3.10 o superior instalado.
* Cualquier navegador moderno (Chrome, Edge, Firefox, Brave, Safari).
* Git instalado en la máquina.

---

### 🚀 Paso a Paso para Correr el Sistema

#### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/aisamajoel-tech/Sistema-Escolar-Fundamentos-.git
cd Sistema-Escolar-Fundamentos-
```

#### Paso 2: (Opcional) Configurar API Key de Gemini
El sistema incluye integración nativa con **Google AI Studio (Gemini 1.5 Flash)**.
* Si dispone de una API Key gratuita de Google AI Studio, configúrela en su terminal:
  * **En Windows (PowerShell):**
    ```powershell
    $env:GEMINI_API_KEY="AIzaSyTuClaveDeGoogleAIStudio..."
    ```
  * **En Linux / macOS:**
    ```bash
    export GEMINI_API_KEY="AIzaSyTuClaveDeGoogleAIStudio..."
    ```
*(Nota: Si no configura ninguna clave, el sistema conmuta automáticamente a modo de prueba con caché validada, garantizando que la demo nunca falle durante la evaluación).*

#### Paso 3: Levantar el Servidor
Ejecute el punto de entrada de la aplicación:
```bash
python app.py
```

Verá en consola la inicialización de los servicios:
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

El navegador se abrirá automáticamente en:  
👉 **`http://localhost:8050/views/demo_panel.html`**

---

### 🌐 Opción Alternativa: Modo Autónomo (*Zero-Config*)
Si se encuentra en un entorno sin permisos para abrir puertos locales o sin terminal:
1. Abra la carpeta `views/`.
2. Haga **doble clic en `demo_panel.html`**.
3. La plataforma se ejecutará al 100% de manera estática y autónoma en su navegador.

---

## 🎯 4. Guía de Navegación de la Demo (Para la Defensa Oral de 5 Minutos)

El panel incorpora en la barra superior los botones de control para recorrer la defensa en vivo:

1. **`01 Carga Semanal`**: Inicia el pipeline multiagente ($A1 \rightarrow A2 \rightarrow A3$). Carga los 120 perfiles consolidados semanales.
2. **`02 Caso Lucas (82)`**: Abre el expediente del estudiante crítico Lucas González (#24901). Muestra el **índice de 82/100**, su trayectoria en 4 semanas y los **3 factores explicativos (XAI)**.
3. **`✨ Asistente Gemini AI (Guía N2)`**: Invoca la API de **Google AI Studio (Gemini 1.5 Flash)** para redactar en tiempo real una **guía pedagógica empática** con 3 preguntas abiertas para la entrevista del tutor, evitando estigmatizaciones.
4. **`03 Falla F1: Campus`**: Simula la caída del campus virtual. Demuestra el principio $O8$: *la falta de datos no se interpreta como abandono*; los casos pasan preventivamente a *«Sin Evaluar»*.
5. **`04 Falla F3: Discordancia`**: Caso Mateo Fernández (92% asistencia presencial pero campus inactivo). Demuestra que la IA **no promedia señales contradictorias**: aplica *«F3 Lock»* y delega en el tutor.
6. **`Sesgo Inter-Turno (N7)`**: Abre la ventana de auditoría de equidad algorítmica: diferencia de recall de **3.8 puntos** ($\le 10\text{ pts}$ exigidos por Coordinación).
7. **`Selector de Roles (Arriba a la derecha)`**:
   * **Tutor (Joel Aisama):** Intervención humana directa ($N1$, $N2$).
   * **Coordinación (Bautista Navarro):** Aprobación de medidas ($N3$), reasignación ($N6$) y recalibración ($N7$).
   * **Docente de Cátedra (Regla C1):** Carga datos pero **tiene los puntajes bloqueados con candado** para no sesgar sus calificaciones.

---

## 👥 5. Equipo y Créditos Institucionales

* **Joel Aisama:** Modelos de IA, Inferencia Logística y Rol Tutor (`joel.aisama@alu.uch.edu.ar`).
* **Bautista Navarro:** Auditoría de Arquitectura, Métricas y Rol Coordinación (`bautista.navarro@alu.uch.edu.ar`).
* **Institución:** Universidad Champagnat — Facultad de Informática.
* **Docente Receptor del Proyecto:** **`ampalmaj`** (Acceso de colaborador otorgado).
