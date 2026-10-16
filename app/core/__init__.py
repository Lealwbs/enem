"""
Módulo Core do Gerador de Provas e Corretor OMR.
"""

from .exam_generator import gerar_prova_pdf
from .answer_sheet_generator import gerar_cartao_resposta_pdf
from .essay_sheet_generator import gerar_folha_redacao_pdf
from .unified_sheet_generator import gerar_folha_unificada_pdf
from .omr_engine import processar_cartao
from .grader import corrigir_pasta_cartoes

__all__ = [
    "gerar_prova_pdf",
    "gerar_cartao_resposta_pdf",
    "gerar_folha_redacao_pdf",
    "gerar_folha_unificada_pdf",
    "processar_cartao",
    "corrigir_pasta_cartoes",
]
