"""
================================================================================
Coletivo • Sistema Integrado de Criação de Provas Estilo ENEM e Correção OMR
CLI Unificada para Geração de Provas, Cartões-Resposta, Redação e Correção
================================================================================
"""

import os
import sys
import argparse

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Garante que a raiz do projeto esteja no PYTHONPATH
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.core.exam_generator import gerar_prova_pdf
from app.core.answer_sheet_generator import gerar_cartao_resposta_pdf
from app.core.essay_sheet_generator import gerar_folha_redacao_pdf
from app.core.grader import corrigir_pasta_cartoes


def cmd_gerar_prova(args):
    """Gera o Caderno de Prova Completo em PDF."""
    print("\n[PROVA] Iniciando geração do Caderno de Prova estilo ENEM...")
    gerar_prova_pdf(caminho_questoes=args.questoes, caminho_saida=args.saida)
    print(f"[PROVA] Sucesso! Caderno salvo em: '{args.saida}'\n")


def cmd_gerar_cartao(args):
    """Gera o Cartão-Resposta OMR de 70 questões em PDF."""
    print("\n[CARTÃO] Iniciando geração do Cartão-Resposta OMR (70 Questões)...")
    gerar_cartao_resposta_pdf(caminho_saida=args.saida)
    print(f"[CARTÃO] Sucesso! Cartão salvo em: '{args.saida}'\n")


def cmd_gerar_redacao(args):
    """Gera a Folha Oficial de Redação em PDF."""
    print("\n[REDAÇÃO] Iniciando geração da Folha de Redação Oficial...")
    gerar_folha_redacao_pdf(caminho_saida=args.saida)
    print(f"[REDAÇÃO] Sucesso! Folha salva em: '{args.saida}'\n")


def cmd_gerar_unificada(args):
    """Gera a folha unificada Frente e Verso (Cartão-Resposta + Redação)."""
    from app.core.unified_sheet_generator import gerar_folha_unificada_pdf
    print("\n[UNIFICADA] Gerando Folha Frente e Verso (Cartão-Resposta + Redação)...")
    gerar_folha_unificada_pdf(caminho_saida=args.saida)
    print(f"[UNIFICADA] Sucesso! Folha salva em: '{args.saida}'\n")


def cmd_gerar_tudo(args):
    """Gera o kit completo para aplicação do exame."""
    print("\n" + "=" * 60)
    print("GERANDO KIT COMPLETO DO EXAME (PROVA + FOLHA FRENTE/VERSO)")
    print("=" * 60)

    pasta_saida = args.pasta_saida
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_prova = os.path.join(pasta_saida, "Caderno_Questoes_70Q.pdf")
    caminho_unificada = os.path.join(pasta_saida, "Cartao_Resposta_e_Redacao_Frente_Verso.pdf")

    gerar_prova_pdf(caminho_questoes=args.questoes, caminho_saida=caminho_prova)

    try:
        from app.core.unified_sheet_generator import gerar_folha_unificada_pdf
        gerar_folha_unificada_pdf(caminho_saida=caminho_unificada)
    except ImportError:
        caminho_cartao = os.path.join(pasta_saida, "Cartao_Resposta_70Q.pdf")
        caminho_redacao = os.path.join(pasta_saida, "Folha_Redacao_Oficial.pdf")
        gerar_cartao_resposta_pdf(caminho_saida=caminho_cartao)
        gerar_folha_redacao_pdf(caminho_saida=caminho_redacao)

    print("\n" + "=" * 60)
    print("[SUCESSO] ARQUIVOS GERADOS COM EXCELÊNCIA!")
    print(f"1. Caderno de Prova: {caminho_prova}")
    print(f"2. Folha Unificada:  {caminho_unificada}")
    print("=" * 60 + "\n")


def cmd_corrigir(args):
    """Executa a leitura OMR e correção automática dos cartões."""
    corrigir_pasta_cartoes(
        pasta_cartoes=args.pasta_cartoes,
        caminho_questoes=args.questoes,
        caminho_saida=args.saida
    )


