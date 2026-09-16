#!/usr/bin/env python3
"""Desenha o canvas do n8n de uma pratica, como ele fica DEPOIS de rodar verde.

Por que desenho e nao print: em 16/09 o print real nao saiu do Chrome por
nenhum dos caminhos tentados (o save_to_disk da extensao nao devolve caminho,
o fetch da pagina https para o loopback nao chega, e o html-to-image congela
a aba do n8n). O padrao do site ja manda "desenhe a ferramenta, nao printe".
Entao a figura da secao 05 e o canvas REDESENHADO a partir do que rodou no
servidor de teste: nomes dos nos, ordem, contagem de itens nas setas e o
check verde vem da execucao (id e data ficam na legenda da pagina). O que e
aproximacao: o icone de cada no, tracado a mao no estilo do n8n.

Uso:  python3 _build/canvas.py           (gera todos em _img/canvas/)
      python3 _build/canvas.py p2        (so um)

Cada pratica e uma entrada em PRATICAS: nos (nome, icone, x, y, sub, trigger)
e setas (de, para, rotulo). Coordenadas no espaco do n8n (no = 96 x 96).
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "_img" / "canvas"

NO = 96          # lado do no
VERDE = "#29a360"
CINZA = "#a8a8b0"
TEXTO = "#2f2f34"
SUB_COR = "#8a8a94"
FUNDO = "#f6f6f8"
PONTO = "#d9d9de"

# icones: viewBox 0 0 24 24, stroke 2, no estilo de linha do n8n atual
ICONES = {
    "manual": '<path d="M9 9l6.5 3.5-2.8 1 2.3 4-1.7 1-2.3-4L9 16.6z"/><path d="M6 4.5a7.5 7.5 0 0 1 10.6 1.9"/><path d="M4 8.5a10 10 0 0 1 3-4"/>',
    "set": '<rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M8 16l1-3.5 6-6a1.4 1.4 0 0 1 2 2l-6 6z"/>',
    "schedule": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3.5 2"/>',
    "gmail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6 8.5-6"/>',
    "sheets": '<rect x="4" y="3.5" width="16" height="17" rx="2"/><path d="M4 9h16M4 14.5h16M10 9v11.5"/>',
    "if": '<path d="M12 21V11"/><path d="M5 5h9l2.5 2.5L14 10H5z"/><path d="M19 13h-9l-2.5 2.5L10 18h9z"/>',
    "switch": '<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M6 8.5v2a4 4 0 0 0 4 4M18 8.5v2a4 4 0 0 1-4 4M12 15.5v0"/>',
    "merge": '<circle cx="6" cy="5" r="2.5"/><circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="12" r="2.5"/><path d="M8 6.5c4 0 5 5.5 7.5 5.5M8 17.5c4 0 5-5.5 7.5-5.5"/>',
    "filter": '<path d="M4 5h16l-6.5 7.5V19l-3 1.5v-8z"/>',
    "splitout": '<path d="M4 12h5"/><path d="M13 7l-4 5 4 5"/><path d="M13 7h7M13 12h7M13 17h7"/>',
    "aggregate": '<path d="M4 7h7M4 12h7M4 17h7"/><path d="M11 7l4 5-4 5"/><path d="M15 12h5"/>',
    "http": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c3 3 3 14 0 17M12 3.5c-3 3-3 14 0 17"/>',
    "webhook": '<path d="M9 16.5a3 3 0 1 1-3-3"/><path d="M12 5.5a3 3 0 0 1 2.6 4.5l-3.3 5.7"/><path d="M6 13.5l3.3-5.7"/><path d="M15 16.5h4.5a3 3 0 1 1-.4 1.5"/><path d="M10.5 16.5H15"/>',
    "form": '<rect x="5" y="3.5" width="14" height="17" rx="2"/><path d="M8.5 8.5h7M8.5 12h7M8.5 15.5h4"/>',
    "chat": '<path d="M4 5.5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H9l-4.5 3.5v-3.5H6a2 2 0 0 1-2-2z"/>',
    "agent": '<rect x="4" y="8" width="16" height="11" rx="2.5"/><path d="M12 4.5V8M9 13h.01M15 13h.01M9 16.5h6"/><circle cx="12" cy="4" r="1"/>',
    "modelo": '<path d="M12 3.5l1.8 4.7 4.7 1.8-4.7 1.8L12 16.5l-1.8-4.7L5.5 10l4.7-1.8z"/><path d="M18.5 15.5l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/>',
    "memoria": '<path d="M6 4.5h10a2 2 0 0 1 2 2v13H6z"/><path d="M6 4.5a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2"/><path d="M9.5 9h5M9.5 12.5h5"/>',
    "code": '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
    "wait": '<path d="M7 3.5h10M7 20.5h10M8 3.5c0 5 8 5 8 8.5s-8 3.5-8 8.5M16 3.5c0 5-8 5-8 8.5s8 3.5 8 8.5"/>',
    "telegram": '<path d="M20.5 4.5L3.5 11l5.5 2 2 5.5 3-3.5 4 3z"/><path d="M9 13l11.5-8.5"/>',
    "drive": '<path d="M9 4h6l6 10.5-3 5H6l-3-5z"/><path d="M9 4l3 5.5-6 10M15 4l-3 5.5h9M12 9.5h-6"/>',
    "docs": '<path d="M6 3.5h8l4 4v13H6z"/><path d="M14 3.5v4h4M9 12h6M9 15.5h6"/>',
    "extract": '<path d="M6 3.5h8l4 4v13H6z"/><path d="M14 3.5v4h4"/><path d="M9 11.5h6M9 15h4"/>',
    "resposta": '<path d="M4 12h12"/><path d="M12 8l4 4-4 4"/><path d="M19 5v14"/>',
    "calendar": '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M8 3.5v3M16 3.5v3"/>',
    "summarize": '<path d="M5 6h14M5 10h10M5 14h14M5 18h7"/>',
    "rss": '<circle cx="6" cy="18" r="1.5"/><path d="M4.5 10.5a9 9 0 0 1 9 9M4.5 4.5a15 15 0 0 1 15 15"/>',
    "sort": '<path d="M6 4v16M6 20l-3-3M6 20l3-3"/><path d="M12 6h9M12 11h7M12 16h5"/>',
    "sticky": '<path d="M5 4h14v10l-4 4H5z"/><path d="M15 18v-4h4"/>',
}


def _no(n, ok):
    x, y = n["x"], n["y"]
    cor = VERDE if ok else CINZA
    trig = n.get("trigger", False)
    if trig:
        # lado esquerdo arredondado, direito reto: a forma do gatilho no n8n
        forma = (f'<path d="M{x+NO/2} {y} H{x+NO-8} a8 8 0 0 1 8 8 V{y+NO-8} a8 8 0 0 1-8 8 '
                 f'H{x+NO/2} A{NO/2} {NO/2} 0 0 1 {x+NO/2} {y} Z" fill="#fff" stroke="{cor}" stroke-width="2"/>')
    else:
        forma = f'<rect x="{x}" y="{y}" width="{NO}" height="{NO}" rx="9" fill="#fff" stroke="{cor}" stroke-width="2"/>'
    ic = ICONES.get(n.get("icone", "set"), ICONES["set"])
    icone = (f'<g transform="translate({x+NO/2-24} {y+NO/2-24}) scale(2)" fill="none" stroke="{n.get("cor", "#3d3d3d")}" '
             f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ic}</g>')
    check = ''
    if ok:
        cx, cy = x + NO - 14, y + NO - 14
        check = (f'<circle cx="{cx}" cy="{cy}" r="8" fill="#fff"/>'
                 f'<path d="M{cx-4} {cy}l3 3 5-6" fill="none" stroke="{VERDE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    # alcas de entrada e saida; um no com varias saidas (IF, Switch) tem uma
    # alca por saida, com o rotulo dela ("true"/"false", as rotas do Switch)
    alcas = ''
    if not trig:
        alcas += f'<circle cx="{x}" cy="{y+NO/2}" r="4.5" fill="#fff" stroke="{CINZA}" stroke-width="1.5"/>'
    saidas = n.get("saidas") or [""]
    for i, nome_s in enumerate(saidas):
        sy = y + NO * (i + 1) / (len(saidas) + 1)
        alcas += f'<circle cx="{x+NO}" cy="{sy}" r="4.5" fill="#fff" stroke="{CINZA}" stroke-width="1.5"/>'
        if nome_s:
            alcas += f'<text x="{x+NO+9}" y="{sy+4}" font-size="11" fill="{SUB_COR}">{escape(nome_s)}</text>'
    nome = escape(n["nome"])
    rot = (f'<text x="{x+NO/2}" y="{y+NO+22}" text-anchor="middle" font-size="14" font-weight="600" fill="{TEXTO}">{nome}</text>')
    if n.get("sub"):
        rot += f'<text x="{x+NO/2}" y="{y+NO+40}" text-anchor="middle" font-size="12" fill="{SUB_COR}">{escape(n["sub"])}</text>'
    return forma + icone + check + alcas + rot


SUB = 64         # lado do sub-no (modelo, memoria, tool), pendurado embaixo do pai


def _subno(n, pai, ok):
    """O sub-no do n8n: quadrado menor, ligado por uma linha ao 'diamante' embaixo do pai."""
    cor = VERDE if ok else CINZA
    px, py = pai["x"] + NO / 2, pai["y"] + NO          # centro da base do pai
    x, y = n["x"], n["y"]
    linha = f'<path d="M{px} {py+6} V{y-4}" fill="none" stroke="{CINZA}" stroke-width="1.5" stroke-dasharray="4 3"/>'
    porta = f'<path d="M{px} {py} l5 5 -5 5 -5-5z" fill="#fff" stroke="{CINZA}" stroke-width="1.5"/>'
    forma = f'<rect x="{x}" y="{y}" width="{SUB}" height="{SUB}" rx="8" fill="#fff" stroke="{cor}" stroke-width="2"/>'
    ic = ICONES.get(n.get("icone", "modelo"), ICONES["modelo"])
    icone = (f'<g transform="translate({x+SUB/2-16} {y+SUB/2-16}) scale(1.33)" fill="none" stroke="{n.get("cor", "#3d3d3d")}" '
             f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ic}</g>')
    check = ''
    if ok:
        cx, cy = x + SUB - 11, y + SUB - 11
        check = (f'<circle cx="{cx}" cy="{cy}" r="7" fill="#fff"/>'
                 f'<path d="M{cx-3.5} {cy}l2.5 2.5 4.5-5" fill="none" stroke="{VERDE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    rot = f'<text x="{x+SUB/2}" y="{y+SUB+18}" text-anchor="middle" font-size="12" font-weight="600" fill="{TEXTO}">{escape(n["nome"])}</text>'
    if n.get("sub"):
        rot += f'<text x="{x+SUB/2}" y="{y+SUB+34}" text-anchor="middle" font-size="11" fill="{SUB_COR}">{escape(n["sub"])}</text>'
    return linha + porta + forma + icone + check + rot


def _seta(a, b, rotulo, ok, porta=0):
    """de a (saida direita, porta i) para b (entrada esquerda); curva se estiver em outra linha."""
    cor = VERDE if ok else CINZA
    saidas = a.get("saidas") or [""]
    x1, y1 = a["x"] + NO + 5, a["y"] + NO * (porta + 1) / (len(saidas) + 1)
    x2, y2 = b["x"] - 5, b["y"] + NO / 2
    if abs(y1 - y2) < 1:
        d = f"M{x1} {y1} H{x2 - 6}"
    else:
        mx = (x1 + x2) / 2
        d = f"M{x1} {y1} C{mx} {y1} {mx} {y2} {x2 - 6} {y2}"
    linha = f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="2"/>'
    ponta = f'<path d="M{x2-7} {y2-5} L{x2} {y2} L{x2-7} {y2+5} Z" fill="{cor}"/>'
    rot = ''
    if rotulo:
        tx, ty = (x1 + x2) / 2, (y1 + y2) / 2 - 10
        rot = f'<text x="{tx}" y="{ty}" text-anchor="middle" font-size="12" fill="{SUB_COR}">{escape(rotulo)}</text>'
    return linha + ponta + rot


def desenha(p):
    nos = {n["id"]: n for n in p["nos"]}
    ok = p.get("ok", True)
    xs = [n["x"] for n in p["nos"]]; ys = [n["y"] for n in p["nos"]]
    x0, y0 = min(xs) - 48, min(ys) - 40
    x1 = max(n["x"] + (SUB if n.get("sub_de") else NO) for n in p["nos"]) + 48
    y1 = max(n["y"] + (SUB if n.get("sub_de") else NO) for n in p["nos"]) + 64
    w, h = x1 - x0, y1 - y0
    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {w} {h}" width="{w}" height="{h}" '
        f'font-family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif">',
        f'<title>{escape(p["titulo"])}</title>',
        '<defs><pattern id="pts" width="20" height="20" patternUnits="userSpaceOnUse">'
        f'<circle cx="10" cy="10" r="1.2" fill="{PONTO}"/></pattern></defs>',
        f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{FUNDO}"/>',
        f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#pts)"/>',
    ]
    for s in p.get("setas", []):
        partes.append(_seta(nos[s["de"]], nos[s["para"]], s.get("rotulo", ""), s.get("ok", ok), s.get("porta", 0)))
    for n in p["nos"]:
        if n.get("sub_de"):
            partes.append(_subno(n, nos[n["sub_de"]], n.get("ok", ok)))
        else:
            partes.append(_no(n, n.get("ok", ok)))
    partes.append("</svg>")
    return "\n".join(partes)


# ---------------------------------------------------------------------------
# AS PRATICAS · uma entrada por figura. O que esta aqui e o que RODOU no
# servidor de teste (n8neditor.n8nrafael.cloud), execucao e data na pagina.
# ---------------------------------------------------------------------------
PRATICAS = {
    # B6 aula 4 · P2 · execucao 401 em 16/09/2026 12:17 (BRT), workflow F01yHGZJOaroUcXS
    "p2-base": dict(
        titulo="Meu Primeiro Fluxo: Disparo Manual e Meus Dados, os dois verdes",
        nos=[
            dict(id="t", nome="▶️ Disparo Manual", icone="manual", x=0, y=0, trigger=True),
            dict(id="s", nome="📦 Meus Dados", icone="set", x=240, y=0, sub="manual"),
        ],
        setas=[dict(de="t", para="s", rotulo="1 item")],
    ),
    "p2-variacoes": dict(
        titulo="Meu Primeiro Fluxo com as duas variações: um segundo Set encadeado",
        nos=[
            dict(id="t", nome="▶️ Disparo Manual", icone="manual", x=0, y=0, trigger=True),
            dict(id="s", nome="📦 Meus Dados", icone="set", x=240, y=0, sub="manual"),
            dict(id="s2", nome="🧹 Adiciona Saudação", icone="set", x=480, y=0, sub="manual"),
        ],
        setas=[dict(de="t", para="s", rotulo="1 item"), dict(de="s", para="s2", rotulo="1 item")],
    ),
    # B6 aula 2 · exemplo guiado · execucao 407 em 16/09/2026, workflow Gil0ED7CHMqRrQI0
    "anatomia-101": dict(
        titulo="Anatomia 101: Disparo Manual e Dados de Teste, os dois verdes",
        nos=[
            dict(id="t", nome="▶️ Disparo Manual", icone="manual", x=0, y=0, trigger=True),
            dict(id="s", nome="📦 Dados de Teste", icone="set", x=240, y=0, sub="manual"),
        ],
        setas=[dict(de="t", para="s", rotulo="1 item")],
    ),
    # B6 aula 5 · P3 · execucoes 410 a 414 em 16/09/2026, workflow wA1NKuTJIaKMrLcw
    "p3-agente": dict(
        titulo="Meu primeiro AI Agent: Chat Trigger, AI Agent e o sub-nó do modelo Gemini",
        nos=[
            dict(id="c", nome="💬 Chat Trigger", icone="chat", x=0, y=0, trigger=True),
            dict(id="a", nome="AI Agent", icone="agent", x=240, y=0, sub="Tools Agent"),
            dict(id="m", nome="Google Gemini Chat Model", icone="modelo", x=256, y=176, sub="gemini-3.5-flash", sub_de="a", cor="#1a73e8"),
        ],
        setas=[dict(de="c", para="a", rotulo="1 item")],
    ),
    # B7 aulas 1 a 4 · exemplos guiados · execucoes 415 a 418 em 16/09/2026
    "manual-hello": dict(
        titulo="Manual Hello: Disparo e Mensagem, os dois verdes",
        nos=[dict(id="t", nome="▶️ Disparo", icone="manual", x=0, y=0, trigger=True),
             dict(id="s", nome="📦 Mensagem", icone="set", x=240, y=0, sub="manual")],
        setas=[dict(de="t", para="s", rotulo="1 item")],
    ),
    "lembrete-semanal": dict(
        titulo="Lembrete Semanal Teste: Toda Seg 9h e Compor Mensagem, os dois verdes",
        nos=[dict(id="t", nome="📅 Toda Seg 9h", icone="schedule", x=0, y=0, trigger=True),
             dict(id="s", nome="📦 Compor Mensagem", icone="set", x=240, y=0, sub="manual")],
        setas=[dict(de="t", para="s", rotulo="1 item")],
    ),
    "webhook-hello": dict(
        titulo="Webhook Hello: o nó Webhook Receber, verde, depois da chamada de teste",
        nos=[dict(id="w", nome="📡 Webhook Receber", icone="webhook", x=0, y=0, trigger=True, sub="POST")],
        setas=[],
    ),
    "form-contato": dict(
        titulo="Form de Contato: o nó Form Contato, verde, depois do envio de teste",
        nos=[dict(id="f", nome="📝 Form Contato", icone="form", x=0, y=0, trigger=True, sub="3 campos")],
        setas=[],
    ),
    # B8 aula 1 · exemplo guiado · execucoes 419 (true) e 420 (erro de tipo), workflow 0AJ3fd84SoLto1xy
    "tipos-de-teste": dict(
        titulo="Tipos de Teste: o IF com idade_correta manda o item pro ramo true; o ramo false fica vazio",
        nos=[
            dict(id="t", nome="▶️ Disparo", icone="manual", x=0, y=120, trigger=True),
            dict(id="s", nome="📦 Tipos de Teste", icone="set", x=240, y=120, sub="manual"),
            dict(id="i", nome="IF idade_correta > 18", icone="if", x=480, y=120, saidas=["true", "false"]),
            dict(id="v", nome="Ramo true", icone="set", x=768, y=0, sub="manual"),
            dict(id="f", nome="Ramo false", icone="set", x=768, y=240, sub="manual", ok=False),
        ],
        setas=[dict(de="t", para="s", rotulo="1 item"), dict(de="s", para="i", rotulo="1 item"),
               dict(de="i", para="v", rotulo="1 item", porta=0), dict(de="i", para="f", rotulo="", porta=1, ok=False)],
    ),
    # B8 aulas 2 a 8 · exemplos guiados · execucoes 433 a 445 em 16/09/2026
    "tres-pessoas": dict(
        titulo="3 Pessoas: o Set em modo JSON, o Split Out abrindo a lista e a Saudação rodando 3 vezes",
        nos=[dict(id="t", nome="▶️ Disparo", icone="manual", x=0, y=0, trigger=True),
             dict(id="s", nome="📦 3 Pessoas", icone="set", x=240, y=0, sub="JSON"),
             dict(id="o", nome="🍕 Separar em 3 Itens", icone="splitout", x=480, y=0, sub="pessoas"),
             dict(id="u", nome="📤 Saudação", icone="set", x=720, y=0, sub="manual")],
        setas=[dict(de="t", para="s", rotulo="1 item"), dict(de="s", para="o", rotulo="1 item"), dict(de="o", para="u", rotulo="3 items")],
    ),
    "lead-limpo": dict(
        titulo="Set + Pinning: Lead Bruto e Lead Limpo",
        nos=[dict(id="t", nome="▶️ Disparo", icone="manual", x=0, y=0, trigger=True),
             dict(id="b", nome="📦 Lead Bruto", icone="set", x=240, y=0, sub="JSON"),
             dict(id="l", nome="🧹 Lead Limpo", icone="set", x=480, y=0, sub="manual")],
        setas=[dict(de="t", para="b", rotulo="1 item"), dict(de="b", para="l", rotulo="1 item")],
    ),
    "expressions": dict(
        titulo="Expressions: Dados de Teste, Leitura com Expression e a leitura direta do primeiro Set",
        nos=[dict(id="t", nome="▶️ Disparo Manual", icone="manual", x=0, y=0, trigger=True),
             dict(id="d", nome="📦 Dados de Teste", icone="set", x=240, y=0, sub="manual"),
             dict(id="l", nome="📤 Leitura com Expression", icone="set", x=480, y=0, sub="manual"),
             dict(id="x", nome="📤 Direto do primeiro Set", icone="set", x=720, y=0, sub="manual")],
        setas=[dict(de="t", para="d", rotulo="1 item"), dict(de="d", para="l", rotulo="1 item"), dict(de="l", para="x", rotulo="1 item")],
    ),
    "if-leads": dict(
        titulo="Qualificação de leads: dois leads, o IF Score maior ou igual a 70 e as duas portas com 1 item cada",
        nos=[dict(id="t", nome="▶️ Disparo", icone="manual", x=0, y=120, trigger=True),
             dict(id="s", nome="📦 2 Leads", icone="set", x=240, y=120, sub="JSON"),
             dict(id="o", nome="🍕 Separar", icone="splitout", x=480, y=120, sub="leads"),
             dict(id="i", nome="❓ Score >= 70?", icone="if", x=720, y=120, saidas=["true", "false"]),
             dict(id="a", nome="📧 Enviar SDR", icone="set", x=1000, y=0, sub="manual"),
             dict(id="b", nome="📋 Nutrir depois", icone="set", x=1000, y=240, sub="manual")],
        setas=[dict(de="t", para="s", rotulo="1 item"), dict(de="s", para="o", rotulo="1 item"), dict(de="o", para="i", rotulo="2 items"),
               dict(de="i", para="a", rotulo="1 item", porta=0), dict(de="i", para="b", rotulo="1 item", porta=1)],
    ),
    "switch-tickets": dict(
        titulo="Roteamento de tickets: cinco tickets, o Switch com quatro regras e o Fallback, cinco destinos",
        nos=[dict(id="t", nome="▶️ Disparo", icone="manual", x=0, y=240, trigger=True),
             dict(id="s", nome="📦 5 Tickets", icone="set", x=240, y=240, sub="JSON"),
             dict(id="o", nome="🍕 Separar", icone="splitout", x=480, y=240, sub="tickets"),
             dict(id="w", nome="🔀 Roteia por categoria", icone="switch", x=720, y=240, saidas=["tecnico", "financeiro", "duvida", "outro", "Fallback"]),
             dict(id="d1", nome="💬 Slack #suporte", icone="set", x=1048, y=0, sub="manual"),
             dict(id="d2", nome="📧 Email pra contas", icone="set", x=1048, y=130, sub="manual"),
             dict(id="d3", nome="📄 Auto-resposta FAQ", icone="set", x=1048, y=260, sub="manual"),
             dict(id="d4", nome="📋 Sheets registro manual", icone="set", x=1048, y=390, sub="manual"),
             dict(id="d5", nome="⚠️ Sheets erros não tratados", icone="set", x=1048, y=520, sub="manual")],
        setas=[dict(de="t", para="s", rotulo="1 item"), dict(de="s", para="o", rotulo="1 item"), dict(de="o", para="w", rotulo="5 items"),
               dict(de="w", para="d1", rotulo="1 item", porta=0), dict(de="w", para="d2", rotulo="1 item", porta=1), dict(de="w", para="d3", rotulo="1 item", porta=2),
               dict(de="w", para="d4", rotulo="1 item", porta=3), dict(de="w", para="d5", rotulo="1 item", porta=4)],
    ),
    "merge-teste": dict(
        titulo="Merge depois do IF, em Append: o item do ramo true passa e o Registrar roda",
        nos=[dict(id="t", nome="▶️ Disparo", icone="manual", x=0, y=120, trigger=True),
             dict(id="l", nome="📦 Lead", icone="set", x=240, y=120, sub="manual"),
             dict(id="i", nome="❓ Score >= 8?", icone="if", x=480, y=120, saidas=["true", "false"]),
             dict(id="q", nome="🔥 Mensagem Quente", icone="set", x=760, y=0, sub="manual"),
             dict(id="f", nome="❄️ Mensagem Fria", icone="set", x=760, y=240, sub="manual", ok=False),
             dict(id="m", nome="🧩 Merge (Append)", icone="merge", x=1040, y=120, sub="append"),
             dict(id="r", nome="📋 Registrar no Sheets", icone="set", x=1280, y=120, sub="manual")],
        setas=[dict(de="t", para="l", rotulo="1 item"), dict(de="l", para="i", rotulo="1 item"),
               dict(de="i", para="q", rotulo="1 item", porta=0), dict(de="i", para="f", rotulo="", porta=1, ok=False),
               dict(de="q", para="m", rotulo="1 item"), dict(de="f", para="m", rotulo="", ok=False), dict(de="m", para="r", rotulo="1 item")],
    ),
    "split-aggregate": dict(
        titulo="Split Out e Aggregate: 1 item vira 3 e volta a ser 1",
        nos=[dict(id="t", nome="▶️ Disparo", icone="manual", x=0, y=0, trigger=True),
             dict(id="s", nome="📦 1 Item com Tags", icone="set", x=240, y=0, sub="JSON"),
             dict(id="o", nome="🔪 Explode Tags", icone="splitout", x=480, y=0, sub="tags"),
             dict(id="a", nome="🛍️ Junta de Volta", icone="aggregate", x=720, y=0, sub="tags")],
        setas=[dict(de="t", para="s", rotulo="1 item"), dict(de="s", para="o", rotulo="1 item"), dict(de="o", para="a", rotulo="3 items")],
    ),
    # B8 aula 9 · P5 · execucao 446 em 16/09/2026, workflow rOqLkp37HNncxOQr (a V1 do Rafael), 800 linhas
    "p5-vendas": dict(
        titulo="Resumo Semanal de Vendas: os oito nós da V1, todos verdes, de 800 linhas a 1 e-mail",
        nos=[dict(id="t", nome="▶️ Disparo", icone="manual", x=0, y=0, trigger=True),
             dict(id="s", nome="📋 Lê Pedidos", icone="sheets", x=240, y=0, sub="get rows", cor="#188038"),
             dict(id="l", nome="🧹 Limpa Tipos", icone="set", x=480, y=0, sub="manual"),
             dict(id="r", nome="📊 Resumo por Categoria", icone="summarize", x=720, y=0, sub="sum · count"),
             dict(id="o", nome="⬇️ Ordena Maior pro Menor", icone="sort", x=960, y=0, sub="descending"),
             dict(id="e", nome="🛍️ Empacota", icone="aggregate", x=1200, y=0, sub="linhas"),
             dict(id="m", nome="📝 Monta Texto", icone="set", x=1440, y=0, sub="manual"),
             dict(id="g", nome="📧 Envia Resumo", icone="gmail", x=1680, y=0, sub="send: message", cor="#c5221f")],
        setas=[dict(de="t", para="s", rotulo="1 item"), dict(de="s", para="l", rotulo="800 items"), dict(de="l", para="r", rotulo="800 items"),
               dict(de="r", para="o", rotulo="5 items"), dict(de="o", para="e", rotulo="5 items"), dict(de="e", para="m", rotulo="1 item"), dict(de="m", para="g", rotulo="1 item")],
    ),
    # B7 aula 6 · P4 · execucao 403 em 16/09/2026 12:45 (BRT), workflow OWd0Hs8O4c8iCQwm
    "p4-lembrete": dict(
        titulo="Lembrete Diário Foco: Schedule, Set e Gmail, os três verdes, e o e-mail enviado",
        nos=[
            dict(id="t", nome="📅 Toda Manhã 8h", icone="schedule", x=0, y=0, trigger=True),
            dict(id="s", nome="📦 Compor Mensagem", icone="set", x=240, y=0, sub="manual"),
            dict(id="g", nome="📧 Enviar Lembrete", icone="gmail", x=480, y=0, sub="send: message", cor="#c5221f"),
        ],
        setas=[dict(de="t", para="s", rotulo="1 item"), dict(de="s", para="g", rotulo="1 item")],
    ),
    # B9 aulas 1, 2 e 5 · exemplos guiados · execucoes 447 a 450 em 16/09/2026
    "doc-open-meteo": dict(
        titulo="Leitura de Doc: Disparo e Lê a Doc (Open-Meteo), os dois verdes",
        nos=[dict(id="t", nome="▶️ Disparo", icone="manual", x=0, y=0, trigger=True),
             dict(id="h", nome="🌤 Lê a Doc (Open-Meteo)", icone="http", x=240, y=0, sub="GET")],
        setas=[dict(de="t", para="h", rotulo="1 item")],
    ),
    "dog-ceo": dict(
        titulo="Dog CEO: Disparo e Busca Foto, os dois verdes",
        nos=[dict(id="t", nome="▶️ Disparo", icone="manual", x=0, y=0, trigger=True),
             dict(id="h", nome="🐶 Busca Foto", icone="http", x=240, y=0, sub="GET")],
        setas=[dict(de="t", para="h", rotulo="1 item")],
    ),
    "post-json": dict(
        titulo="POST com body JSON: Disparo e Cria Post, os dois verdes",
        nos=[dict(id="t", nome="▶️ Disparo", icone="manual", x=0, y=0, trigger=True),
             dict(id="h", nome="📮 Cria Post", icone="http", x=240, y=0, sub="POST")],
        setas=[dict(de="t", para="h", rotulo="1 item")],
    ),
    "mini-api": dict(
        titulo="Mini-API Saudacao: Recebe Pedido, Monta Saudacao e Devolve Resposta, os três verdes",
        nos=[dict(id="w", nome="🎣 Recebe Pedido", icone="webhook", x=0, y=0, trigger=True, sub="POST"),
             dict(id="s", nome="📝 Monta Saudacao", icone="set", x=240, y=0, sub="manual"),
             dict(id="r", nome="📤 Devolve Resposta", icone="resposta", x=480, y=0, sub="JSON")],
        setas=[dict(de="w", para="s", rotulo="1 item"), dict(de="s", para="r", rotulo="1 item")],
    ),
    # B9 aula 6 · P6 · execucao 451 em 16/09/2026 16:29 (BRT), workflow LALGt9XApgAbWJwR
    "p6-tempo": dict(
        titulo="Previsão do Tempo: Toda Manhã 7h, Busca Clima, Monta Texto e Envia Pra Você, os quatro verdes",
        nos=[
            dict(id="t", nome="⏰ Toda Manhã 7h", icone="schedule", x=0, y=0, trigger=True),
            dict(id="h", nome="🌤 Busca Clima", icone="http", x=240, y=0, sub="GET"),
            dict(id="s", nome="📝 Monta Texto", icone="set", x=480, y=0, sub="manual"),
            dict(id="g", nome="📧 Envia Pra Você", icone="gmail", x=720, y=0, sub="send: message", cor="#c5221f"),
        ],
        setas=[dict(de="t", para="h", rotulo="1 item"), dict(de="h", para="s", rotulo="1 item"), dict(de="s", para="g", rotulo="1 item")],
    ),
}


def main():
    DESTINO.mkdir(parents=True, exist_ok=True)
    quais = [a for a in sys.argv[1:] if not a.startswith("-")] or list(PRATICAS)
    for k in quais:
        svg = desenha(PRATICAS[k])
        (DESTINO / f"{k}.svg").write_text(svg, encoding="utf-8")
        print(f"{k}.svg  {len(svg)} bytes")


if __name__ == "__main__":
    main()
