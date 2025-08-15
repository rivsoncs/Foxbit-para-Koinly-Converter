
from decimal import Decimal, InvalidOperation, getcontext
import pandas as pd
import csv
import sys
import os

getcontext().prec = 50

OUT_COLS = [
    "Date","Sent Amount","Sent Currency","Received Amount","Received Currency",
    "Fee Amount","Fee Currency","Net Worth Amount","Net Worth Currency",
    "Label","Description","TxHash"
]

REQUIRED = {"operation_date","operation","base_currency","base_amount","quote_amount","fee"}

def D(x):
    if x is None: return None
    s = str(x).strip()
    if s == "" or s.lower() in ("nan","none"): return None
    s = s.replace(",", ".")
    try:
        return Decimal(s)
    except Exception:
        try:
            return Decimal(str(float(s)))
        except Exception:
            return None

def S(x):
    """String sem notação científica e sem zeros à direita."""
    if x is None: return ""
    if not isinstance(x, Decimal):
        x = D(x)
        if x is None: return ""
    s = format(x, 'f')
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    if s == "-0": s = "0"
    return s

def read_csv_as_text(path):
    # Lê tudo como texto para não perder precisão
    return pd.read_csv(path, encoding="utf-8", sep=None, engine="python", dtype=str)

def to_utc_str(x):
    return pd.to_datetime(x, errors="coerce").strftime("%Y-%m-%d %H:%M:%S UTC")

def map_row(r):
    op = (r.get("operation") or "")
    base_ccy = (r.get("base_currency") or "")
    base_amt = D(r.get("base_amount"))
    quote_amt = D(r.get("quote_amount"))
    fee = D(r.get("fee"))
    date = to_utc_str(r.get("operation_date"))

    out = {
        "Date": date, "Sent Amount": "", "Sent Currency": "",
        "Received Amount": "", "Received Currency": "",
        "Fee Amount": "", "Fee Currency": "",
        "Net Worth Amount": "", "Net Worth Currency": "",
        "Label": "", "Description": "", "TxHash": ""
    }

    def set_fee():
        if fee is not None and fee != 0:
            out["Fee Amount"] = S(abs(fee))
            out["Fee Currency"] = "BRL"

    if "Depósito" in op:
        out.update({
            "Received Amount": S(base_amt), "Received Currency": base_ccy,
            "Label": "Deposit", "Description": "Depósito - Foxbit"
        })

    elif "Retirada" in op:
        out.update({
            "Sent Amount": S(base_amt), "Sent Currency": base_ccy,
            "Label": "Withdrawal", "Description": "Retirada - Foxbit"
        })

    elif "Trade Venda" in op:
        out.update({
            "Sent Amount": S(base_amt), "Sent Currency": base_ccy,
            "Received Amount": S(abs(quote_amt) if quote_amt is not None else None),
            "Received Currency": "BRL",
            "Label": "Trade", "Description": "Venda - Foxbit"
        })
        set_fee()

    elif "Trade Compra" in op:
        out.update({
            "Sent Amount": S(abs(quote_amt) if quote_amt is not None else None),
            "Sent Currency": "BRL",
            "Received Amount": S(base_amt), "Received Currency": base_ccy,
            "Label": "Trade", "Description": "Compra - Foxbit"
        })
        set_fee()

    else:
        out["Description"] = op or "Operação não mapeada - Foxbit"

    return out

def converter_foxbit_para_koinly(input_path, output_path=None, check=False):
    df = read_csv_as_text(input_path)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}. Encontradas: {list(df.columns)}")

    rows = [map_row(r) for _, r in df.iterrows()]
    kdf = pd.DataFrame(rows, columns=OUT_COLS)

    if not output_path:
        base = os.path.splitext(os.path.basename(input_path))[0]
        output_path = f"{base}_koinly.csv"

    kdf.to_csv(output_path, index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)

    if check:
        dbg = pd.concat([
            df.reset_index(drop=True)[["operation_date","operation","base_currency","base_amount","currency_price","quote_amount","fee"]],
            kdf.reset_index(drop=True)
        ], axis=1)
        check_path = os.path.splitext(output_path)[0] + "_check.csv"
        dbg.to_csv(check_path, index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)

    return output_path

if __name__ == "__main__":
    import sys
    in_file = None
    out_file = None
    check = False
    args = sys.argv[1:]
    if not args:
        print("Uso: python foxbit.py <arquivo.csv> [saida.csv] [--check]")
        sys.exit(0)
    in_file = args[0]
    for a in args[1:]:
        if a == "--check":
            check = True
        else:
            out_file = a
    path = converter_foxbit_para_koinly(in_file, out_file, check=check)
    print("Arquivo convertido salvo em:", path)
