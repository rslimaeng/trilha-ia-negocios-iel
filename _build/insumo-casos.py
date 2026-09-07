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
import json
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
# O DE-PARA COMUM
#
# 🔴 Cinco dos seis CSV foram inventados para simular a realidade de OUTRA
# turma: um instituto de educacao medica. A estrutura e os numeros servem; o
# contexto e que e de outra sala. A turma desta trilha e industria.
#
# 🔴 E ha uma segunda razao, que o prompt nao previu e que a leitura dos
# arquivos revelou: eles carregam NOME DE PESSOA e a sigla do cliente. Sete
# nomes na coluna Consultor do comercial, o primeiro nome de uma pessoa real
# em 18 comentarios de evento, e a sigla do cliente em 556 celulas. A regra 5 do pedido do Rafael e explicita:
# nome de pessoa, empresa ou cliente nao entra em lugar nenhum. O de-para
# abaixo tira os tres, e a trava no fim do arquivo impede que voltem.
# ---------------------------------------------------------------------------

# As seis linhas de produto substituem os seis codigos de curso. Codigo de
# familia de SKU e o que industria usa, e nao lembra nada de sala de aula.
LINHAS = [(r"\bSHHE\b", "LP-100"), (r"\bNEXAL\b", "LP-200"),
          (r"\bHTI\b", "LP-300"), (r"\bPOS\b", "LP-400"),
          (r"\bR2\b", "LP-500"), (r"\bEAD\b", "LP-600")]

# As doze especialidades medicas viram doze segmentos de cliente industrial.
SEGMENTOS = [(r"\bMedicina do Trabalho\b", "Rede nacional"),
             (r"\bMedicina Integrativa\b", "Food service"),
             (r"\bClinica Geral\b|\bClínica Geral\b", "Varejo regional"),
             (r"\bCardiologia\b", "Supermercado"),
             (r"\bDermatologia\b", "Padaria e confeitaria"),
             (r"\bEndocrinologia\b", "Restaurante"),
             (r"\bGeriatria\b", "Hotelaria"),
             (r"\bGinecologia\b", "Distribuidor"),
             (r"\bNeurologia\b", "Atacado"),
             (r"\bNutrologia\b", "Conveniencia"),
             (r"\bOrtopedia\b", "Industria"),
             (r"\bPediatria\b", "Exportacao"),
             (r"\bPsiquiatria\b", "Loja propria")]

# O lote substitui a turma na identificacao: T3/26 vira L3/26.
LOTES = [(r"\bT([1-5])/26\b", r"L\1/26")]

# As tres modalidades de ensino viram os tres canais de venda.
CANAIS = [(r"\bPresencial\b", "Distribuidor"), (r"\bOnline\b", "Direto"),
          (r"\bHíbrido\b", "Varejo")]


def lit(*pares):
    """Trocas literais: escapa o lado esquerdo para o ponto e o parenteses de
    uma frase inteira nao virarem sintaxe de expressao regular."""
    return [(re.escape(a), b) for a, b in pares]


# ---------------------------------------------------------------------------
# 🔴 OS CAMINHOS DE ORIGEM NAO MORAM AQUI, e a razao e o G50.
#
# Este repositorio e PUBLICO. Os seis CSV de origem sao material interno de
# outros dois treinamentos, e o caminho deles carrega nome de cliente e nome de
# pessoa em nome de pasta. Nome de cliente nao entra em arquivo do template, e
# comentario tambem viaja: o gate confere o codigo-fonte, nao so a tela.
#
# Entao o codigo fica aqui e o nome fica fora: `origens.local.json`, que o
# .gitignore segura, traduz IC-A e IC-B em caminho de verdade. A decodificacao
# esta no PROVENIENCIA-INTERNA.md da pasta do curso, que vive no repositorio
# local, sem remoto.
#
# Consequencia aceita: quem clonar este repositorio NAO consegue regerar os
# xlsx, so usa os que estao em `_arquivos/`. E o certo. O insumo publicado e
# anonimo; a materia-prima nao e, e nao deve viajar junto.
# ---------------------------------------------------------------------------
ORIGENS = os.path.join(AQUI, "origens.local.json")


def _local():
    """O arquivo que traduz codigo em nome. Sem ele nao da para REGERAR."""
    if not os.path.exists(ORIGENS):
        raise SystemExit(
            "🔴 Falta o {}.\n"
            "   Ele mora so na maquina do Rafael, e e o que traduz IC-A e IC-B\n"
            "   em caminho de verdade. Sem ele nao da para REGERAR os insumos,\n"
            "   e os que ja estao em _arquivos/ continuam validos."
            .format(os.path.basename(ORIGENS)))
    with open(ORIGENS, encoding="utf-8") as f:
        return json.load(f)


