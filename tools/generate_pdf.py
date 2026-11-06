import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdf_path = r'C:\Users\aisam\OneDrive\Escritorio\3AÑO-FACULTAD\FUNDAMENTOS DE IA\TRABAJO GRUPAL\Presentacion_Parcial_SITA_IA.pdf'
shots_dir = r'C:\Users\aisam\OneDrive\Escritorio\3AÑO-FACULTAD\FUNDAMENTOS DE IA\TRABAJO GRUPAL\screenshots'

PAGE_W, PAGE_H = landscape(letter)
doc = SimpleDocTemplate(pdf_path, pagesize=(PAGE_W, PAGE_H), leftMargin=36, rightMargin=36, topMargin=26, bottomMargin=26)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CoverTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=25,
    leading=30,
    textColor=colors.HexColor('#0f172a'),
    spaceAfter=6
)
subtitle_style = ParagraphStyle(
    'CoverSub',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=13,
    leading=17,
    textColor=colors.HexColor('#475569'),
    spaceAfter=14
)
slide_title = ParagraphStyle(
    'SlideTitle',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=colors.HexColor('#1e3a8a'),
    spaceAfter=3
)
slide_sub = ParagraphStyle(
    'SlideSub',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=10,
    leading=13,
    textColor=colors.HexColor('#64748b'),
    spaceAfter=8
)
body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=13.5,
    textColor=colors.HexColor('#1e293b')
)
body_bold = ParagraphStyle(
    'BodyBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9.5,
    leading=13.5,
    textColor=colors.HexColor('#0f172a')
)

story = []

