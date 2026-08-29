# COMO EXECUTAR

> **Este arquivo é o roteiro. O `CLAUDE.md` é a referência.**
> Leia este primeiro, do começo ao fim. Ele diz o que fazer, em que ordem, e manda
> você ao `CLAUDE.md` quando precisar do detalhe.

Ele existe porque as três coisas do padrão viviam separadas: a andragogia dizia *por
quê*, a vitrine mostrava *o que existe*, e a regra do diagrama dizia *como desenhar*.
Faltava dizer **na seção 03 você precisa de imagem, e destas seis figuras a certa é
esta**. É isso aqui.

---

## O ciclo de trabalho, em uma tela

```
 pasta do cliente
        ↓
 [0] inventariar a pasta   python3 _build/entrada.py <pasta do cliente>
     e ler o padrão        CLAUDE.md inteiro + abrir a vitrine no navegador
        ↓
 [1] recortar em aulas     e mostrar o recorte ANTES de escrever
        ↓
 [2] preparar UMA aula     o GPS no papel, antes de qualquer HTML
        ↓
 [3] escrever o fragmento  _build/conteudo/<slug>.html, seção por seção
        ↓
 [4] escolher cada figura  a árvore do passo 4, e a diagram-design antes de desenhar
        ↓
 [5] gerar o insumo        python3 _build/insumo.py   (se a aula tem exercício)
     gerar e reprovar      python3 _build/gerar.py && python3 _build/gates.py
        ↓
 [6] medir no navegador    1280px e 375px, e só então mostrar ao Rafael
        ↓
 volta ao [2] para a próxima aula
```

🔴 **Uma aula por vez.** Escrever seis aulas e depois rodar os gates é como se descobre
seis vezes o mesmo defeito. A leva é uma aula, do GPS até a medição.

---

## Passo 0 · Antes de escrever uma linha

| # | O que fazer | Por quê |
|---|---|---|
| 0 | **`python3 _build/entrada.py <pasta do cliente>`** | inventaria a pasta, aponta qual versão do documento usar, e lista o que falta antes de escrever |
| 1 | Ler `CLAUDE.md` **inteiro**, com atenção à seção 3 | é o porquê. Sem ele você aplica a regra e erra no caso que ela não previu |
| 2 | Abrir `componentes/index.html` no navegador | **48 seções**, uma por componente — o mesmo 48 do catálogo. Você não vai lembrar deles lendo CSS |
| 2b | **Abrir `aula/index.html`** | é a aula modelo: as oito seções montadas, com a peça de cada uma. Copie de `_build/conteudo/aula.html` e troque o conteúdo. É a página que evita desenhar do zero o que já existe |
| 3 | Se houver briefing, ementa ou transcrição, aplicar a skill `leitura-de-fonte` | material-fonte tem rito próprio, e ele vem antes do entregável |
| 4 | Propor o recorte das aulas e **esperar o OK** | recortar errado custa o curso inteiro; perguntar custa uma mensagem |
| 4b | Com o recorte aprovado, **preencher `TRILHA` no `gerar.py`** | é a ordem das aulas, e ela alimenta a barra lateral de todas as páginas. Sem preencher, a aula sai sem barra e ninguém sabe onde está no curso |
| 4c | Para cada aula, **escrever o `nesta-aula` antes de escrever a aula** | o contrato feito depois vira resumo do que saiu, não promessa do que ia sair. Escrito antes, ele é o filtro: o que não serve a nenhuma das três linhas não entra |
| 4d | **Decidir se o curso tem nível de módulo** | opcional. Serve quando as aulas se agrupam por assunto que vale anunciar sozinho (primeiro a ferramenta, depois o código). Curso curto ou de páginas temáticas vai da capa direto para a aula, e fica melhor. Forçar módulo em curso que não pede deixa uma página vazia entre a pessoa e o conteúdo |
| 4e | **Escrever o `fecho` DEPOIS de escrever a aula** | é o par do `nesta-aula`. O contrato promete, o fecho registra. Escrito antes, vira cópia do contrato e repete o que a pessoa leu quarenta minutos atrás |
| 4f | **Fechar com os TRÊS blocos**: `.checagem`, `.fecho`, `.gancho` | são três momentos, não um. A pessoa confere sozinha, registra o que sabe, e recebe a trava que abre a próxima aula |
| 4g | **Se o curso ensina um produto pelo nome**, declarar em `CURSO["ensina"]` no `gerar.py` | o gate G2 proíbe nome de bastidor na tela, e "Claude Code" está na lista. Num curso que VENDE Claude Code como módulo, o nome é o assunto. Declarar tira só esse termo, e o resto da lista continua valendo |

