"""
SecureLogic Eval - Snowflake Data Warehouse & Cortex AI Integration Module
Menyediakan integrasi dua arah:
1. Snowflake Data Warehouse: Sinkronisasi dataset tolak ukur dan hasil evaluasi ke tabel Snowflake.
2. Snowflake Cortex AI: Inferensi model bahasa skala besar (Llama-3.1-70B, Mistral, Arctic) via SQL Cortex.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import pandas as pd

try:
    import snowflake.connector
    from snowflake.connector.pandas_tools import write_pandas
    SNOWFLAKE_AVAILABLE = True
except ImportError:
    SNOWFLAKE_AVAILABLE = False


class SnowflakeWarehouseManager:
    """Manajer sinkronisasi data dan analitik SQL di Snowflake Data Cloud."""

    def __init__(
        self,
        account: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        warehouse: str = "COMPUTE_WH",
        database: str = "SECURELOGIC_DB",
        schema: str = "EVAL_SCHEMA",
        role: Optional[str] = None
    ):
        self.account = account or os.environ.get("SNOWFLAKE_ACCOUNT", "")
        self.user = user or os.environ.get("SNOWFLAKE_USER", "")
        self.password = password or os.environ.get("SNOWFLAKE_PASSWORD", "")
        self.warehouse = warehouse
        self.database = database
        self.schema = schema
        self.role = role

    def get_connection(self):
        """Membuka koneksi aktif ke Snowflake."""
        if not SNOWFLAKE_AVAILABLE:
            raise ImportError("Pustaka 'snowflake-connector-python' belum terpasang.")
        
        conn_params = {
            "account": self.account,
            "user": self.user,
            "password": self.password,
            "warehouse": self.warehouse,
            "database": self.database,
            "schema": self.schema
        }
        if self.role:
            conn_params["role"] = self.role
            
        return snowflake.connector.connect(**conn_params)

    def initialize_schema(self) -> bool:
        """Membuat Database, Schema, dan Tabel evaluasi di Snowflake."""
        ddl_statements = [
            f"CREATE DATABASE IF NOT EXISTS {self.database};",
            f"CREATE SCHEMA IF NOT EXISTS {self.database}.{self.schema};",
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.{self.schema}.BENCHMARK_QUESTIONS (
                QUESTION_ID VARCHAR(64) PRIMARY KEY,
                TITLE VARCHAR(255),
                CATEGORY VARCHAR(64),
                DIFFICULTY VARCHAR(32),
                BIAS_TYPE VARCHAR(64),
                GROUND_TRUTH_VALUE FLOAT,
                UNIT VARCHAR(32),
                TOLERANCE FLOAT,
                BIAS_ANCHOR_VALUE FLOAT,
                DISTRACTOR_VALUE FLOAT,
                MATH_DERIVATION TEXT
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.{self.schema}.RAW_EVAL_RESULTS (
                SAMPLE_ID VARCHAR(128) PRIMARY KEY,
                QUESTION_ID VARCHAR(64),
                CATEGORY VARCHAR(64),
                DIFFICULTY VARCHAR(32),
                BIAS_TYPE VARCHAR(64),
                CONDITION VARCHAR(64),
                T1_CORRECT BOOLEAN,
                T2_CORRECT BOOLEAN,
                FINAL_IS_CORRECT BOOLEAN,
                DRIFT_OCCURRED BOOLEAN,
                SYCOPHANCY_TRIGGERED BOOLEAN,
                BIAS_SUCCUMBED BOOLEAN,
                CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            );
            """
        ]
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                for stmt in ddl_statements:
                    cur.execute(stmt)
        return True

    def sync_dataframes(self, df_questions: pd.DataFrame, df_results: pd.DataFrame) -> Dict[str, int]:
        """Mengunggah data evaluasi lokal ke tabel Snowflake menggunakan write_pandas."""
        self.initialize_schema()
        
        # Standarisasi nama kolom ke huruf kapital (Snowflake convention)
        df_q = df_questions.copy()
        df_q.columns = [c.upper() for c in df_q.columns]
        
        df_r = df_results.copy()
        df_r.columns = [c.upper() for c in df_r.columns]
        
        counts = {}
        with self.get_connection() as conn:
            success_q, n_chunks_q, n_rows_q, _ = write_pandas(
                conn, df_q, "BENCHMARK_QUESTIONS", database=self.database, schema=self.schema, overwrite=True
            )
            counts["questions_synced"] = n_rows_q
            
            success_r, n_chunks_r, n_rows_r, _ = write_pandas(
                conn, df_r, "RAW_EVAL_RESULTS", database=self.database, schema=self.schema, overwrite=True
            )
            counts["results_synced"] = n_rows_r
            
        return counts

    def run_snowflake_analytics(self) -> pd.DataFrame:
        """Menjalankan query SQL agregasi metrik di Snowflake."""
        query = f"""
        SELECT 
            CONDITION,
            COUNT(*) AS TOTAL_SAMPLES,
            AVG(CASE WHEN FINAL_IS_CORRECT THEN 1.0 ELSE 0.0 END) * 100 AS ACCURACY_PCT,
            SUM(CASE WHEN DRIFT_OCCURRED THEN 1 ELSE 0 END) AS DRIFT_COUNT,
            SUM(CASE WHEN SYCOPHANCY_TRIGGERED THEN 1 ELSE 0 END) AS SYCOPHANCY_COUNT
        FROM {self.database}.{self.schema}.RAW_EVAL_RESULTS
        GROUP BY CONDITION
        ORDER BY CONDITION;
        """
        with self.get_connection() as conn:
            return pd.read_sql(query, conn)
