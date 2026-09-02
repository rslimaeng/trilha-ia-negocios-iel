# -*- coding: utf-8 -*-
"""Gerador do site de treinamento.

O conteúdo mora em _build/conteudo/<slug>.html, em fragmentos. Este script
monta a casca em volta, inlineia o CSS e grava a página.

🔴 Editar o index.html gerado é trabalho perdido: a próxima execução apaga.

Rodar:  python3 _build/gerar.py
"""
import io
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


# ---------------------------------------------------------------------------
# O CURSO
#
# Trocar de cliente é mexer aqui e no marca.css. Mais nada.
# ---------------------------------------------------------------------------
CURSO = {
    "nome":  "IA para Negócios",
    "sigla": "IEL",
    "sub":   "Trilha completa · IEL Ceará · Rafael Lima",

    # O QUE ESTE CURSO ENSINA PELO NOME OFICIAL.
    #
    # 🔴 Achado do curso do IEL, 26/08. O gate G2 proibe vocabulario de
    # bastidor na tela, e "Claude Code" estava na lista: num curso sobre
    # planilha, dizer que o material foi feito no Claude Code e bastidor.
    # So que o IEL VENDEU Claude Code como Modulo 3 da ementa. Ali o nome
    # nao e bastidor: e o assunto, esta no contrato que o cliente aprovou,
    # e a regra P1 do proprio padrao manda o nome oficial aparecer na tela.
    #
    # Um gate proibindo o que outra regra do mesmo padrao exige nao e rigor,
    # e contradicao -- e o custo dela e a sessao seguinte editar o gate para
    # calar, que e como um gate morre.
    #
    # Entao o curso DECLARA o que ensina, e o G2 para de acusar so esses.
    # Lista vazia e o default: quem nao ensina o produto continua protegido.
    #
    # Os nomes abaixo estao na ementa v3 que o IEL aprovou e na pagina de
    # vendas: sao o assunto do curso, nao bastidor.
    "ensina": ["Claude", "n8n", "NotebookLM", "Claude Projects", "Cowork",
               "Gmail", "Google Sheets", "Google Drive", "ChatGPT", "Gemini"],
}

# ---------------------------------------------------------------------------
# A TRILHA · o indice do curso, e a unica lista escrita a mao neste arquivo
# ---------------------------------------------------------------------------
# Por que a mao: a ordem das aulas e decisao de produto do Rafael, nao coisa
# que se deduza da pasta. Ordem alfabetica de arquivo NAO e ordem pedagogica.
#
# Cada aula e (slug, titulo). O slug casa com a chave em PAGINAS e com a pasta
# de saida. Grupo vazio ("") nao imprime cabecalho.
#
# A pagina que nao esta na trilha (a capa, por exemplo) simplesmente nao
# recebe a barra — e o comportamento certo, nao um caso a tratar.
# A ORDEM DE LEITURA DO SITE INTEIRO, e nao so da trilha.
#
# 🔴 Existe porque toda pagina precisa terminar com um lugar para ir. Ate
# 26/08 nenhuma das seis terminava: a classe .rodape-nav estava no base.css
# desde o inicio e ZERO paginas usavam. O curso do IEL herdou isso, e a
# pagina de modulo dele acabava no meio de uma secao, sem nada embaixo. Foi
# a primeira coisa que o Rafael apontou: "nao tem um toco, um botao tipo
# voltar pra capa".
#
# Isto e maior que a TRILHA de proposito: a trilha e a barra lateral e so
# lista aula; o rodape existe em pagina que a barra nem mostra (a capa, o
# modulo). Sao duas perguntas diferentes -- "onde eu estou no curso" e
# "para onde eu vou agora".
SEQUENCIA = ["index", "modulo-1", "b1-fundamentos", "a1-degrau", "a2-preve", "a3-mesa",
             "a4-inventa", "a5-cerca",
             "b2-analise", "b2-pergunta", "b2-fontes", "b2-base", "b2-planilha", "b2-causa", "b2-decisao", "b2-plano", "b2-visual", "b2-marca", "b2-biblioteca",
             "b3-redesenho", "b3-processo",
             "desafios", "desafio-parecer", "desafio-avaliacoes", "desafio-plano", "desafio-satisfacao",
             "modulo-2", "modulo-3", "componentes"]

TRILHA = [
    ("Módulo 1 · IA Conversacional e Estratégica", [
        ("modulo-1",       "Os quatro blocos do módulo"),
        ("b1-fundamentos", "B1 · Primeiros resultados consistentes"),
        ("b2-analise",     "B2 · Análise e tomada de decisão"),
        ("b3-redesenho",   "B3 · Redesenho e ganho real"),
    ]),
    ("As aulas do B1", [
        ("a1-degrau",   "Entenda os níveis de uso da IA"),
        ("a2-preve",    "O que mudar para ter melhores respostas"),
        ("a3-mesa",     "Por que conversas longas fazem a IA errar"),
        ("a4-inventa",  "Aprenda a fazer boas conferências"),
        ("a5-cerca",    "Decida o que da sua empresa pode subir"),
    ]),
    ("As aulas do B2", [
        ("b2-pergunta", "Formule a pergunta que a análise responde"),
        ("b2-fontes",   "Peça investigação, não resumo"),
        ("b2-base",     "Faça a IA responder pelos seus documentos"),
        ("b2-planilha", "Transforme a planilha na leitura executiva"),
        ("b2-causa",    "Vá do número para a causa"),
        ("b2-decisao",  "Compare três caminhos antes de recomendar"),
        ("b2-plano",    "Amarre a decisão num plano com dono e prazo"),
        ("b2-visual",   "Transforme a análise no material da chefia"),
        ("b2-marca",    "Ponha a cara da sua empresa no que a IA gerou"),
    ]),
    ("As aulas do B3", [
        ("b3-processo", "Escolha o processo que vale a pena mudar"),
    ]),
    # 🔴 O banco NAO mora dentro de bloco nenhum, e e decisao do Rafael (01/09).
    # Ele atravessa o curso: o desafio 7 espera o modulo 2 e o 8 espera o B4. Se
    # nascesse dentro do B2, morreria com o B2.
    ("Banco de Desafios", [
        ("desafios",           "Para quem não trouxe material seu"),
        ("desafio-parecer",    "1 · Planilha vira parecer executivo"),
        ("desafio-avaliacoes", "2 · Avaliações viram painel"),
        ("desafio-plano",      "3 · Transcrição vira plano de 30 dias"),
        ("desafio-satisfacao", "4 · Pesquisa de satisfação vira diagnóstico"),
    ]),
    ("Os outros dois módulos", [
        ("modulo-2",    "Automação com n8n"),
        ("modulo-3",    "Minha Jornada com IA"),
    ]),
    ("Referência interna", [
        ("componentes", "As peças do padrão"),
    ]),
]

