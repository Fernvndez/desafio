import json, shutil, tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from comissoes import calcular_comissao, calcular_por_vendedor
from estoque import Deposito, ErroEstoque
from juros import calcular_juros

BASE = Path(__file__).parent


def test_faixas_de_comissao():
    assert calcular_comissao(Decimal("99.99")) == 0
    assert calcular_comissao(Decimal("100")) == Decimal("1.00")
    assert calcular_comissao(Decimal("499.99")) == Decimal("4.9999")
    assert calcular_comissao(Decimal("500")) == Decimal("25.00")


def test_comissao_total_vendedores():
    vendas = json.loads((BASE / "vendas.json").read_text(encoding="utf-8"))["vendas"]
    r = calcular_por_vendedor(vendas)
    assert set(r) == {"João Silva", "Maria Souza", "Carlos Oliveira", "Ana Lima"}
    # confere João manualmente: 5% das vendas >= 500 + 1% das de 100..499
    esperado = sum(Decimal(str(v["valor"])) * Decimal("0.05") for v in vendas
                   if v["vendedor"] == "João Silva" and v["valor"] >= 500)
    esperado += sum(Decimal(str(v["valor"])) * Decimal("0.01") for v in vendas
                    if v["vendedor"] == "João Silva" and 100 <= v["valor"] < 500)
    assert r["João Silva"]["comissao"] == esperado.quantize(Decimal("0.01"))


@pytest.fixture
def dep(tmp_path):
    shutil.copy(BASE / "estoque.json", tmp_path / "estoque.json")
    return Deposito(tmp_path / "estoque.json", tmp_path / "movs.json")


def test_entrada_saida_e_ids_unicos(dep):
    m1 = dep.movimentar(101, "E", 50, "Compra")
    m2 = dep.movimentar(101, "S", 20, "Venda")
    assert m1["estoqueFinal"] == 200 and m2["estoqueFinal"] == 180
    assert m1["id"] != m2["id"]


def test_persistencia_mantem_ids(dep, tmp_path):
    dep.movimentar(102, "E", 5, "Compra")
    novo = Deposito(tmp_path / "estoque.json", tmp_path / "movs.json")
    assert novo.movimentar(102, "S", 1, "Venda")["id"] == 2


def test_validacoes(dep):
    with pytest.raises(ErroEstoque): dep.movimentar(101, "S", 9999, "Venda")
    with pytest.raises(ErroEstoque): dep.movimentar(999, "E", 1, "Compra")
    with pytest.raises(ErroEstoque): dep.movimentar(101, "E", 0, "Compra")
    with pytest.raises(ErroEstoque): dep.movimentar(101, "X", 1, "Compra")


def test_juros():
    r = calcular_juros(Decimal("1000"), date(2026, 9, 28), hoje=date(2026, 10, 3))
    assert r["dias_atraso"] == 5 and r["juros"] == Decimal("125.00")
    assert calcular_juros(Decimal("1000"), date(2026, 10, 3), date(2026, 10, 3))["juros"] == 0
    assert calcular_juros(Decimal("1000"), date(2026, 11, 1), date(2026, 10, 3))["juros"] == 0