### O que o `entrada.py` faz, e o que ele não faz

Ele separa duas coisas que a busca por palavra trata igual e não são:

| | |
|---|---|
| **indício** | vocabulário distintivo, com dois sinais diferentes. A ementa e a carga horária a busca prova |
| **PERGUNTE** | nenhuma palavra prova. "marca" tanto é a paleta do cliente quanto "formatação de marca" num guia de prompt. **Estes sempre viram pergunta**, com a pasta cheia ou vazia |

🔴 Ele **não decide e não escreve**. Ele impede o começo cego, que é escrever seis
aulas em cima de uma ementa e descobrir na última que ninguém sabia quem estava na
sala.

E ele aponta **qual versão usar** quando há `v1`, `v2` e `v3` do mesmo documento.
Produzir em cima da versão velha entrega o que o cliente já descartou.

---

## Passo 1 · Recortar o curso em aulas

O recorte é onde o curso se ganha ou se perde, e a régua é uma só:

🔴 **Duas ideias por aula, três no limite.** Se a aula tem quatro, ela vira duas aulas.
O sinal de que passou do teto: você não consegue escrever o título sem usar "e".

**O título da aula diz o assunto da aula.** A pessoa vai voltar procurando semanas
depois; com título vago ela varre o curso inteiro e desiste.

**Cada aula termina numa trava que a próxima resolve.** É isso que faz um curso ser
uma corrente e não uma pilha de páginas. Se você não consegue escrever o gancho, as
duas aulas provavelmente são uma só, ou estão na ordem errada.

Entregue o recorte assim, e pare:

```
Aula 1 · <título>      as 2 ideias: <a>, <b>      trava que fica: <c>
Aula 2 · <título>      resolve <c>, e traz: <d>   trava que fica: <e>
...
```

---

## Passo 2 · Preparar a aula, antes de qualquer HTML

Preencha isto em texto puro. **Não abra o HTML antes de terminar.** Quem escreve HTML
primeiro acaba encaixando a andragogia no que já ficou pronto.

### 2.1 O destino, pela essência

Encadeie cinco "por quê", cada um em cima da resposta anterior:

```
Por que aprender <o tema desta aula>?   → ...
Por que <resposta 1>?                    → ...
Por que <resposta 2>?                    → ...
Por que <resposta 3>?                    → ...
Por que <resposta 4>?                    → ...

ESSÊNCIA (a última resposta) = com o que a seção 01 abre
```

🔴 **A aula abre pela última resposta, não pela primeira.** E em material corporativo,
sem exagero: emoção grande demais soa a folheto e a sala fecha.

### 2.2 A origem

- O que essa pessoa **já sabe** neste ponto do curso
- O que ela **não sabe**, e que a aula não pode assumir
- Que ferramenta ela **já tem instalada** (o exercício não pode pedir outra)

### 2.3 A rota

Liste os conceitos, em ordem, **um por linha**. Se passar de três, volte ao passo 1.
Para cada conceito, a figura que vira imagem dele e o exercício que o fecha.

---

## Passo 3 · A aula, seção por seção

**A tabela mestra.** Cada linha diz: a pergunta que a seção responde, o movimento
andragógico por trás, o que usar, e o que reprova.

