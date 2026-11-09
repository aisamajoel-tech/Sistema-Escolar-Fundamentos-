"""
Generador de Presentación PowerPoint (.pptx) Nativa y Estética estilo Canva Pitch Deck
Produce Presentacion_Parcial_FIA_SITA.pptx (6 diapositivas 16:9 editables en PowerPoint)
con fondos ambient glow de alta resolución, mockups Mac con sombra proyectada y cajas nativas.
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
ASSETS_DIR = SCREENSHOTS_DIR / "pptx_assets"
PPTX_PATH = BASE_DIR / "Presentacion_Parcial_FIA_SITA.pptx"


def create_ambient_background(filename: str, variant: str = "hero") -> Path:
    """Genera un fondo 2560x1440 estilo Canva Dark/Bordeaux Pitch Deck con luces ambientales."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = ASSETS_DIR / filename
    w, h = 2560, 1440

    # Base oscura elegante (#0B0F19)
    base = Image.new("RGBA", (w, h), (11, 15, 25, 255))

    # Capa de luces radiales (orbes difuminados)
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)

    if variant == "hero":
        # Orbe Bordó UCH arriba derecha y abajo izquierda
        gdraw.ellipse((1450, -300, 2750, 950), fill=(138, 21, 56, 115))
        gdraw.ellipse((-350, 650, 950, 1750), fill=(99, 102, 241, 70))
        gdraw.ellipse((850, 150, 1950, 1150), fill=(245, 158, 11, 35))
    elif variant == "ai":
        gdraw.ellipse((1500, -250, 2700, 900), fill=(124, 58, 237, 95))
        gdraw.ellipse((-300, 500, 1000, 1700), fill=(138, 21, 56, 95))
        gdraw.ellipse((900, 700, 2100, 1600), fill=(14, 165, 233, 45))
    elif variant == "closing":
        gdraw.ellipse((1300, -200, 2650, 1050), fill=(138, 21, 56, 120))
        gdraw.ellipse((-250, -200, 1050, 950), fill=(16, 185, 129, 55))
        gdraw.ellipse((600, 650, 1950, 1650), fill=(245, 158, 11, 50))
    else:
        gdraw.ellipse((1550, -250, 2750, 900), fill=(138, 21, 56, 95))
        gdraw.ellipse((-350, 600, 900, 1700), fill=(30, 64, 175, 70))

    glow = glow.filter(ImageFilter.GaussianBlur(radius=160))
    base = Image.alpha_composite(base, glow)

    # Grilla sutil arquitectónica estilo Canva Tech
    grid = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    grdraw = ImageDraw.Draw(grid)
    step = 64
    for x in range(0, w, step):
        grdraw.line([(x, 0), (x, h)], fill=(255, 255, 255, 7), width=1)
    for y in range(0, h, step):
        grdraw.line([(0, y), (w, y)], fill=(255, 255, 255, 7), width=1)

    # Línea superior decorativa degradada (Bordó -> Dorado -> Violeta)
    for x in range(w):
        ratio = x / w
        if ratio < 0.5:
            t = ratio * 2
            r = int(138 * (1 - t) + 245 * t)
            g = int(21 * (1 - t) + 158 * t)
            b = int(56 * (1 - t) + 11 * t)
        else:
            t = (ratio - 0.5) * 2
            r = int(245 * (1 - t) + 139 * t)
            g = int(158 * (1 - t) + 92 * t)
            b = int(11 * (1 - t) + 246 * t)
        grdraw.line([(x, 0), (x, 8)], fill=(r, g, b, 230))

    final_img = Image.alpha_composite(base, grid).convert("RGB")
    final_img.save(out_path, "PNG", optimize=True)
    return out_path


