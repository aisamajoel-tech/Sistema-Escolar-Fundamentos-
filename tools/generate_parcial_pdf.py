import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdf_path = r'C:\Users\aisam\OneDrive\Escritorio\3AÑO-FACULTAD\FUNDAMENTOS DE IA\TRABAJO GRUPAL\Presentacion_Parcial_FIA_SITA.pdf'
shots_dir = r'C:\Users\aisam\OneDrive\Escritorio\3AÑO-FACULTAD\FUNDAMENTOS DE IA\TRABAJO GRUPAL\screenshots'

PAGE_W, PAGE_H = landscape(letter)
doc = SimpleDocTemplate(pdf_path, pagesize=(PAGE_W, PAGE_H), leftMargin=34, rightMargin=34, topMargin=24, bottomMargin=24)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CoverTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=24,
    leading=29,
    textColor=colors.HexColor('#0f172a'),
    spaceAfter=6
)
subtitle_style = ParagraphStyle(
    'CoverSub',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=12.5,
    leading=16.5,
    textColor=colors.HexColor('#475569'),
    spaceAfter=14
)
slide_title = ParagraphStyle(
    'SlideTitle',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=17,
    leading=21,
    textColor=colors.HexColor('#1e3a8a'),
    spaceAfter=3
)
slide_sub = ParagraphStyle(
    'SlideSub',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=9.5,
    leading=13,
    textColor=colors.HexColor('#64748b'),
    spaceAfter=8
)
body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=13,
    textColor=colors.HexColor('#1e293b')
)
body_bold = ParagraphStyle(
    'BodyBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9,
    leading=13,
    textColor=colors.HexColor('#0f172a')
)

story = []

def make_slide(title_text, subtitle_text, bullet_paras, img_name, key_takeaway):
    elems = []
    elems.append(Paragraph(title_text, slide_title))
    elems.append(Paragraph(subtitle_text, slide_sub))
    
    img_path = os.path.join(shots_dir, img_name)
    if os.path.exists(img_path):
        img_elem = Image(img_path, width=420, height=270)
    else:
        img_elem = Paragraph('Captura de pantalla', body_style)

    text_content = []
    for bp in bullet_paras:
        text_content.append(bp)
        text_content.append(Spacer(1, 4.5))

    takeaway_table = Table(
        [[Paragraph(f'<b>Criterio Tecnico / Evaluacion FIA:</b> {key_takeaway}', body_style)]],
        colWidths=[290]
    )
    takeaway_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#eff6ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#93c5fd')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    text_content.append(Spacer(1, 5))
    text_content.append(takeaway_table)

    main_table = Table(
        [[text_content, img_elem]],
        colWidths=[295, 425]
    )
    main_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    elems.append(main_table)
    return elems

# -------------------------------------------------------------
# SLIDE 1: PORTADA OFICIAL
# -------------------------------------------------------------
story.append(Spacer(1, 30))
badge_table = Table([[Paragraph('<b>EVALUACION PARCIAL · FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL (3° ANO)</b>', ParagraphStyle('B', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor('#1e40af')))]], colWidths=[540])
badge_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#dbeafe')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#93c5fd')),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(badge_table)
story.append(Spacer(1, 10))
story.append(Paragraph('SITA-IA: Deteccion Temprana del Abandono Universitario', title_style))
story.append(Paragraph('Solucion Basada en IA: Clasificacion Supervisada (ML) + LLM (Google AI Studio Gemini API)', subtitle_style))
story.append(Spacer(1, 14))

