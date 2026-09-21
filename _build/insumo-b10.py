#!/usr/bin/env python3
"""Gera os dois insumos do B10 (M5 do curso de n8n), em _arquivos/.

Os dois nascem dos prompts geradores do vault do curso (D13 do PROMPT-marco2
v2): "Prompt para gerar planilha de contatos de teste" (m5-ai-agents/09) e
"Prompt para gerar os PDFs de teste" (m5-ai-agents/10). O export do Notion nao
os trouxe; a pagina mostra o prompt e entrega o resultado. Rodado uma vez em
21/09/2026. Tudo ficticio: nome, empresa, e-mail, projeto. Nenhum dado real
de pessoa, aluno ou cliente.

  contatos-de-teste.csv   15 contatos, 2 "Pedro" de sobrenome diferente, 1 nome
                          composto raro, 6 projetos (P9, Agente E-mail)
  atas-de-teste.zip       ata-reuniao-01.pdf a 05.pdf, 1 pagina A4, Helvetica
                          11 (o "Arial 11pt" do prompt), com as 5 variacoes que
                          o prompt pede (P10, Triador de Documentos)

Uso:  python3 _build/insumo-b10.py
"""
import csv
import io
import zipfile
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas as pdfcanvas

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "_arquivos"

# ---------------------------------------------------------------------------
# 1 · a planilha de contatos (P9)
# ---------------------------------------------------------------------------
CONTATOS = [
    # nome, email, empresa, projeto, notas
    ("Pedro Albuquerque", "pedro.albuquerque@exemplo-alvorada.com.br", "Alvorada Distribuidora", "Implantação do CRM", "Pediu proposta revisada na última call; aguarda retorno até sexta"),
    ("Pedro Sales", "pedro.sales@exemplo-serraverde.com.br", "Grupo Serra Verde", "Expansão da filial Norte", "Reunião de kickoff marcada; quer o cronograma por e-mail"),
    ("Maria Aparecida Coutinho", "maria.coutinho@exemplo-litoral.com.br", "Litoral Engenharia", "Auditoria interna 2026", "Prefere contato por e-mail, nunca por telefone"),
    ("Ana Beatriz Farias", "ana.farias@exemplo-pontocerto.com.br", "Ponto Certo Varejo", "Implantação do CRM", "Aprovou o escopo; falta assinatura do contrato"),
    ("Carlos Henrique Duarte", "carlos.duarte@exemplo-mirante.com.br", "Mirante Consultoria", "Lançamento do produto Q4", "Enviou o briefing; quer feedback em 48h"),
    ("Juliana Prado", "juliana.prado@exemplo-valefertil.com.br", "Vale Fértil Agro", "Implantação ERP, Fase 2", "Go-live adiado pra junho; ela conduz o plano revisado"),
    ("Rodrigo Menezes", "rodrigo.menezes@exemplo-nordestelog.com.br", "Nordeste Logística", "Expansão da filial Norte", "Responsável pelo orçamento de frota"),
    ("Fernanda Lopes", "fernanda.lopes@exemplo-casaazul.com.br", "Casa Azul Clínica", "Auditoria interna 2026", "Pediu a lista de documentos da auditoria"),
    ("Thiago Nascimento", "thiago.nascimento@exemplo-horizonte.com.br", "Horizonte Educação", "Lançamento do produto Q4", "Quer a apresentação em PDF antes da reunião"),
    ("Camila Rocha", "camila.rocha@exemplo-brisa.com.br", "Brisa Tecnologia", "Integração de sistemas", "Última interação: teste de API aprovado"),
    ("Marcos Vinícius Teles", "marcos.teles@exemplo-alvorada.com.br", "Alvorada Distribuidora", "Integração de sistemas", "Dono da homologação; responde rápido no fim do dia"),
    ("Patrícia Amaral", "patricia.amaral@exemplo-serraverde.com.br", "Grupo Serra Verde", "Implantação ERP, Fase 2", "Fornecedora do módulo fiscal; reunião quinzenal"),
    ("Lucas Ferreira", "lucas.ferreira@exemplo-pontocerto.com.br", "Ponto Certo Varejo", "Implantação do CRM", "Novo no projeto; precisa do histórico"),
    ("Renata Guimarães", "renata.guimaraes@exemplo-mirante.com.br", "Mirante Consultoria", "Auditoria interna 2026", "Confirmou presença na reunião de quinta às 15h"),
    ("Gustavo Pires", "gustavo.pires@exemplo-horizonte.com.br", "Horizonte Educação", "Expansão da filial Norte", "Pediu prazo de entrega do laudo"),
]