def _caminho(origem):
    """Traduz IC-A e IC-B/arquivo.csv no caminho real."""
    codigo, _, resto = origem.partition("/")
    return os.path.join(CARTEIRA, _local()["caminhos"][codigo] + resto)


def _nomes():
    """As trocas dos nomes de pessoa, literais, vindas do arquivo local."""
    return lit(*_local()["nomes_de_pessoa"].items())


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
        origem="IC-A",
        # 🔴 O CSV de origem e de metal-mecanica: ele solda e pinta. Nove das
        # empresas da turma sao industria de alimentos, e laticinio nao solda.
        # As duas etapas trocam por nomes que servem aos tres setores da sala,
        # alimentos, confeccao e transformacao. Numero nenhum e tocado: o
        # achado continua sendo o mesmo cruzamento, com o rotulo novo.
        de_para=[(r"\bSoldagem\b", "Processamento"),
                 (r"\bPintura\b", "Acabamento")],
    ),

    # O funil de matriculas de um instituto vira o funil de pedidos de uma
    # industria. 🔴 A coluna Consultor trazia SETE NOMES DE PESSOA.
    "comercial": dict(
        origem="IC-B/A2_Comercial_Funil_Matriculas.csv",
        de_para=(
            # os cabecalhos primeiro, senao uma troca de valor os alcanca
            lit(("Curso", "Linha_Produto"),
                ("Especialidade_Medico", "Segmento_Cliente"),
                ("Consultor", "Vendedor"),
                ("Turma_Interesse", "Lote_Interesse"))
            # 🔴 os sete nomes de pessoa saem, e nao viram pseudonimo. Eles
            # moram no origens.local.json pela mesma razao dos caminhos: a
            # regra que apaga um nome precisa escrever o nome, e este
            # repositorio e publico.
            + _nomes()
            + lit(("Parceiro Clínica", "Parceiro Distribuidor"),
                  ("Congresso", "Feira"),
                  ("Matriculado", "Fechado"),
                  ("Adiou para próxima turma", "Adiou para o próximo lote"),
                  ("Perfil não alinhado com o curso", "Perfil não alinhado com a linha"))
            + SEGMENTOS + LINHAS + LOTES),
    ),

    # O congresso medico vira a feira do setor. 🔴 Este arquivo trazia a sigla
    # do cliente em 556 celulas e o PRIMEIRO NOME de uma pessoa real em 18
    # comentarios.
    "marketing": dict(
        origem="IC-B/A2_Eventos_Feedback_Congresso.csv",
        de_para=(
            lit(("Edicao_Congresso", "Edicao_Feira"),
                ("Especialidade", "Segmento_Cliente"),
                ("Primeiro_Congresso", "Primeira_Visita"),
                ("Nota_Conteudo_Cientifico", "Nota_Conteudo_Tecnico"))
            + lit(("11° Congresso Internacional LS", "11ª Feira Internacional do Setor"),
                  ("Equipe interna LS", "Equipe interna"),
                  ("Médico palestrante", "Palestrante"),
                  ("Médico participante", "Visitante"),
                  ("Médico residente", "Visitante de primeira viagem"),
                  ("Congresso anterior", "Feira anterior"),
                  ("Site LS", "Site da feira"),
                  ("Parceiro clínica", "Parceiro distribuidor"))
            # 🔴 os comentarios que carregavam nome de pessoa, o nome do
            # cliente ou o vocabulario de congresso medico
            # 🔴 As duas primeiras trocas sao EXPRESSAO REGULAR, e nao literal,
            # justamente para o lado esquerdo nao precisar escrever o nome que
            # se quer tirar. O G50 acusou este arquivo quando a frase original
            # estava aqui por extenso: o de-para carregava o nome do cliente
            # dentro da propria regra que existe para elimina-lo.
            + [(r"O Dr\. \w+ é um inspirador nato\. Presença obrigatória\.",
                "A palestra de abertura é inspiradora. Presença obrigatória."),
               (r"O melhor congresso de \w+ do Brasil, sem dúvida\. Estarei no próximo\.",
                "A melhor feira do setor no Brasil, sem dúvida. Estarei na próxima.")]
            + lit(("Conteúdo atualizado e imediatamente aplicável na prática clínica.",
                   "Conteúdo atualizado e imediatamente aplicável na operação."),
                  ("Palestrantes de altíssimo nível. Conteúdo científico denso e aplicável.",
                   "Palestrantes de altíssimo nível. Conteúdo técnico denso e aplicável."),
                  ("Já indiquei para 5 colegas. Vale muito o investimento.",
                   "Já indiquei para 5 parceiros. Vale muito o investimento."),
                  ("Networking incrível. Já tenho novos parceiros de consultório.",
                   "Networking incrível. Já tenho novos parceiros comerciais."))
            + SEGMENTOS),
    ),

    # O NPS de turmas vira o NPS de lotes entregues.
    "operacoes": dict(
        origem="IC-B/A2_Operacoes_NPS_Turmas.csv",
        de_para=(
            lit(("Nota_Plataforma_EAD", "Nota_Entrega"),
                ("Nota_Professor", "Nota_Atendimento"),
                ("Nota_Conteudo", "Nota_Produto"),
                ("Mes_Realizacao", "Mes_Entrega"),
                ("Perfil_Aluno", "Perfil_Cliente"),
                ("Modalidade", "Canal"),
                ("Curso", "Linha_Produto"),
                ("Turma", "Lote"))
            + lit(("Médico recém-formado", "Comprador novo"),
                  ("Coordenador de área", "Coordenador de compras"),
                  ("Residente", "Assistente de compras"),
                  ("Médico", "Comprador"))
            + lit(("A plataforma EAD funcionou perfeitamente, sem nenhuma interrupção.",
                   "A entrega funcionou perfeitamente, sem nenhuma falha."),
                  ("Bom de forma geral. A plataforma EAD precisa melhorar.",
                   "Bom de forma geral. O prazo de entrega precisa melhorar."),
                  ("Bom curso mas esperava mais casos clínicos práticos.",
                   "Bom produto mas esperava mais opções de embalagem."),
                  ("Conteúdo atualizado e imediatamente aplicável na prática clínica.",
                   "Ficha técnica atualizada e imediatamente aplicável na operação."),
                  ("Conteúdo excelente, professor muito didático. Já apliquei na prática.",
                   "Produto excelente, atendimento muito atencioso. Já recompramos."),
                  ("Conteúdo repetitivo em relação ao que aprendi em outro curso.",
                   "Especificação repetitiva em relação à do fornecedor anterior."),
                  ("Excelente curadoria de palestrantes. Muito além do esperado.",
                   "Excelente curadoria de itens no mix. Muito além do esperado."),
                  ("Melhor curso que fiz nos últimos anos. Recomendo a todos os colegas.",
                   "Melhor fornecedor dos últimos anos. Recomendo a todos os parceiros."),
                  ("O suporte antes e durante o curso foi impecável.",
                   "O suporte antes e durante a entrega foi impecável."),
                  ("Professor incrível, conteúdo denso mas muito bem explicado.",
                   "Atendimento incrível, ficha técnica densa mas bem explicada."),
                  ("Transformador. Indicarei para toda a minha equipe da clínica.",
                   "Transformador. Indicarei para toda a minha equipe de compras."),
                  ("Apostila com erros em vários módulos.",
                   "Ficha técnica com erros em vários itens."),
                  ("Plataforma travou várias vezes durante o módulo 3. Muito frustrante.",
                   "A entrega atrasou várias vezes no lote 3. Muito frustrante."),
                  ("Alguns módulos muito densos para o tempo disponível.",
                   "Alguns itens do mix muito complexos para o prazo disponível."),
                  ("Intervalo muito curto para o volume de conteúdo.",
                   "Janela de recebimento muito curta para o volume do pedido."),
                  ("Material impresso com alguns erros de formatação.",
                   "Rótulo impresso com alguns erros de formatação."),
                  ("Material didático de altíssima qualidade.",
                   "Material de apoio de altíssima qualidade."),
                  ("Válido, mas a carga horária poderia ser melhor distribuída.",
                   "Válido, mas o volume poderia ser melhor distribuído."),
                  ("O suporte demorou para responder minhas dúvidas pré-evento.",
                   "O suporte demorou para responder minhas dúvidas pré-pedido."))
            + LINHAS + LOTES + CANAIS),
    ),

    # A receita por curso vira a receita por linha de produto.
    "financeiro": dict(
        origem="IC-B/A2_Financeiro_Receita_Cursos.csv",
        de_para=(
            lit(("Turmas_Previstas", "Lotes_Previstos"),
                ("Turmas_Realizadas", "Lotes_Realizados"),
                ("Alunos_Orcados", "Pedidos_Orcados"),
                ("Alunos_Matriculados", "Pedidos_Fechados"),
                ("Modalidade", "Canal"),
                ("Curso", "Linha_Produto"))
            + lit(("Ação de reengajamento de ex-alunos",
                   "Ação de reativação de clientes inativos"),
                  ("Black Friday educacional", "Black Friday do varejo"),
                  ("Cancelamentos por questões financeiras dos alunos",
                   "Cancelamentos por questões financeiras dos clientes"),
                  ("Cancelamento de turma", "Cancelamento de lote"),
                  ("Competição com curso concorrente", "Competição com linha concorrente"),
                  ("Problemas técnicos na plataforma EAD",
                   "Problemas técnicos na linha de envase"),
                  ("Turma extra aberta por demanda", "Lote extra aberto por demanda"))
            + LINHAS + CANAIS),
    ),

    # 🔴 O RH ja era generico, e o prompt registrou isso. Sobraram DOIS
    # marcadores que nomeiam o setor do cliente, e so eles saem.
    "rh": dict(
        origem="IC-B/A2_RH_Pipeline_Recrutamento.csv",
        de_para=lit(("Coordenador Educacional", "Coordenador de Treinamento"),
                    ("Sem experiência no setor de saúde/educação",
                     "Sem experiência no setor")),
    ),
}



