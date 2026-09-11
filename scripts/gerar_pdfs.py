"""Gera, para uma pasta de trabalho, as versões em PDF (com folha de rosto)
dos relatórios exigidos por AGENT.md: POST_MORTEM.md, CODE_REVIEW.md,
ANALISE_CRITICA.md e RELATORIO_TESTES.md.

A lista de integrantes é lida diretamente da tabela em AGENT.md (na raiz do
repositório), para que exista uma única fonte de verdade.

Uso:
    python scripts/gerar_pdfs.py classe_pilha_preenchimento
    python scripts/gerar_pdfs.py classe_pilha_preenchimento --titulo "Preenchimento de Região em Matriz de Caracteres"

Dependências (não fazem parte da solução dos exercícios, só desta ferramenta):
    pip install reportlab
"""

import argparse
import datetime
import html
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

RAIZ_DO_REPOSITORIO = Path(__file__).resolve().parent.parent
DISCIPLINA = "MAE014 - Tóp. Ciência Dados B [Turmas MAP e EMA]"
RELATORIOS_PADRAO = ["POST_MORTEM.md", "CODE_REVIEW.md", "ANALISE_CRITICA.md", "RELATORIO_TESTES.md"]

LINHA_TABELA_RE = re.compile(r"^\|(.+)\|\s*$")


def ler_integrantes(caminho_agent_md):
    """Extrai (nome, dre) da tabela de integrantes em AGENT.md."""
    texto = caminho_agent_md.read_text(encoding="utf-8")
    linhas = texto.splitlines()

    integrantes = []
    dentro_da_tabela = False
    for linha in linhas:
        combinacao = LINHA_TABELA_RE.match(linha.strip())
        if not combinacao:
            if dentro_da_tabela:
                break
            continue

        celulas = [c.strip() for c in combinacao.group(1).split("|")]
        if len(celulas) < 2:
            continue
        if celulas[0].lower().startswith("nome"):
            dentro_da_tabela = True
            continue
        if set(celulas[0]) <= {"-", ":"}:
            continue  # linha separadora do cabeçalho da tabela

        nome, dre = celulas[0], celulas[1]
        if not re.search(r"\d", dre):
            continue  # linha de placeholder ("adicionar novo integrante aqui")
        integrantes.append((nome, dre))

    return integrantes


def montar_folha_de_rosto(estilos, titulo_trabalho, integrantes):
    elementos = []
    elementos.append(Spacer(1, 4 * cm))
    elementos.append(Paragraph(DISCIPLINA, estilos["TituloCapa"]))
    elementos.append(Spacer(1, 1.5 * cm))
    elementos.append(Paragraph(titulo_trabalho, estilos["SubtituloCapa"]))
    elementos.append(Spacer(1, 2 * cm))

    dados_tabela = [["Nome completo", "DRE"]] + [[nome, dre] for nome, dre in integrantes]
    tabela = Table(dados_tabela, colWidths=[10 * cm, 4 * cm])
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2b2b2b")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elementos.append(tabela)
    elementos.append(Spacer(1, 2 * cm))
    data_de_hoje = datetime.date.today().strftime("%d/%m/%Y")
    elementos.append(Paragraph(f"Data: {data_de_hoje}", estilos["Rodape"]))
    elementos.append(PageBreak())
    return elementos


def _inline_para_reportlab(texto):
    """Escapa o texto e converte um subconjunto simples de markdown inline."""
    texto = html.escape(texto)
    texto = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", texto)
    texto = re.sub(r"`([^`]+?)`", r'<font face="Courier">\1</font>', texto)
    return texto


def _converter_tabela(linhas_tabela, estilos):
    linhas_celulas = []
    for linha in linhas_tabela:
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        linhas_celulas.append(celulas)

    if len(linhas_celulas) >= 2 and set("".join(linhas_celulas[1])) <= {"-", ":", " "}:
        linhas_celulas.pop(1)  # linha separadora do cabeçalho

    largura_pagina_util = 17 * cm
    n_colunas = max(len(linha) for linha in linhas_celulas)
    largura_coluna = largura_pagina_util / n_colunas

    dados = [
        [Paragraph(_inline_para_reportlab(celula), estilos["CelulaTabela"]) for celula in linha]
        for linha in linhas_celulas
    ]
    tabela = Table(dados, colWidths=[largura_coluna] * n_colunas, repeatRows=1)
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return tabela


