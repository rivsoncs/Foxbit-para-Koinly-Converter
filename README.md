
# 🦊 Foxbit para Koinly Converter

Este script converte extratos CSV da exchange **Foxbit** (Brasil) para o formato **Koinly Custom CSV**, facilitando a importação de movimentações cripto no sistema de apuração fiscal do Koinly.

---

## 📦 Arquivo principal

**`foxbit.py`**

- Compatível com extratos da Foxbit com colunas:
  `operation_date`, `operation`, `base_currency`, `base_amount`, `quote_amount`, `fee`
- Reconhece os seguintes tipos de operações:
  - `Depósito`
  - `Retirada`
  - `Trade Compra`
  - `Trade Venda`

---

## 🛠️ Requisitos

- Python 3.7+
- Bibliotecas:
  ```bash
  pip install pandas
  ```

---

## ▶️ Como usar

1. Coloque o arquivo `foxbit.py` na mesma pasta do seu extrato `.csv`.

2. No terminal, execute:

```bash
python foxbit.py seu-arquivo.csv
```

3. O arquivo convertido será salvo como:

```bash
seu-arquivo_koinly.csv
```

---

## 🔁 Formato de saída (Koinly CSV)

O arquivo gerado conterá colunas como:

- `Date`
- `Sent Amount`
- `Sent Currency`
- `Received Amount`
- `Received Currency`
- `Fee Amount`
- `Fee Currency`
- `Label`
- `Description`

---

## 💡 Exemplo de uso avançado

Você pode especificar um nome personalizado para o arquivo de saída:

```bash
python foxbit.py meu_extrato.csv resultado.csv
```

---

## 🙋 Suporte

Se você quiser sugerir melhorias, relatar bugs ou contribuir, sinta-se à vontade para abrir uma issue ou pull request neste repositório!

---

**Desenvolvido por Rivson Souza** 🧾💙