meta_data = [
    [Paragraph('<b>Institucion:</b>', body_bold), Paragraph('Universidad Champagnat — Facultad de Informatica', body_style)],
    [Paragraph('<b>Alumnos:</b>', body_bold), Paragraph('Joel Aisama (Tutor del Sistema) · Bautista Navarro (Coordinador y Auditor)', body_style)],
    [Paragraph('<b>Docente Evaluador:</b>', body_bold), Paragraph('Prof. ampalmaj (Repositorio GitHub Privado)', body_style)],
    [Paragraph('<b>Objetivo y Meta:</b>', body_bold), Paragraph('Deteccion preventiva en semanas 1 a 6 con anticipacion >= 4 sem para reducir el 15% del abandono.', body_style)],
]
meta_table = Table(meta_data, colWidths=[140, 480])
meta_table.setStyle(TableStyle([
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
]))
story.append(meta_table)
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 2: PUNTO 1 Y 2 - PROBLEMA LOCAL, USUARIOS Y ALCANCE
# -------------------------------------------------------------
b_s2 = [
    Paragraph('<b>1. Problema Local:</b> En Argentina, casi 70 de cada 100 ingresantes abandonan, concentrandose en 1.° ano. El aviso manual llega tarde: cuando el docente nota que no viene, ya deserto.', body_style),
    Paragraph('<b>2. Usuarios:</b> Tutores (acompanamiento N2) y Coordinacion (medidas N3/N6). Docente de catedra como aportante ciego (Regla C1). Alumno como sujeto con derecho a consentir (N8).', body_style),
    Paragraph('<b>3. Alcance (Que hace y que NO hace):</b><br/>• <b>SI hace:</b> Cruza asistencia, notas y campus; calcula riesgo (0-100); prioriza (tope 15); redacta guia de charla.<br/>• <b>NO hace:</b> NUNCA contacta alumnos de forma autonoma, no sanciona, no da de baja ni publica notas.', body_style)
]
story.extend(make_slide(
    '1. Problema Local, Usuarios y Alcance (Ptos 1 y 2)',
    'Deteccion proactiva semanal y limites estrictos de intervencion',
    b_s2,
    'sc1_normal.png',
    'La solucion alerta y prioriza, pero la decision de intervenir o cerrar un caso es 100% potestad del tutor humano.'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 3: PUNTO 3 - CAPACIDADES DE IA Y SUBCAMPOS
# -------------------------------------------------------------
b_s3 = [
    Paragraph('<b>Subcampo 1 · Machine Learning (Supervisado / Conexionista):</b><br/>• <i>Capacidad:</i> Clasificacion y estimacion de propension probabilistica de desercion (score 0-100).<br/>• <i>Implementacion:</i> Regresion logistica multivariable calibrada con sigmoide.<br/>• <i>Explicabilidad (XAI):</i> Descomposicion de logit para extraer los 3 factores de mayor peso.', body_style),
    Paragraph('<b>Subcampo 2 · Procesamiento de Lenguaje Natural (NLP / Generative AI):</b><br/>• <i>Capacidad:</i> Modelos de Lenguaje (LLMs) para redaccion contextual.<br/>• <i>Implementacion:</i> API de Google AI Studio (Gemini 1.5 Flash). Produce la guia de preguntas empaticas para el tutor.', body_style)
]
story.extend(make_slide(
    '2. Capacidades de IA y Subcampos (Punto 3)',
    'Hibridacion: Clasificacion Predictiva (A2) + Lenguaje Natural Generativo (Gemini API)',
    b_s3,
    'sc1_normal.png',
    'Se combinan modelos cuantitativos de scoring con modelos generativos para humanizar el acompanamiento.'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 4: PUNTO 4 - FLUJO TECNICO (ENTRADAS -> API -> SALIDAS)
# -------------------------------------------------------------
b_s4 = [
    Paragraph('<b>1. Entradas (CSVs semanales):</b> Asistencia presencial, notas de parciales/TPs y logs de Moodle (dias inactivo, descargas).', body_style),
    Paragraph('<b>2. Procesamiento Multiagente:</b><br/>• <i>A1 Monitoreo:</i> Cruza fuentes en <= 24 h. Si campus se corta, activa Falla F1 (Sin Evaluar).<br/>• <i>A2 Riesgo:</i> Evalua score 0-100 y 3 factores.<br/>• <i>A3 Alertas:</i> Prioriza con tope <= 15 casos.', body_style),
    Paragraph('<b>3. API Google AI Studio (Gemini 1.5 Flash):</b> Prompt estructurado sin PII con variables academicas -> Generacion de guia.', body_style),
    Paragraph('<b>4. Salidas:</b> Bandeja priorizada del tutor y protocolo de accion N1-N4.', body_style)
]
story.extend(make_slide(
    '3. Flujo Tecnico de la Solucion (Punto 4)',
    'Entradas heterogeneas -> Procesamiento en cadena (A1-A3 + Gemini API) -> Salidas humanas',
    b_s4,
    'sc1_normal.png',
    'Flujo desacoplado y trazable bajo el estandar de mensajeria Prometheus (Mensajes 0 a 12).'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 5: PROTOTIPO CON GEMINI API (GOOGLE AI STUDIO)
# -------------------------------------------------------------
b_s5 = [
    Paragraph('<b>Integracion Real con Google AI Studio:</b><br/>• <i>Endpoint:</i> v1beta/models/gemini-1.5-flash:generateContent.<br/>• <i>Costo:</i> $0 USD (Free Tier: 15 RPM / 1500 RPD).', body_style),
    Paragraph('<b>Demostracion en Vivo (Lucas Gonzalez #24901):</b><br/>• El modelo A2 detecta score 82 (asistencia 40%, 2 TPs debidos, 12d sin campus).<br/>• El tutor presiona <b>«Asistente Gemini AI»</b>.<br/>• Gemini analiza las causas y redacta preguntas empaticas: <i>«¿Como venis con los horarios de cursada?»</i>, descartando sesgo punitivo.', body_style),
    Paragraph('<b>Proteccion de Privacidad:</b> Solo se transmiten variables academicas desidentificadas.', body_style)
]
story.extend(make_slide(
    '4. Prototipo con API Real de Gemini (Evidencia)',
    'Asistente de dialogo socratico generado por Gemini 1.5 Flash en tiempo real',
    b_s5,
    'sc8_gemini_api.png',
    'La IA generativa asiste al profesional con preguntas pedagogicas abiertas, evitando que el alumno se sienta juzgado.'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 6: PUNTO 5 - REQUISITOS, COSTOS Y SEGURIDAD
# -------------------------------------------------------------
b_s6 = [
    Paragraph('<b>Datos Necesarios:</b> Padrón de inscriptos, asistencia docente y actividad en campus virtual. Sin necesidad de datos biometricos ni socioeconomicos invasivos.', body_style),
    Paragraph('<b>Costos de la Solucion:</b><br/>• <i>Modelo Predictivo (A2):</i> Python estandar local ($0).<br/>• <i>API de Lenguaje:</i> Google AI Studio Free Tier ($0). Capacidad gratuita de sobra para 15 casos/tutor/semana.', body_style),
    Paragraph('<b>Seguridad y Privacidad:</b><br/>• <b>Habilitacion N8:</b> Coordinacion verifica consentimiento firmado.<br/>• <b>Transmision Cifrada:</b> HTTPS hacia la API de Google.<br/>• <b>No persistencia de PII:</b> La API de Gemini no almacena datos de alumnos.', body_style)
]
story.extend(make_slide(
    '5. Requisitos Minimos, Costos y Seguridad (Pto 5)',
    'Viabilidad economica costo cero ($0 USD) y privacidad por diseno (N8)',
    b_s6,
    'sc7_coordinacion.png',
    'Solucion accesible para cualquier universidad publica o privada sin costo de licencias.'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 7: PUNTO 6 - ANALISIS ETICO (5 RIESGOS Y MITIGACIONES)
# -------------------------------------------------------------
b_s7 = [
    Paragraph('<b>1. Sesgo Algoritmico:</b> Error mayor en turno noche -> <i>Mitigacion:</i> Auditoria semestral N7 (delta recall inter-turno <= 10 pts).', body_style),
    Paragraph('<b>2. Privacidad:</b> Sensacion de vigilancia -> <i>Mitigacion:</i> Consentimiento informado N8 y derecho a pedir auditoria de variables.', body_style),
    Paragraph('<b>3. Uso Indebido / Estigmatizacion:</b> Docente calificando peor -> <i>Mitigacion:</i> <b>Regla C1</b> (scores bloqueados con candado al docente).', body_style),
    Paragraph('<b>4. Dependencia / Falla de Sensor:</b> Moodle caido -> <i>Mitigacion:</i> <b>Regla F1</b> (falta de dato != inactividad, pasa a "Sin Evaluar").', body_style),
    Paragraph('<b>5. Deshumanizacion:</b> Mails automaticos frios -> <i>Mitigacion:</i> <b>Compuerta N1-N4</b> (contacto 100% humano del tutor).', body_style)
]
story.extend(make_slide(
    '6. Analisis Etico Obligatorio (Punto 6)',
    'Identificacion de 5 riesgos cardinales y sus salvaguardas tecnicas de diseno',
    b_s7,
    'sc5_sesgo_n7.png',
    'El sistema fue auditado integralmente: la etica y los derechos estudiantiles estan integrados en el codigo.'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 8: TOLERANCIA A FALLAS F1, F2 Y F3
# -------------------------------------------------------------
b_s8 = [
    Paragraph('<b>Falla F1 (Sensor Campus Caido):</b> No se inventa riesgo con datos rotos. Se congela el scoring preventivamente y Coordinacion gestiona la reconexion (N5).', body_style),
    Paragraph('<b>Falla F2 (Inaccion del Tutor):</b> A los 7 dias se emite recordatorio. A los 10 dias A3 escala a Coordinacion, quien reasigna al Tutor B (N6). La IA nunca cubre al tutor ausente.', body_style),
    Paragraph('<b>Falla F3 (Senales Opuestas):</b> Alumno con 92% presencial y campus inactivo. A3 no promedia: clasifica como «En Revision» (F3 Lock) para que el tutor desempate. Si es error, se computa como Falso Positivo (Precision >= 50%).', body_style)
]
story.extend(make_slide(
    '7. Tolerancia a Fallas Institucionales (F1, F2 y F3)',
    'Resiliencia operativa: contingencias ante caidas tecnicas, desidia o datos discordantes',
    b_s8,
    'sc3_f1_corte.png',
    'El sistema no falla ante imprevistos: tiene caminos formales de contingencia predefinidos.'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 9: PUNTO 7 - DEFENSA ORAL Y RECOMENDACIÓN FINAL
# -------------------------------------------------------------
story.append(Paragraph('8. Defensa Oral de 5 Minutos y Recomendacion (Pto 7)', slide_title))
story.append(Paragraph('Estructura de exposicion cronometrada para Joel Aisama y Bautista Navarro', slide_sub))
story.append(Spacer(1, 8))

summary_cards = [
    [
        Paragraph('<b>0:00 - 0:45 | El Problema (Joel):</b><br/>Desercion critica en 1.° ano. El aviso manual llega tarde. "El problema no es que nadie quiera ayudar, es que nadie se entera a tiempo".', body_style),
        Paragraph('<b>0:45 - 1:45 | Arquitectura (Joel):</b><br/>Tres agentes en cadena (A1 Ingesta, A2 Scoring logistico 0-100, A3 Priorizacion tope 15). IA debil: alerta y prioriza, no decide.', body_style)
    ],
    [
        Paragraph('<b>1:45 - 3:30 | Demo en Vivo + Gemini API (Bauti & Joel):</b><br/>Caso Lucas (82 pts, 3 factores). API Gemini genera guia empatica N2. Falla F1 (corte campus = Sin Evaluar).', body_style),
        Paragraph('<b>3:30 - 4:15 | Compuerta Humana N1-N8 (Joel):</b><br/>La IA se detiene en la bandeja. Docente ciego al score (C1). Medidas institucionales aprobadas por Coordinacion (N3/N6).', body_style)
    ]
]
sum_table = Table(summary_cards, colWidths=[355, 355])
sum_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING', (0,0), (-1,-1), 12),
    ('RIGHTPADDING', (0,0), (-1,-1), 12),
]))
story.append(sum_table)

story.append(Spacer(1, 12))
final_banner = Table([[
    Paragraph('<b>4:15 - 5:00 | Cierre y Recomendacion Final del Equipo (Bautista):</b><br/><i>«Nuestra recomendacion concluyente es que la Inteligencia Artificial debe implementarse en la educacion publica como un radar preventivo que detecta senales a tiempo para potenciar el vinculo y el acompanamiento humano, pero NUNCA como un tribunal automatizado que decida, etiquete o juzgue la trayectoria de un estudiante.»</i>', ParagraphStyle('FB', fontName='Helvetica', fontSize=9.5, leading=14, textColor=colors.HexColor('#1e3a8a')))
]], colWidths=[710])
final_banner.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#eff6ff')),
    ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#3b82f6')),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('LEFTPADDING', (0,0), (-1,-1), 14),
    ('RIGHTPADDING', (0,0), (-1,-1), 14),
]))
story.append(final_banner)

doc.build(story)
print('Presentacion_Parcial_FIA_SITA.pdf generada exitosamente con 9 diapositivas.')
