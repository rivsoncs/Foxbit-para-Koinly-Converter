
import pandas as pd
import csv
from datetime import datetime
import sys
import os

def converter_foxbit_para_koinly(input_path, output_path=None):
    df = pd.read_csv(input_path, encoding='utf-8', sep=None, engine='python')
    df["Date"] = pd.to_datetime(df["operation_date"]).dt.strftime("%Y-%m-%d %H:%M:%S UTC")

    koinly_rows = []

    for _, row in df.iterrows():
        base_currency = row["base_currency"]
        base_amount = row["base_amount"]
        quote_amount = row["quote_amount"]
        fee = row["fee"]
        date = row["Date"]
        operation = row["operation"]

        koinly_row = {
            "Date": date,
            "Sent Amount": "",
            "Sent Currency": "",
            "Received Amount": "",
            "Received Currency": "",
            "Fee Amount": "",
            "Fee Currency": "",
            "Net Worth Amount": "",
            "Net Worth Currency": "",
            "Label": "",
            "Description": operation,
            "TxHash": ""
        }

        if "Depósito" in operation:
            koinly_row["Received Amount"] = base_amount
            koinly_row["Received Currency"] = base_currency
            koinly_row["Description"] = "Depósito - Foxbit"

        elif "Retirada" in operation:
            koinly_row["Sent Amount"] = base_amount
            koinly_row["Sent Currency"] = base_currency
            koinly_row["Label"] = "Withdrawal"
            koinly_row["Description"] = "Retirada - Foxbit"

        elif "Trade Venda" in operation:
            koinly_row["Sent Amount"] = base_amount
            koinly_row["Sent Currency"] = base_currency
            koinly_row["Received Amount"] = -quote_amount
            koinly_row["Received Currency"] = "BRL"
            if fee > 0:
                koinly_row["Fee Amount"] = fee
                koinly_row["Fee Currency"] = base_currency
            koinly_row["Label"] = "Trade"
            koinly_row["Description"] = "Venda - Foxbit"

        elif "Trade Compra" in operation:
            koinly_row["Sent Amount"] = -quote_amount
            koinly_row["Sent Currency"] = "BRL"
            koinly_row["Received Amount"] = base_amount
            koinly_row["Received Currency"] = base_currency
            if fee > 0:
                koinly_row["Fee Amount"] = fee
                koinly_row["Fee Currency"] = base_currency
            koinly_row["Label"] = "Trade"
            koinly_row["Description"] = "Compra - Foxbit"

        koinly_rows.append(koinly_row)

    df_koinly = pd.DataFrame(koinly_rows)

    if not output_path:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = f"{base_name}_koinly.csv"

    df_koinly.to_csv(output_path, index=False, quoting=csv.QUOTE_ALL)
    print(f"Arquivo convertido salvo em: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python foxbit_to_koinly.py <caminho_do_csv>")
    else:
        input_csv = sys.argv[1]
        output_csv = sys.argv[2] if len(sys.argv) > 2 else None
        converter_foxbit_para_koinly(input_csv, output_csv)