def make_slide(title_text, subtitle_text, bullet_paras, img_name, key_takeaway):
    elems = []
    elems.append(Paragraph(title_text, slide_title))
    elems.append(Paragraph(subtitle_text, slide_sub))
    
    img_path = os.path.join(shots_dir, img_name)
    if os.path.exists(img_path):
        img_elem = Image(img_path, width=415, height=265)
    else:
        img_elem = Paragraph('Captura de pantalla', body_style)

    text_content = []
    for bp in bullet_paras:
        text_content.append(bp)
        text_content.append(Spacer(1, 5))

    takeaway_table = Table(
        [[Paragraph(f'<b>Impacto Academico / Criterio:</b> {key_takeaway}', body_style)]],
        colWidths=[290]
    )
    takeaway_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#eff6ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#93c5fd')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    text_content.append(Spacer(1, 6))
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
# SLIDE 1: PORTADA EJECUTIVA
# -------------------------------------------------------------
story.append(Spacer(1, 35))
badge_table = Table([[Paragraph('<b>PROYECTO DE INNOVACION · FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL (3° ANO)</b>', ParagraphStyle('B', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#1e40af')))]], colWidths=[530])
badge_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#dbeafe')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#93c5fd')),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(badge_table)
story.append(Spacer(1, 12))
story.append(Paragraph('SITA-IA: Deteccion Temprana del Abandono Universitario', title_style))
story.append(Paragraph('Arquitectura Multiagente Cooperativa, Gobernanza Etica y Salvaguarda Humana', subtitle_style))
story.append(Spacer(1, 16))

meta_data = [
    [Paragraph('<b>Institucion:</b>', body_bold), Paragraph('Universidad Champagnat — Facultad de Informatica', body_style)],
    [Paragraph('<b>Equipo Desarrollador:</b>', body_bold), Paragraph('Joel Aisama (Tutor del Sistema) · Bautista Navarro (Coordinador y Auditor)', body_style)],
    [Paragraph('<b>Principio Rector:</b>', body_bold), Paragraph('<i>«Un asistente que alerta y prioriza, pero nunca decide ni sanciona»</i> (IA Debil)', body_style)],
    [Paragraph('<b>Hipotesis del Canvas:</b>', body_bold), Paragraph('Detectar en las primeras 6 semanas con 4+ semanas de anticipacion para reducir el 15% del abandono.', body_style)],
]
meta_table = Table(meta_data, colWidths=[140, 480])
meta_table.setStyle(TableStyle([
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
]))
story.append(meta_table)
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 2: EL PROBLEMA Y POR QUÉ HACE FALTA IA
# -------------------------------------------------------------
b_s2 = [
    Paragraph('<b>El Desafio Academico:</b> En Argentina, solo ~30 de cada 100 ingresantes logran graduarse. La desercion se concentra en el 1.° ano y se detecta tarde (cuando el docente nota que no viene, ya abandono).', body_style),
    Paragraph('<b>Por que falla la alternativa manual:</b> Revisar planillas a mano no escala a cientos de alumnos, depende de la subjetividad de cada docente y las alertas llegan semanas tarde.', body_style),
    Paragraph('<b>Aporte diferencial de la IA:</b> Cruza semanalmente 3 fuentes disjuntas (asistencia presencial, notas parciales y logs del campus virtual) para emitir alertas preventivas en tiempo real.', body_style)
]
story.extend(make_slide(
    '1. El Problema Local y la Oportunidad de la IA',
    'Deteccion reactiva vs. Intervencion preventiva en las primeras 6 semanas',
    b_s2,
    'sc1_normal.png',
    'La IA cruza senales debiles que un docente aislado no ve, permitiendo ganar 4 semanas de tiempo vital para intervenir.'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 3: ARQUITECTURA EN CADENA A1 -> A2 -> A3
# -------------------------------------------------------------
b_s3 = [
    Paragraph('<b>A1 · Agente de Monitoreo:</b> Ingesta semanalmente asistencia, notas y campus. Garantiza al menos 95% de perfiles completos en 24 h.', body_style),
    Paragraph('<b>A2 · Evaluacion de Riesgo:</b> Aplica regresion logistica multivariable (0-100). Genera los 3 factores causales principales (XAI). Metas: Recall &ge; 70%, Precision &ge; 50%.', body_style),
    Paragraph('<b>A3 · Priorizacion y Alertas:</b> Ordena los casos y respeta el tope de carga del tutor: <b>maximo 15 casos por semana</b> para evitar fatiga cognitiva.', body_style)
]
story.extend(make_slide(
    '2. Arquitectura de Tres Agentes en Cadena',
    'Desacoplamiento funcional: Ingesta (A1) -> Inferencia (A2) -> Priorizacion (A3)',
    b_s3,
    'sc1_normal.png',
    'Ningun agente actua de forma aislada. La informacion fluye en un ciclo semanal formal validado por la matriz Prometheus.'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 4: EXPLICABILIDAD XAI (CASO LUCAS 82 PTS)
# -------------------------------------------------------------
b_s4 = [
    Paragraph('<b>Fin de la Caja Negra:</b> El modelo no emite un puntaje arbitrario; descompone con precision que factores determinan el riesgo.', body_style),
    Paragraph('<b>Caso Lucas Gonzalez (Score 82):</b><br/>• Asistencia cayo al 40% (+38 pts peso logit).<br/>• 2 TPs adeudados en Programacion I (+26 pts).<br/>• 12 dias sin login al campus virtual (+18 pts).', body_style),
    Paragraph('<b>Evolucion Temporal:</b> Muestra la trayectoria de 4 semanas (14 -> 38 -> 62 -> 82 pts), evidenciando el deterioro progresivo antes del abandono definitivo.', body_style)
]
story.extend(make_slide(
    '3. Explicabilidad Algoritmica (XAI) y Tendencia',
    'Comprension causal: como y por que el modelo estima el riesgo del estudiante',
    b_s4,
    'sc1_normal.png',
    'El tutor no tiene que confiar a ciegas en la IA: ve con precision que variables cambiaron para preparar una entrevista empatica.'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 5: COMPUERTA HUMANA N1 A N4 (LA IA NO DECIDE)
# -------------------------------------------------------------
b_s5 = [
    Paragraph('<b>Principio No Delegable (Canvas Casilla 7):</b> La IA se detiene en la bandeja del tutor. <b>Ningun agente tiene permiso de escribirle al alumno, sancionarlo ni darlo de baja.</b>', body_style),
    Paragraph('<b>Protocolo Humano en 4 Puntos:</b><br/>• <b>N1:</b> Tutor acepta o rechaza la sugerencia de la IA.<br/>• <b>N2:</b> Tutor contacta personalmente al alumno (el alumno puede aceptar o rechazar).<br/>• <b>N3:</b> Tutor propone medida institucional y Coordinacion aprueba.<br/>• <b>N4:</b> Solo el tutor cierra o deja el caso en seguimiento.', body_style),
    Paragraph('<b>Firma Digital y Trazabilidad:</b> Cada intervencion se sella con hash de auditoria inmutable.', body_style)
]
story.extend(make_slide(
    '4. Compuerta Humana No Delegable (N1 a N4)',
    'Gobernanza etica: el sistema asiste al tutor pero no toma ninguna accion autonoma',
    b_s5,
    'sc2_intervencion.png',
    'Se evita la estigmatizacion algoritmica: el contacto siempre lo realiza un ser humano con nombre y apellido.'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 6: FALLA F1 (ROBUSTEZ Y SENSOR CAÍDO)
# -------------------------------------------------------------
b_s6 = [
    Paragraph('<b>El Peligro de los Datos Rotos:</b> Si el servidor de Moodle o el campus se cae 48 h, un algoritmo ingenuo asumiria que los 120 alumnos dejaron de ingresar y los marcaria a todos en riesgo alto.', body_style),
    Paragraph('<b>Regla de Falla F1:</b> <i>Falta de dato != Inactividad del estudiante</i>.', body_style),
    Paragraph('<b>Mecanismo de Proteccion:</b> A1 detecta la interrupcion del conector y A2 congela la puntuacion, catalogando a los afectados como <b>«Sin Evaluar»</b>.', body_style),
    Paragraph('<b>Intervencion N5:</b> Coordinacion y Sistemas resuelven el incidente tecnico sin alarmar a tutores ni estudiantes.', body_style)
]
story.extend(make_slide(
    '5. Resiliencia ante Fallas: Sensor Caido (Regla F1)',
    'Blindaje tecnico: como se evita generar panico o falsas alarmas ante caidas de sistemas',
    b_s6,
    'sc3_f1_corte.png',
    'La integridad de datos prima sobre la inferencia: ante fallas de infraestructura, el modelo se suspende preventivamente.'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 7: FALLA F3 (DISCORDANCIA Y FALSOS POSITIVOS)
# -------------------------------------------------------------
b_s7 = [
    Paragraph('<b>Conflicto de Evidencias:</b> Mateo Fernandez presenta 92% de asistencia presencial pero 14 dias sin ingresar al campus virtual.', body_style),
    Paragraph('<b>Regla de Falla F3:</b> A3 <b>no elige que agente tiene razon ni promedia senales opuestas</b>.', body_style),
    Paragraph('<b>Protocolo F3 Lock:</b> El caso se baja a prioridad media y se rotula <b>«En Revision»</b> para que el tutor desempate investigando si el alumno perdio su contrasena.', body_style),
    Paragraph('<b>Control de Precision (&ge; 50%):</b> Si el tutor descarta el riesgo, queda registrado como falso positivo para auditoria cuatrimestral.', body_style)
]
story.extend(make_slide(
    '6. Resolucion de Conflictos y Discordancia (Regla F3)',
    'Humano en el bucle: desempate ante senales presenciales y virtuales contradictorias',
    b_s7,
    'sc4_f3_discordancia.png',
    'El sistema reconoce sus propios limites de observabilidad y cede el control al tutor ante casos ambiguos.'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 8: CONTROL DE SESGO N7 Y MATRIZ DE PERMISOS C1
# -------------------------------------------------------------
b_s8 = [
    Paragraph('<b>Auditoria de Sesgo Algoritmico (N7):</b> Coordinacion audita que la disparidad de recall entre turnos no supere los 10 puntos: Manana 74.5%, Tarde 72.1%, Noche 75.9% (&Delta; = 3.8 pts &le; 10 pts).', body_style),
    Paragraph('<b>Proteccion Anti-Sesgo Docente (Regla C1):</b> Los docentes de catedra cargan notas y asistencia, pero <b>tienen prohibido ver los puntajes de riesgo de sus alumnos</b> para no condicionar sus correcciones parciales.', body_style),
    Paragraph('<b>Aprobacion N8:</b> Solo se procesan datos con consentimiento expreso del alumno.', body_style)
]
story.extend(make_slide(
    '7. Control de Sesgo (N7) y Regla Docente (C1)',
    'Equidad algoritmica inter-turno y aislamiento de evaluaciones de catedra',
    b_s8,
    'sc5_sesgo_n7.png',
    'Garantia de justicia distributiva: el modelo trata con el mismo nivel de acierto a los alumnos de la noche, tarde y manana.'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 9: ROL COORDINACIÓN INSTITUCIONAL (N3, N6, N7)
# -------------------------------------------------------------
b_s9 = [
    Paragraph('<b>Separacion de Roles:</b> El tutor acompana; las decisiones de impacto en la carrera las aprueba la autoridad institucional.', body_style),
    Paragraph('<b>Aprobacion de Derivaciones (N3):</b> Si el tutor detecta que Lucas Gonzalez trabaja de noche, propone el cambio al turno manana y Coordinacion lo oficializa.', body_style),
    Paragraph('<b>Escalamiento ante Inaccion (F2 / N6):</b> Si un tutor no atiende un caso critico en 10 dias, el sistema escala automaticamente a Coordinacion para reasignarlo al Tutor B.', body_style),
    Paragraph('<b>Aprobacion de Recalibracion:</b> A2 no se reentrena solo; Coordinacion valida cada cambio.', body_style)
]
story.extend(make_slide(
    '8. Vista de Coordinacion y Medidas Institucionales',
    'Gobierno academico: aprobacion de cambios de comision, becas y reasignaciones (N6)',
    b_s9,
    'sc7_coordinacion.png',
    'La herramienta digital se acopla a la estructura real de la facultad: secretaria academica tiene el control institucional final.'
))
story.append(PageBreak())

# -------------------------------------------------------------
# SLIDE 10: CONCLUSIÓN Y VALIDACIÓN DE LA HIPÓTESIS
# -------------------------------------------------------------
story.append(Paragraph('9. Conclusion: Que Aporta y Como se Valida la Hipotesis', slide_title))
story.append(Paragraph('Resumen ejecutivo para la defensa del Trabajo Practico de Innovacion', slide_sub))
story.append(Spacer(1, 10))

summary_cards = [
    [
        Paragraph('<b>1. ¿Que hace el sistema?</b><br/>Consolida semanalmente los rastros digitales de los estudiantes en un modelo de IA debil explicable, priorizando los 15 casos mas criticos por tutor.', body_style),
        Paragraph('<b>2. ¿Por que es necesario?</b><br/>Porque el metodo tradicional de esperar el aviso manual de un docente llega tarde: la desercion se consuma en las primeras semanas sin ser advertida.', body_style)
    ],
    [
        Paragraph('<b>3. ¿Como ayuda a la institucion?</b><br/>Multiplica la capacidad de acompanamiento de los tutores, garantiza que ningun estudiante quede sin evaluar y erradica el sesgo humano en la deteccion temprana.', body_style),
        Paragraph('<b>4. Validacion de la Hipotesis del Canvas:</b><br/>La meta de <b>reducir el 15% del abandono</b> se valida en un piloto comparando la tasa de desercion del cuatrimestre con el anterior.', body_style)
    ]
]
sum_table = Table(summary_cards, colWidths=[355, 355])
sum_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ('TOPPADDING', (0,0), (-1,-1), 12),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ('LEFTPADDING', (0,0), (-1,-1), 14),
    ('RIGHTPADDING', (0,0), (-1,-1), 14),
]))
story.append(sum_table)

story.append(Spacer(1, 18))
final_banner = Table([[
    Paragraph('<b>Frase de Cierre de la Defensa:</b> <i>«El problema del abandono universitario no es que nadie quiera ayudar a los alumnos; el problema es que nadie se entera a tiempo. SITA-IA no reemplaza a las personas: les da la informacion oportuna para que puedan actuar antes de que sea tarde.»</i>', ParagraphStyle('FB', fontName='Helvetica', fontSize=10.5, leading=15, textColor=colors.HexColor('#1e3a8a')))
]], colWidths=[710])
final_banner.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#eff6ff')),
    ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#3b82f6')),
    ('TOPPADDING', (0,0), (-1,-1), 11),
    ('BOTTOMPADDING', (0,0), (-1,-1), 11),
    ('LEFTPADDING', (0,0), (-1,-1), 15),
    ('RIGHTPADDING', (0,0), (-1,-1), 15),
]))
story.append(final_banner)

doc.build(story)
print('PDF generado correctamente')
