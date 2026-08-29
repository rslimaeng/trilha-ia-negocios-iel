# IA para Negócios · Trilha Completa · IEL Ceará

Material do aluno da formação **IA para Negócios**, do IEL Ceará. Turma de
31/08/2026, online ao vivo, 19h às 22h, com mentoria em grupo depois do último
encontro.

> [!warning] Carga não entra na tela do aluno
> Decisão do Rafael, 29/08. **Nenhuma página deste site declara carga horária**,
> nem do curso nem de bloco. O tempo de cada assunto depende da aula: o n8n leva
> mais do que a ementa previu, porque começa em criar conta e aprender a
> interface, e a parte de pesquisa e análise leva menos. Selo de hora vira
> promessa que o calendário não sustenta.

**No ar:** https://rslimaeng.github.io/trilha-ia-negocios-iel/

## O que está pronto

| Encontro | Aulas | Estado |
|---|---|---|
| **1 · 31/08 · Mentalidade e Fundamentos** | 5 | ✅ publicadas |
| 2 em diante | — | em produção |

As cinco aulas do primeiro encontro:

1. **Em que degrau você está** · o diagnóstico dos 7 níveis e a escolha da rotina
2. **A IA não sabe, ela prevê** · por que a mesma pergunta volta diferente
3. **A mesa: o que ela tem à vista** · a janela de contexto, e por que o combinado cai
4. **Quando ela inventa com o mesmo tom** · a alucinação, e conferir contra trabalho fechado
5. **O que não entra no chat** · quatro perguntas que decidem se um dado pode ir

## Como o material nasce

Este site é gerado pelo **padrão de treinamentos**, e não editado à mão. O
roteiro é o [`COMO-EXECUTAR.md`](./COMO-EXECUTAR.md) desta pasta.

```bash
python3 _build/gerar.py     # monta as páginas a partir de _build/conteudo/
python3 _build/gates.py     # 41 gates · 410 checagens
```

**Não edite os `index.html`.** Eles são saída. O conteúdo mora em
`_build/conteudo/<slug>.html`, e a ordem das aulas em `_build/gerar.py`.

### A anatomia de uma aula

Oito seções, sempre na mesma ordem: a situação, o conceito, como funciona, a
demonstração, a sua vez, o gabarito, as pegadinhas e a cerca. Entre o gabarito
e as pegadinhas fica **o divisor**, que declara onde a aula acaba e onde começa
o aprofundamento.

Três regras que os gates cobram:

- **Uma aula, um conceito.** Se são dois, são duas aulas.
- **O conceito nasce com a imagem.** Toda analogia é do cotidiano e traz o
  de-para item a item entre a imagem e a coisa real.
- **Todo exercício que pede texto próprio traz destrave**, e o destrave diz o
  que *não* conta como resposta.

## Marca

`_build/marca.css` carrega as cinco linhas de `--accent` do IEL. O azul
institucional `#164194` mede **9,05:1** sobre o papel do padrão.

🔴 O azul claro `#40B8EB` da faixa do IEL tem **1,95:1**: serve de fundo, nunca
de letra.

---

*Rafael Lima · material de curso, não material de venda.*
