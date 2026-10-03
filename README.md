# Desafio Técnico – Python

Solução dos três exercícios do desafio: cálculo de comissões, movimentação de estoque e cálculo de juros por atraso.

## Requisitos

- Python 3.10 ou superior
- Nenhuma biblioteca externa para executar os programas
- `pytest` apenas para rodar os testes (opcional)

## Estrutura do projeto

```
.
├── comissoes.py        # Exercício 1 – comissão por vendedor
├── estoque.py          # Exercício 2 – movimentação de estoque
├── juros.py            # Exercício 3 – juros por atraso
├── vendas.json         # Dados do exercício 1
├── estoque.json        # Dados do exercício 2 (saldo atual dos produtos)
├── test_desafio.py     # Testes automatizados
└── README.md
```

## Como executar

### Exercício 1 – Comissões

```bash
python comissoes.py
```

Lê o `vendas.json` e calcula a comissão de cada vendedor. A regra é aplicada **venda a venda**:

| Valor da venda | Comissão |
|---|---|
| Abaixo de R$ 100,00 | Sem comissão |
| De R$ 100,00 a R$ 499,99 | 1% |
| A partir de R$ 500,00 | 5% |

Resultado com os dados do desafio:

| Vendedor | Total vendido | Comissão |
|---|---|---|
| João Silva | R$ 10.754,70 | R$ 495,68 |
| Maria Souza | R$ 9.874,30 | R$ 465,95 |
| Carlos Oliveira | R$ 7.928,35 | R$ 379,37 |
| Ana Lima | R$ 8.763,95 | R$ 404,98 |

Também é possível informar outro arquivo: `python comissoes.py outro_arquivo.json`.

### Exercício 2 – Movimentação de estoque

```bash
python estoque.py
```

Programa interativo no terminal. Para cada movimentação, informe:

1. O código do produto (digite `0` para sair)
2. O tipo: `E` (entrada) ou `S` (saída)
3. A quantidade
4. Uma descrição do tipo de movimentação (ex.: *Compra*, *Venda*, *Devolução*, *Perda*)

Cada movimentação recebe um **ID único e sequencial**, e ao final o programa mostra a **quantidade final** do produto movimentado.

Exemplo:

```
Código do produto (0 para sair): 101
Tipo [E]ntrada / [S]aída: E
Quantidade: 50
Descrição da movimentação: Compra de fornecedor

Movimentação #1 registrada (ENTRADA - Compra de fornecedor).
Quantidade final de 'Caneta Azul' em estoque: 200
```

Persistência:

- O saldo dos produtos é atualizado no `estoque.json`.
- O histórico é gravado em `movimentacoes.json` (criado automaticamente), o que mantém os IDs únicos entre execuções.

Validações: tipo inválido, produto inexistente, quantidade menor ou igual a zero, descrição vazia e saída maior que o saldo disponível.

### Exercício 3 – Juros por atraso

```bash
python juros.py
```

ou informando os dados direto na linha de comando:

```bash
python juros.py 1000 28/09/2026
```

Calcula os juros na data de hoje, com taxa de **2,5% ao dia**:

```
juros = valor × 2,5% × dias em atraso
```

Se o vencimento for hoje ou uma data futura, não há juros. O valor aceita `1500.50` ou `1.500,50`, e a data aceita `DD/MM/AAAA` ou `AAAA-MM-DD`.

## Testes

```bash
pip install pytest
pytest
```

Os testes cobrem as faixas de comissão, o total por vendedor, entradas e saídas de estoque, unicidade e persistência dos IDs, validações e o cálculo de juros.

## Decisões e premissas

- **Precisão monetária:** uso `Decimal` em vez de `float`, evitando erros de arredondamento em valores financeiros. O arredondamento é feito só no final, para não acumular diferenças.
- **Limites da comissão:** exatamente R$ 100,00 gera 1% e exatamente R$ 500,00 gera 5%, seguindo o enunciado ("abaixo de" para os limites inferiores e "a partir de" para os de 5%).
- **Juros simples:** o enunciado fala em "multa de 2,5% ao dia"; interpretei como juros simples, sem capitalização. Para juros compostos, basta alterar a função `calcular_juros` em `juros.py`.
- **IDs de movimentação:** sequenciais e persistidos em arquivo, garantindo unicidade sem depender de bibliotecas externas.
- **Persistência em JSON:** escolhida pela simplicidade e por usar o mesmo formato dos dados fornecidos no desafio.
