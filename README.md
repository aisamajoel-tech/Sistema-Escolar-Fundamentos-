# SITA-IA · Sistema Institucional de Tutorías y Alerta Temprana
> **Plataforma Integral de Detección Temprana del Abandono Universitario con Gobernanza Ética e Inteligencia Artificial Híbrida.**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/architecture-MVC%20Enterprise-orange.svg)]()
[![AI Engine](https://img.shields.io/badge/AI-Scoring%20ML%20%2B%20Gemini%201.5%20Flash-green.svg)](https://aistudio.google.com/)
[![License](https://img.shields.io/badge/governance-Human--in--the--Loop%20(N1--N8)-purple.svg)]()

---

## 🏛️ 1. Descripción del Producto

**SITA-IA** es una solución enterprise diseñada para instituciones de educación superior que resuelve el problema de la **deserción estudiantil en el primer año universitario**. 

A diferencia de los enfoques reactivos tradicionales —donde la facultad advierte la deserción cuando el estudiante ya dejó de asistir—, SITA-IA cruza semanalmente señales heterogéneas (asistencia presencial, libretas de calificaciones y telemetría de campus virtual Moodle) para estimar la probabilidad de abandono con **al menos 4 semanas de anticipación**, permitiendo intervenciones personalizadas antes del cierre del primer cuatrimestre.

### 🌟 Diferenciadores Clave
* **Arquitectura Híbrida de IA:** Combina inferencia probabilística calibrada (Machine Learning supervisado) con explicabilidad matemática ($XAI$) y un Asistente Pedagógico Generativo impulsado por **Google AI Studio (Gemini 1.5 Flash)**.
* **Gobernanza Ética y Salvaguarda Humana (*Human-in-the-Loop*):** Cumplimiento estricto de los **Puntos No Delegables N1 a N8**. La IA nunca contacta al alumno, no sanciona, no da de baja ni publica calificaciones.
* **Protección Anti-Sesgo Docente (Regla C1):** Los profesores de cátedra cargan notas y asistencias, pero tienen **estrictamente ocultos y bloqueados los índices de riesgo** para evitar sesgos de expectativa al momento de corregir exámenes.
* **Tolerancia y Resiliencia a Fallas (F1, F2, F3):** Protocolos automáticos que impiden calificar con datos rotos (F1), gestionan la inacción humana (F2) y aíslan señales contradictorias sin promediar (F3).

---

## 📂 2. Arquitectura de Software: Patrón MVC

El sistema está estructurado bajo el patrón **Modelo-Vista-Controlador (MVC)**, garantizando desacoplamiento, alta cohesión y código listo para producción:

```
TRABAJO GRUPAL/
├── models/                           # [M] MODELOS: Lógica de negocio y agentes de IA
│   ├── agente1_monitoreo.py          # Ingesta, validación y detección de fallas de fuentes (Regla F1)
│   ├── agente2_riesgo.py             # Modelo logístico multivariable (0-100) + Explicabilidad XAI
│   ├── agente3_alertas.py            # Priorización con tope (<=15), balanceo de tutores y regla F3
│   ├── gemini_service.py             # Integración con Google AI Studio (Gemini 1.5 Flash API)
│   └── generator.py                  # Generador determinista de cohorte sintética de evaluación
│
├── views/                            # [V] VISTAS: Interfaz de usuario y presentación gráfica
│   ├── demo_panel.html               # Panel Web Institucional (Modo Multirrol con telemetría en vivo)
│   └── logo_uch.png                  # Identidad institucional (Universidad Champagnat)
│
├── controllers/                      # [C] CONTROLADORES: Orquestación, reglas y API
│   ├── api_controller.py             # Controlador REST: gestiona mutaciones, gobernanza N1-N8 y Gemini
│   └── pipeline_controller.py        # Orquestador del ciclo semanal y matriz de mensajes Prometheus
│
├── data/                             # Repositorio de datos crudos (Ingesta semanal)
│   ├── asistencia.csv                # Asistencias y faltas recientes por comisión y turno
│   ├── campus.csv                    # Telemetría de Moodle (días inactivo, sesiones, descargas)
│   └── notas.csv                     # Calificaciones de parciales y trabajos prácticos
│
├── docs/                             # Documentación técnica, académica y legal del proyecto
│   ├── Entrega2_PEAS_Arquitectura.pdf
│   ├── Entrega3_Roles_Secuencia.pdf
│   ├── Entrega4_Coherencia_PlanDemo.pdf
│   └── Guia_Defensa_Entrega4.pdf
│
├── screenshots/                      # Evidencias visuales de auditoría y ejecución de la API
│   ├── sc1_normal.png
│   ├── sc5_sesgo_n7.png
│   └── sc8_gemini_api.png            # Captura de inferencia con Gemini 1.5 Flash
│
├── tools/                            # Scripts de utilidad para auditoría y generación de reportes
├── CONSIGNA_PARCIAL_FIA.md           # Resolución integral de los 7 puntos del examen parcial
├── Presentacion_Parcial_FIA_SITA.pdf # Presentación ejecutiva en 9 diapositivas para defensa oral
├── README.md                         # Guía comercial y manual de operaciones del sistema
└── app.py                            # Punto de entrada y servidor HTTP institucional
```

---

## 🚀 3. Guía de Instalación y Puesta en Marcha

El sistema fue diseñado con **cero fricción operativa**: utiliza exclusivamente librerías nativas de la biblioteca estándar de Python (no requiere `pip install` de frameworks pesados para su ejecución local).

### Requisitos Previos
* Python 3.10 o superior instalado en el sistema.
* Un navegador web moderno (Google Chrome, Microsoft Edge, Mozilla Firefox o Safari).

---

### Opción A: Despliegue con Servidor Local (Recomendado)

1. **Abrir la terminal** en el directorio raíz del proyecto:
   ```bash
   cd "TRABAJO GRUPAL"
   ```

2. **(Opcional) Configurar API Key de Google AI Studio:**  
   Para habilitar llamadas en vivo a la nube con Gemini 1.5 Flash, configure su variable de entorno:
   * En Windows (PowerShell):
     ```powershell
     $env:GEMINI_API_KEY="AIzaSyYourApiKeyHere..."
     ```
   * En Linux / macOS:
     ```bash
     export GEMINI_API_KEY="AIzaSyYourApiKeyHere..."
     ```
   *(Nota: Si no dispone de clave en el momento, el sistema cuenta con un motor de prueba validado que replica fielmente el esquema JSON de Google AI Studio).*

3. **Iniciar el servidor institucional:**
   ```bash
   python app.py
   ```

4. **Acceso a la plataforma:**  
   El sistema levantará el servicio en el puerto `8050` y abrirá automáticamente su navegador en:
   👉 **`http://localhost:8050/views/demo_panel.html`**

---

### Opción B: Modo Autónomo Inmediato (*Zero-Config*)

Si se encuentra en una sala de conferencias sin acceso a consola o sin permisos de ejecución:
1. Navegue hasta la carpeta `views/`.
2. Haga **doble clic en `demo_panel.html`**.
3. La interfaz iniciará de forma 100% interactiva y funcional directamente en su navegador web.

---

## 🎮 4. Guía de Demostración para Presentación Ejecutiva (5 Minutos)

El panel incorpora una **Barra de Navegación de Escenarios** en la parte superior para recorrer el flujo en vivo sin contratiempos:

| Escenario | Acción en Pantalla | Qué demuestra arquitectónicamente |
| :---: | :--- | :--- |
| **`01 Carga Semanal`** | Clic en botón `01` | Ingesta de 3 CSVs por el Agente A1 y procesamiento secuencial hacia A2 y A3. Carga 120 perfiles consolidados. |
| **`02 Caso Lucas (82)`** | Clic en botón `02` | Muestra al estudiante crítico Lucas González (#24901). Expone el **score de 82**, la evolución en 4 semanas y el desglose de los **3 factores determinantes (XAI)**. |
| **`✨ Asistente Gemini AI`** | Clic en el botón verde de Gemini | Invoca la API de **Google AI Studio (Gemini 1.5 Flash)** para redactar en tiempo real una **guía de entrevista empática** con 3 preguntas abiertas para el tutor (Punto N2). |
| **`03 Falla F1: Campus`** | Clic en botón `03` | Simula la caída de Moodle por 48 h. Demuestra que **falta de dato $\neq$ inactividad**: los casos pasan preventivamente a *«Sin Evaluar»* para evitar pánico o falsas alarmas. |
| **`04 Falla F3: Discordancia`** | Clic en botón `04` | Caso Mateo Fernández (92% asistencia presencial pero campus inactivo). Demuestra que la IA **no promedia señales contradictorias**: aplica *«F3 Lock»* y delega en el tutor. |
| **`Sesgo Inter-Turno (N7)`** | Botón en barra superior | Despliega la auditoría de equidad: diferencia de recall entre turnos de **3.8 puntos**, cumpliendo el estándar ético institucional ($\le 10\text{ pts}$). |
| **`Selector de Roles`** | Botones de Rol (Arriba a la derecha) | Permite alternar entre **Tutor (Joel Aisama)**, **Coordinación (Bautista Navarro)** para aprobar derivaciones institucionales (N3), y **Docente de Cátedra (Regla C1)** con los puntajes bloqueados con candado. |

---

## 🛡️ 5. Cumplimiento de Gobernanza Ética (Puntos No Delegables N1 a N8)

SITA-IA fue concebido bajo el principio de **Inteligencia Artificial Débil y de Acompañamiento**:
* **N1:** El tutor humano acepta o desestima cada alerta antes de cualquier acción.
* **N2:** Todo contacto hacia el estudiante es realizado personalmente por un tutor (la IA jamás redacta ni envía correos directos al alumno).
* **N3:** Las medidas académicas de fondo (cambios de turno, becas) son propuestas por el tutor y formalmente aprobadas por Coordinación.
* **N4:** La etiqueta de riesgo nunca es definitiva ni persistente; se recalcula cada 7 días.
* **N5:** La gestión de incidentes tecnológicos corresponde a Coordinación y Sistemas.
* **N6:** Ante inacción prolongada del tutor (10 días), Coordinación reasigna el caso a otro profesional (la IA nunca cubre al tutor ausente).
* **N7:** Las recalibraciones semestrales del modelo requieren aprobación expresa de Coordinación tras auditar métricas de sesgo.
* **N8:** Solo se procesan registros de estudiantes con consentimiento informado registrado.

---

## 👥 6. Equipo Desarrollador y Contacto Institucional

* **Joel Aisama:** Desarrollador de Modelos y Tutor Académico del Sistema (`joel.aisama@alu.uch.edu.ar`).
* **Bautista Navarro:** Auditor de Arquitectura y Coordinador del Sistema (`bautista.navarro@alu.uch.edu.ar`).
* **Institución:** Universidad Champagnat — Facultad de Informática.
* **Repositorio Evaluador:** Acceso concedido al usuario docente: **`ampalmaj`**.