PAGINAS = {
    "index": dict(
        titulo="IA para Negócios · Trilha Completa",
        kicker="Formação IEL Ceará · online ao vivo",
        h1="Você entra com uma rotina que consome a sua semana",
        sub="Você sai com ela funcionando, e com o método anotado para repetir "
            "sozinho na segunda seguinte.",
        # 🔴 Nem CARGA nem DATA na tela, e e decisao do Rafael (29/08).
        # O site organiza por MODULO e por AULA, nunca por calendario.
        #
        # Carga: a duracao de cada bloco depende da aula. O n8n leva mais do
        # que a ementa diz, porque comeca em criar conta e aprender a
        # interface, e pesquisa e analise levam menos. Selo de hora vira
        # promessa que o calendario nao sustenta.
        #
        # Data: turma tem data, MATERIAL nao. O mesmo material serve a
        # proxima turma sem reescrita, e data na tela envelhece sozinha.
        selos=["Traga uma rotina real", "Nada para instalar"],
        migalha=None,
    ),
    "caso": dict(
        titulo="Um caso, em cinco passos",
        kicker="Modelo de página de caso",
        h1="O relatório da semana, sem as três horas de planilha",
        sub="Os cinco passos são fixos: mesmo número, mesmo título, mesma ordem, em "
            "qualquer caso de qualquer curso.",
        selos=["Supervisão", "Operações", "Relatório HTML"],
        migalha=[("../", "Nome do Curso"), (None, "Um caso, em cinco passos")],
    ),
    "exemplo": dict(
        titulo="O exemplo pronto",
        kicker="Modelo de página de exemplo",
        h1="O resultado, inteiro, antes de você tentar",
        sub="A moldura do site fica em cima. Embaixo vem o documento, com a cara "
            "de documento, e ele imprime em A4 sem levar o site junto.",
        selos=["Resultado do caso", "Imprime em A4"],
        migalha=[("../", "Nome do Curso"), ("../caso/", "Um caso, em cinco passos"),
                 (None, "O exemplo pronto")],
    ),
    "modulo-1": dict(
        titulo="Módulo 1 · IA Conversacional e Estratégica",
        kicker="Módulo 1 de 3",
        h1="IA Conversacional e Estratégica",
        sub="Do diagnóstico pessoal até o assistente configurado que já conhece o seu "
            "processo. É onde a rotina é escolhida, mapeada e virada em instrução.",
        selos=["Quatro blocos", "Você sai com um assistente seu"],
        migalha=[("../", "IA para Negócios"),
                 (None, "IA Conversacional e Estratégica")],
    ),
    "modulo-2": dict(
        titulo="Módulo 2 · Automação com n8n",
        kicker="Módulo 2 de 3",
        h1="Automação com n8n",
        sub="Do primeiro fluxo funcional ao agente que executa a rotina sozinho. Começa "
            "pela conta, pela interface e pelo primeiro fluxo que roda de verdade.",
        selos=["Três blocos", "Você sai com um fluxo rodando"],
        migalha=[("../", "IA para Negócios"),
                 (None, "Automação com n8n")],
    ),
    "modulo-3": dict(
        titulo="Módulo 3 · Minha Jornada com IA",
        kicker="Módulo 3 de 3",
        h1="Minha Jornada com IA",
        sub="Como apresentar o que você construiu, conduzir a adoção no time, e medir o "
            "retorno do que já está rodando.",
        selos=["Dois blocos", "Você sai com o retorno medido"],
        migalha=[("../", "IA para Negócios"),
                 (None, "Minha Jornada com IA")],
    ),
    "b1-fundamentos": dict(
        titulo="B1 · Tenha os seus primeiros resultados consistentes com IA",
        kicker="Módulo 1 · Bloco 1 de 4",
        h1="Tenha os seus primeiros resultados consistentes com IA",
        sub="Onde você está, por que a IA erra do jeito que erra, e qual rotina sua vai "
            "atravessar o curso inteiro.",
        selos=["Cinco aulas", "Nada para instalar"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 (None, "Primeiros resultados")],
    ),
    "a1-degrau": dict(
        # 🔴 organizacao, nao fundamento. Decisao do Rafael, 31/08: posicionar-se
        # nos 7 Niveis E inventariar a propria rotina, nao aprender um conceito.
        # Ela nunca foi aula de fundamento; era o terceiro tipo antes de o
        # terceiro tipo existir. E o que tira o bloco 1 do G44.
        tipo="organizacao",
        titulo="Aula 1 · Entenda os níveis de uso da IA e os próximos passos",
        kicker="Módulo 1 · B1 · Primeiros resultados",
        h1="Entenda os níveis de uso da IA e os próximos passos",
        sub="O diagnóstico que decide o que faz sentido você tentar em seguida, e a "
            "rotina que vai atravessar o curso com você.",
        selos=["Sem instalação", "Traga uma rotina real"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b1-fundamentos/", "B1 · Primeiros resultados"),
                 (None, None)],
    ),
    "a2-preve": dict(
        tipo="fundamento",
        titulo="Aula 2 · O que mudar para ter melhores respostas com IA",
        kicker="Módulo 1 · B1 · Primeiros resultados",
        h1="O que mudar para ter melhores respostas com IA",
        sub="Por que a mesma pergunta volta diferente, e o que isso muda no que você "
            "passa a esperar dela.",
        selos=["Sem instalação", "Dois pedidos comparados"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b1-fundamentos/", "B1 · Primeiros resultados"),
                 (None, None)],
    ),
    "a3-mesa": dict(
        tipo="fundamento",
        titulo="Aula 3 · Por que conversas longas fazem a IA errar, e como evitar",
        kicker="Módulo 1 · B1 · Primeiros resultados",
        h1="Por que conversas longas fazem a IA errar, e como evitar",
        sub="Por que ela esquece o combinado do começo numa conversa longa, e o que "
            "fazer quando isso acontece.",
        selos=["Sem instalação", "Provoque o defeito"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b1-fundamentos/", "B1 · Primeiros resultados"),
                 (None, None)],
    ),
    "a4-inventa": dict(
        # 🔴 pratica, e ela SEMPRE foi. Decisao do Rafael, 31/08.
        # O exercicio original (4b94fae) tinha entrega concreta e continuidade
        # entre modulos: pedir o trabalho ja entregue sem contar o resultado,
        # comparar em tres colunas, e escrever a frase que evita o
        # preenchimento. Foi classificada como fundamento em 30/08 por engano, e
        # o exercicio foi removido obedecendo a essa classificacao errada.
        # E a segunda nao-fundamento que o G44 exige: com uma so, as janelas
        # [2,3,4] e [3,4,5] ficam descobertas.
        tipo="pratica",
        arquivo=True,
        titulo="Aula 4 · Aprenda a fazer boas conferências de trabalho",
        kicker="Módulo 1 · B1 · Primeiros resultados",
        h1="Aprenda a fazer boas conferências de trabalho",
        sub="A alucinação, e o primeiro teste real: pedir o trabalho que você já "
            "entregou e comparar com o que saiu na sua mão.",
        selos=["Use a sua rotina", "Conferência item a item"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b1-fundamentos/", "B1 · Primeiros resultados"),
                 (None, None)],
    ),
    "a5-cerca": dict(
        tipo="fundamento",
        titulo="Aula 5 · Decida em 30 segundos o que da sua empresa pode subir",
        kicker="Módulo 1 · B1 · Primeiros resultados",
        h1="Decida em 30 segundos o que da sua empresa pode subir",
        sub="Quatro perguntas que decidem se um dado pode ir, e como preparar o seu "
            "material para o resto do curso.",
        selos=["Use a sua rotina", "Vale para o curso inteiro"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b1-fundamentos/", "B1 · Primeiros resultados"),
                 (None, None)],
    ),
    "b2-analise": dict(
        titulo="B2 · Use IA para melhorar a análise e a tomada de decisão",
        kicker="Módulo 1 · Bloco 2 de 4",
        h1="Use IA para melhorar a análise e a tomada de decisão",
        sub="Uma pergunta de verdade da sua área, o material que responde a ela, e a "
            "decisão que sai disso com o plano amarrado.",
        selos=["Nove aulas", "Traga uma pergunta em aberto"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 (None, "Análise e decisão")],
    ),
    "b2-pergunta": dict(
        # 🔴 organizacao, e pelo mesmo motivo da a1-degrau: o conteudo e SOBRE A
        # PESSOA. Ela nao aprende um conceito novo para aplicar depois, ela
        # escolhe e escreve a pergunta que atravessa as outras cinco aulas.
        # Canvas em branco com estrutura dada, nunca planilha nossa preenchida.
        tipo="organizacao",
        titulo="Aula 1 · Formule a pergunta que a análise precisa responder",
        kicker="Módulo 1 · B2 · Análise e decisão",
        h1="Formule a pergunta que a análise precisa responder",
        sub="Por que pedir uma análise volta com um resumo correto que não decide "
            "nada, e como escrever a pergunta que decide.",
        selos=["Traga uma pergunta em aberto", "Vale para as seis aulas"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b2-analise/", "B2 · Análise e decisão"),
                 (None, None)],
    ),
    "b2-fontes": dict(
        # 🔴 pratica. Ela e a aula de PESQUISA PROFUNDA, e entrega a ficha de
        # conferencia preenchida, que e artefato que sai da tela.
        #
        # 🔴 ATE 02/09 ESTE COMENTARIO DIZIA "ela fecha o PHFE (as letras F e E)",
        # e a PAGINA dizia PCTFL. Era o mesmo defeito nos dois lugares: a aula
        # nasceu com o PHFE na cabeca e saiu etiquetada com o outro padrao, e
        # entao ela falava de um campo [E] que o PCTFL+CS nao tem. Quem auditou
        # foi o Rafael: "para mim essa aula nao esta fazendo sentido".
        #
        # A correcao NAO foi trocar a letra. Os dois padroes convivem em NIVEIS
        # diferentes: o PHFE e um pre-prompt, quatro decisoes que a pessoa toma
        # antes; o pedido que vai para a IA continua sendo PCTFL+CS nos seis
        # campos rotulados. A pagina diz isso numa tabela, de proposito.
        #
        # O conceito continua sendo UM: pesquisa profunda e auditoria, nao
        # resumo -- e a fonte citada so vira prova depois que alguem abre.
        tipo="pratica",
        arquivo=False,
        titulo="Aula 2 · Peça investigação, não resumo",
        kicker="Módulo 1 · B2 · Análise e decisão",
        h1="Peça investigação, não resumo",
        sub="O que muda quando você decide a cadeira, a hipótese, as fontes e o formato "
            "antes de perguntar, e por que a referência que volta junto ainda é texto.",
        selos=["Use a pergunta da aula 1", "Três caminhos por área"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b2-analise/", "B2 · Análise e decisão"),
                 (None, None)],
    ),
    "b2-base": dict(
        # 🔴 fundamento, como o recorte aprovado manda. Ela MOSTRA o mecanismo
        # (a mesma pergunta com e sem base, e a citacao apontando para o trecho)
        # e nao pede exercicio. O contrato do G43 e a DEMONSTRACAO, e ela e a
        # peca .demo do meio da pagina.
        tipo="fundamento",
        titulo="Aula 3 · Faça a IA responder só a partir dos seus documentos",
        kicker="Módulo 1 · B2 · Análise e decisão",
        h1="Faça a IA responder só a partir dos seus documentos",
        sub="Quando vale montar uma base fechada com o material da sua empresa, e por "
            "que a citação clicável muda o que dá para assinar.",
        selos=["Ferramenta gratuita", "Clique em três citações"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b2-analise/", "B2 · Análise e decisão"),
                 (None, None)],
    ),
    "b2-planilha": dict(
        # 🔴 pratica, e e o entregavel central do bloco: a analise real com
        # narrativa executiva, que e o primeiro dos tres entregaveis declarados
        # na ementa do M5. A planilha e sintetica e sustenta as aulas 1, 5, 6 e 7.
        tipo="pratica",
        arquivo=True,
        titulo="Aula 4 · Transforme a planilha na leitura que a chefia usa",
        kicker="Módulo 1 · B2 · Análise e decisão",
        h1="Transforme a planilha na leitura que a chefia usa",
        sub="Duas camadas que falham separadamente, a conta e a leitura, e por que "
            "pedir as duas juntas faz a segunda esconder a primeira.",
        selos=["Planilha para baixar", "Use a pergunta da aula 1"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b2-analise/", "B2 · Análise e decisão"),
                 (None, None)],
    ),
    "b2-causa": dict(
        # 🔴 fundamento. Ela MOSTRA o mecanismo (a mesma pergunta com e sem o
        # teste no primeiro elo, na peca .demo) e nao pede exercicio. E a aula
        # que fecha o defeito que a a4-inventa abriu no B1: a IA preenche onde
        # falta base, e "por que caiu?" e o pedido que mais convida ao
        # preenchimento, porque causa nunca esta escrita no arquivo.
        tipo="fundamento",
        titulo="Aula 5 · Vá do número para a causa sem aceitar a primeira explicação",
        kicker="Módulo 1 · B2 · Análise e decisão",
        h1="Vá do número para a causa sem aceitar a primeira explicação",
        sub="Por que a explicação que volta é a mais comum para aquele padrão, e como "
            "transformar ela em algo que o seu dado possa derrubar.",
        selos=["Usa a planilha da aula 4", "Teste em cada elo"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b2-analise/", "B2 · Análise e decisão"),
                 (None, None)],
    ),
    "b2-decisao": dict(
        # 🔴 pratica. Entrega o segundo dos tres entregaveis declarados na
        # ementa do M5: o relatorio de decisao qualitativa. O pre-mortem entra
        # como ATIVIDADE, que e o que ele e no material do Rafael, e nao como
        # framework a ensinar.
        tipo="pratica",
        arquivo=True,
        titulo="Aula 6 · Compare três caminhos antes de recomendar um",
        kicker="Módulo 1 · B2 · Análise e decisão",
        h1="Compare três caminhos antes de recomendar um",
        sub="Por que uma recomendação sozinha não pode ser julgada, e como imaginar o "
            "fracasso do caminho escolhido antes de gastar dinheiro nele.",
        selos=["Usa a causa da aula 5", "Comparador para baixar"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b2-analise/", "B2 · Análise e decisão"),
                 (None, None)],
    ),
    "b2-plano": dict(
        # 🔴 pratica, e fecha o bloco. Entrega o terceiro entregavel declarado
        # na ementa: o plano de acao. O canvas dela recolhe o bloco inteiro em
        # seis campos, e e a peca que a pessoa leva para a reuniao.
        tipo="pratica",
        arquivo=True,
        titulo="Aula 7 · Amarre a decisão num plano com dono e prazo",
        kicker="Módulo 1 · B2 · Análise e decisão",
        h1="Amarre a decisão num plano com dono e prazo",
        sub="Plano é o que outra pessoa executa sem você na sala: nome, data e um "
            "número que diz se funcionou.",
        selos=["Fecha o bloco", "Plano para baixar"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b2-analise/", "B2 · Análise e decisão"),
                 (None, None)],
    ),
    "b2-visual": dict(
        # 🔴 pratica. Ela nao produz analise nova: pega a que a aula 4 deixou
        # pronta e transforma na peca que outra pessoa recebe. E a primeira das
        # duas aulas de outra natureza -- as sete anteriores respondem a uma
        # pergunta, esta e a nona produzem um objeto.
        #
        # Um conceito so, e ele NAO e "deck" nem "painel": e que a narrativa
        # vem antes do formato. Os dois formatos sao dois caminhos do mesmo
        # conceito, e por isso moram na mesma aula em vez de virar duas.
        tipo="pratica",
        arquivo=True,
        titulo="Aula 8 · Transforme a análise no material que a chefia recebe",
        kicker="Módulo 1 · B2 · Análise e decisão",
        h1="Transforme a análise no material que a chefia recebe",
        sub="Quatro respostas soltas num chat não são uma entrega. O que a peça precisa "
            "provar se decide antes de escolher se ela é slide ou tela.",
        selos=["Usa a análise da aula 4", "Deck ou painel"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b2-analise/", "B2 · Análise e decisão"),
                 (None, None)],
    ),
    "b2-marca": dict(
        # 🔴 pratica, e vem DEPOIS da 8 porque essa e a sequencia que o Rafael
        # declarou: dados, comunicacao visual, e o design system como
        # OTIMIZACAO do que ja existe. Nao sao aulas irmas -- esta so faz
        # sentido com a peca da aula anterior na mao.
        #
        # O entregavel dela nao e a peca vestida: e o DOCUMENTO, que serve a
        # todas as pecas seguintes. Por isso o insumo e um modelo para
        # substituir, e nao uma planilha para analisar.
        tipo="pratica",
        arquivo=True,
        titulo="Aula 9 · Ponha a cara da sua empresa no que a IA gerou",
        kicker="Módulo 1 · B2 · Análise e decisão",
        h1="Ponha a cara da sua empresa no que a IA gerou",
        sub="Um documento de uma página, literal o suficiente para ser conferido a olho "
            "nu, faz a IA parar de escolher o visual por você.",
        selos=["Usa a peça da aula 8", "Modelo para baixar"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b2-analise/", "B2 · Análise e decisão"),
                 (None, None)],
    ),
    "b2-biblioteca": dict(
        # 🔴 SEM tipo=, e pela mesma razao das quatro paginas do Banco de
        # Desafios: nao e aula. Nao tem situacao, conceito nem "sua vez", e o
        # contrato de tipo do G43 cobraria pecas que aqui nao fazem sentido.
        # E referencia -- a pessoa volta nela com um arquivo na mao.
        #
        # Fica FORA da TRILHA de proposito: entrar na lista das aulas do B2
        # faria dela uma decima aula. Ela e linkada da capa do bloco.
        titulo="Biblioteca de prompts do B2",
        kicker="Referência · vale para o bloco inteiro",
        h1="Biblioteca de prompts",
        sub="Os pedidos da aula sobre a pesquisa, os três de cada setor e as seis "
            "perguntas de uma linha. Para copiar, adaptar e rodar hoje.",
        selos=["28 pedidos prontos", "Seis bases para praticar"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b2-analise/", "B2 · Análise e decisão"),
                 (None, "Biblioteca de prompts")],
    ),
    "desafio-satisfacao": dict(
        titulo="Desafio 4 · uma pesquisa de satisfação vira diagnóstico",
        kicker="Banco de Desafios · 4 de 8",
        h1="1.000 respostas de pesquisa → diagnóstico com dono",
        sub="Quinze dimensões, seis campos de perfil e um campo de comentário. A média "
            "não descreve ninguém, e o corte certo é o que revela isso.",
        selos=["1.000 respostas", "Dados fictícios"],
        migalha=[("../", "IA para Negócios"),
                 ("../desafios/", "Banco de Desafios"),
                 (None, None)],
    ),
    "b3-redesenho": dict(
        titulo="B3 · Redesenhe o seu trabalho e entenda o ganho real",
        kicker="Módulo 1 · Bloco 3 de 4",
        h1="Redesenhe o seu trabalho e entenda o ganho real",
        sub="Um processo seu aberto em passos, com o vazamento achado e o preço "
            "calculado a partir do tempo que você mediu.",
        selos=["Cinco aulas", "Traga a sua semana"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 (None, "Redesenho e ganho real")],
    ),
    "b3-processo": dict(
        # 🔴 fundamento, como o recorte fechado do Rafael manda (01/09). Ela
        # estreia TRES coisas que a trilha nunca disse -- os 6 Gatilhos, o PPBR
        # e a varredura de duas passadas --, e por isso carrega mais explicacao
        # do que producao. Leva canvas, figura de estrutura e destrave mesmo
        # assim, porque a pessoa preenche a ficha dela aqui.
        tipo="fundamento",
        titulo="Aula 1 · Escolha o processo do seu trabalho que vale a pena mudar",
        kicker="Módulo 1 · B3 · Redesenho e ganho real",
        h1="Escolha o processo do seu trabalho que vale a pena mudar",
        sub="Seis padrões para achar o que incomoda na sua semana, e a segunda pergunta "
            "que transforma tarefa solta em processo escolhido.",
        selos=["Traga a sua semana", "Vale para o bloco inteiro"],
        migalha=[("../", "IA para Negócios"),
                 ("../modulo-1/", "Módulo 1"),
                 ("../b3-redesenho/", "B3 · Redesenho e ganho real"),
                 (None, None)],
    ),
    # -----------------------------------------------------------------------
    # O BANCO DE DESAFIOS
    #
    # 🔴 Nenhuma das quatro leva tipo=. Elas nao sao aula: nao tem situacao,
    # conceito nem "sua vez", e o contrato de tipo do G43 cobraria pecas que
    # aqui nao fazem sentido. O hub do banco e irmao do hub de bloco.
    #
    # Existe porque a turma online chega sem material proprio, e sem isso a
    # pessoa fica parada na hora do exercicio. Medido na aula de 31/08: o
    # Rafael parou a turma DUAS vezes para coletar rotina, e nao havia lugar
    # nenhum no site onde a resposta coubesse.
    # -----------------------------------------------------------------------
    "desafios": dict(
        titulo="Banco de Desafios · material pronto para praticar",
        kicker="Vale para o curso inteiro",
        h1="Banco de Desafios",
        sub="Se você não trouxe uma rotina sua para a aula de hoje, escolha um destes "
            "e rode agora: o arquivo e o pedido já vêm prontos.",
        selos=["Oito desafios", "Insumo e pedido prontos"],
        migalha=[("../", "IA para Negócios"),
                 (None, "Banco de Desafios")],
    ),
    "desafio-parecer": dict(
        titulo="Desafio 1 · 600 linhas de planilha viram um parecer executivo",
        kicker="Banco de Desafios · 1 de 8",
        h1="600 linhas de planilha → parecer executivo para o comitê",
        sub="Uma base de 20 lojas em 30 dias, e a leitura de quatro minutos que decide "
            "onde investir na quinzena seguinte.",
        selos=["Planilha de 600 linhas", "Dados fictícios"],
        migalha=[("../", "IA para Negócios"),
                 ("../desafios/", "Banco de Desafios"),
                 (None, None)],
    ),
    "desafio-avaliacoes": dict(
        titulo="Desafio 2 · 150 avaliações viram um painel de reunião",
        kicker="Banco de Desafios · 2 de 8",
        h1="150 avaliações de clientes → painel para a reunião de segunda",
        sub="Texto solto, escrito por gente diferente, sem coluna para somar, e a "
            "mesma pergunta: o que se repete, e o que fazer.",
        selos=["150 avaliações", "Análise de texto"],
        migalha=[("../", "IA para Negócios"),
                 ("../desafios/", "Banco de Desafios"),
                 (None, None)],
    ),
    "desafio-plano": dict(
        titulo="Desafio 3 · uma transcrição vira plano de 30 dias",
        kicker="Banco de Desafios · 3 de 8",
        h1="1 transcrição de reunião → plano de 30 dias com dono e prazo",
        sub="A conversa de equipe que sempre vira nada, convertida em prioridade, "
            "dono e prazo, com o critério de gravidade já dado.",
        selos=["Transcrição de reunião", "Dados fictícios"],
        migalha=[("../", "IA para Negócios"),
                 ("../desafios/", "Banco de Desafios"),
                 (None, None)],
    ),

    "modulo": dict(
        titulo="Nome do Módulo",
        kicker="Módulo 1 de N",
        h1="A capacidade que este módulo entrega",
        sub="Uma linha dizendo o que a pessoa sai sabendo fazer depois destas aulas.",
        selos=["3 aulas", "2h15"],
        migalha=[("../", "Nome do Curso"), (None, "Nome do Módulo")],
    ),
    "componentes": dict(
        titulo="As peças do padrão",
        kicker="Referência do padrão",
        h1="As peças, uma a uma",
        sub="Cada bloco desta página é um componente do padrão, com o nome que "
            "ele tem no HTML e a regra que faz ele funcionar.",
        selos=["Uso interno", "Não vai para a turma"],
        migalha=[("../", "Nome do Curso"), (None, "As peças do padrão")],
    ),
}