| Seção | A pergunta do aluno | O movimento | Componentes | Figuras que servem | O que reprova |
|---|---|---|---|---|---|
| **01** situação | "por que eu deveria ler isto?" | **destino**, escrito pela essência | prosa, `.aviso` | `.cascata` `.cem` `.loops` `.linha-tempo` | abrir pelo técnico ou pela definição |
| **02** conceito | "o que é isso, afinal?" | **um** conceito, **com a analogia junto** | `.conceito` `.analogia` `.contraste` `.cartao` `.grade` `.ctr` `.duo` | `.venn` `.aninhado` `.escada` `.opcoes` + `.resumos` | dois conceitos na mesma aula · **conceito sem imagem** |
| **03** como funciona | **"virou filme na cabeça?"** | a **imagem**. É a seção mais visual do padrão | `.fig-leg` obrigatório, `.anatomia` `.espec` | `.fluxo` `.cadeia` `.ciclo` `.retorno` `.converge` `.arvore` `.raias` | explicar com três parágrafos o que um desenho resolve |
| **04** demonstração | "como é ver isso acontecer?" | **ver antes de fazer** | `.demo` `.tela` `.prompt` `.glosa` `.fonte` | `.gantt` `.raias` `.antes-depois` | mostrar o resultado pronto, sem o caminho |
| **05** sua vez | "e agora eu faço o quê?" | a **prática**, que fecha o ciclo do conceito | `.arquivo` `.passo` `.destrave` `.previa` `.criador` `.canvas` `.perguntas` | `.setor` `.colunas` `.dispersao` `.mapa-area` | pedir o que o aluno ainda não tem |
| **06** confira | "eu acertei?" | a **revisão**, para fixar | `.gabarito` `.checagem` | `.diagnostico` | gabarito aberto: ninguém tenta |
| **🏁** o divisor | "já posso parar?" | onde a **aula acaba** e começa o aprofundamento | `.ate-aqui` `.ate-aqui-nota` | — | a aula inteira chegar como obrigatória |
| **07** pegadinhas | "onde eu vou tropeçar?" | **origem**: os erros de quem parte dali | `.aviso erro` `.diagnostico` | `.antes-depois` `.contraste` | a pessoa descobrir sozinha, três semanas depois |
| **08** a cerca | "quando eu **não** faço isso?" | o **etos**: o limite dito por quem sabe | `.aviso atencao` `.vereditos` `.decide` | `.matriz` `.priorizar` `.radar` | ensinar a fazer sem ensinar quando não fazer |
| **o gancho** | "e depois?" | o **hook** da próxima aula | `.gancho` | | retórica vazia: o gancho é a trava real, não uma promessa |

🔴 **A régua do `.destrave`, que o piloto pagou caro para descobrir.** Todo `.passo`
que pede o aluno a **produzir texto próprio** leva destrave, e todo destrave diz o que
**não conta** como resposta. Sem ele o exercício vira "e agora faça", e metade da sala
responde uma linha achando que respondeu.

Esta linha existe porque a peça **já estava no padrão** e o primeiro curso real nasceu
sem ela: a anatomia mandava o destrave para a seção 07, esta tabela não o citava, o
modelo não o mostrava, e a vitrine o exibia dentro de pergunta de grupo. Quatro
documentos apontando para longe da mesma peça, e o autor teve que reclamar duas vezes.
**O G23 agora varre `.passo` além de `.perguntas`** — antes, exercício sem destrave
passava na suíte inteira sem um achado.

### O conceito nasce com a imagem: a fórmula AIDEN

> **"As pessoas não entendem o que você fala, mas o que elas veem ou o que elas sentem
> quando você fala."** E: **"a imagem vem primeiro, para depois processar o
> entendimento."**

Isso vira estrutura, não conselho. Cinco partes, e você já tinha duas:

| | o que é | peça |
|---|---|---|
| **A** | o conceito técnico, **em uma frase** | `.conceito` |
| **I** | a imagem do cotidiano | `.analogia` |
| **D** | o de-para entre a analogia e a coisa, item a item | `.analogia-mapa` |
| **E** | onde mais aquilo aparece | `.analogia-mais` |
| **N** | o que **não** é | `.contraste` |

🔴 **O erro que isto corrige.** Na aula `n1` do primeiro curso real, a seção de conceito
tinha **632 palavras** e a primeira figura só aparecia na seção seguinte. Seiscentas
palavras de abstração antes de qualquer imagem. O aluno recebe palavra, procura na cabeça
uma imagem do que já conhece, não acha, e para de acompanhar. **A ordem das seções não
tem nada a ver com isso** — o conserto é a imagem entrar junto, não a demonstração subir.