def main():
    parser = argparse.ArgumentParser(
        description="Coletivo • Gerador de Provas estilo ENEM e Corretor OMR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python -m app.cli gerar-tudo                  Gera a Prova e Folha Frente e Verso
  python -m app.cli gerar-prova                 Gera apenas o Caderno de Prova
  python -m app.cli gerar-cartao                Gera apenas o Cartão-Resposta OMR
  python -m app.cli gerar-redacao               Gera apenas a Folha Oficial de Redação
  python -m app.cli gerar-unificada             Gera Folha Frente e Verso
  python -m app.cli corrigir                    Corrige cartões da pasta configurada
        """
    )

    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponíveis")

    # Comando: gerar-prova
    p_prova = subparsers.add_parser("gerar-prova", help="Gera o Caderno de Questões completo em PDF")
    p_prova.add_argument("--questoes", default="simulado_2/banco_questoes/questoes.json", help="Caminho do JSON com as questões")
    p_prova.add_argument("--saida", default="simulado_2/resultado/Caderno_Questoes_70Q.pdf", help="Caminho do PDF de saída")
    p_prova.set_defaults(func=cmd_gerar_prova)

    # Comando: gerar-cartao
    p_cartao = subparsers.add_parser("gerar-cartao", help="Gera o Cartão-Resposta OMR (70Q) em PDF")
    p_cartao.add_argument("--saida", default="simulado_2/resultado/Cartao_Resposta_70Q.pdf", help="Caminho do PDF de saída")
    p_cartao.set_defaults(func=cmd_gerar_cartao)

    # Comando: gerar-redacao
    p_redacao = subparsers.add_parser("gerar-redacao", help="Gera a Folha Oficial de Redação em PDF")
    p_redacao.add_argument("--saida", default="simulado_2/resultado/Folha_Redacao_Oficial.pdf", help="Caminho do PDF de saída")
    p_redacao.set_defaults(func=cmd_gerar_redacao)

    # Comando: gerar-unificada
    p_unif = subparsers.add_parser("gerar-unificada", help="Gera a Folha Frente e Verso (Cartão + Redação)")
    p_unif.add_argument("--saida", default="simulado_2/resultado/Cartao_Resposta_e_Redacao_Frente_Verso.pdf", help="Caminho do PDF de saída")
    p_unif.set_defaults(func=cmd_gerar_unificada)

    # Comando: gerar-tudo
    p_tudo = subparsers.add_parser("gerar-tudo", help="Gera Prova e Folha Unificada de uma só vez")
    p_tudo.add_argument("--simulado", type=int, choices=[1, 2], default=2, help="Seleciona o simulado (1 ou 2)")
    p_tudo.add_argument("--questoes", default="simulado_2/banco_questoes/questoes.json", help="Caminho do JSON com as questões")
    p_tudo.add_argument("--pasta-saida", default="simulado_2/resultado", help="Pasta para salvar os PDFs")
    p_tudo.set_defaults(func=cmd_gerar_tudo)

    # Comando: corrigir
    p_corrigir = subparsers.add_parser("corrigir", help="Lê e corrige cartões-resposta usando visão computacional")
    p_corrigir.add_argument("--simulado", type=int, choices=[1, 2], default=None, help="Seleciona o simulado específico (1 ou 2)")
    p_corrigir.add_argument("--pasta-cartoes", default="simulado_2/cartoes", help="Pasta com as fotos/scans dos cartões")
    p_corrigir.add_argument("--questoes", default="simulado_2/banco_questoes/questoes.json", help="Caminho do JSON com as questões e gabarito")
    p_corrigir.add_argument("--saida", default="simulado_2/resultado/resultado_correcao.xlsx", help="Caminho da planilha de resultados")
    p_corrigir.set_defaults(func=cmd_corrigir)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if hasattr(args, "simulado") and args.simulado is not None:
        if args.comando == "corrigir":
            if args.simulado == 1:
                args.pasta_cartoes = "simulado_1/cartoes_digitalizados"
                args.saida = "simulado_1/resultado_correcao.xlsx"
            elif args.simulado == 2:
                args.pasta_cartoes = "simulado_2/cartoes"
                args.questoes = "simulado_2/banco_questoes/questoes.json"
                args.saida = "simulado_2/resultado/resultado_correcao.xlsx"
        elif args.comando in ("gerar-tudo", "gerar-prova"):
            if args.simulado == 2:
                args.questoes = "simulado_2/banco_questoes/questoes.json"
                if hasattr(args, "pasta_saida"):
                    args.pasta_saida = "simulado_2/resultado"

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
