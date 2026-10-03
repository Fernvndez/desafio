"""Exercício 3 - Cálculo de juros por atraso.

A partir de um valor e de uma data de vencimento, calcula o valor dos juros
na data de hoje, considerando taxa de 2,5% ao dia (juros simples):

    juros = valor * 2,5% * dias_em_atraso

Se a data de vencimento for hoje ou futura, não há juros.

Uso: python juros.py            (pergunta valor e vencimento)
     python juros.py 1000 10/09/2026
"""
import sys
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

TAXA_DIARIA = Decimal("0.025")


def calcular_juros(valor: Decimal, vencimento: date, hoje: date | None = None) -> dict:
    hoje = hoje or date.today()
    dias = max((hoje - vencimento).days, 0)
    juros = (valor * TAXA_DIARIA * dias).quantize(Decimal("0.01"), ROUND_HALF_UP)
    return {"dias_atraso": dias, "juros": juros, "total": valor + juros}


def parse_data(texto: str) -> date:
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(texto.strip(), fmt).date()
        except ValueError:
            pass
    raise ValueError("Data inválida. Use DD/MM/AAAA ou AAAA-MM-DD.")


def parse_valor(texto: str) -> Decimal:
    # aceita "1500.50" e "1.500,50"
    t = texto.strip().replace("R$", "").strip()
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    return Decimal(t)


def brl(v: Decimal) -> str:
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main() -> None:
    try:
        if len(sys.argv) >= 3:
            valor, venc = parse_valor(sys.argv[1]), parse_data(sys.argv[2])
        else:
            valor = parse_valor(input("Valor: "))
            venc = parse_data(input("Data de vencimento (DD/MM/AAAA): "))
    except Exception as e:
        sys.exit(f"Entrada inválida: {e}")

    if valor <= 0:
        sys.exit("O valor deve ser maior que zero.")

    r = calcular_juros(valor, venc)
    if r["dias_atraso"] == 0:
        print("Pagamento em dia: sem juros.")
    else:
        print(f"Dias em atraso: {r['dias_atraso']}")
        print(f"Juros (2,5% ao dia): {brl(r['juros'])}")
        print(f"Valor total a pagar: {brl(r['total'])}")


if __name__ == "__main__":
    main()