**Como escrever a analogia:**

- **Do cotidiano, não do domínio.** Encomendar uma mesa, esperar o ônibus, montar
  churrasco. Se a analogia precisa de repertório técnico, ela não é analogia.
- **O de-para é obrigatório**, e é ele que separa analogia de enfeite. Cada item da
  imagem aponta para um item da coisa real. Sem isso o aluno acha bonito e não transfere.
- **Não tenha medo do exemplo simples.** Steve Jobs explicava computador como bicicleta
  para a mente; Einstein explicava relatividade com trem e plataforma.
- **A extensão transforma exemplo em princípio.** "Onde mais isso aparece" é o que faz o
  aluno reconhecer o padrão fora da aula.

Forma herdada da fórmula AIDEN, de Adriano de Marqui (*Didática Lendária*). A pesquisa
que a trouxe está em `4-ativo-pedagogico/notas/vault-alan--didatica-e-feynman.md`.
**Medido pelo G41**, que reprova conceito sem analogia e analogia sem de-para.

### Quando o insumo é a rotina do próprio aluno

A linha da seção 05 oferece `.canvas` no lugar do `.arquivo` quando o exercício roda em
cima do trabalho real de quem está na sala. **O que escolher, nesse caso, tem regra** —
e ela é método autoral do Rafael, registrado em
`4-ativo-pedagogico/meu-material/metodo-avaliar-ia-com-trabalho-fechado.md`:

> **O aluno traz um trabalho que ele já entregou e cujo resultado ele conhece.** Não um
> trabalho novo. O relatório do mês que já fechou, não o do mês corrente.

Isso resolve duas coisas de uma vez:

- **O gabarito vem junto.** Sem trabalho fechado, avaliar a saída da IA é julgar no
  escuro: o texto sai plausível e não há contra o quê comparar. Com ele, a seção 06 não
  precisa de uma versão de referência escrita pelo padrão — a referência é o que a
  própria pessoa entregou.
- **A pessoa calibra confiança antes de usar para valer.** Quem começa por um processo
  novo aprende a gostar da resposta, não a avaliá-la.

### O que esta tabela é, e o que ela não alcança

🔴 **Esta tabela é o índice real do padrão.** Peça que não está em nenhuma linha
**não existe na prática**, mesmo estando na vitrine com um comentário bom. Foi o que
aconteceu com `.setor`, `.opcoes` e `.resumos` no primeiro curso: as três só entraram
depois que o autor pediu pelo nome, e uma delas já explicava a própria escolha num
comentário do CSS que ninguém tinha lido.

**O limite, dito na cara:** a vitrine renderiza 387 classes e esta tabela cita 57. As
outras são partes internas de componentes, não peças que alguém escolhe. Não existe
gate para isso — um gate que exigisse as 387 seria impossível de satisfazer, e gate
impossível é gate ignorado. **A defesa aqui é humana:** ao acrescentar peça escolhível
à vitrine, ela entra na linha da seção dela nesta tabela, no mesmo passe.

### Cinco decisões de método que o primeiro curso real produziu

Nasceram no piloto de 27/08 e não estavam escritas em lugar nenhum.

**1 · Nome real no operacional, metáfora onde ela ensina.** Quando o aluno **decide
onde trabalhar**, vale o nome do produto. Onde a metáfora ensina, ela fica inteira e
**o rótulo** carrega o nome real. Trocar o rótulo apaga a imagem sem ensinar nada.

**2 · O insumo se compartilha entre aulas. A demonstração, não.** Duas aulas apontando
para a mesma página de caso deixam o passo a passo ensinando a aula errada.

**3 · Catálogo que o aluno escolhe mora na aula, ao lado do exercício.** A página de
caso é **um** caso. "Quero na aula" é sobre a página que o aluno lê.

**4 · Bloco copiável se gera a partir do arquivo-fonte**, no script que monta a página.
É a cura do acoplamento que o `CLAUDE.md` descreve, e custa dez linhas.