def create_browser_mockup(src_png: Path, out_name: str, url_text: str) -> Path:
    """Empaqueta una captura del sistema en una ventana estilo macOS con bordes redondeados y sombra suave."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = ASSETS_DIR / out_name

    shot = Image.open(src_png).convert("RGBA")
    target_w = 1360
    scale = target_w / shot.width
    target_h = int(shot.height * scale)
    shot = shot.resize((target_w, target_h), Image.Resampling.LANCZOS)

    header_h = 54
    border_pad = 6
    win_w = target_w + border_pad * 2
    win_h = target_h + header_h + border_pad
    radius = 22

    # Lienzo con margen para la sombra proyectada
    pad = 44
    canvas = Image.new("RGBA", (win_w + pad * 2, win_h + pad * 2), (0, 0, 0, 0))

    # Sombra suave
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle(
        (pad + 6, pad + 14, pad + win_w + 6, pad + win_h + 14),
        radius=radius + 4,
        fill=(0, 0, 0, 155),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=22))
    canvas = Image.alpha_composite(canvas, shadow)

    # Cuerpo de la ventana oscura (#1E293B) con borde brillante sutil
    win = Image.new("RGBA", (win_w, win_h), (0, 0, 0, 0))
    wdraw = ImageDraw.Draw(win)
    wdraw.rounded_rectangle(
        (0, 0, win_w - 1, win_h - 1),
        radius=radius,
        fill=(24, 33, 50, 255),
        outline=(100, 116, 139, 160),
        width=2,
    )

    # Botones semáforo macOS
    dots = [((24, 19), (239, 68, 68)), ((48, 19), (245, 158, 11)), ((72, 19), (16, 185, 129))]
    for (dx, dy), color in dots:
        wdraw.ellipse((dx, dy, dx + 15, dy + 15), fill=color)

    # Barra de URL
    bar_left = 110
    bar_right = win_w - 28
    wdraw.rounded_rectangle(
        (bar_left, 11, bar_right, 42),
        radius=10,
        fill=(13, 18, 30, 255),
        outline=(51, 65, 85, 180),
        width=1,
    )

    try:
        font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 17)
    except Exception:
        font = ImageFont.load_default()
    wdraw.text((bar_left + 18, 17), url_text, fill=(203, 213, 225, 255), font=font)

    # Máscara redondeada inferior para la captura
    shot_mask = Image.new("L", (target_w, target_h), 0)
    mdraw = ImageDraw.Draw(shot_mask)
    mdraw.rounded_rectangle((0, -20, target_w, target_h), radius=16, fill=255)
    win.paste(shot, (border_pad, header_h), shot_mask)

    canvas.alpha_composite(win, (pad, pad))
    canvas.save(out_path, "PNG", optimize=True)
    return out_path


def add_pill(slide, left, top, width, height, text, bg_rgb, fg_rgb, border_rgb=None, font_size=10.5, bold=True, align=PP_ALIGN.CENTER):
    """Agrega una etiqueta tipo píldora (badge) editable en PowerPoint."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.adjustments[0] = 0.5
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(*bg_rgb)
    if border_rgb:
        shape.line.color.rgb = RGBColor(*border_rgb)
        shape.line.width = Pt(1.2)
    else:
        shape.line.fill.background()

    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    tf.margin_top = Inches(0.03)
    tf.margin_bottom = Inches(0.03)
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = "Segoe UI"
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(*fg_rgb)
    return shape