# ---------------------------------------------------------------------------
# A TRAVA
#
# 🔴 Ela existe porque a secao 5 do pedido listou o vocabulario de dominio e
# NAO listou o que a leitura dos arquivos encontrou: sete nomes de pessoa numa
# coluna, o primeiro nome de uma pessoa real em 18 comentarios, e a sigla do
# cliente em 556 celulas. A regra 5 do Rafael e explicita, e um de-para escrito
# a mao esquece. A trava nao esquece, e ela roda a cada geracao.
#
# Ela reprova, nao avisa: arquivo com marcador nao chega a ser gravado.
# ---------------------------------------------------------------------------
PROIBIDO = [
    # o vocabulario da outra turma, que e a prova pedida no proprio enunciado
    r"congresso", r"medic", r"matricul", r"\bEAD\b", r"aluno", r"turma", r"curso",
    # o cliente e a pessoa, que o enunciado nao previu
    r"\bLS\b", r"[ÍI]talo", r"cl[ií]nic", r"professor", r"palestra clínica",
    # os sete nomes da coluna Consultor entram em tempo de execucao, vindos do
    # origens.local.json: escreve-los aqui poria no repositorio publico
    # exatamente o que a trava existe para tirar de la.
]

# Nome de pessoa e duas palavras capitalizadas seguidas. A regra sozinha acusa
# demais ("Black Friday", "Google Ads"), entao ela AVISA em vez de reprovar, e
# o que ja se sabe que e legitimo sai da lista.
NOME_DE_PESSOA = re.compile(r"\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-zá-úâêôãõç]{2,}"
                            r" [A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-zá-úâêôãõç]{2,}\b")
