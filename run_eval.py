"""
SecureLogic Eval - Skrip Eksekusi Tolak Ukur Utama
Dapat dijalankan langsung dari terminal:
  python run_eval.py --mode ollama --model qwen2.5:7b
  python run_eval.py --mode openai --api-key sk-xxxx --model gpt-4o-mini
  python run_eval.py --mode simulate
"""

import os
import sys
from pathlib import Path

# Pastikan root direktori berada di sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.evaluator.runner import main

if __name__ == "__main__":
    main()
