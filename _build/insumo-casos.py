# -*- coding: utf-8 -*-
"""Gerador dos insumos do desafio de análise por área.

Ele é primo do `insumo.py` e resolve um problema diferente. Lá o arquivo NASCE
de uma especificação, com sujeira declarada. Aqui o arquivo já existe como CSV,
e o que se faz é CONVERTER: para xlsx, com uma aba, cabeçalho congelado, número
como número e data como data.

🔴 A conversão é declarada, e não feita à mão, por uma razão contável: são seis
casos, e o que a página afirma sobre o arquivo tem de continuar verdade depois
de qualquer regeração. Conversão à mão não se repete igual.

🔴 O DE-PARA existe porque cinco dos seis CSV foram inventados para simular a
realidade de outra turma. A estrutura e os números servem; o contexto é que é de
outra sala. Só rótulo e valor de TEXTO mudam: nenhuma coluna numérica é tocada,
e a contagem de linhas do xlsx é idêntica à do CSV de origem.

Rodar:  python3 _build/insumo-casos.py
"""
import csv
import datetime
import os
import re

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DESTINO = os.path.join(RAIZ, "_arquivos")
CARTEIRA = os.path.dirname(os.path.dirname(os.path.dirname(RAIZ)))


# ---------------------------------------------------------------------------
# OS CASOS
#
# `origem`  · caminho do CSV, a partir da raiz da carteira de cursos
# `de_para` · trocas de texto, aplicadas a cabeçalho e a célula de texto.
#             Lista de pares, aplicada na ordem. Vazia quando o domínio do
#             arquivo já é o da turma.
# ---------------------------------------------------------------------------
CASOS = {
    "producao": dict(
        origem="2-treinamentos-in-company/collaborative-workshop/turma-5/"
               "factory_production_data_BIG.csv",
        # 🔴 O CSV de origem e de metal-mecanica: ele solda e pinta. Nove das
        # empresas da turma sao industria de alimentos, e laticinio nao solda.
        # As duas etapas trocam por nomes que servem aos tres setores da sala,
        # alimentos, confeccao e transformacao. Numero nenhum e tocado: o
        # achado continua sendo o mesmo cruzamento, com o rotulo novo.
        de_para=[(r"\bSoldagem\b", "Processamento"),
                 (r"\bPintura\b", "Acabamento")],
    ),
}


def _converte(valor):
    """Texto do CSV para o tipo que o Excel vai entender.

    A ordem importa: data antes de número, senão "2024-01-01" nunca chega a ser
    testado como data. E o teste de número é `fullmatch`, porque um código de
    produto como "12A" não é número e não pode virar um.
    """
    v = valor.strip()
    if not v:
        return None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
        return datetime.date(int(v[:4]), int(v[5:7]), int(v[8:10]))
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    return v


def _troca(texto, de_para):
    for de, para in de_para:
        texto = re.sub(de, para, texto, flags=re.IGNORECASE)
    return texto


def grava(slug, caso):
    origem = os.path.join(CARTEIRA, caso["origem"])
    with open(origem, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.reader(f))
    cabecalho, dados = linhas[0], linhas[1:]

    wb = Workbook()
    ws = wb.active
    ws.title = "Dados"

    cabecalho = [_troca(c, caso["de_para"]) for c in cabecalho]
    ws.append(cabecalho)
    for c in range(1, len(cabecalho) + 1):
        cel = ws.cell(row=1, column=c)
        cel.font = Font(bold=True, color="FFFFFF")
        cel.fill = PatternFill("solid", fgColor="164194")
        cel.alignment = Alignment(horizontal="center", vertical="center")

    for linha in dados:
        ws.append([_converte(_troca(v, caso["de_para"])) for v in linha])

    # 🔴 Congelar em A2 é o que faz o cabeçalho sobreviver à rolagem. Numa base
    # de cinco mil linhas, sem isso a pessoa perde o nome da coluna na primeira
    # rolada e passa o exercício conferindo qual coluna era qual.
    ws.freeze_panes = "A2"

    for c in range(1, len(cabecalho) + 1):
        letra = get_column_letter(c)
        # A largura sai do conteúdo, e a amostra é limitada: medir cinco mil
        # células para achar a mais larga custa mais do que vale.
        larguras = [len(str(ws.cell(row=r, column=c).value or ""))
                    for r in range(1, min(ws.max_row, 200) + 1)]
        ws.column_dimensions[letra].width = min(max(larguras) + 4, 24)
        if isinstance(ws.cell(row=2, column=c).value, datetime.date):
            for r in range(2, ws.max_row + 1):
                ws.cell(row=r, column=c).number_format = "DD/MM/YYYY"

    caminho = os.path.join(DESTINO, slug + ".xlsx")
    wb.save(caminho)
    return caminho, len(dados), len(cabecalho), cabecalho


def main():
    for slug, caso in CASOS.items():
        caminho, linhas, colunas, cabecalho = grava(slug, caso)
        print("{}: {} linhas x {} colunas".format(
            os.path.basename(caminho), linhas, colunas))
        print("   colunas: " + " | ".join(cabecalho))


if __name__ == "__main__":
    main()