def converter_markdown_para_flowables(texto_markdown, estilos):
    elementos = []
    linhas = texto_markdown.splitlines()

    buffer_lista = []
    estilo_lista_atual = None

    def esvaziar_lista():
        nonlocal buffer_lista, estilo_lista_atual
        if buffer_lista:
            elementos.append(
                ListFlowable(
                    [ListItem(Paragraph(_inline_para_reportlab(item), estilos["Corpo"])) for item in buffer_lista],
                    bulletType=estilo_lista_atual,
                    leftIndent=16,
                )
            )
            buffer_lista = []
            estilo_lista_atual = None

    indice = 0
    total = len(linhas)
    while indice < total:
        linha = linhas[indice]
        bruta = linha.rstrip()

        if bruta.startswith("```"):
            esvaziar_lista()
            indice += 1
            bloco = []
            while indice < total and not linhas[indice].startswith("```"):
                bloco.append(linhas[indice])
                indice += 1
            elementos.append(Preformatted("\n".join(bloco), estilos["Codigo"]))
            indice += 1
            continue

        if bruta.strip().startswith("|"):
            esvaziar_lista()
            bloco_tabela = []
            while indice < total and linhas[indice].strip().startswith("|"):
                bloco_tabela.append(linhas[indice])
                indice += 1
            elementos.append(_converter_tabela(bloco_tabela, estilos))
            elementos.append(Spacer(1, 0.3 * cm))
            continue

        if bruta.startswith("### "):
            esvaziar_lista()
            elementos.append(Paragraph(_inline_para_reportlab(bruta[4:]), estilos["Heading3"]))
            indice += 1
            continue
        if bruta.startswith("## "):
            esvaziar_lista()
            elementos.append(Paragraph(_inline_para_reportlab(bruta[3:]), estilos["Heading2"]))
            indice += 1
            continue
        if bruta.startswith("# "):
            esvaziar_lista()
            elementos.append(Paragraph(_inline_para_reportlab(bruta[2:]), estilos["Heading1"]))
            indice += 1
            continue

        if bruta.startswith("> "):
            esvaziar_lista()
            elementos.append(Paragraph(_inline_para_reportlab(bruta[2:]), estilos["Citacao"]))
            indice += 1
            continue

        combinacao_item_lista = re.match(r"^\s*[-*]\s+(.*)", bruta)
        if combinacao_item_lista:
            if estilo_lista_atual not in (None, "bullet"):
                esvaziar_lista()
            estilo_lista_atual = "bullet"
            buffer_lista.append(combinacao_item_lista.group(1))
            indice += 1
            continue

        combinacao_item_numerado = re.match(r"^\s*\d+\.\s+(.*)", bruta)
        if combinacao_item_numerado:
            if estilo_lista_atual not in (None, "1"):
                esvaziar_lista()
            estilo_lista_atual = "1"
            buffer_lista.append(combinacao_item_numerado.group(1))
            indice += 1
            continue

        esvaziar_lista()
        if bruta.strip() == "":
            elementos.append(Spacer(1, 0.15 * cm))
        else:
            elementos.append(Paragraph(_inline_para_reportlab(bruta), estilos["Corpo"]))
        indice += 1

    esvaziar_lista()
    return elementos


def montar_estilos():
    base = getSampleStyleSheet()
    estilos = {
        "TituloCapa": ParagraphStyle("TituloCapa", parent=base["Title"], fontSize=18, leading=22, alignment=1),
        "SubtituloCapa": ParagraphStyle("SubtituloCapa", parent=base["Title"], fontSize=14, leading=18, alignment=1),
        "Rodape": ParagraphStyle("Rodape", parent=base["Normal"], alignment=1, textColor=colors.grey),
        "Heading1": ParagraphStyle("Heading1", parent=base["Heading1"], spaceBefore=12, spaceAfter=8),
        "Heading2": ParagraphStyle("Heading2", parent=base["Heading2"], spaceBefore=10, spaceAfter=6),
        "Heading3": ParagraphStyle("Heading3", parent=base["Heading3"], spaceBefore=8, spaceAfter=4),
        "Corpo": ParagraphStyle("Corpo", parent=base["Normal"], spaceAfter=4, leading=14),
        "CelulaTabela": ParagraphStyle("CelulaTabela", parent=base["Normal"], fontSize=9, leading=11),
        "Citacao": ParagraphStyle(
            "Citacao", parent=base["Normal"], leftIndent=18, textColor=colors.HexColor("#444444"),
            fontName="Helvetica-Oblique", spaceAfter=6,
        ),
        "Codigo": ParagraphStyle(
            "Codigo", parent=base["Code"], fontName="Courier", fontSize=8, leading=10,
            backColor=colors.HexColor("#f4f4f4"),
        ),
    }
    return estilos


def gerar_pdf(caminho_md, caminho_pdf, titulo_trabalho, integrantes):
    estilos = montar_estilos()
    texto_markdown = caminho_md.read_text(encoding="utf-8")

    documento = SimpleDocTemplate(
        str(caminho_pdf), pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=2 * cm, rightMargin=2 * cm,
    )
    elementos = montar_folha_de_rosto(estilos, titulo_trabalho, integrantes)
    elementos += converter_markdown_para_flowables(texto_markdown, estilos)
    documento.build(elementos)


def main(argv=None):
    analisador = argparse.ArgumentParser(description=__doc__)
    analisador.add_argument("pasta_do_trabalho", help="Pasta do exercício (ex.: classe_pilha_preenchimento)")
    analisador.add_argument("--titulo", default=None, help="Título do trabalho exibido na folha de rosto")
    analisador.add_argument(
        "--relatorios", nargs="+", default=RELATORIOS_PADRAO,
        help="Arquivos .md a converter (padrão: os quatro relatórios exigidos por AGENT.md)",
    )
    argumentos = analisador.parse_args(argv)

    pasta = Path(argumentos.pasta_do_trabalho).resolve()
    if not pasta.is_dir():
        print(f"Pasta não encontrada: {pasta}", file=sys.stderr)
        return 1

    titulo_trabalho = argumentos.titulo or pasta.name.replace("_", " ").title()
    integrantes = ler_integrantes(RAIZ_DO_REPOSITORIO / "AGENT.md")
    if not integrantes:
        print("Aviso: nenhum integrante encontrado em AGENT.md.", file=sys.stderr)

    gerou_algum = False
    for nome_relatorio in argumentos.relatorios:
        caminho_md = pasta / nome_relatorio
        if not caminho_md.is_file():
            print(f"Aviso: {caminho_md} não existe, pulando.", file=sys.stderr)
            continue
        caminho_pdf = caminho_md.with_suffix(".pdf")
        gerar_pdf(caminho_md, caminho_pdf, titulo_trabalho, integrantes)
        print(f"Gerado: {caminho_pdf.relative_to(RAIZ_DO_REPOSITORIO)}")
        gerou_algum = True

    return 0 if gerou_algum else 1


if __name__ == "__main__":
    raise SystemExit(main())
