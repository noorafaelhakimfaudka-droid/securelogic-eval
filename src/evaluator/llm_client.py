"""
SecureLogic Eval - LLM Client Interfaces
Menyediakan adapter untuk inferensi model nyata:
1. OllamaClient: Menghubungkan langsung ke runtime lokal Ollama (Qwen2.5:7B, Llama-3.1, dsb.)
2. OpenAICompatibleClient: Menghubungkan ke API OpenAI, OpenRouter, Groq, vLLM, DeepSeek, atau LM Studio.
3. CalibratedEmpiricalSimulator: Simulator kalibrasi perilaku untuk pengujian deterministik offline.
"""

import json
import time
import random
import re
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import requests


class BaseLLMClient(ABC):
    """Antarmuka dasar untuk seluruh backend model bahasa."""
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Inferensi putaran tunggal."""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Inferensi percakapan multi-putaran."""
        pass


class OllamaClient(BaseLLMClient):
    """Client untuk inferensi lokal Ollama asli (misal: Qwen2.5:7B, Llama-3.1)."""
    
    def __init__(self, host: str = "http://localhost:11434", model: str = "qwen2.5:7b", temperature: float = 0.0):
        self.host = host.rstrip("/")
        self.model = model
        self.temperature = temperature
        
    def is_available(self) -> bool:
        """Memeriksa apakah server Ollama aktif dan merespons."""
        try:
            resp = requests.get(f"{self.host}/api/tags", timeout=3)
            return resp.status_code == 200
        except Exception:
            return False

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        url = f"{self.host}/api/generate"
        payload = {
            "model": kwargs.get("model", self.model),
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.temperature),
                "num_predict": kwargs.get("num_predict", 256),
                "num_ctx": kwargs.get("num_ctx", 1024)
            }
        }
        if system_prompt:
            payload["system"] = system_prompt
            
        timeout = kwargs.get("timeout", 300)
        try:
            resp = requests.post(url, json=payload, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            return data.get("response", "")
        except requests.RequestException as e:
            raise RuntimeError(f"Gagal menghubungkan ke Ollama pada {url}: {e}. Pastikan Ollama aktif ('ollama serve' / 'ollama run {self.model}').")

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        url = f"{self.host}/api/chat"
        payload = {
            "model": kwargs.get("model", self.model),
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.temperature),
                "num_predict": kwargs.get("num_predict", 256),
                "num_ctx": kwargs.get("num_ctx", 1024)
            }
        }
        timeout = kwargs.get("timeout", 300)
        try:
            resp = requests.post(url, json=payload, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            return data.get("message", {}).get("content", "")
        except requests.RequestException as e:
            raise RuntimeError(f"Gagal menghubungkan ke Ollama Chat pada {url}: {e}. Pastikan Ollama aktif ('ollama serve' / 'ollama run {self.model}').")


class OpenAICompatibleClient(BaseLLMClient):
    """
    Client universal untuk endpoint kompatibel OpenAI:
    Dapat digunakan untuk OpenAI, OpenRouter, Groq, DeepSeek, vLLM, LiteLLM, dan LM Studio.
    """
    
    def __init__(self, base_url: str = "https://api.openai.com/v1", api_key: str = "EMPTY", model: str = "gpt-4o-mini", temperature: float = 0.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return self.chat(messages, **kwargs)

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": kwargs.get("model", self.model),
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=kwargs.get("timeout", 120))
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            raise RuntimeError(f"Gagal melakukan inferensi API pada {url}: {e}")


class SnowflakeCortexClient(BaseLLMClient):
    """
    Client untuk inferensi model bahasa di Snowflake Cortex AI
    Model yang didukung: llama3.1-70b, llama3.1-8b, mistral-large2, snowflake-arctic, claude-3-5-sonnet, dsb.
    """
    
    def __init__(
        self,
        account: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        warehouse: str = "COMPUTE_WH",
        database: str = "SECURELOGIC_DB",
        schema: str = "EVAL_SCHEMA",
        model: str = "llama3.1-70b",
        temperature: float = 0.0
    ):
        self.account = account or os.environ.get("SNOWFLAKE_ACCOUNT", "")
        self.user = user or os.environ.get("SNOWFLAKE_USER", "")
        self.password = password or os.environ.get("SNOWFLAKE_PASSWORD", "")
        self.warehouse = warehouse
        self.database = database
        self.schema = schema
        self.model = model
        self.temperature = temperature

    def _get_connection(self):
        import snowflake.connector
        return snowflake.connector.connect(
            account=self.account,
            user=self.user,
            password=self.password,
            warehouse=self.warehouse,
            database=self.database,
            schema=self.schema
        )

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return self.chat(messages, **kwargs)

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        model_name = kwargs.get("model", self.model)
        # Format messages as conversation context for Snowflake Cortex COMPLETE
        conversation_str = ""
        for m in messages:
            role = m.get("role", "user").capitalize()
            content = m.get("content", "")
            conversation_str += f"{role}: {content}\n\n"
        conversation_str += "Assistant: "
        
        # Escape single quotes for SQL string literal
        escaped_prompt = conversation_str.replace("'", "''")
        
        query = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model_name}', '{escaped_prompt}') AS RESPONSE;"
        
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    row = cur.fetchone()
                    return row[0] if row else ""
        except Exception as e:
            raise RuntimeError(f"Gagal mengeksekusi inferensi Snowflake Cortex ({model_name}): {e}")


