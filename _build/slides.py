#!/usr/bin/env python3
"""Copia para _img/slides/ os slides da turma 2 que as paginas do Modulo 2 usam.

A fonte e a unica fonte de figura do curso de n8n (PROMPT-marco2 v2, secao 0):
../curso-agente-n8n/turma-2-abr-26/slides-notebookLM/jpg/mX-NN.jpg, 1600 x 851,
ja sem a faixa dos carimbos. Em alguns slides sobrou um resto cinza-claro do
"Estruturado por @iacomrafael" na ultima linha; CORTE diz ate que altura o
slide vai quando isso acontece, e so quando embaixo nao ha conteudo.

Uso:  python3 _build/slides.py            (copia o que USADOS lista)
      python3 _build/slides.py --lista    (so imprime a lista)

A lista USADOS e o registro: slide -> pagina. Quem escreve uma aula nova
acrescenta a linha aqui antes de usar o <img>.
"""
import sys
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ.parent.parent / "curso-agente-n8n" / "turma-2-abr-26" / "slides-notebookLM" / "jpg"
DESTINO = RAIZ / "_img" / "slides"

# slide -> paginas que o usam (uma figura pode servir a mais de uma pagina)
USADOS = {
    "m0-02": ["b5-antes"],
    "m0-03": ["b5-pensar"],
    "m0-04": ["b5-pensar"],
    "m0-05": ["b5-pensar"],
    "m0-06": ["b5-pensar"],
    "m0-07": ["b5-gatilho"],
    "m0-08": ["b5-gatilho"],
    "m0-09": ["b5-gatilho"],
    "m0-10": ["b5-gatilho"],
    "m0-11": ["b5-gatilho"],
    "m0-12": ["b5-gatilho"],
    "m0-13": ["b5-gatilho"],
    "m0-14": ["b5-mapear"],
    "m0-15": ["b5-mapear"],
    "m1-09": ["b6-primeiro"],
    "m1-10": ["b6-primeiro"],
    "m1-02": ["b6-oque"],
    "m1-03": ["b6-oque"],
    "m1-04": ["b6-oque"],
    "m1-05": ["b6-anatomia"],
    "m1-06": ["b6-anatomia"],
    "m1-07": ["b6-canvas"],
    "m1-08": ["b6-canvas"],
    "m1-11": ["b6-primeiro"],
    "m1-12": ["b6-agente"],
    "m1-13": ["b6-agente"],
    "m2-03": ["b7-manual"],
    "m2-04": ["b7-manual"],
    "m2-05": ["b7-manual"],
    "m2-06": ["b7-schedule"],
    "m2-07": ["b7-schedule"],
    "m2-08": ["b7-webhook"],
    "m2-09": ["b7-webhook"],
    "m2-10": ["b7-form"],
    "m2-11": ["b7-appevent"],
    "m2-12": ["b7-gatilhos"],
    "m3-03": ["b8-json"],
    "m3-04": ["b8-json"],
    "m3-05": ["b8-dados"],
    "m3-06": ["b8-dados"],
    "m3-07": ["b8-set"],
    "m3-08": ["b8-expressions"],
    "m3-09": ["b8-if"],
    "m3-10": ["b8-switch"],
    "m3-12": ["b8-listas"],
    "m3-13": ["b8-vendas"],
    "m3-14": ["b8-execucao"],
    "m2-13": ["b7-lembrete"],
    "m2-14": ["b7-lembrete"],
    "m2-15": ["b7-lembrete"],
}

# slide -> altura final (px). Ausente = 851, inteiro.
CORTE = {
    "m0-04": 836, "m0-05": 836, "m0-06": 836, "m0-07": 836,
    "m0-15": 828,
    "m2-03": 836, "m2-05": 836, "m2-09": 836, "m2-10": 836,
    "m2-12": 836,
    "m3-04": 836, "m3-07": 842, "m3-08": 824, "m3-14": 834,
}

# slide -> retangulos (x0, y0, x1, y1) pintados com a cor do fundo, amostrada
# em AMOSTRA. E para o carimbo "por @iacomrafael" que no deck do M1 ficou na
# MESMA linha de um texto de conteudo (x 85-288, y 828-850): cortar a linha
# levaria o texto junto. Nao e retoque de conteudo: e o carimbo que a
# exportacao devia ter tirado e nao tirou.
TAPA = {
    "m1-03": [(70, 820, 300, 851)],
    "m1-04": [(70, 820, 300, 851)],
    "m1-05": [(70, 820, 300, 851)],
    "m1-06": [(70, 820, 300, 851)],
    "m1-07": [(70, 820, 300, 851)],
    "m1-08": [(70, 820, 300, 851)],
    "m1-09": [(70, 820, 300, 851)],
    "m1-10": [(70, 820, 300, 851)],
    "m3-12": [(55, 826, 280, 851)],
}
AMOSTRA = (40, 840)

QUALIDADE = 82


def copiar(nome):
    origem = FONTE / f"{nome}.jpg"
    destino = DESTINO / f"{nome}.jpg"
    im = Image.open(origem)
    w, h = im.size
    alt = CORTE.get(nome, h)
    if alt < h:
        im = im.crop((0, 0, w, alt))
    if nome in TAPA:
        cor = im.getpixel(AMOSTRA)
        for x0, y0, x1, y1 in TAPA[nome]:
            im.paste(cor, (x0, y0, min(x1, w), min(y1, alt)))
    im.save(destino, "JPEG", quality=QUALIDADE, optimize=True)
    return im.size, destino.stat().st_size


def main():
    if "--lista" in sys.argv:
        for s, pags in USADOS.items():
            print(f"{s}  ->  {', '.join(pags)}")
        return
    DESTINO.mkdir(parents=True, exist_ok=True)
    total = 0
    for nome in USADOS:
        (w, h), kb = copiar(nome)
        total += kb
        print(f"{nome}.jpg  {w}x{h}  {kb // 1024} KB")
    print(f"{len(USADOS)} slides, {total // 1024} KB")


if __name__ == "__main__":
    main()