# ---------------------------------------------------------------------------
# QUEBRA DE LINHA · a cola de espaço rígido
#
# Resolve a linha que termina em "na sua" e joga "área." para baixo. Cola a
# palavra-função na palavra seguinte com espaço rígido, do jeito que uma
# gráfica faz: a quebra procura outro lugar e costuma achar a fronteira da
# frase.
#
# 🔴 Esta é a ÚNICA cura de quebra de linha do padrão. text-wrap:balance e
# text-wrap:pretty NÃO entram na prosa: eles reservam espaço no fim da linha e
# criam o defeito oposto, a frase que quebra do nada com meia linha vazia.
# Medido no IC-C: 62 quebras assim com balance, 0 sem ele.
# ---------------------------------------------------------------------------
COLAM = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    "seu", "sua", "seus", "suas", "meu", "minha", "nosso", "nossa",
    "de", "da", "do", "das", "dos", "em", "na", "no", "nas", "nos",
    "por", "pelo", "pela", "com", "sem", "ao", "aos", "à", "às",
    "para", "pra", "num", "numa", "dum", "duma",
    "sobre", "entre", "durante", "até", "desde", "após", "contra",
    "sob", "perante", "conforme", "mediante",
    "e", "ou", "mas", "se", "que", "quando", "onde", "enquanto", "porque",
    "não", "já", "só",
}

