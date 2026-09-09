# -*- coding: utf-8 -*-
"""Empacota a habilidade do caso do B4 no .zip que a pessoa sobe.

🔴 O ARQUIVO EMPACOTADO E O ENTREGAVEL, e por isso ele nao se monta a mao.
A fonte e `_arquivos/conferir-contra-tabela/skill.md`; este script so fecha o
.zip em volta dela, com a PASTA NA RAIZ.

A forma do pacote vem do material oficial do Claude, capturado em 03/09/2026:
o .zip contem a pasta da habilidade como raiz, e nao os arquivos soltos; o
nome da pasta casa com o nome da habilidade; e o arquivo obrigatorio dentro
dela e o `skill.md`, com frontmatter de `name` e `description`.

Rodar:  python3 _build/insumo-skill.py
"""
import os
import re
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA = "conferir-contra-tabela"
FONTE = os.path.join(RAIZ, "_arquivos", PASTA, "skill.md")
SAIDA = os.path.join(RAIZ, "_arquivos", PASTA + ".zip")

# Os dois tetos declarados na fonte oficial. Nao sao chute nosso: se um dia
# mudarem, a conferencia abaixo acusa antes de a aula mentir na tela.
TETO_NOME = 64
TETO_DESCRICAO = 200


def campos(texto):
    fm = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    if not fm:
        raise SystemExit("skill.md sem frontmatter: o arquivo precisa de name e description")
    fora = {}
    for linha in fm.group(1).splitlines():
        if ":" in linha:
            k, v = linha.split(":", 1)
            fora[k.strip()] = v.strip()
    return fora


def main():
    texto = open(FONTE, encoding="utf-8").read()
    c = campos(texto)
    for chave in ("name", "description"):
        if not c.get(chave):
            raise SystemExit("skill.md sem o campo obrigatorio %r" % chave)
    if c["name"] != PASTA:
        raise SystemExit("o name (%r) precisa casar com a pasta (%r)" % (c["name"], PASTA))
    if len(c["name"]) > TETO_NOME:
        raise SystemExit("name com %d caracteres, e o teto e %d" % (len(c["name"]), TETO_NOME))
    if len(c["description"]) > TETO_DESCRICAO:
        raise SystemExit("description com %d caracteres, e o teto e %d"
                         % (len(c["description"]), TETO_DESCRICAO))

    with zipfile.ZipFile(SAIDA, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(FONTE, os.path.join(PASTA, "skill.md"))

    print("  name:        %-40s %d de %d caracteres" % (c["name"], len(c["name"]), TETO_NOME))
    print("  description: %d de %d caracteres" % (len(c["description"]), TETO_DESCRICAO))
    print("  raiz do zip: %s/" % PASTA)
    print("  gravado:     _arquivos/%s.zip  (%d bytes)" % (PASTA, os.path.getsize(SAIDA)))


if __name__ == "__main__":
    main()