def gera_csv():
    destino = DESTINO / "contatos-de-teste.csv"
    with open(destino, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["nome", "email", "empresa", "projeto", "notas"])
        w.writerows(CONTATOS)
    pedros = sum(1 for c in CONTATOS if c[0].startswith("Pedro "))
    projetos = len({c[3] for c in CONTATOS})
    assert len(CONTATOS) == 15 and pedros == 2 and 5 <= projetos <= 6, (len(CONTATOS), pedros, projetos)
    print(f"{destino.name}: {len(CONTATOS)} linhas, {pedros} Pedros, {projetos} projetos")


# ---------------------------------------------------------------------------
# 2 · as cinco atas (P10)
# ---------------------------------------------------------------------------
ATAS = [
    # (data, projeto, participantes, pauta, decisoes, proximos_passos, redator, nota_de_variacao)
    dict(  # PDF 1: curta e enxuta (3 participantes, 2 decisoes)
        data="15 de março de 2026",
        projeto="Implantação ERP, Fase 2",
        participantes=["Juliana Prado (Gerente de Projetos)", "Rodrigo Menezes (Diretor de TI)", "Patrícia Amaral (Fornecedora, módulo fiscal)"],
        pauta=["Status do go-live", "Plano revisado"],
        decisoes=["Prorrogar o go-live para junho de 2026 (responsável: Juliana Prado, prazo: 22/03/2026)",
                  "Congelar novas customizações até o go-live (responsável: Rodrigo Menezes, prazo: imediato)"],
        proximos=["Juliana Prado envia o plano revisado até 22/03/2026", "Patrícia Amaral entrega o cronograma do módulo fiscal até 29/03/2026"],
        redator="Juliana Prado, Gerente de Projetos",
    ),
    dict(  # PDF 2: longa (5 participantes, 4 decisoes, pauta detalhada)
        data="2 de abril de 2026",
        projeto="Implantação do CRM",
        participantes=["Ana Beatriz Farias (Diretora Comercial)", "Lucas Ferreira (Analista de Processos)", "Pedro Albuquerque (Gerente de Contas)", "Camila Rocha (Líder Técnica)", "Marcos Vinícius Teles (Coordenador de Homologação)"],
        pauta=["Escopo aprovado e o que ficou de fora", "Migração da base de clientes", "Integração com o sistema de faturamento", "Treinamento da equipe comercial"],
        decisoes=["Migrar apenas clientes ativos nos últimos 24 meses (responsável: Lucas Ferreira, prazo: 30/04/2026)",
                  "Integração com o faturamento entra na segunda onda (responsável: Camila Rocha, prazo: 15/06/2026)",
                  "Treinamento em duas turmas de 10 pessoas (responsável: Ana Beatriz Farias, prazo: 20/05/2026)",
                  "Homologação semanal às sextas, 14h (responsável: Marcos Vinícius Teles, prazo: a partir de 10/04/2026)"],
        proximos=["Lucas Ferreira mapeia os campos da base atual até 15/04/2026", "Camila Rocha apresenta o desenho da integração até 30/04/2026", "Pedro Albuquerque valida a lista de clientes ativos até 20/04/2026"],
        redator="Lucas Ferreira, Analista de Processos",
    ),
    dict(  # PDF 3: 1 decisao pendente, sem responsavel definido
        data="18 de abril de 2026",
        projeto="Auditoria interna 2026",
        participantes=["Maria Aparecida Coutinho (Controller)", "Fernanda Lopes (Gerente Administrativa)", "Renata Guimarães (Consultora)"],
        pauta=["Lista de documentos", "Calendário das visitas", "Ferramenta de coleta de evidências"],
        decisoes=["Visitas às unidades entre 5 e 16 de maio (responsável: Fernanda Lopes, prazo: 02/05/2026)",
                  "Evidências coletadas na pasta compartilhada, uma subpasta por unidade (responsável: Renata Guimarães, prazo: 25/04/2026)",
                  "Contratação de ferramenta de coleta: decisão pendente, sem responsável definido"],
        proximos=["Maria Aparecida Coutinho consolida a lista de documentos até 25/04/2026", "Definir responsável pela ferramenta na próxima reunião"],
        redator="Renata Guimarães, Consultora",
    ),
    dict(  # PDF 4: data em outro formato
        data="20/03/2026",
        projeto="Lançamento do produto Q4",
        participantes=["Carlos Henrique Duarte (Gerente de Produto)", "Thiago Nascimento (Marketing)", "Gustavo Pires (Operações)", "Camila Rocha (Líder Técnica)"],
        pauta=["Data de lançamento", "Plano de comunicação", "Capacidade de produção"],
        decisoes=["Lançamento em 14/10/2026 (responsável: Carlos Henrique Duarte, prazo: confirmado)",
                  "Campanha começa quatro semanas antes do lançamento (responsável: Thiago Nascimento, prazo: 16/09/2026)",
                  "Estoque inicial de 5.000 unidades (responsável: Gustavo Pires, prazo: 30/09/2026)"],
        proximos=["Thiago Nascimento apresenta o plano de comunicação até 30/04/2026", "Gustavo Pires confirma a capacidade da linha até 15/05/2026"],
        redator="Carlos Henrique Duarte, Gerente de Produto",
    ),
    dict(  # PDF 5: participante remoto e empresa parceira citada
        data="7 de maio de 2026",
        projeto="Expansão da filial Norte",
        participantes=["Pedro Sales (Diretor Regional)", "Rodrigo Menezes (Diretor de TI)", "Gustavo Pires (Operações)", "Renata Guimarães (Consultora, remoto)"],
        pauta=["Imóvel escolhido", "Parceria logística", "Cronograma de abertura"],
        decisoes=["Assinar o contrato do imóvel da avenida principal (responsável: Pedro Sales, prazo: 20/05/2026)",
                  "Operação logística com a parceira Nordeste Logística nos primeiros seis meses (responsável: Gustavo Pires, prazo: 30/05/2026)",
                  "Abertura em 1º de agosto de 2026 (responsável: Pedro Sales, prazo: confirmado)"],
        proximos=["Rodrigo Menezes orça a infraestrutura de rede até 25/05/2026", "Renata Guimarães envia a minuta do contrato com a parceira até 15/05/2026"],
        redator="Gustavo Pires, Operações",
    ),
]

