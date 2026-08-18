"""
SecureLogic Eval - Skrip Eksekusi Praktis Snowflake
Menjalankan sinkronisasi data ke Snowflake Data Warehouse atau inferensi Cortex AI.

Penggunaan:
1. Sinkronisasi Data Warehouse:
   python run_snowflake.py --action sync --account YOUR_ACCOUNT --user YOUR_USER --password YOUR_PASS

2. Jalankan Analitik SQL Snowflake:
   python run_snowflake.py --action analytics --account YOUR_ACCOUNT --user YOUR_USER --password YOUR_PASS

3. Jalankan Uji Inferensi Snowflake Cortex AI:
   python run_snowflake.py --action cortex --account YOUR_ACCOUNT --user YOUR_USER --password YOUR_PASS --model llama3.1-70b
"""

import os
import sys
import argparse
import pandas as pd
from pathlib import Path

# Pastikan sys.path mendeteksi root repositori
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.integrations.snowflake_sync import SnowflakeWarehouseManager
from src.evaluator.llm_client import SnowflakeCortexClient


def main():
    parser = argparse.ArgumentParser(description="Snowflake Integration Runner")
    parser.add_argument("--action", choices=["sync", "analytics", "cortex"], default="analytics",
                        help="Aksi: 'sync' (unggah data), 'analytics' (kueri SQL), 'cortex' (inferensi AI)")
    parser.add_argument("--account", default=os.environ.get("SNOWFLAKE_ACCOUNT", ""), help="Snowflake Account Identifier")
    parser.add_argument("--user", default=os.environ.get("SNOWFLAKE_USER", ""), help="Snowflake Username")
    parser.add_argument("--password", default=os.environ.get("SNOWFLAKE_PASSWORD", ""), help="Snowflake Password")
    parser.add_argument("--warehouse", default="COMPUTE_WH", help="Snowflake Warehouse")
    parser.add_argument("--database", default="SECURELOGIC_DB", help="Snowflake Database")
    parser.add_argument("--schema", default="EVAL_SCHEMA", help="Snowflake Schema")
    parser.add_argument("--model", default="llama3.1-70b", help="Model Snowflake Cortex")

    args = parser.parse_args()

    if not args.account or not args.user or not args.password:
        print("[PERINGATAN] Kredensial Snowflake belum lengkap. Harap sertakan --account, --user, dan --password.")
        print("Contoh: python run_snowflake.py --action sync --account myorg-myaccount --user myuser --password mypass")
        return

    sf = SnowflakeWarehouseManager(
        account=args.account,
        user=args.user,
        password=args.password,
        warehouse=args.warehouse,
        database=args.database,
        schema=args.schema
    )

    if args.action == "sync":
        print("[1/2] Memuat dataset lokal...")
        q_path = project_root / "data" / "benchmark_questions.csv"
        r_path = project_root / "data" / "raw_eval_results.csv"
        
        df_q = pd.read_csv(q_path)
        df_r = pd.read_csv(r_path)
        
        print(f"[2/2] Mengunggah {len(df_q)} butir soal dan {len(df_r)} hasil evaluasi ke Snowflake ({args.database}.{args.schema})...")
        counts = sf.sync_dataframes(df_q, df_r)
        print(f"[SUKSES] Data berhasil disinkronkan ke Snowflake: {counts}")

    elif args.action == "analytics":
        print(f"[1/1] Menjalankan kueri analitik SQL agregasi di Snowflake ({args.database}.{args.schema})...")
        df_res = sf.run_snowflake_analytics()
        print("\n" + "="*80)
        print("HASIL ANALITIK SQL SNOWFLAKE:")
        print("="*80)
        print(df_res.to_string(index=False))
        print("="*80)

    elif args.action == "cortex":
        print(f"[1/1] Menjalankan inferensi Snowflake Cortex AI menggunakan model '{args.model}'...")
        client = SnowflakeCortexClient(
            account=args.account,
            user=args.user,
            password=args.password,
            warehouse=args.warehouse,
            database=args.database,
            schema=args.schema,
            model=args.model
        )
        sample_prompt = "Hitung probabilitas Bayesian jika P(Threat)=0.001, P(Alert|Threat)=0.90, P(Alert|Clean)=0.01. Berikan nilai eksak."
        response = client.generate(sample_prompt)
        print("\n" + "="*80)
        print(f"OUTPUT PENALARAN CORTEX AI ({args.model}):")
        print("="*80)
        print(response)
        print("="*80)


if __name__ == "__main__":
    main()
