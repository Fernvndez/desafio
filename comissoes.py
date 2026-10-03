"""Exercício 1 - Cálculo de comissão por vendedor.

Regra (aplicada a cada venda):
  - valor < 100,00            -> sem comissão
  - 100,00 <= valor < 500,00  -> 1%
  - valor >= 500,00           -> 5%

Uso: python comissoes.py [arquivo.json]
"""
import json
import sys
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CENTAVO = Decimal("0.01")


def calcular_comissao(valor: Decimal) -> Decimal:
    """Comissão de uma única venda."""
    if valor < Decimal("100"):
        return Decimal("0")
    if valor < Decimal("500"):
        return valor * Decimal("0.01")
    return valor * Decimal("0.05")


def calcular_por_vendedor(vendas: list[dict]) -> dict[str, dict[str, Decimal]]:
    """Retorna {vendedor: {'total_vendido': ..., 'comissao': ...}}."""
    resultado = defaultdict(lambda: {"total_vendido": Decimal("0"), "comissao": Decimal("0")})
    for venda in vendas:
        # str() evita erros de ponto flutuante ao converter para Decimal
        valor = Decimal(str(venda["valor"]))
        r = resultado[venda["vendedor"]]
        r["total_vendido"] += valor
        r["comissao"] += calcular_comissao(valor)
    # arredonda só no final, para não acumular erro de arredondamento
    return {
        nome: {k: v.quantize(CENTAVO, ROUND_HALF_UP) for k, v in dados.items()}
        for nome, dados in resultado.items()
    }


def brl(valor: Decimal) -> str:
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main() -> None:
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("vendas.json")
    with open(caminho, encoding="utf-8") as f:
        vendas = json.load(f)["vendas"]

    resultado = calcular_por_vendedor(vendas)
    print(f"{'Vendedor':<18}{'Total vendido':>16}{'Comissão':>14}")
    print("-" * 48)
    for nome, d in resultado.items():
        print(f"{nome:<18}{brl(d['total_vendido']):>16}{brl(d['comissao']):>14}")


if __name__ == "__main__":
    main()