**5 · Proposta ainda não implementada: "resultado esperado" por passo.** O `.passo` não
tem o campo, e é ele que faz o aluno saber que errou **antes** de chegar ao fim. É a
peça que o curso do Couto tem em cada passo do tutorial e o padrão não tem.

### As três regras que atravessam a tabela inteira

**1 · Uma aula, um conceito.** O ciclo de um conceito não se mistura com o do outro
porque **não há outro**: se são dois, são duas aulas.

```
conceito → imagem → prática → link declarado → próximo conceito
```

**Medido pelo G39** desde 28/08. A regra estava escrita aqui e no `CLAUDE.md` desde
sempre, e o primeiro curso real nasceu com **dois conceitos em 9 de 9 aulas** — regra de
prosa não segura. A causa não era desatenção: duas voltas do ciclo não cabiam em oito
seções, então a única saída de quem escrevia era empilhar os conceitos e adiar a prática.

Nunca dois conceitos e um exercício só no fim: a pessoa não consegue separar as peças
e não sabe qual das duas ela não entendeu.

**2 · Nenhuma seção passa de dois parágrafos seguidos sem figura, tabela ou bloco.**
Piso de três figuras por aula. É o equivalente escrito de não falar em um tom só.

**3 · Toda figura leva `.fig-leg` embaixo** dizendo o que a pessoa deveria ter
reparado. Figura sem legenda é enfeite.

---

## Passo 4 · Escolher a figura

🔴 **Antes de desenhar qualquer coisa, carregue a skill `diagram-design`.** Ela decide
o **tipo**; a tabela abaixo diz qual classe do padrão renderiza aquele tipo. Pegue o
raciocínio dela e deixe a pele: a cor e a fonte saem do `marca.css`.

### Primeiro, a pergunta que evita a figura

**Uma tabela de três colunas diz a mesma coisa?** Então é tabela. Desenhar o que uma
tabela resolve é gasto sem retorno, e a `diagram-design` cobra isso.

### Depois, o que você quer que a pessoa veja

| Se você quer mostrar… | A classe |
|---|---|
| que uma coisa vira outra, em ordem | `.cadeia` · `.fluxo` (com ator) |
| que o fim volta e alimenta o começo | `.ciclo` (um ciclo) · `.loops` (com × sem a volta) · `.retorno` (fios que voltam) |
| que vários caminhos dão na mesma exigência | `.converge` |
| que uma coisa **se divide em** partes | `.arvore` |
| que uma coisa está **dentro** de outra | `.aninhado` |
| **quem decide o quê**, e para onde escala | `.organograma` |
| que o trabalho **atravessa áreas** e para nas passagens | `.raias` |
| quanto de cada, num total | `.barra` (segmentada) · `.mapa-area` (o tamanho é o argumento) |
| quanto por etapa, subindo e descendo | `.colunas` |
| uma proporção que surpreende | `.cem` |
| o funil que aperta até uma decisão | `.cascata` |
| duas medidas contínuas ao mesmo tempo | `.dispersao` |
| uma escolha que depende de duas perguntas | `.matriz` · `.priorizar` (com itens dentro) |
| uma escolha com três a cinco perguntas independentes | `.decide` |
| o mesmo item medido em várias frentes | `.radar` |
| o que mudou ao longo do tempo | `.linha-tempo` · `.gantt` (o que anda junto) |
| o que duas coisas têm em comum | `.venn` |
| o antes e o depois | `.antes-depois` · `.demo` (A/B) · `.contraste` |
| **o que quebrou, por quê, e como consertar** | `.diagnostico` |
| níveis que dependem do anterior | `.escada` |
| três opções, uma recomendada | `.opcoes` |

**Faltou o tipo que você quer?** Componha com os tokens e crie a classe nova no
`base.css`, com `var()` e nada mais. O padrão é piso, não jaula.

### As regras de desenho que valem sempre

- **A melhor jogada costuma ser apagar.** Dois nós que sempre andam juntos são um só
- **Densidade 4 de 10.** Acima de nove nós, provavelmente são dois diagramas
- **Destaque em um ou dois nós**, no `--accent`. Cinco destaques apagam o sinal
- **Conector em ângulo reto, nunca diagonal.** Nenhum fio passa por trás de caixa que
  não é ponta dele, e dois fios nunca se sobrepõem
