"""
Gera diagramas cientificos tecnicos em alto contraste (Preto e Branco / Escala de Cinza)
usando Pillow (PIL) para as questoes do Simulado 2.
"""

import os
from PIL import Image, ImageDraw, ImageFont

IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "banco_questoes", "imagens")
os.makedirs(IMG_DIR, exist_ok=True)


def get_font(size, bold=False):
    # Tenta carregar Arial ou fonte padrao do Windows
    font_paths = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()


def gerar_diagrama_venn_q52():
    """Gera o Diagrama de Venn para a Questão 52 (Conjuntos e Interseção)."""
    w, h = 600, 320
    im = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(im)

    # Retângulo Universo
    draw.rectangle([20, 20, w - 20, h - 20], outline="black", width=2, fill="#FAFAFA")
    f_title = get_font(16, bold=True)
    f_lbl = get_font(18, bold=True)
    f_sub = get_font(13)
    f_num = get_font(20, bold=True)

    draw.text((35, 30), "U (Universo = 1 000)", fill="black", font=f_title)

    # Círculos
    # Círculo A (Livros): center (220, 170), r = 100
    # Círculo B (Videoaulas): center (380, 170), r = 100
    draw.ellipse([120, 70, 320, 270], outline="black", width=2, fill="#FFFFFF")
    draw.ellipse([280, 70, 480, 270], outline="black", width=2, fill=None)

    # Rótulos
    draw.text((150, 40), "L (Livros Digitais)", fill="black", font=f_lbl)
    draw.text((330, 40), "V (Videoaulas)", fill="black", font=f_lbl)

    # Valores numéricos
    draw.text((180, 155), "410", fill="black", font=f_num)
    draw.text((285, 155), "210", fill="black", font=f_num)
    draw.text((390, 155), "240", fill="black", font=f_num)
    draw.text((510, 250), "?", fill="#555555", font=f_num)

    p = os.path.join(IMG_DIR, "q52_diagrama_venn.png")
    im.save(p)
    print(f"Salvo: {p}")


def gerar_diagrama_eletrostatica_q45():
    """Gera o esquema de carga pontual e ponto P para a Questão 45 (Física)."""
    w, h = 600, 200
    im = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(im)

    f_bold = get_font(18, bold=True)
    f_norm = get_font(14)
    f_sub = get_font(12)

    # Carga Q
    draw.ellipse([60, 70, 120, 130], outline="black", width=2, fill="#E8E8E8")
    draw.text((78, 88), "+Q", fill="black", font=f_bold)
    draw.text((50, 140), "Carga Fixa", fill="#333333", font=f_sub)

    # Linha tracejada de distância d
    for x in range(125, 420, 12):
        draw.line([x, 100, x + 6, 100], fill="#444444", width=2)
    draw.text((250, 75), "distância d", fill="black", font=f_norm)

    # Ponto P
    draw.ellipse([420, 94, 432, 106], fill="black", outline="black")
    draw.text((410, 68), "Ponto P (q₀)", fill="black", font=f_bold)
    draw.text((400, 115), "Carga de prova", fill="#333333", font=f_sub)

    # Vetor campo elétrico E
    draw.line([435, 100, 540, 100], fill="black", width=3)
    draw.polygon([(540, 94), (555, 100), (540, 106)], fill="black")
    draw.text((562, 90), "E", fill="black", font=f_bold)

    p = os.path.join(IMG_DIR, "q45_campo_eletrico.png")
    im.save(p)
    print(f"Salvo: {p}")


def gerar_diagrama_catraca_q50():
    """Gera o esquema do acoplamento coaxial catraca-roda para a Questão 50 (Física)."""
    w, h = 500, 360
    im = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(im)

    f_bold = get_font(15, bold=True)
    f_norm = get_font(13)
    f_sub = get_font(11)

    cx, cy = 250, 170

    # Roda traseira (raio 140)
    draw.ellipse([cx - 140, cy - 140, cx + 140, cy + 140], outline="black", width=3)

    # Catraca coaxial (raio 45)
    draw.ellipse([cx - 45, cy - 45, cx + 45, cy + 45], outline="black", width=2, fill="#E0E0E0")

    # Eixo central
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill="black")

    # Raios
    draw.line([cx, cy, cx + 140, cy], fill="black", width=2)
    draw.text((cx + 40, cy - 20), "R = 35 cm", fill="black", font=f_bold)

    draw.line([cx, cy, cx, cy - 45], fill="black", width=2)
    draw.text((cx - 75, cy - 35), "r = 5 cm", fill="black", font=f_bold)

    # Seta de rotação
    draw.arc([cx - 75, cy - 75, cx + 75, cy + 75], start=210, end=330, fill="black", width=2)
    draw.polygon([(cx - 12, cy - 75), (cx - 2, cy - 65), (cx - 2, cy - 85)], fill="black")
    draw.text((cx - 40, cy + 60), "ω = 60 rad/s", fill="black", font=f_bold)

    draw.text((45, 325), "Acoplamento coaxial: mesma velocidade angular (ω)", fill="#222222", font=f_sub)

    p = os.path.join(IMG_DIR, "q50_bicicleta_catraca.png")
    im.save(p)
    print(f"Salvo: {p}")


if __name__ == "__main__":
    gerar_diagrama_venn_q52()
    gerar_diagrama_eletrostatica_q45()
    gerar_diagrama_catraca_q50()
    print("Diagramas Pillow gerados com sucesso!")
