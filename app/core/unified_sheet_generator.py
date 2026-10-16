"""
Gerador de Folha Unificada de Respostas (Frente e Verso) em PDF:
- Página 1 (Frente): Cartão-Resposta OMR de 70 questões com marcadores de alta precisão.
- Página 2 (Verso): Folha Oficial de Redação com 30 linhas pautadas e instruções oficiais.
Pronto para impressão em folha única frente e verso (duplex).
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Importações dos renderizadores das duas páginas
try:
    from app.core.answer_sheet_generator import render_answer_sheet_on_canvas
    from app.core.essay_sheet_generator import render_essay_sheet_on_canvas
except ImportError:
    from core.answer_sheet_generator import render_answer_sheet_on_canvas
    from core.essay_sheet_generator import render_essay_sheet_on_canvas


def gerar_folha_unificada_pdf(
    caminho_saida="simulado_2/resultado/Cartao_Resposta_e_Redacao_Frente_Verso.pdf",
    gabarito_oficial=None
):
    """
    Gera um PDF de exatamente 2 páginas:
    Página 1: Cartão-Resposta 70Q
    Página 2: Folha de Redação
    """
    os.makedirs(os.path.dirname(os.path.abspath(caminho_saida)), exist_ok=True)
    c = canvas.Canvas(caminho_saida, pagesize=A4)

    is_gabarito = (gabarito_oficial is not None and len(gabarito_oficial) > 0)

    # --- PÁGINA 1: CARTÃO-RESPOSTA ---
    geometry = render_answer_sheet_on_canvas(c, is_gabarito=is_gabarito, gabarito_oficial=gabarito_oficial)
    c.showPage()

    # --- PÁGINA 2: FOLHA DE REDAÇÃO ---
    render_essay_sheet_on_canvas(c, is_model=is_gabarito)
    c.showPage()

    c.save()
    tipo = "GABARITO OFICIAL FRENTE E VERSO" if is_gabarito else "CARTÃO E REDAÇÃO FRENTE E VERSO"
    print(f"[OK] {tipo} gerado em: {caminho_saida}")
    return geometry


if __name__ == "__main__":
    gerar_folha_unificada_pdf()