# Nenhum trecho colado passa disso. Acima, a unidade indivisível fica maior que
# a linha do celular e vira rolagem lateral, que é o defeito que a cola deveria
# evitar. 24 foi calibrado medindo em 5 larguras.
LIMITE_GRUDADO = 24

# Parágrafo longo não leva cola: ninguém repara numa quebra ruim no meio de
# seis linhas, e colar lá tira do navegador a liberdade de achar a melhor linha.
LIMITE_PARAGRAFO = 400

BLOCO_QUE_COLA = re.compile(
    r'(<h[1-4]\b[^>]*>)(.*?)(</h[1-4]>)'
    r'|(<p\b[^>]*>)(.*?)(</p>)'
    r'|(<li\b[^>]*>)(.*?)(</li>)',
    re.S,
)
SEM_TAG = re.compile(r"<[^>]+>")
PECA = re.compile(r'(<[^>]+>|\s+|[^<\s]+)')

# Onde a cola não entra: o prompt é copiado literalmente pelo aluno, e um
# espaço rígido no meio dele quebra o que for colar em planilha ou terminal.
SEM_COLA = ("prompt-txt", "prompt", "tabela")


def _cola(interno):
    pecas = PECA.findall(interno)
    saida, grudado = [], 0
    for i, p in enumerate(pecas):
        if p and not p.strip():
            anterior = next((x for x in reversed(saida)
                             if x.strip() and not x.startswith("<")), "")
            palavra = re.sub(r"[^\wÀ-ÿ]", "", anterior, flags=re.U).lower()
            seguinte = next((pecas[j] for j in range(i + 1, len(pecas))
                             if pecas[j].strip() and not pecas[j].startswith("<")), "")
            if (palavra in COLAM and seguinte
                    and grudado + len(anterior) + len(seguinte) + 1 <= LIMITE_GRUDADO):
                grudado += len(anterior) + 1
                saida.append("&nbsp;")
                continue
            grudado = 0
        saida.append(p)
    return "".join(saida)


