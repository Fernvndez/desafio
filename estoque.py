"""Exercício 2 - Movimentação de estoque.

Cada movimentação tem um ID único (sequencial, persistido) e uma descrição
do tipo de movimentação. Ao final, é exibida a quantidade final do produto.

Arquivos:
  estoque.json        -> saldo atual dos produtos (atualizado a cada movimentação)
  movimentacoes.json  -> histórico de movimentações

Uso interativo: python estoque.py
"""
import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent
ARQ_ESTOQUE = BASE / "estoque.json"
ARQ_MOVS = BASE / "movimentacoes.json"


class ErroEstoque(Exception):
    pass


class Deposito:
    def __init__(self, arq_estoque: Path = ARQ_ESTOQUE, arq_movs: Path = ARQ_MOVS):
        self.arq_estoque = arq_estoque
        self.arq_movs = arq_movs
        with open(arq_estoque, encoding="utf-8") as f:
            self.produtos = {p["codigoProduto"]: p for p in json.load(f)["estoque"]}
        self.movimentacoes = []
        if arq_movs.exists():
            with open(arq_movs, encoding="utf-8") as f:
                self.movimentacoes = json.load(f)

    def _proximo_id(self) -> int:
        return max((m["id"] for m in self.movimentacoes), default=0) + 1

    def _salvar(self) -> None:
        with open(self.arq_estoque, "w", encoding="utf-8") as f:
            json.dump({"estoque": list(self.produtos.values())}, f, ensure_ascii=False, indent=2)
        with open(self.arq_movs, "w", encoding="utf-8") as f:
            json.dump(self.movimentacoes, f, ensure_ascii=False, indent=2)

    def movimentar(self, codigo: int, tipo: str, quantidade: int, descricao: str) -> dict:
        """Registra uma entrada ('E') ou saída ('S') e devolve a movimentação."""
        tipo = tipo.strip().upper()[:1]
        if tipo not in ("E", "S"):
            raise ErroEstoque("Tipo inválido: use 'E' (entrada) ou 'S' (saída).")
        if codigo not in self.produtos:
            raise ErroEstoque(f"Produto {codigo} não encontrado.")
        if quantidade <= 0:
            raise ErroEstoque("A quantidade deve ser maior que zero.")
        if not descricao.strip():
            raise ErroEstoque("Informe a descrição da movimentação.")

        produto = self.produtos[codigo]
        if tipo == "S" and quantidade > produto["estoque"]:
            raise ErroEstoque(
                f"Estoque insuficiente: há {produto['estoque']} un. e foram solicitadas {quantidade}."
            )

        produto["estoque"] += quantidade if tipo == "E" else -quantidade
        mov = {
            "id": self._proximo_id(),
            "data": datetime.now().isoformat(timespec="seconds"),
            "codigoProduto": codigo,
            "tipo": "ENTRADA" if tipo == "E" else "SAIDA",
            "quantidade": quantidade,
            "descricao": descricao.strip(),
            "estoqueFinal": produto["estoque"],
        }
        self.movimentacoes.append(mov)
        self._salvar()
        return mov


def _ler_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número inteiro.")


def main() -> None:
    dep = Deposito()
    print("=== Movimentação de Estoque ===")
    while True:
        print("\nProdutos:")
        for p in dep.produtos.values():
            print(f"  {p['codigoProduto']} - {p['descricaoProduto']} (estoque: {p['estoque']})")
        codigo = _ler_int("\nCódigo do produto (0 para sair): ")
        if codigo == 0:
            break
        tipo = input("Tipo [E]ntrada / [S]aída: ")
        qtd = _ler_int("Quantidade: ")
        desc = input("Descrição da movimentação (ex.: Compra, Venda, Devolução, Perda): ")
        try:
            mov = dep.movimentar(codigo, tipo, qtd, desc)
        except ErroEstoque as e:
            print(f"Erro: {e}")
            continue
        nome = dep.produtos[codigo]["descricaoProduto"]
        print(f"\nMovimentação #{mov['id']} registrada ({mov['tipo']} - {mov['descricao']}).")
        print(f"Quantidade final de '{nome}' em estoque: {mov['estoqueFinal']}")


if __name__ == "__main__":
    main()