def add_card(slide, left, top, width, height, bg_rgb=(21, 28, 44), border_rgb=(45, 58, 84), accent_rgb=None, radius=0.06):
    """Agrega una tarjeta estilizada con borde sutil y barra de acento opcional."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.adjustments[0] = radius
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(*bg_rgb)
    card.line.color.rgb = RGBColor(*border_rgb)
    card.line.width = Pt(1.2)

    if accent_rgb:
        bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(0.09), height)
        bar.adjustments[0] = 0.2
        bar.fill.solid()
        bar.fill.fore_color.rgb = RGBColor(*accent_rgb)
        bar.line.fill.background()
    return card


def add_textbox(slide, left, top, width, height, lines, align=PP_ALIGN.LEFT):
    """
    Agrega un cuadro de texto limpio.
    lines es una lista de tuplas: (texto, font_size, bold, rgb_color, space_after_pt)
    """
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)

    for idx, item in enumerate(lines):
        text, size, bold, color, space_after = item
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        run = p.add_run()
        run.text = text
        run.font.name = "Segoe UI"
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = RGBColor(*color)
    return tb


def add_header(slide, badge_text, badge_bg, badge_fg, badge_border, title_text, slide_num_str):
    """Cabecera uniforme de estilo Canva Pitch Deck para las diapositivas 2 a 6."""
    add_pill(
        slide,
        Inches(0.55),
        Inches(0.38),
        Inches(4.9),
        Inches(0.34),
        badge_text,
        bg_rgb=badge_bg,
        fg_rgb=badge_fg,
        border_rgb=badge_border,
        font_size=9.5,
        bold=True,
        align=PP_ALIGN.LEFT,
    )
    add_pill(
        slide,
        Inches(11.35),
        Inches(0.38),
        Inches(1.42),
        Inches(0.34),
        slide_num_str,
        bg_rgb=(24, 33, 52),
        fg_rgb=(226, 232, 240),
        border_rgb=(65, 84, 118),
        font_size=9.5,
        bold=True,
    )
    add_textbox(
        slide,
        Inches(0.55),
        Inches(0.78),
        Inches(12.2),
        Inches(0.62),
        [(title_text, 23, True, (248, 250, 252), 0)],
    )


def add_footer(slide, left_text, right_text):
    """Pie de página minimalista y elegante."""
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(7.02), Inches(12.23), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(40, 52, 75)
    line.line.fill.background()

    add_textbox(
        slide,
        Inches(0.55),
        Inches(7.08),
        Inches(7.5),
        Inches(0.3),
        [(left_text, 9.5, False, (148, 163, 184), 0)],
    )
    add_textbox(
        slide,
        Inches(8.1),
        Inches(7.08),
        Inches(4.68),
        Inches(0.3),
        [(right_text, 9.5, True, (251, 191, 36), 0)],
        align=PP_ALIGN.RIGHT,
    )


def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Fondos ambient glow
    bg_hero = create_ambient_background("bg_hero.png", "hero")
    bg_std = create_ambient_background("bg_std.png", "std")
    bg_ai = create_ambient_background("bg_ai.png", "ai")
    bg_close = create_ambient_background("bg_close.png", "closing")

    # Asegurar que existan las capturas específicas de Docente C1 y Falla F3
    temp_dir = Path(r"C:\Users\aisam\AppData\Local\Temp\sita_shots")
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_html = temp_dir / "demo_panel.html"
    import shutil, subprocess
    shutil.copy2(BASE_DIR / "views" / "demo_panel.html", temp_html)
    shutil.copy2(BASE_DIR / "views" / "demo_panel.html", BASE_DIR / "demo_panel.html")
    if (BASE_DIR / "views" / "logo_uch.png").exists():
        shutil.copy2(BASE_DIR / "views" / "logo_uch.png", temp_dir / "logo_uch.png")

    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    edge_exe = next((p for p in edge_paths if os.path.exists(p)), None)
    if edge_exe:
        extra_shots = [
            ("sc2_docente_c1.png", f"file:///{str(temp_html).replace(os.sep, '/')}?sc=docente"),
            ("sc4_f3_mateo.png", f"file:///{str(temp_html).replace(os.sep, '/')}?sc=f3"),
        ]
        for fname, url in extra_shots:
            if not (SCREENSHOTS_DIR / fname).exists():
                out_tmp = temp_dir / fname
                subprocess.run(
                    [edge_exe, "--headless", "--disable-gpu", "--window-size=1440,900", f"--screenshot={out_tmp}", url],
                    check=False,
                )
                if out_tmp.exists():
                    shutil.copy2(out_tmp, SCREENSHOTS_DIR / fname)

    # Mockups Mac con capturas reales del Campus UCH
    mk_sc1 = create_browser_mockup(
        SCREENSHOTS_DIR / "sc1_normal.png",
        "mk_sc1.png",
        "https://campus.uch.edu.ar/mod/assign/view.php?id=560274  ·  SITA-IA",
    )
    mk_sc2 = create_browser_mockup(
        SCREENSHOTS_DIR / "sc8_gemini_api.png",
        "mk_sc2.png",
        "Google AI Studio REST API (gemini-1.5-flash)  ·  Expediente #24901",
    )
    mk_sc3 = create_browser_mockup(
        SCREENSHOTS_DIR / ("sc2_docente_c1.png" if (SCREENSHOTS_DIR / "sc2_docente_c1.png").exists() else "sc1_normal.png"),
        "mk_sc3.png",
        "Vista Docente de Cátedra  ·  Score SITA Bloqueado (Regla Anti-Sesgo C1)",
    )
    mk_sc4 = create_browser_mockup(
        SCREENSHOTS_DIR / "sc3_f1_corte.png",
        "mk_sc4.png",
        "Protocolo F1 Activo  ·  Perfiles Protegidos en Estado 'Sin Evaluar'",
    )
    mk_sc5 = create_browser_mockup(
        SCREENSHOTS_DIR / ("sc4_f3_mateo.png" if (SCREENSHOTS_DIR / "sc4_f3_mateo.png").exists() else "sc3_f1_corte.png"),
        "mk_sc5.png",
        "Protocolo F3 Activo  ·  Señales Contradictorias (Mateo 92% Asist. vs 14d)",
    )
    mk_sc6 = create_browser_mockup(
        SCREENSHOTS_DIR / "sc5_sesgo_n7.png",
        "mk_sc6.png",
        "Secretaría Académica  ·  Derivación N3, Reasignación N6 y Auditoría N7",
    )
    logo_path = BASE_DIR / "views" / "logo_uch.png"

    # =========================================================================
    # SLIDE 1: PORTADA HACKATHON PITCH (IMPACTO VISUAL + CAMPUS UCH)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    s1.shapes.add_picture(str(bg_hero), Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    # Top bar institucional
    if logo_path.exists():
        logo_card = add_card(s1, Inches(0.55), Inches(0.42), Inches(0.58), Inches(0.58), bg_rgb=(255, 255, 255), border_rgb=(226, 232, 240), radius=0.2)
        s1.shapes.add_picture(str(logo_path), Inches(0.61), Inches(0.54), width=Inches(0.46))

    add_textbox(
        s1,
        Inches(1.24),
        Inches(0.42),
        Inches(6.5),
        Inches(0.6),
        [
            ("UNIVERSIDAD CHAMPAGNAT · FACULTAD DE INFORMÁTICA", 11.5, True, (248, 250, 252), 1),
            ("Fundamentos de Inteligencia Artificial (3° Año) · Pitch Deck & Defensa Oral", 10, False, (148, 163, 184), 0),
        ],
    )

    add_pill(
        s1,
        Inches(8.55),
        Inches(0.48),
        Inches(2.65),
        Inches(0.38),
        "⚡ IA Híbrida: ML XAI + Gemini 1.5",
        bg_rgb=(36, 24, 54),
        fg_rgb=(251, 191, 36),
        border_rgb=(139, 92, 246),
        font_size=10,
    )
    add_pill(
        s1,
        Inches(11.35),
        Inches(0.48),
        Inches(1.42),
        Inches(0.38),
        "SLIDE 01 / 06",
        bg_rgb=(24, 33, 52),
        fg_rgb=(226, 232, 240),
        border_rgb=(65, 84, 118),
        font_size=9.5,
    )

    # Pill principal del Pitch
    add_pill(
        s1,
        Inches(0.55),
        Inches(1.38),
        Inches(3.75),
        Inches(0.36),
        "🚀 SOLUCIÓN EDTECH PARA RETENCIÓN UNIVERSITARIA",
        bg_rgb=(88, 17, 38),
        fg_rgb=(253, 164, 175),
        border_rgb=(225, 29, 72),
        font_size=9.5,
    )

    # Gran titular de venta
    add_textbox(
        s1,
        Inches(0.55),
        Inches(1.86),
        Inches(5.75),
        Inches(2.35),
        [
            ("SITA-IA: Detectamos", 34, True, (255, 255, 255), 0),
            ("el abandono 4 semanas", 34, True, (251, 191, 36), 0),
            ("antes de que ocurra.", 34, True, (255, 255, 255), 8),
            (
                "Un sistema multiagente integrado al Campus Virtual Moodle (campus.uch.edu.ar) que transforma la asistencia, entregas de TPs y actividad digital en acompañamiento humano temprano.",
                12.5,
                False,
                (203, 213, 225),
                0,
            ),
        ],
    )

    # 3 Tarjetas de métricas de alto impacto
    kpis = [
        ("≥ 4 Sem.", "Anticipación real", "Antes del 1° parcial", (251, 191, 36), (138, 21, 56)),
        ("≤ 15 Casos", "Tope por tutor (O4)", "Cero saturación docente", (52, 211, 153), (16, 185, 129)),
        ("$0 USD", "Costo operativo", "Python MVC + Gemini API", (56, 189, 248), (59, 130, 246)),
    ]
    for idx, (big, sub1, sub2, col_txt, col_bar) in enumerate(kpis):
        cx = Inches(0.55 + idx * 1.92)
        cy = Inches(4.92)
        add_card(s1, cx, cy, Inches(1.80), Inches(1.62), bg_rgb=(19, 27, 46), border_rgb=(51, 65, 85), accent_rgb=col_bar, radius=0.08)
        add_textbox(
            s1,
            cx + Inches(0.16),
            cy + Inches(0.16),
            Inches(1.56),
            Inches(1.32),
            [
                (big, 20, True, col_txt, 4),
                (sub1, 10.5, True, (241, 245, 249), 2),
                (sub2, 9.5, False, (148, 163, 184), 0),
            ],
        )

    # Mockup grande del Campus UCH a la derecha
    s1.shapes.add_picture(str(mk_sc1), Inches(6.28), Inches(1.28), width=Inches(6.65))

    add_footer(
        s1,
        "Equipo Desarrollador: Joel Aisama (Modelos IA & Tutoría) · Bautista Navarro (Arquitectura MVC, Auditoría & Coordinación)",
        "github.com/aisamajoel-tech/Sistema-Escolar-Fundamentos-",
    )

    # =========================================================================
    # SLIDE 2: PROBLEMA, ROLES Y LÍMITES ÉTICOS (PUNTOS 1 Y 2)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    s2.shapes.add_picture(str(bg_std), Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    add_header(
        s2,
        "📌 PUNTOS 1 Y 2 · PROBLEMA LOCAL, USUARIOS Y LÍMITES",
        (76, 17, 36),
        (253, 164, 175),
        (225, 29, 72),
        "El Problema: Las señales de abandono existen, pero están aisladas",
        "SLIDE 02 / 06",
    )

    # Card 1: El Dolor Institucional
    add_card(s2, Inches(0.55), Inches(1.48), Inches(5.85), Inches(1.55), bg_rgb=(20, 27, 45), border_rgb=(51, 65, 85), accent_rgb=(225, 29, 72))
    add_textbox(
        s2,
        Inches(0.75),
        Inches(1.58),
        Inches(5.5),
        Inches(1.35),
        [
            ("🔥 1. Deserción Silenciosa en las Primeras 6 Semanas", 13.5, True, (251, 191, 36), 4),
            (
                "En 1° año, la asistencia (SIU-Guaraní), las entregas vencidas en Moodle (/mod/assign) y las notas de parciales viven en silos separados. Cuando la facultad los cruza a fin de cuatrimestre, el estudiante ya abandonó.",
                10.5,
                False,
                (203, 213, 225),
                0,
            ),
        ],
    )

    # Card 2: Ecosistema de 4 Roles
    add_card(s2, Inches(0.55), Inches(3.16), Inches(5.85), Inches(2.22), bg_rgb=(20, 27, 45), border_rgb=(51, 65, 85), accent_rgb=(56, 189, 248))
    add_textbox(
        s2,
        Inches(0.75),
        Inches(3.26),
        Inches(5.5),
        Inches(2.05),
        [
            ("👥 2. Cuatro Roles con Permisos Estrictamente Aislados", 13.5, True, (56, 189, 248), 5),
            ("• Tutor Pedagógico (Joel Aisama): Recibe ≤ 15 alertas y guía la entrevista (N1–N4).", 10.2, False, (241, 245, 249), 3),
            ("• Secretaría Académica (Bautista Navarro): Aprueba pases/becas (N3) y audita sesgos (N7).", 10.2, False, (241, 245, 249), 3),
            ("• Profesor de Cátedra (Ing. Méndez): Carga notas con el Score Bloqueado (Regla C1).", 10.2, True, (253, 224, 71), 3),
            ("• Estudiante (Lucas González): Firma consentimiento (N8) y recibe apoyo humano.", 10.2, False, (241, 245, 249), 0),
        ],
    )

    # Dos tarjetas inferiores: QUÉ SÍ HACE vs QUÉ NO HACE JAMÁS
    add_card(s2, Inches(0.55), Inches(5.52), Inches(2.85), Inches(1.32), bg_rgb=(14, 38, 34), border_rgb=(16, 185, 129), accent_rgb=(16, 185, 129))
    add_textbox(
        s2,
        Inches(0.73),
        Inches(5.60),
        Inches(2.58),
        Inches(1.15),
        [
            ("✅ Qué SÍ hace SITA-IA", 11.5, True, (52, 211, 153), 3),
            ("Calcula riesgo 0–100 semanal, explica los 3 motivos (XAI) y sugiere preguntas empáticas al tutor.", 9.5, False, (209, 250, 229), 0),
        ],
    )

    add_card(s2, Inches(3.55), Inches(5.52), Inches(2.85), Inches(1.32), bg_rgb=(46, 18, 29), border_rgb=(244, 63, 94), accent_rgb=(244, 63, 94))
    add_textbox(
        s2,
        Inches(3.73),
        Inches(5.60),
        Inches(2.58),
        Inches(1.15),
        [
            ("🚫 Qué NO hace jamás", 11.5, True, (251, 113, 133), 3),
            ("No envía alertas automáticas al alumno, no sanciona, no altera notas ni da de baja cursadas.", 9.5, False, (254, 205, 211), 0),
        ],
    )

    # Columna derecha: Mockup Vista Docente con Candado C1 + KPIs de éxito
    s2.shapes.add_picture(str(mk_sc3), Inches(6.55), Inches(1.42), width=Inches(6.35))

    # Barra de 4 criterios de éxito (Punto 2d)
    add_card(s2, Inches(6.65), Inches(5.52), Inches(6.12), Inches(1.32), bg_rgb=(20, 27, 45), border_rgb=(59, 130, 246))
    add_textbox(
        s2,
        Inches(6.82),
        Inches(5.58),
        Inches(5.8),
        Inches(0.32),
        [("🎯 Criterios de Éxito Cuantificables del Proyecto (Punto 2d)", 11, True, (147, 197, 253), 0)],
    )
    metrics_s2 = [
        ("≥ 70%", "Recall (O1)"),
        ("≥ 50%", "Precisión (O2)"),
        ("≤ 15", "Alertas/Tutor"),
        ("-15%", "Baja Deserción"),
    ]
    for i, (m_val, m_lbl) in enumerate(metrics_s2):
        mx = Inches(6.82 + i * 1.46)
        my = Inches(5.94)
        add_card(s2, mx, my, Inches(1.36), Inches(0.76), bg_rgb=(13, 18, 32), border_rgb=(51, 65, 85), radius=0.12)
        add_textbox(
            s2,
            mx,
            my + Inches(0.08),
            Inches(1.36),
            Inches(0.62),
            [
                (m_val, 14, True, (251, 191, 36), 1),
                (m_lbl, 8.8, False, (203, 213, 225), 0),
            ],
            align=PP_ALIGN.CENTER,
        )

    add_footer(
        s2,
        "SITA-IA · Arquitectura MVC (models/ · views/ · controllers/)",
        "Regla C1: Prevención del Efecto Pigmalión en Evaluaciones",
    )

    # =========================================================================
    # SLIDE 3: ARQUITECTURA MULTIAGENTE + GEMINI 1.5 FLASH (PUNTOS 3 Y 4)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    s3.shapes.add_picture(str(bg_ai), Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    add_header(
        s3,
        "🧠 PUNTOS 3 Y 4 · PIPELINE MULTIAGENTE (A1 → A2 → A3) Y GEMINI 1.5 FLASH",
        (46, 22, 78),
        (216, 180, 254),
        (168, 85, 247),
        "IA Híbrida en Acción: Scoring Predictivo XAI + Empatía con Gemini 1.5",
        "SLIDE 03 / 06",
    )

    # Fila superior: 4 bloques del Pipeline conectados
    steps = [
        ("1. ENTRADAS CSV", "Agente 1 (Monitoreo)", "Consolida asistencia.csv, campus.csv, notas.csv e historial de 4 semanas.", (56, 189, 248)),
        ("2. ML + XAI (LOGIT)", "Agente 2 (Scoring)", "Regresión Logística P = σ(z) (0–100) + desglose exacto de los 3 motivos en puntos.", (251, 191, 36)),
        ("3. PRIORIZACIÓN + LLM", "Agente 3 + Gemini 1.5", "Filtra tope ≤ 15 alertas y consulta Google AI Studio con datos anonimizados.", (168, 85, 247)),
        ("4. SALIDA HUMANA", "Tutoría y Secretaría", "Ficha explicable para el tutor + entrevista empática (N2) y derivación (N3).", (52, 211, 153)),
    ]
    for idx, (st_tag, st_title, st_desc, st_col) in enumerate(steps):
        sx = Inches(0.55 + idx * 3.10)
        sy = Inches(1.45)
        add_card(s3, sx, sy, Inches(2.92), Inches(1.42), bg_rgb=(20, 27, 45), border_rgb=st_col, accent_rgb=st_col)
        add_textbox(
            s3,
            sx + Inches(0.16),
            sy + Inches(0.10),
            Inches(2.68),
            Inches(1.24),
            [
                (st_tag, 9.5, True, st_col, 2),
                (st_title, 12, True, (255, 255, 255), 3),
                (st_desc, 9.3, False, (203, 213, 225), 0),
            ],
        )

    # Fila inferior izquierda: Caso Demostrativo Lucas González (#24901)
    add_card(s3, Inches(0.55), Inches(3.04), Inches(5.75), Inches(3.82), bg_rgb=(20, 27, 45), border_rgb=(139, 92, 246), accent_rgb=(251, 191, 36))
    add_textbox(
        s3,
        Inches(0.75),
        Inches(3.14),
        Inches(5.4),
        Inches(1.95),
        [
            ("🔍 Caso Real Demostrativo: Lucas González (Legajo #24901)", 13.5, True, (251, 191, 36), 3),
            ("Evolución 4 semanas: 35 → 52 → 68 → 82 / 100 (Riesgo Alto · Prioridad #1)", 10.5, True, (248, 113, 113), 6),
            ("EXPLICABILIDAD XAI (DESCOMPOSICIÓN DE LOGIT · AGENTE A2):", 9.5, True, (148, 163, 184), 3),
            ("1. Asistencia presencial del 40% (4 faltas recientes)  →  +35 pts", 10.2, True, (241, 245, 249), 2),
            ("2. Adeuda 2 de 4 TPs en Moodle (TP N° 2 y TP N° 3)  →  +27 pts", 10.2, True, (241, 245, 249), 2),
            ("3. 12 días corridos sin ingresar al Campus Virtual  →  +20 pts", 10.2, True, (241, 245, 249), 0),
        ],
    )

    # Sub-card violeta: Respuesta generada por Gemini 1.5 Flash
    add_card(s3, Inches(0.75), Inches(5.32), Inches(5.35), Inches(1.36), bg_rgb=(35, 23, 62), border_rgb=(168, 85, 247))
    add_textbox(
        s3,
        Inches(0.90),
        Inches(5.40),
        Inches(5.10),
        Inches(1.20),
        [
            ("✨ Guía de Entrevista Generada por Gemini 1.5 Flash (Punto N2):", 10.5, True, (216, 180, 254), 3),
            (
                "«¿Sentís que el horario del turno noche o alguna exigencia laboral te está dificultando asistir a las prácticas? ¿Te ayudaría armar un cronograma de entregas escalonadas o gestionar un pase de comisión?»",
                9.8,
                False,
                (243, 232, 255),
                0,
            ),
        ],
    )

    # Fila inferior derecha: Mockup del modal JSON de Gemini 1.5 Flash
    s3.shapes.add_picture(str(mk_sc2), Inches(6.42), Inches(2.96), width=Inches(6.48))

    add_footer(
        s3,
        "Flujo técnico auditable bajo Metodología Prometheus (Mensajes P msj. 0* a P msj. 12*)",
        "Integración REST en models/gemini_service.py (gemini-1.5-flash)",
    )

    # =========================================================================
    # SLIDE 4: TOLERANCIA A FALLAS F1, F2, F3 Y COSTO $0 (PUNTO 5)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    s4.shapes.add_picture(str(bg_std), Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    add_header(
        s4,
        "🛡️ PUNTO 5 · INGENIERÍA RESILIENTE, SEGURIDAD Y COSTO $0 USD",
        (16, 52, 76),
        (125, 211, 252),
        (56, 189, 248),
        "Tolerancia a Fallas Reales (F1, F2, F3): Ningún error técnico perjudica al alumno",
        "SLIDE 04 / 06",
    )

    # 3 Tarjetas de Fallas + 1 de Costos a la izquierda
    fallas = [
        (
            "⚠️ Falla F1 · Caída del Servidor de Campus (Falta de dato ≠ Inactividad)",
            "Si Moodle se cae, el Agente A1 detecta la falla técnica y congela los perfiles en estado SIN EVALUAR (F1). Jamás se infla el riesgo del estudiante por un corte informático (Punto N5).",
            (245, 158, 11),
        ),
        (
            "🔍 Falla F3 · Señales Contradictorias (Caso Mateo Fernández #24945)",
            "Mateo registra 92% de asistencia en aula pero 14 días sin entrar a Moodle. El Agente A3 no promedia señales opuestas: lo separa como EN REVISIÓN (F3) para verificación humana.",
            (56, 189, 248),
        ),
        (
            "⏱️ Falla F2 · Inacción del Tutor (SLA de 7 y 10 días → Reasignación N6)",
            "Si una alerta crítica no se atiende en 7 días, A3 envía recordatorio; a los 10 días, escala a Secretaría Académica para reasignar al Tutor Suplente (Prof. Martín Suárez). Nunca actúa un bot.",
            (168, 85, 247),
        ),
        (
            "💻 Costo Operativo $0 USD y Privacidad de Datos (Ley 25.326)",
            "Python 3.10+ nativo (sin GPUs) + Free Tier de Google AI Studio (1.500 req/día gratis; el sistema usa ~15 req/semana). Prompts 100% desidentificados sin DNI ni apellido (Punto N8).",
            (52, 211, 153),
        ),
    ]
    for idx, (f_title, f_desc, f_col) in enumerate(fallas):
        fy = Inches(1.46 + idx * 1.38)
        add_card(s4, Inches(0.55), fy, Inches(5.85), Inches(1.26), bg_rgb=(20, 27, 45), border_rgb=(51, 65, 85), accent_rgb=f_col)
        add_textbox(
            s4,
            Inches(0.75),
            fy + Inches(0.10),
            Inches(5.52),
            Inches(1.08),
            [
                (f_title, 11.5, True, f_col, 3),
                (f_desc, 9.6, False, (203, 213, 225), 0),
            ],
        )

    # Derecha: Doble Mockup escalonado mostrando F1 (Sin Evaluar) y F3 (Mateo en Revisión)
    s4.shapes.add_picture(str(mk_sc4), Inches(6.50), Inches(1.38), width=Inches(5.65))
    s4.shapes.add_picture(str(mk_sc5), Inches(7.15), Inches(3.85), width=Inches(5.65))

    add_footer(
        s4,
        "SITA-IA · Viabilidad inmediata para cualquier universidad pública o privada",
        "Resiliencia verificada en vivo desde el Campus Virtual UCH",
    )

    # =========================================================================
    # SLIDE 5: ANÁLISIS ÉTICO OBLIGATORIO Y GOBERNANZA N1–N8 (PUNTO 6)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    s5.shapes.add_picture(str(bg_std), Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    add_header(
        s5,
        "⚖️ PUNTO 6 · ANÁLISIS ÉTICO OBLIGATORIO Y COMPUERTAS HUMANAS N1–N8",
        (76, 17, 36),
        (253, 164, 175),
        (225, 29, 72),
        "Ética Programada en Código: 5 Riesgos Mitigados por Diseño",
        "SLIDE 05 / 06",
    )

    riesgos = [
        (
            "1. Sesgo Algorítmico contra el Turno Noche",
            "Mitigación (N7): Auditoría semestral de sensibilidad (Recall) entre Mañana (76.2%), Tarde (74.8%) y Noche (72.4%) → Brecha Δ = 3.8 pts ≤ 10 pts.",
            (251, 191, 36),
        ),
        (
            "2. Estigmatización Docente (Efecto Pigmalión)",
            "Mitigación (Regla C1): El profesor de cátedra tiene el score de riesgo bloqueado con candado para no sesgar la corrección de exámenes.",
            (244, 63, 94),
        ),
        (
            "3. Privacidad y Vigilancia Digital Invasiva",
            "Mitigación (N8): Opt-in mediante consentimiento informado (P msj. 0*), variables solo académicas y anonimización antes de Gemini API.",
            (56, 189, 248),
        ),
        (
            "4. Automatización Ciega ante Fallas Técnicas",
            "Mitigación (Reglas F1 y F3): Suspensión automática en estado 'Sin Evaluar' ante caída de Moodle y revisión humana ante datos opuestos.",
            (168, 85, 247),
        ),
        (
            "5. Deshumanización del Vínculo Pedagógico",
            "Mitigación (N1 a N4): Cero bots al alumno. El tutor humano valida el caso, realiza la entrevista empática y firma cada resolución.",
            (52, 211, 153),
        ),
    ]
    for idx, (r_title, r_desc, r_col) in enumerate(riesgos):
        ry = Inches(1.44 + idx * 1.09)
        add_card(s5, Inches(0.55), ry, Inches(5.85), Inches(0.99), bg_rgb=(20, 27, 45), border_rgb=(51, 65, 85), accent_rgb=r_col)
        add_textbox(
            s5,
            Inches(0.75),
            ry + Inches(0.07),
            Inches(5.52),
            Inches(0.86),
            [
                (r_title, 11, True, r_col, 2),
                (r_desc, 9.2, False, (203, 213, 225), 0),
            ],
        )

    # Derecha: Mockup de Secretaría Académica (Gobernanza N3, N6, N7)
    s5.shapes.add_picture(str(mk_sc6), Inches(6.52), Inches(1.48), width=Inches(6.38))

    # Pill resumen de equidad debajo del mockup
    add_card(s5, Inches(6.62), Inches(5.78), Inches(6.16), Inches(1.06), bg_rgb=(16, 38, 34), border_rgb=(16, 185, 129))
    add_textbox(
        s5,
        Inches(6.80),
        Inches(5.86),
        Inches(5.82),
        Inches(0.90),
        [
            ("✅ Resultado de Auditoría Algorítmica Semestral (Punto N7 · Verificado):", 11, True, (52, 211, 153), 3),
            ("Recall Mañana: 76.2%  |  Recall Tarde: 74.8%  |  Recall Noche: 72.4%  →  Diferencia: 3.8 pts (Cumple umbral ≤ 10 pts).", 9.6, False, (209, 250, 229), 0),
        ],
    )

    add_footer(
        s5,
        "Cumplimiento integral de los 8 Puntos de Gobernanza Humana (N1 a N8)",
        "Supervisión algorítmica: Secretaría Académica UCH",
    )

    # =========================================================================
    # SLIDE 6: HOJA DE RUTA DE DEFENSA (5 MIN) Y CIERRE EJECUTIVO (PUNTO 7)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    s6.shapes.add_picture(str(bg_close), Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    add_header(
        s6,
        "🎤 PUNTO 7 · GUION DE DEFENSA ORAL (5 MINUTOS) Y CONCLUSIÓN DEL EQUIPO",
        (68, 42, 14),
        (253, 224, 71),
        (245, 158, 11),
        "Hoja de Ruta de la Exposición y Recomendación Institucional Final",
        "SLIDE 06 / 06",
    )

    bloques = [
        (
            "0:00 – 1:15 · JOEL AISAMA",
            "1. Problema y Valor",
            "Deserción silenciosa en las primeras 6 semanas de 1° año. Cómo cruzar asistencia, TPs de Moodle y parciales anticipa el riesgo 4 semanas antes.",
            (225, 29, 72),
        ),
        (
            "1:15 – 2:45 · JOEL AISAMA",
            "2. IA Híbrida + Caso Lucas",
            "Pipeline MVC (A1 → A2 → A3). Caso Lucas González (#24901, Score 82/100 + 3 factores XAI) y guía empática en vivo con Gemini 1.5 Flash.",
            (168, 85, 247),
        ),
        (
            "2:45 – 4:00 · BAUTISTA NAVARRO",
            "3. Roles y Fallas F1–F3",
            "Demostración del Bloqueo Docente C1 (candado anti-sesgo), contingencia F1 (Sin Evaluar), contradicción F3 (Mateo) y SLA F2/N6.",
            (56, 189, 248),
        ),
        (
            "4:00 – 5:00 · BAUTISTA & JOEL",
            "4. Ética, Costo $0 y Cierre",
            "Auditoría inter-turno N7 (Δ 3.8 pts), privacidad Ley 25.326 (N8), costo operativo $0 USD y recomendación ética final del equipo.",
            (52, 211, 153),
        ),
    ]
    for idx, (b_time, b_title, b_desc, b_col) in enumerate(bloques):
        bx = Inches(0.55 + idx * 3.10)
        by = Inches(1.52)
        add_card(s6, bx, by, Inches(2.92), Inches(2.38), bg_rgb=(20, 27, 45), border_rgb=b_col, accent_rgb=b_col)
        add_pill(
            s6,
            bx + Inches(0.18),
            by + Inches(0.18),
            Inches(2.35),
            Inches(0.30),
            b_time,
            bg_rgb=(13, 18, 32),
            fg_rgb=b_col,
            border_rgb=b_col,
            font_size=8.5,
        )
        add_textbox(
            s6,
            bx + Inches(0.18),
            by + Inches(0.58),
            Inches(2.60),
            Inches(1.68),
            [
                (b_title, 13.5, True, (255, 255, 255), 5),
                (b_desc, 9.8, False, (203, 213, 225), 0),
            ],
        )

    # Gran Banner de Cierre / Recomendación Final
    add_card(s6, Inches(0.55), Inches(4.18), Inches(12.23), Inches(2.62), bg_rgb=(32, 14, 28), border_rgb=(245, 158, 11), accent_rgb=(251, 191, 36), radius=0.05)
    add_textbox(
        s6,
        Inches(0.88),
        Inches(4.36),
        Inches(11.65),
        Inches(2.25),
        [
            ("💡 RECOMENDACIÓN INSTITUCIONAL FINAL DEL EQUIPO (CIERRE DE DEFENSA ORAL)", 10.5, True, (251, 191, 36), 8),
            (
                "«Nuestra recomendación como equipo es adoptar SITA-IA bajo una premisa innegociable: en la educación universitaria, la Inteligencia Artificial debe funcionar como un radar temprano que multiplique la capacidad humana de escuchar y llegar a tiempo, pero jamás como un tribunal automatizado que etiquete, sancione o decida el futuro académico de un estudiante.»",
                15.5,
                True,
                (255, 255, 255),
                14),
            (
                "Autores: Joel Aisama & Bautista Navarro   ·   Campus Virtual UCH (demo_panel.html + app.py)   ·   Repositorio: github.com/aisamajoel-tech/Sistema-Escolar-Fundamentos-",
                10.5,
                False,
                (253, 164, 175),
                0,
            ),
        ],
    )

    add_footer(
        s6,
        "SITA-IA · Presentación Ejecutiva en Formato PowerPoint (.pptx) de 6 Diapositivas",
        "¡Muchas gracias! Quedamos abiertos a preguntas de la cátedra.",
    )

    prs.save(str(PPTX_PATH))
    print(f"[OK] PowerPoint generado exitosamente en: {PPTX_PATH}")


if __name__ == "__main__":
    build_presentation()