FONTE = "Helvetica"
FONTE_N = "Helvetica-Bold"
TAM = 11


def _pdf(ata):
    buf = io.BytesIO()
    c = pdfcanvas.Canvas(buf, pagesize=A4)
    w, h = A4
    x, y = 2.5 * cm, h - 2.5 * cm
    lh = TAM * 1.45

    def linha(txt, negrito=False, recuo=0):
        nonlocal y
        c.setFont(FONTE_N if negrito else FONTE, TAM)
        c.drawString(x + recuo, y, txt)
        y -= lh

    def pula(n=0.6):
        nonlocal y
        y -= lh * n

    c.setFont(FONTE_N, 16)
    c.drawString(x, y, "Ata de Reunião")
    y -= 16 * 1.6
    linha(f"Data da reunião: {ata['data']}")
    linha(f"Projeto / Iniciativa: {ata['projeto']}")
    pula()
    linha("Participantes", negrito=True)
    for p in ata["participantes"]:
        linha(f"• {p}", recuo=10)
    pula()
    linha("Pauta", negrito=True)
    for p in ata["pauta"]:
        linha(f"• {p}", recuo=10)
    pula()
    linha("Decisões tomadas", negrito=True)
    for d in ata["decisoes"]:
        # quebra simples em duas linhas quando passa da margem
        partes = _quebra(d, 88)
        linha(f"• {partes[0]}", recuo=10)
        for resto in partes[1:]:
            linha(resto, recuo=22)
    pula()
    linha("Próximos passos", negrito=True)
    for p in ata["proximos"]:
        partes = _quebra(p, 88)
        linha(f"• {partes[0]}", recuo=10)
        for resto in partes[1:]:
            linha(resto, recuo=22)
    pula(1.2)
    linha(f"Redator: {ata['redator']}")
    pula(1.5)
    c.setFont(FONTE, 8)
    c.drawString(x, 1.8 * cm, "Documento fictício, gerado para exercício de curso. Nomes, empresas e projetos são inventados.")
    c.showPage()
    c.save()
    return buf.getvalue()


def _quebra(txt, largura):
    palavras, linhas, atual = txt.split(), [], ""
    for p in palavras:
        if len(atual) + len(p) + 1 > largura and atual:
            linhas.append(atual)
            atual = p
        else:
            atual = (atual + " " + p).strip()
    if atual:
        linhas.append(atual)
    return linhas


def gera_pdfs():
    destino = DESTINO / "atas-de-teste.zip"
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for i, ata in enumerate(ATAS, 1):
            z.writestr(f"ata-reuniao-{i:02d}.pdf", _pdf(ata))
    assert len(ATAS) == 5
    print(f"{destino.name}: 5 PDFs, {destino.stat().st_size // 1024} KB")


if __name__ == "__main__":
    DESTINO.mkdir(exist_ok=True)
    gera_csv()
    gera_pdfs()