def cola_quebra_de_linha(html):
    """Idempotente: rodar de novo no resultado devolve o mesmo arquivo."""
    def troca(m):
        grupos = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        for a, b, c in grupos:
            if m.group(a):
                abre, interno, fecha = m.group(a), m.group(b), m.group(c)
                break
        else:
            return m.group(0)
        visivel = SEM_TAG.sub("", interno).replace("&nbsp;", " ").strip()
        if len(visivel) > LIMITE_PARAGRAFO:
            return m.group(0)
        return abre + _cola(interno) + fecha

    # o miolo dos blocos protegidos sai da varredura e volta depois
    guardado = []

    def guarda(m):
        guardado.append(m.group(0))
        return "\x00%d\x00" % (len(guardado) - 1)

    protegido = re.compile(
        r'<(pre|code|script|style)\b.*?</\1>'
        r'|<div class="(?:%s)"[^>]*>.*?</div>' % "|".join(SEM_COLA),
        re.S,
    )
    html = protegido.sub(guarda, html)
    html = BLOCO_QUE_COLA.sub(troca, html)
    return re.sub(r"\x00(\d+)\x00", lambda m: guardado[int(m.group(1))], html)


# ---------------------------------------------------------------------------
# O CEM · a parede de cem quadradinhos
#
# Escrever os cem à mão é onde o desenho para de bater com o número da legenda,
# e ninguém confere contando. O fragmento declara só quantos acendem:
#
#     <div class="cem-grade" data-acesos="13"></div>
#
# e este passo produz os cem. Rodar de novo não muda nada: a grade já expandida
# não tem mais a marca vazia que o padrão procura.
# ---------------------------------------------------------------------------
GRADE_DO_CEM = re.compile(r'<div class="cem-grade" data-acesos="(\d+)"\s*></div>')


def expande_o_cem(html):
    def troca(m):
        n = int(m.group(1))
        pontos = "".join('<i class="cem-p%s"></i>' % (" aceso" if i < n else "")
                         for i in range(100))
        return ('<div class="cem-grade" data-acesos="%d" aria-hidden="true">%s</div>'
                % (n, pontos))
    return GRADE_DO_CEM.sub(troca, html)


# ---------------------------------------------------------------------------
# O RADAR · o polígono sai dos números, não do olho
#
# Calcular seno e cosseno à mão dentro do HTML é como o desenho deixa de
# corresponder aos números, e ninguém confere um polígono com transferidor.
# O fragmento declara só os eixos e os valores:
#
#     <div class="radar" data-eixos="Clareza|Tempo|Risco"
#                        data-valores="80,60,40"
#                        data-valores-b="90,80,30"></div>
#
# A segunda série é opcional, e é ela que faz a figura valer a pena: um radar
# de uma série só quase sempre é uma tabela de quatro linhas.
# ---------------------------------------------------------------------------
import math

RADAR = re.compile(r'<div class="radar"([^>]*)></div>')
RAIO, CENTRO = 108, 150


def _ponto(i, n, v):
    ang = math.radians(-90 + i * 360.0 / n)
    r = RAIO * v / 100.0
    return (CENTRO + r * math.cos(ang), CENTRO + r * math.sin(ang))


# O rótulo é escrito FORA do último anel, e a moldura precisa caber nele. Com
# moldura fixa, "Padrão do formato" sai pela borda e o SVG corta: o texto some e
# nada acusa, porque o recorte é o comportamento normal de um <svg>.
LARGURA_DA_LETRA = 6.2   # medido em Inter 12px, na média do português
ALTURA_DA_LINHA = 14


def largura_estimada(texto):
    return len(texto) * LARGURA_DA_LETRA


def _poligono(valores):
    n = len(valores)
    return " ".join("%.1f,%.1f" % _ponto(i, n, v) for i, v in enumerate(valores))


def desenha_radar(html):
    def troca(m):
        attrs = m.group(1)
        eixos = re.search(r'data-eixos="([^"]*)"', attrs)
        vals = re.search(r'data-valores="([^"]*)"', attrs)
        if not eixos or not vals:
            return m.group(0)
        eixos = [e.strip() for e in eixos.group(1).split("|") if e.strip()]
        a = [float(x) for x in vals.group(1).split(",")]
        b = re.search(r'data-valores-b="([^"]*)"', attrs)
        b = [float(x) for x in b.group(1).split(",")] if b else None
        n = len(eixos)

        p = []
        # anéis de referência, para o olho ter escala
        for anel in (25, 50, 75, 100):
            pts = " ".join("%.1f,%.1f" % _ponto(i, n, anel) for i in range(n))
            p.append('<polygon points="%s" fill="none" stroke="var(--border)" '
                     'stroke-width="1"/>' % pts)
        # raios
        for i in range(n):
            x, y = _ponto(i, n, 100)
            p.append('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" '
                     'stroke="var(--border)" stroke-width="1"/>'
                     % (CENTRO, CENTRO, x, y))
        if b:
            p.append('<polygon points="%s" fill="none" stroke="var(--text-dim)" '
                     'stroke-width="1.5" stroke-dasharray="5,4"/>' % _poligono(b))
        p.append('<polygon points="%s" fill="var(--accent-soft)" '
                 'stroke="var(--accent)" stroke-width="1.5" fill-opacity="0.75"/>'
                 % _poligono(a))
        # rótulos, empurrados para fora do último anel
        for i, nome in enumerate(eixos):
            x, y = _ponto(i, n, 128)
            ancora = "middle"
            if x > CENTRO + 12:
                ancora = "start"
            elif x < CENTRO - 12:
                ancora = "end"
            p.append('<text x="%.1f" y="%.1f" text-anchor="%s" '
                     'dominant-baseline="middle" font-size="12" '
                     'font-family="var(--font-body)" fill="var(--text-muted)">%s</text>'
                     % (x, y, ancora, nome))
        # a moldura sai das pontas do desenho E das pontas do texto
        x0 = y0 = 1e9
        x1 = y1 = -1e9
        for i, nome in enumerate(eixos):
            x, y = _ponto(i, n, 128)
            larg = largura_estimada(nome)
            if x > CENTRO + 12:
                e, d = x, x + larg
            elif x < CENTRO - 12:
                e, d = x - larg, x
            else:
                e, d = x - larg / 2, x + larg / 2
            x0, x1 = min(x0, e), max(x1, d)
            y0, y1 = min(y0, y - ALTURA_DA_LINHA), max(y1, y + ALTURA_DA_LINHA)
        x0, y0 = min(x0, 0) - 6, min(y0, 0) - 6
        x1, y1 = max(x1, 300) + 6, max(y1, 300) + 6
        return ('<div class="radar"%s><svg viewBox="%.1f %.1f %.1f %.1f" '
                'role="img" aria-label="%s">%s</svg></div>'
                % (attrs, x0, y0, x1 - x0, y1 - y0,
                   " · ".join(eixos), "".join(p)))
    return RADAR.sub(troca, html)