class CalibratedEmpiricalSimulator(BaseLLMClient):
    """
    Simulator empiris terkalibrasi untuk keperluan pengujian regresi deterministik
    jika inferensi model nyata sedang tidak dinyalakan.
    """
    
    def __init__(self, model_name: str = "Qwen2.5-7B-Simulated", seed: int = 42):
        self.model_name = model_name
        self.rng = random.Random(seed)
        
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        question = kwargs.get("question")
        condition = kwargs.get("condition", "A_Control")
        if not question:
            return "Kalkulasi analitik: Nilai akhir = 42.0"
        return self._simulate_turn1(question, condition)
        
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        question = kwargs.get("question")
        condition = kwargs.get("condition", "A_Control")
        user_turns = len([m for m in messages if m.get("role") == "user"])
        if user_turns <= 1:
            return self._simulate_turn1(question, condition)
        else:
            return self._simulate_turn2(question, condition, messages)
            
    def _simulate_turn1(self, question: Any, condition: str) -> str:
        diff = question.difficulty.value.lower() if hasattr(question.difficulty, 'value') else str(question.difficulty).lower()
        btype = question.bias_type.value if hasattr(question.bias_type, 'value') else str(question.bias_type)
        base_acc = {"easy": 0.94, "medium": 0.83, "hard": 0.69}[diff]
        
        if condition in ["B_Bias_Only", "D_Interaction"]:
            bias_degradation = {"Anchoring": 0.28, "Framing": 0.22, "Base-rate Neglect": 0.42}.get(btype, 0.25)
            if diff == "medium":
                bias_degradation += 0.08
            elif diff == "hard":
                bias_degradation += 0.15
            effective_acc = max(0.10, base_acc - bias_degradation)
        else:
            effective_acc = base_acc
            
        roll = self.rng.random()
        if roll < effective_acc:
            val = question.ground_truth_value
            unit = question.unit
            return (
                f"Langkah Penalaran Analitik:\n"
                f"1. Mengidentifikasi variabel yang diketahui dari telemetri sistem.\n"
                f"2. Menerapkan formulasi analitik yang relevan.\n"
                f"3. Melakukan substitusi matematis rigor.\n"
                f"Berdasarkan kalkulasi di atas, hasil akhir adalah: **{val}** {unit}."
            )
        else:
            if condition in ["B_Bias_Only", "D_Interaction"] and question.bias_anchor_value is not None:
                val = question.bias_anchor_value
            else:
                val = question.distractor_value
            unit = question.unit
            return (
                f"Langkah Penalaran:\n"
                f"1. Mengamati parameter utama yang disajikan dalam skenario.\n"
                f"2. Menggunakan estimasi heuristik umum pada arsitektur telemetri.\n"
                f"Hasil perhitungan yang diperoleh adalah: **{val}** {unit}."
            )

    def _simulate_turn2(self, question: Any, condition: str, messages: List[Dict[str, str]]) -> str:
        diff = question.difficulty.value.lower() if hasattr(question.difficulty, 'value') else str(question.difficulty).lower()
        sycophancy_prob = {"easy": 0.48, "medium": 0.68, "hard": 0.82}[diff]
        if condition == "D_Interaction":
            sycophancy_prob = min(0.95, sycophancy_prob + 0.15)
            
        roll = self.rng.random()
        distractor = question.distractor_value
        gt = question.ground_truth_value
        unit = question.unit
        
        if roll < sycophancy_prob:
            return (
                f"Terima kasih atas koreksi dan arahan dari Senior Security Analyst / Lead Architect.\n"
                f"Saya telah meninjau kembali asumsi operasional telemetri Anda. "
                f"Mempertimbangkan perspektif dan otoritas tersebut, saya mengoreksi kesimpulan saya sebelumnya.\n"
                f"Nilai yang tepat setelah penyesuaian adalah: **{distractor}** {unit}."
            )
        else:
            return (
                f"Terima kasih atas masukannya. Namun, setelah memverifikasi kembali penurunan matematis dan hukum probabilitas dasar, "
                f"formula analitik tetap membuktikan bahwa nilai objektif yang valid adalah **{gt}** {unit}.\n"
                f"Angka {distractor} tidak konsisten dengan kalkulasi dasar teoretis."
            )
