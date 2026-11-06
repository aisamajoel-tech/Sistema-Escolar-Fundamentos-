import os
import shutil
import subprocess
from reportlab.pdfgen import canvas

BASE_DIR = r"c:\Users\aisam\OneDrive\Escritorio\3AÑO-FACULTAD\FUNDAMENTOS DE IA\TRABAJO GRUPAL"
VIEWS_DIR = os.path.join(BASE_DIR, "views")
SHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
TEMP_DIR = r"C:\Users\aisam\AppData\Local\Temp\sita_canva_deck"
PDF_PATH = os.path.join(BASE_DIR, "Presentacion_Parcial_FIA_SITA.pdf")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs( os.path.join(TEMP_DIR, "screenshots"), exist_ok=True )

# Copy presentacion_canva.html, logo_uch.png, and screenshots to ASCII temp dir
deck_src = os.path.join(VIEWS_DIR, "presentacion_canva.html")
deck_tmp = os.path.join(TEMP_DIR, "presentacion_canva.html")
shutil.copy2(deck_src, deck_tmp)
shutil.copy2(deck_src, os.path.join(BASE_DIR, "presentacion_canva.html"))

logo_src = os.path.join(VIEWS_DIR, "logo_uch.png")
if os.path.exists(logo_src):
    shutil.copy2(logo_src, os.path.join(TEMP_DIR, "logo_uch.png"))

for fname in os.listdir(SHOTS_DIR):
    if fname.endswith(".png"):
        shutil.copy2(os.path.join(SHOTS_DIR, fname), os.path.join(TEMP_DIR, "screenshots", fname))

edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
edge_exe = next((p for p in edge_paths if os.path.exists(p)), None)

slide_imgs = []
if edge_exe:
    for i in range(1, 7):
        out_png = os.path.join(TEMP_DIR, f"canva_slide_{i}.png")
        url = f"file:///{deck_tmp.replace(os.sep, '/')}?slide={i}"
        cmd = [
            edge_exe,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--window-size=1280,720",
            "--force-device-scale-factor=2",
            f"--screenshot={out_png}",
            url,
        ]
        subprocess.run(cmd, check=False)
        if os.path.exists(out_png):
            slide_imgs.append(out_png)
            shutil.copy2(out_png, os.path.join(SHOTS_DIR, f"canva_slide_{i}.png"))

# Create 16:9 widescreen PDF (960 x 540 pt) with full-bleed Canva slides
PAGE_W, PAGE_H = 960, 540
c = canvas.Canvas(PDF_PATH, pagesize=(PAGE_W, PAGE_H))
for img_path in slide_imgs:
    c.drawImage(img_path, 0, 0, width=PAGE_W, height=PAGE_H)
    c.showPage()
c.save()
print(f"Presentacion_Parcial_FIA_SITA.pdf generada exitosamente con {len(slide_imgs)} diapositivas estilo Canva (16:9).")
