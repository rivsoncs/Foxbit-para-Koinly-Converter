
# 🦊 Foxbit → Koinly Converter

Conversor de extratos **Foxbit** (`.csv`) para **Koinly Custom CSV**.  
Compatível com os layouts que possuem as colunas:
`operation_date`, `operation`, `base_currency`, `base_amount`, `quote_amount`, `fee` (+ campos extras opcionais).

---

## ✨ Recursos

- **Mapeamento confiável** de `Depósito`, `Retirada`, `Trade Venda` e `Trade Compra`.
- **Interpretação correta de sinais**: `quote_amount` negativo em venda = **BRL recebido** (positivo na saída).
- **Taxas**: usa `fee` **em BRL** para operações de trade (conforme extratos testados).
- **Alta precisão** com `Decimal` e **sem notação científica** (nada de `1e-08`).  
- **Auditoria lado a lado (`--check`)**: gera um `_check.csv` com colunas originais + resultado Koinly.
- Leitura automática com `,` **ou** `;` como separador.

---

## 📦 Instalação

Requer **Python 3.8+** e `pandas`:

```bash
pip install pandas
```

Coloque `foxbit.py` na pasta do(s) seu(s) extrato(s).

---

## ▶️ Uso básico

```bash
# Conversão simples
python foxbit.py extrato-foxbit.csv

# Conversão + auditoria lado a lado
python foxbit.py extrato-foxbit.csv --check

# Definir nome de saída
python foxbit.py entrada.csv saida_koinly.csv
```

Saídas:
- `entrada_koinly.csv` — arquivo pronto para o Koinly.
- `entrada_koinly_check.csv` — (se `--check`) auditoria com dados brutos + mapeamento.

---

## 🔁 Regras de mapeamento

**Depósito**  
- `Received Amount = base_amount`  
- `Received Currency = base_currency`  
- `Label = Deposit`

**Retirada**  
- `Sent Amount = base_amount`  
- `Sent Currency = base_currency`  
- `Label = Withdrawal`

**Trade Venda** (vende cripto e recebe BRL)  
- `Sent Amount = base_amount` (cripto)  
- `Received Amount = abs(quote_amount)` (**BRL**)  
- `Fee Amount = fee` (**BRL**), se houver  
- `Label = Trade`

**Trade Compra** (paga BRL e recebe cripto) – suportado se constar no arquivo  
- `Sent Amount = abs(quote_amount)` (**BRL**)  
- `Received Amount = base_amount` (cripto)  
- `Fee Amount = fee` (**BRL**), se houver  
- `Label = Trade`

> **Observação:** Nos extratos Foxbit analisados, `fee` veio em **BRL**. Caso encontre taxa em cripto, abra uma *issue* para ajustarmos a detecção automática.

---

## ✅ Boas práticas de conferência

1. Rode com `--check` e valide algumas linhas com foco em:
   - **Sinal** de `quote_amount` nas vendas (deve virar **BRL positivo** em `Received Amount`).  
   - **Moeda** da taxa (BRL) e valores atípicos.
2. Confirme se **Retiradas** em BRL entram como `Withdrawal` (saída de BRL).  
3. Verifique se não há números em notação científica; os valores devem sair como `0.00000001` etc.

---

## 🧪 Exemplos

```csv
# Entrada (Foxbit)
operation_date,operation,base_currency,base_amount,quote_amount,fee
2025-01-02 11:53:39,Trade Venda,SOL,2.16191521,-2799.68019695,6.15929643329

# Saída (Koinly)
Date,Sent Amount,Sent Currency,Received Amount,Received Currency,Fee Amount,Fee Currency,Net Worth Amount,Net Worth Currency,Label,Description,TxHash
2025-01-02 11:53:39 UTC,2.16191521,SOL,2799.68019695,BRL,6.15929643329,BRL,,,,Trade,Venda - Foxbit,
```

---

## 🩺 Troubleshooting

- **“Colunas obrigatórias ausentes”**  
  O arquivo não está no layout Foxbit esperado. Exporte novamente da Foxbit ou compartilhe um exemplo para darmos suporte.
- **Números com `e-`**  
  Você está usando versão antiga. Atualize para a **V3.3** (usa `Decimal` e impede notação científica).
- **Taxas divergentes**  
  Em caso de taxa em cripto, anexe o `_check.csv` com o *timestamp* para avaliarmos.

---

## 🗓️ Changelog

- **V3.3**: números com `Decimal` (sem notação científica), reforço de sinais e auditoria.  
- V3.2: correção de taxa (BRL) e sinais de `quote_amount`.  
- V3.1: modo `--check` e validações de colunas.  

---

## 🤝 Contribuição

Sinta-se à vontade para abrir **issues** e **PRs** com ajustes/novos layouts.

---

2025 - **Desenvolvido por Rivson Souza** 🧾💙