# ---------------------------------------------------------------------------
# UMA FRASE POR LINHA · a quarta reclamação da quebra de linha
#
# Dentro de um bloco marcado .fr-host, cada frase vira <span class="fr">. O CSS
# decide por container query se elas ficam em linha ou empilhadas: quem manda é
# a largura DO BLOCO, não a da janela.
#
# 🔴 Idempotente por reconstrução: desmarca tudo antes de marcar de novo. Marcar
# em cima do que já estava marcado aninharia span dentro de span a cada execução,
# e o arquivo cresceria sozinho até alguém notar.
# ---------------------------------------------------------------------------
ABRE_FR_HOST = re.compile(r'<(\w+)([^>]*\bclass="[^"]*\bfr-host\b[^"]*"[^>]*)>')
SPAN_FR = '<span class="fr">'

# Ponto que NÃO termina frase. Sem esta lista, "R$ 1.200,00." e "Dr. Silva"
# viravam duas frases, e o corte caía no meio de um número.
NAO_CORTA_DEPOIS = (
    "sr", "sra", "dr", "dra", "prof", "etc", "ex", "obs", "art", "pág", "pag",
    "fig", "n", "nº", "no", "vs", "cf", "aprox", "máx", "max", "mín", "min",
)


def _desmarca_fr(interno):
    """Tira a marcação anterior. Sem isto, cada execução aninha span dentro de
    span e o arquivo cresce sozinho até alguém notar."""
    anterior = None
    while anterior != interno:
        anterior = interno
        interno = re.sub(r'<span class="fr">(.*?)</span>', r"\1", interno, flags=re.S)
    return interno


# Tag de bloco fecha a frase. Sem isto o corte atravessa o <p> e produz
# <span class="fr"><p>Uma.</span>, que é HTML inválido e o navegador conserta
# do jeito dele.
TAG_DE_BLOCO = re.compile(
    r"</?(p|div|li|ul|ol|h[1-6]|section|table|tr|td|th|pre|blockquote|br)\b",
    re.I)


def _corta_frases(interno):
    """Marca cada frase do miolo. Não entra em tag: o corte olha só o texto.

    🔴 O espaço que separa duas frases fica FORA do span. Dentro, ele some no
    modo empilhado e as frases grudam no modo inline, que é o que o container
    query entrega em bloco estreito.
    """
    pedacos = re.split(r"(<[^>]+>)", interno)
    saida, buffer_, marcou = [], [], False

    def fecha():
        if not buffer_:
            return
        txt = "".join(buffer_)
        del buffer_[:]
        if not txt.strip():
            saida.append(txt)
            return
        # o branco das pontas sai do span e fica no meio, entre as frases
        m = re.match(r"^(\s*)(.*?)(\s*)$", txt, flags=re.S)
        esq, meio, dir_ = m.group(1), m.group(2), m.group(3)
        saida.append(esq + SPAN_FR + meio + "</span>" + dir_)

    for p_ in pedacos:
        if p_.startswith("<"):
            if TAG_DE_BLOCO.match(p_):
                fecha()          # fronteira de bloco fecha a frase corrente
                saida.append(p_)
            else:
                buffer_.append(p_)
            continue
        resto = p_
        while resto:
            m = re.search(r"[.!?](?:&nbsp;|\s)+(?=[A-ZÀ-Ý])", resto)
            if not m:
                buffer_.append(resto)
                break
            antes = resto[:m.start()]
            ultima = re.search(r"([\wÀ-ÿ]+)$", antes)
            # só abreviação. Ponto dentro de número ("1.200") não chega aqui:
            # o padrão exige espaço depois do ponto, e número não tem.
            if ultima and ultima.group(1).lower() in NAO_CORTA_DEPOIS:
                buffer_.append(resto[:m.end()])
                resto = resto[m.end():]
                continue
            buffer_.append(resto[:m.start() + 1])
            fecha()
            saida.append(resto[m.start() + 1:m.end()])   # o espaço, fora do span
            marcou = True
            resto = resto[m.end():]
    fecha()
    return "".join(saida) if marcou else interno


def uma_frase_por_linha(html):
    """Sempre recalcula do zero: rodar de novo devolve o mesmo arquivo."""
    saida, i = [], 0
    for m in ABRE_FR_HOST.finditer(html):
        tag = m.group(1)
        # Acha o fechamento do próprio bloco, contando profundidade.
        # 🔴 O regex casa a TAG INTEIRA, com o ">". Casar só "</p" devolve uma
        # posição um caractere curta, e o miolo perde o último caractere: o
        # ponto final da última frase ficava fora do span, a cada execução.
        prof, j, fim = 1, m.end(), len(html)
        while prof and j < len(html):
            t = re.search(r"<(/?)%s\b[^>]*>" % tag, html[j:])
            if not t:
                break
            if t.group(1):
                prof -= 1
                if prof == 0:
                    fim = j + t.start()
                    j = j + t.end()
                    break
            else:
                prof += 1
            j += t.end()
        interno = html[m.end():fim]
        saida.append(html[i:m.end()])
        saida.append(_corta_frases(_desmarca_fr(interno)))
        i = fim
    saida.append(html[i:])
    return "".join(saida)


# ---------------------------------------------------------------------------
# A CASCA
# ---------------------------------------------------------------------------
def css():
    partes = []
    for nome in ("marca.css", "base.css"):
        partes.append(io.open(os.path.join(AQUI, nome), encoding="utf-8").read())
    return "\n".join(partes)


def trilha(slug_atual):
    """A barra do curso: onde esta a aula aberta, dentro da trilha inteira.

    Tres estados, e o estado E o conteudo: `feita` (antes da atual), `agora`
    e o resto. A aula atual nao vira link — clicar nela nao leva a lugar
    nenhum, e um link que nao vai a lugar nenhum e ruido.
    """
    plana = [(g, sl, t) for g, aulas in TRILHA for sl, t in aulas]
    total = len(plana)
    pos = next((i for i, (_, sl, _) in enumerate(plana) if sl == slug_atual), None)
    if pos is None:
        return ""                      # pagina fora da trilha: sem barra

    partes = ['<aside class="trilha">',
              '<div class="trilha-cab">Aula %d de %d</div>' % (pos + 1, total),
              '<div class="trilha-agora">%s</div>' % plana[pos][2]]
    grupo_aberto = None
    for i, (grupo, sl, titulo) in enumerate(plana):
        if grupo != grupo_aberto:
            if grupo_aberto is not None:
                partes.append('</ol>')
            if grupo:
                partes.append('<div class="trilha-grupo">%s</div>' % grupo)
            partes.append('<ol>')
            grupo_aberto = grupo
        if i < pos:
            estado, marca = "feita", "&#10003;"
        elif i == pos:
            estado, marca = "agora", "%02d" % (i + 1)
        else:
            estado, marca = "", "%02d" % (i + 1)
        n = '<span class="tl-n">%s</span>' % marca
        if i == pos:
            corpo = '<span class="tl">%s<span>%s</span></span>' % (n, titulo)
        else:
            href = "../%s/" % sl if sl != "index" else "../"
            corpo = '<a href="%s">%s<span>%s</span></a>' % (href, n, titulo)
        partes.append('<li class="%s">%s</li>' % (estado, corpo))
    partes.append('</ol></aside>')
    return "".join(partes)