- **Grade com número variável de colunas usa `minmax(0,1fr)`**, nunca `1fr` puro
- **Figura de escolha mostra o custo dos dois lados.** Só o lado bom é propaganda

---

## Passo 5 · A página de caso

Quando o exercício é grande o bastante para ter página própria. **Cinco passos, os
mesmos títulos, sempre nesta ordem:**

| # | O título, literal | O que entra |
|---|---|---|
| 01 | Descreva a tarefa | o problema real, e quem enfrenta na rotina |
| 02 | Dê o contexto que a IA precisa | o que ela precisa para não devolver genérico |
| 03 | Baixe o insumo | o `.xlsx` ou `.docx`, com o aviso de dados fictícios |
| 04 | Cole o prompt no chat | quatro parágrafos: `Anexei` · `O que eu preciso:` · `Restrições:` · `Na dúvida:` |
| 05 | **O que esperar** | a **prévia do resultado**, antes de rodar |

🔴 **O passo 5 é o que separa o material de uma lista de prompts.** Miniatura desenhada
à esquerda, o que vem dentro dela à direita, e o callout "depois de gerar · como
refinar" no fim.

### O insumo sai do gerador, não da mão

```bash
python3 _build/insumo.py
```

A especificação mora no topo do arquivo: as colunas, o volume, e **as armadilhas
declaradas por nome**. O gerador grava o `.xlsx` em `_arquivos/`, escreve o
`_build/insumos.json`, e **imprime o que cada armadilha ensina**, porque esse texto
precisa reaparecer no material.

🔴 **O prompt do passo 4 cita as colunas do insumo, e o G32 confere o par.** Ele pega
quatro coisas: o arquivo que sumiu do disco, o número de linhas que a página inventou,
o número de abas errado, e a coluna citada no prompt que não existe em aba nenhuma.

🔴 **Tudo com semente fixa.** Sem isso cada execução gera uma planilha diferente, a
turma recebe arquivos que não batem entre si, e o gabarito deixa de valer.

Depois do passo 5, e só depois, o link para a **página de exemplo pronto**.

---

## Passo 6 · Fechar a leva

```bash
python3 _build/gerar.py     # monta as páginas
python3 _build/gates.py     # reprova o que quebrou
```

**Exit code sozinho não é prova.** Leia a saída: ela imprime achado por gate e diz
quais gates não se provaram contra o próprio defeito injetado.

Depois, **no navegador**, porque três defeitos desta pasta passaram por todos os gates
e só a medição pegou:

| Medir | O que já quebrou aqui |
|---|---|
| rolagem lateral a **375px** | `1fr` que não encolhe fez a página inteira rolar de lado |
| rolagem lateral a **1280px** | breakout que estoura a coluna |
| geometria da figura | grid que posiciona sozinho saiu em escada; `gap` diferente fez o fio apontar para a caixa errada |
| texto dentro de `<svg>` | o `<svg>` **recorta** o que passa da moldura, sem erro e sem console |

🔴 **Confira `window.innerWidth` antes de acreditar em qualquer medida.** Painel oculto
devolve largura zero, e todo número medido nesse estado é lixo.

Só então mostre ao Rafael.

---

## O que reprova, numa lista

Se qualquer uma destas for verdade, a aula volta:

- [ ] abriu pelo técnico, sem ter feito as cinco perguntas
- [ ] mais de três conceitos, ou dois conceitos com um exercício só
- [ ] menos de três figuras, ou figura sem `.fig-leg`
- [ ] o exercício pede o que o aluno ainda não tem naquele ponto
- [ ] o gabarito nasce aberto, ou promete resposta única
- [ ] tem travessão, minutagem, direção de cena ou nome de outro cliente
- [ ] tem cor escrita fora do `marca.css`
- [ ] o prompt cita coluna que você não conferiu no insumo
- [ ] você desenhou sem ter carregado a `diagram-design`
- [ ] você não mediu a página no navegador