NAO_E_PESSOA = {"Black Friday", "Google Ads", "Email Marketing", "Site Orgânico",
                "Parceiro Distribuidor", "Parceiro Clínica", "Feira Internacional",
                "Programa de", "Analista de", "Assistente Financeiro",
                "Coordenador Educacional", "Consultor Comercial", "Entrevista Gestor",
                "Teste Técnico", "Contato Realizado", "Lead Captado",
                "Proposta Enviada", "Rede nacional", "Food service",
                "Medicina Integrativa", "Clínica Geral", "Medicina do"}


def confere(slug, celulas):
    """Reprova o arquivo que ainda carrega marcador. Devolve os avisos."""
    duros = []
    for termo in PROIBIDO + [re.escape(n) for n in _local()["nomes_de_pessoa"]]:
        achados = [c for c in celulas if re.search(termo, c, flags=re.IGNORECASE)]
        if achados:
            duros.append("{}: {} celula(s) ainda casam com {!r}. Ex: {!r}"
                         .format(slug, len(achados), termo, achados[0][:70]))
    if duros:
        raise SystemExit("🔴 A TRAVA REPROVOU:\n  " + "\n  ".join(duros))
    avisos = set()
    for c in celulas:
        for m in NOME_DE_PESSOA.finditer(c):
            if m.group(0) not in NAO_E_PESSOA:
                avisos.add(m.group(0))
    return sorted(avisos)


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
    """Aplica as trocas na ordem declarada.

    🔴 SEM ignorecase, e de proposito. Com ele, `\bPOS\b` casaria com um "pos"
    solto no meio de um comentario, e `\bLS\b` com qualquer "ls". Quem precisa
    das duas caixas declara as duas: e mais linha e nenhuma surpresa.
    """
    for de, para in de_para:
        texto = re.sub(de, para, texto)
    return texto


def grava(slug, caso):
    origem = _caminho(caso["origem"])
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

    celulas = [str(c.value) for linha in ws.iter_rows() for c in linha
               if isinstance(c.value, str)]
    avisos = confere(slug, celulas)

    caminho = os.path.join(DESTINO, slug + ".xlsx")
    wb.save(caminho)
    return caminho, len(dados), len(cabecalho), cabecalho, avisos


def main():
    for slug, caso in CASOS.items():
        caminho, linhas, colunas, cabecalho, avisos = grava(slug, caso)
        print("{:16s} {:>5} linhas x {:>2} colunas".format(
            os.path.basename(caminho), linhas, colunas))
        print("   colunas: " + " | ".join(cabecalho))
        if avisos:
            print("   ⚠️  parece nome de pessoa, confira: " + " · ".join(avisos))


if __name__ == "__main__":
    main()