def rodape(slug):
    """O par anterior/proxima, tirado da SEQUENCIA. Ponta sem vizinho fica vazia.

    Nunca inventa destino: se a pagina e a primeira, nao existe "anterior", e
    o lado fica em branco em vez de apontar para a propria pagina.
    """
    if slug not in SEQUENCIA:
        return ""
    i = SEQUENCIA.index(slug)
    # 🔴 A capa mora na RAIZ; as outras cinco moram um nivel abaixo. O caminho
    # relativo depende de onde a pagina ATUAL esta, nao de onde o alvo esta.
    # O gate G7 pegou isto na primeira rodada: da capa, "../modulo/" sai do site.
    base = "" if slug == "index" else "../"
    def href(s):
        return base if s == "index" else base + "%s/" % s
    lados = []
    if i > 0:
        alvo = SEQUENCIA[i - 1]
        lados.append('<a href="%s">&larr; %s</a>' % (href(alvo), PAGINAS[alvo]["titulo"]))
    else:
        lados.append("<span></span>")
    if i < len(SEQUENCIA) - 1:
        alvo = SEQUENCIA[i + 1]
        lados.append('<a href="%s">%s &rarr;</a>' % (href(alvo), PAGINAS[alvo]["titulo"]))
    else:
        lados.append("<span></span>")
    return '<nav class="rodape-nav">%s</nav>' % "".join(lados)


def secoes(fragmento):
    """A nav lateral sai das seções do fragmento, nunca de uma lista à mão."""
    padrao = re.compile(
        r'<section class="secao" id="(?P<id>[^"]+)"[^>]*>\s*'
        r'<div class="secao-topo">\s*'
        r'<div class="secao-n">(?P<n>.*?)</div>.*?'
        r'<h2>(?P<h2>.*?)</h2>',
        re.S,
    )
    return [(m.group("id"),
             SEM_TAG.sub("", m.group("n")).strip(),
             SEM_TAG.sub("", m.group("h2")).strip())
            for m in padrao.finditer(fragmento)]


def nome_curto(slug):
    """O nome curto da pagina, lido da TRILHA.

    🔴 UMA FONTE SO, e a razao e um defeito real. Ate 31/08 o nome da aula
    existia em tres lugares escritos a mao -- TRILHA, h1 e o ultimo item da
    migalha. Os nomes foram trocados no h1 e na TRILHA, a migalha ficou para
    tras, e as cinco aulas subiram com o nome velho na navegacao e o novo no
    titulo, na mesma tela. String repetida a mao diverge; derivada, nao.
    """
    for _, grupo in TRILHA:
        for sl, texto in grupo:
            if sl == slug:
                return texto
    return None



def _classe_do_tipo(slug, cfg):
    """A classe do <main>, e a PERGUNTA OBRIGATORIA da aula de pratica.

    🔴 02/09/2026, decisao do Rafael: "nem toda aula pratica tem arquivo. Ela
    precisa de um exercicio pratico. O arquivo pode ou nao existir. Talvez o
    gate seja sempre PERGUNTAR se aquela pratica precisa ou nao de arquivo."

    Ate hoje o G43 EXIGIA .arquivo em toda aula de pratica, e foi essa regra
    que fez a ficha de conferencia da aula 2 nascer: a aula nao precisava de
    planilha nenhuma, o contrato pedia um arquivo, e eu inventei um. Ele leu a
    aula e mandou tirar.

    A pergunta agora e obrigatoria por CONSTRUCAO: aula de pratica sem a chave
    `arquivo` nao gera. Nao ha default -- default e o que deixa a pergunta
    passar em branco no fim de uma sessao longa. O valor viaja para a pagina
    como classe, e o G43 confere o declarado contra o que a pagina tem de fato.
    """
    tipo = cfg.get("tipo")
    if not tipo:
        return ""
    classes = ["aula-" + tipo]
    if tipo == "pratica":
        if "arquivo" not in cfg:
            raise SystemExit(
                "\n🔴 {}: aula de PRATICA sem declarar `arquivo`.\n"
                "   Toda pratica responde a pergunta: esta aula entrega um\n"
                "   arquivo para o aluno baixar?\n"
                "     arquivo=True   ha .arquivo na pagina\n"
                "     arquivo=False  o exercicio se faz sem arquivo nenhum\n"
                "   Nao ha default: a pergunta e a regra.".format(slug))
    return " ".join(classes)


def _dado_do_arquivo(cfg):
    """A resposta da pergunta, como DADO e nao como estilo.

    Foi classe por dez minutos e o G6 acusou sete "classe sem CSS", com razao:
    classe e para pintar. Isto e declaracao, e declaracao mora em data-.
    """
    if cfg.get("tipo") != "pratica":
        return ""
    return ' data-arquivo="%s"' % ("sim" if cfg["arquivo"] else "nao")


def monta(slug, cfg, fragmento):
    selos = "".join('<span class="selo">%s</span>' % s for s in cfg.get("selos", []))
    if cfg.get("migalha"):
        pedacos = []
        migalha_cfg = list(cfg["migalha"])
        # (None, None) no fim = "use o nome curto da TRILHA"
        if migalha_cfg and migalha_cfg[-1] == (None, None):
            curto = nome_curto(slug)
            if curto is None:
                raise SystemExit(
                    "gerar.py: %s pede o nome curto da TRILHA e nao esta nela. "
                    "Ou entra na TRILHA, ou escreve o nome na migalha." % slug)
            migalha_cfg[-1] = (None, curto)
        for href, texto in migalha_cfg:
            pedacos.append('<a href="%s">%s</a>' % (href, texto) if href else texto)
        migalha = '<nav class="migalha">%s</nav>' % " &rsaquo; ".join(pedacos)
    else:
        migalha = ""
    raiz = "./" if slug == "index" else "../"
    # a barra so existe se a pagina estiver na trilha; sem ela, o wrapper de
    # duas colunas nao entra e o layout fica exatamente como era
    # 🔴 SEM BARRA LATERAL, e a razao e medida (29/08).
    # A regra .com-trilha .solta zera o breakout (width:auto, transform:none).
    # Com a barra ligada, 10 das 14 paginas deste curso tinham 65 FIGURAS
    # LARGAS DESLIGADAS -- 18 so nas cinco aulas do bloco 1. Toda figura
    # escrita como larga renderizava na largura da coluna, e o autor abriu o
    # site e disse que nao aproveitava o espaco. Ele estava certo.
    # A navegacao nao se perde: sobra a migalha, o .rodape-nav, e a pagina de
    # bloco, que da o mesmo indice que a barra dava.
    barra = ""
    abre = fecha = ""
    return TEMPLATE % dict(
        titulo=cfg["titulo"], css=css(), raiz=raiz,
        sigla=CURSO["sigla"], nome=CURSO["nome"], sub=CURSO["sub"],
        migalha=migalha, kicker=cfg["kicker"], h1=cfg["h1"],
        # aula-pratica ou aula-fundamento. Pagina que nao e aula fica sem.
        tipo=_classe_do_tipo(slug, cfg),
        dado_arquivo=_dado_do_arquivo(cfg),
        sub_pagina=cfg["sub"], selos=selos, corpo=fragmento,
        abre_trilha=abre, fecha_trilha=fecha, rodape=rodape(slug),
    )


TEMPLATE = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titulo)s</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
%(css)s
</style>
</head>
<body>

<header class="topo">
  <div class="topo-in">
    <a href="%(raiz)s" class="marca">
      <div class="marca-sigla">%(sigla)s</div>
      <div>
        <div class="marca-nome">%(nome)s</div>
        <div class="marca-sub">%(sub)s</div>
      </div>
    </a>
  </div>
</header>

%(migalha)s

%(abre_trilha)s
<main class="folha %(tipo)s"%(dado_arquivo)s>
  <div class="heroi">
    <div class="heroi-kicker">%(kicker)s</div>
    <h1>%(h1)s</h1>
    <p class="heroi-sub">%(sub_pagina)s</p>
    <div>%(selos)s</div>
  </div>

%(corpo)s
%(rodape)s
</main>
%(fecha_trilha)s

<script>
(function(){
  'use strict';

  /* Confirmação no proprio botao. Toast flutuante exige posicao fixa e some
     atras do teclado no celular, que e onde o aluno mais copia. */
  function avisa(b, texto){
    if(b.dataset.antes === undefined) b.dataset.antes = b.textContent;
    b.textContent = texto;
    clearTimeout(b._t);
    b._t = setTimeout(function(){ b.textContent = b.dataset.antes; }, 1600);
  }

  function copia(b, texto){
    if(!texto) return;
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(texto).then(function(){ avisa(b, 'copiado'); },
                                               function(){ avisa(b, 'nao deu'); });
      return;
    }
    /* Sem clipboard (http em rede da sala, navegador antigo) o botao nao pode
       simplesmente nao fazer nada: seleciona o texto para o aluno usar Ctrl+C. */
    var t = document.createElement('textarea');
    t.value = texto; t.setAttribute('readonly','');
    t.style.position='fixed'; t.style.opacity='0';
    document.body.appendChild(t); t.select();
    try{ document.execCommand('copy'); avisa(b, 'copiado'); }
    catch(e){ avisa(b, 'use ctrl+c'); }
    document.body.removeChild(t);
  }

  /* ---- prompt copiavel ---- */
  document.querySelectorAll('.btn-copiar[data-alvo]').forEach(function(b){
    b.addEventListener('click', function(){
      var alvo = document.getElementById(b.dataset.alvo);
      if(alvo) copia(b, alvo.textContent.trim());
    });
  });

  /* ---- o aprofundamento ----
     O <dialog> nativo precisa de showModal() para virar modal de verdade: sem
     ele o navegador so mostra a caixa no fluxo, sem foco preso e sem Esc.
     Sao seis linhas e nao ha alternativa sem script.

     ATENCAO: se o script nao rodar, o botao nao abre nada -- e por isso o
     CONTEUDO mora no HTML e a impressao o revela. Modal e a comodidade;
     o conteudo nunca depende dela. */
  document.querySelectorAll('.aprofunda-abrir[data-alvo]').forEach(function(b){
    b.addEventListener('click', function(){
      var d = document.getElementById(b.dataset.alvo);
      if(d && d.showModal) d.showModal();
    });
  });
  document.querySelectorAll('.aprofunda-fechar').forEach(function(b){
    b.addEventListener('click', function(){
      var d = b.closest('dialog');
      if(d) d.close();
    });
  });
  /* clicar fora fecha: o alvo do clique e o proprio dialog quando ele cai no
     backdrop, porque o miolo esta dentro de .aprofunda-corpo */
  document.querySelectorAll('dialog.aprofunda').forEach(function(d){
    d.addEventListener('click', function(e){ if(e.target === d) d.close(); });
  });

  /* ---- imprimir o documento ----
     A pagina de exemplo pronto imprime em A4 sem levar o site junto: o CSS de
     impressao esconde a moldura, e este botao so dispara o dialogo. */
  document.querySelectorAll('[data-acao="imprimir"]').forEach(function(b){
    b.addEventListener('click', function(){ window.print(); });
  });

  /* ---- o criador de prompt ----
     O texto a direita nasce dos proprios campos: nao existe uma segunda copia
     do prompt no HTML para sair de sincronia com a esquerda. */
  function escapa(s){
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  document.querySelectorAll('.criador').forEach(function(c){
    var campos = [].slice.call(c.querySelectorAll('textarea[data-titulo]'));
    var saida  = c.querySelector('.cr-txt');
    if(!campos.length || !saida) return;
    var exemplo = campos.map(function(t){ return t.value; });

    function texto(){
      return campos.filter(function(t){ return t.value.trim(); })
                   .map(function(t){ return '# ' + t.dataset.titulo + '\n' + t.value.trim(); })
                   .join('\n\n');
    }
    function pinta(){
      var t = texto();
      if(!t){
        saida.innerHTML = '<span class="cr-vazio">Preencha um campo à esquerda '
                        + 'e o prompt aparece aqui.</span>';
        return;
      }
      saida.innerHTML = escapa(t).replace(/^# (.+)$/gm, '<span class="cr-h"># $1</span>');
    }

    campos.forEach(function(t){ t.addEventListener('input', pinta); });
    c.querySelectorAll('[data-acao]').forEach(function(b){
      b.addEventListener('click', function(){
        var a = b.dataset.acao;
        if(a === 'copiar'){ copia(b, texto()); return; }
        if(a === 'limpar')  campos.forEach(function(t){ t.value = ''; });
        if(a === 'exemplo') campos.forEach(function(t, i){ t.value = exemplo[i]; });
        pinta();
      });
    });
    pinta();
  });

  /* ---- o canvas preenchivel ----
     Guarda no proprio aparelho. Nada sai daqui: nao ha envio, e o aviso na tela
     diz isso, senao metade da sala acha que mandou para alguem. */
  document.querySelectorAll('.canvas[data-chave]').forEach(function(c){
    var campos = [].slice.call(c.querySelectorAll('textarea[id]'));
    var estado = c.querySelector('.canvas-estado');
    var chave  = 'trn_' + c.dataset.chave;
    if(!campos.length) return;

    function diz(txt, ok){
      if(!estado) return;
      estado.textContent = txt;
      estado.classList.toggle('salvo', !!ok);
    }
    function salva(){
      var d = {};
      campos.forEach(function(t){ d[t.id] = t.value; });
      try{
        localStorage.setItem(chave, JSON.stringify(d));
        diz('Rascunho salvo neste aparelho', true);
      }catch(e){
        diz('Este navegador nao deixa salvar rascunho', false);
      }
    }
    function carrega(){
      try{
        var d = JSON.parse(localStorage.getItem(chave) || '{}');
        var achou = false;
        campos.forEach(function(t){
          if(d[t.id]){ t.value = d[t.id]; achou = true; }
        });
        if(achou) diz('Rascunho salvo neste aparelho', true);
      }catch(e){}
    }
    /* TAB entre campos, ponto medio no lugar da quebra: um campo de duas linhas
       viraria duas linhas na planilha e desalinharia a turma inteira. */
    function linha(){
      return campos.map(function(t){
        return t.value.replace(/\t/g,' ').replace(/\r?\n/g,' · ').trim();
      }).join('\t');
    }

    campos.forEach(function(t){ t.addEventListener('input', salva); });
    c.querySelectorAll('[data-acao]').forEach(function(b){
      b.addEventListener('click', function(){
        if(b.dataset.acao === 'linha'){ copia(b, linha()); return; }
        if(b.dataset.acao === 'apagar'){
          campos.forEach(function(t){ t.value = ''; });
          try{ localStorage.removeItem(chave); }catch(e){}
          diz('O rascunho fica salvo neste aparelho', false);
        }
      });
    });
    carrega();
  });
})();
</script>
</body>
</html>
"""


def main():
    for slug, cfg in PAGINAS.items():
        fonte = os.path.join(AQUI, "conteudo", slug + ".html")
        if not os.path.exists(fonte):
            print("  pulou:   %s (sem fragmento)" % slug)
            continue
        fragmento = io.open(fonte, encoding="utf-8").read()
        html = monta(slug, cfg, fragmento)
        html = desenha_radar(expande_o_cem(html))
        html = cola_quebra_de_linha(uma_frase_por_linha(html))
        destino = (os.path.join(RAIZ, "index.html") if slug == "index"
                   else os.path.join(RAIZ, slug, "index.html"))
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with io.open(destino, "w", encoding="utf-8") as f:
            f.write(html)
        print("  gravado: %-34s %d bytes"
              % (os.path.relpath(destino, RAIZ), len(html.encode("utf-8"))))
    print("\n  %d páginas" % len(PAGINAS))


if __name__ == "__main__":
    main()
