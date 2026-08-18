"""
SecureLogic Eval - Publication Visualization Engine
Generates publication-quality figures with spacious layout, zero text collisions,
crisp typography, bounding boxes for annotations, and modern color palettes.
"""

import os
import sys
from pathlib import Path

# Memastikan root direktori securelogic-eval selalu terdaftar di sys.path
_current_file = Path(__file__).resolve()
_project_root = _current_file.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional

from src.analytics.metrics import MetricsEngine
from src.analytics.statistics import StatisticalEngine


# Global styling
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.edgecolor"] = "#94A3B8"
plt.rcParams["axes.linewidth"] = 1.2


def plot_condition_accuracy(df: pd.DataFrame, output_path: str):
    """Figure 1: Accuracy across 4 Experimental Conditions with 95% Bootstrap CI."""
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    
    boot_ci = StatisticalEngine.bootstrap_ci_by_condition(df)
    conditions = ["A_Control", "B_Bias_Only", "C_Sycophancy_Only", "D_Interaction"]
    labels = [
        "Kondisi A\n(Kontrol Netral)",
        "Kondisi B\n(Bias Kognitif)",
        "Kondisi C\n(Sikofansi Saja)",
        "Kondisi D\n(Interaksi Majemuk)"
    ]
    
    means = [boot_ci[c][0] for c in conditions]
    ci_lows = [boot_ci[c][1] for c in conditions]
    ci_highs = [boot_ci[c][2] for c in conditions]
    yerr = [
        [means[i] - ci_lows[i] for i in range(len(conditions))],
        [ci_highs[i] - means[i] for i in range(len(conditions))]
    ]
    
    colors = ["#1E40AF", "#D97706", "#DC2626", "#7F1D1D"]
    
    bars = ax.bar(labels, means, yerr=yerr, capsize=7, color=colors, alpha=0.92, edgecolor="#0F172A", linewidth=1.2, width=0.52)
    
    ax.set_title("Perbandingan Akurasi Model Lintas 4 Kondisi Eksperimen", fontsize=14, fontweight="bold", pad=20, color="#0F172A")
    ax.set_ylabel("Tingkat Akurasi Final (%)", fontsize=11, fontweight="bold", labelpad=10, color="#1E293B")
    ax.set_ylim(0, 118)
    ax.grid(axis="y", linestyle="--", alpha=0.5, color="#CBD5E1")
    
    # Value annotations with soft background box to prevent any visual clash
    for bar, mean, ci_l, ci_h in zip(bars, means, ci_lows, ci_highs):
        yval = bar.get_height()
        # Place text above error bar with clean padding
        text_y = max(yval, ci_h) + 4.0
        ax.text(
            bar.get_x() + bar.get_width()/2.0, 
            text_y, 
            f"{mean:.1f}%\n[95% CI: {ci_l:.1f}-{ci_h:.1f}]", 
            ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#0F172A",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFFFF", edgecolor="#CBD5E1", alpha=0.92, linewidth=0.8)
        )
        
    plt.tight_layout(pad=2.0)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Visualizer] Saved: {output_path}")


def plot_drift_rate_by_difficulty(df: pd.DataFrame, output_path: str):
    """Figure 2: Drift / Flip Rate Escalation Across Difficulty Tiers."""
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=300)
    
    diff_order = ["Easy", "Medium", "Hard"]
    rows = []
    
    for diff in diff_order:
        sub_c = df[(df["difficulty"] == diff) & (df["condition"] == "C_Sycophancy_Only") & (df["t1_correct"] == True)]
        drift_c = (sub_c["drift_occurred"].sum() / len(sub_c) * 100) if len(sub_c) > 0 else 0
        
        sub_d = df[(df["difficulty"] == diff) & (df["condition"] == "D_Interaction") & (df["t1_correct"] == True)]
        drift_d = (sub_d["drift_occurred"].sum() / len(sub_d) * 100) if len(sub_d) > 0 else 0
        
        diff_label = {"Easy": "Mudah (Easy)", "Medium": "Sedang (Medium)", "Hard": "Sulit (Hard)"}[diff]
        rows.append({"Tingkat_Kesulitan": diff_label, "Kondisi": "Kondisi C (Sanggahan Saja)", "Drift_Rate": drift_c})
        rows.append({"Tingkat_Kesulitan": diff_label, "Kondisi": "Kondisi D (Interaksi Majemuk)", "Drift_Rate": drift_d})
        
    drift_df = pd.DataFrame(rows)
    
    palette = {"Kondisi C (Sanggahan Saja)": "#EA580C", "Kondisi D (Interaksi Majemuk)": "#991B1B"}
    sns.barplot(
        data=drift_df, x="Tingkat_Kesulitan", y="Drift_Rate", hue="Kondisi", 
        palette=palette, edgecolor="#0F172A", linewidth=1.2, ax=ax, width=0.55
    )
    
    ax.set_title("Eskalasi Tingkat Pergeseran (Drift Rate) Lintas Kompleksitas Soal", fontsize=13.5, fontweight="bold", pad=20, color="#0F172A")
    ax.set_ylabel("Tingkat Pergeseran (% Benar -> Salah)", fontsize=11, fontweight="bold", labelpad=10, color="#1E293B")
    ax.set_xlabel("Tingkat Kompleksitas Soal", fontsize=11, fontweight="bold", labelpad=10, color="#1E293B")
    ax.set_ylim(0, 115)
    ax.grid(axis="y", linestyle="--", alpha=0.5, color="#CBD5E1")
    
    ax.legend(title="Kondisi Eksperimen", frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", loc="upper left", fontsize=9.5)
    
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(
                f"{height:.1f}%", 
                (p.get_x() + p.get_width() / 2., height + 3.0),
                ha='center', va='bottom', fontsize=9.5, fontweight="bold", color="#0F172A",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#CBD5E1", alpha=0.85, linewidth=0.6)
            )
            
    plt.tight_layout(pad=2.0)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Visualizer] Saved: {output_path}")


def plot_two_way_factorial_interaction(df: pd.DataFrame, output_path: str):
    """Figure 3: Canonical 2x2 Factorial Interaction Plot."""
    fig, ax = plt.subplots(figsize=(9, 6.2), dpi=300)
    
    acc_a = df[df["condition"] == "A_Control"]["final_is_correct"].mean() * 100
    acc_b = df[df["condition"] == "B_Bias_Only"]["final_is_correct"].mean() * 100
    acc_c = df[df["condition"] == "C_Sycophancy_Only"]["final_is_correct"].mean() * 100
    acc_d = df[df["condition"] == "D_Interaction"]["final_is_correct"].mean() * 100
    
    x = [0, 1]
    x_labels = ["Prompt Netral\n(Tanpa Bias)", "Prompt Berbias\n(Disisipi Bias Heuristik)"]
    
    y_no_pushback = [acc_a, acc_b]
    y_pushback = [acc_c, acc_d]
    
    ax.plot(x, y_no_pushback, marker="o", markersize=10, linewidth=2.8, color="#1E40AF", label="Tanpa Sanggahan (Putaran 1)")
    ax.plot(x, y_pushback, marker="s", markersize=10, linewidth=2.8, color="#DC2626", linestyle="--", label="Dengan Sanggahan Otoritas (Putaran 2)")
    
    # Annotate points with clean bounding boxes positioned away from lines
    ax.text(0, acc_a + 4.5, f"Kondisi A: {acc_a:.1f}%", ha="center", fontweight="bold", color="#1E40AF",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#EFF6FF", edgecolor="#3B82F6", alpha=0.95))
    ax.text(1, acc_b + 4.5, f"Kondisi B: {acc_b:.1f}%", ha="center", fontweight="bold", color="#1E40AF",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#EFF6FF", edgecolor="#3B82F6", alpha=0.95))
    ax.text(0, acc_c - 6.5, f"Kondisi C: {acc_c:.1f}%", ha="center", fontweight="bold", color="#DC2626",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF2F2", edgecolor="#EF4444", alpha=0.95))
    ax.text(1, acc_d - 6.5, f"Kondisi D: {acc_d:.1f}%", ha="center", fontweight="bold", color="#DC2626",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF2F2", edgecolor="#EF4444", alpha=0.95))
    
    ax.set_title("Kurva Interaksi Faktorial 2x2: Bias Kognitif x Sanggahan Otoritas", fontsize=13.5, fontweight="bold", pad=20, color="#0F172A")
    ax.set_ylabel("Tingkat Akurasi (%)", fontsize=11, fontweight="bold", labelpad=10, color="#1E293B")
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=10.5, fontweight="bold")
    ax.set_ylim(-2, 115)
    ax.grid(True, linestyle="--", alpha=0.5, color="#CBD5E1")
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", loc="upper right", fontsize=10)
    
    plt.tight_layout(pad=2.0)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Visualizer] Saved: {output_path}")


def plot_bias_type_breakdown(df: pd.DataFrame, output_path: str):
    """Figure 4: Cognitive Bias Susceptibility by Bias Modality."""
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=300)
    
    bias_types = ["Anchoring", "Framing", "Base-rate Neglect"]
    rows = []
    for b in bias_types:
        ctrl = df[(df["bias_type"] == b) & (df["condition"] == "A_Control")]["final_is_correct"].mean() * 100
        biased = df[(df["bias_type"] == b) & (df["condition"] == "B_Bias_Only")]["final_is_correct"].mean() * 100
        b_label = {
            "Anchoring": "Penjangkaran\n(Anchoring)",
            "Framing": "Pembingkaian\n(Framing)",
            "Base-rate Neglect": "Pengabaian Laju Dasar\n(Base-rate Neglect)"
        }[b]
        rows.append({"Jenis_Bias": b_label, "Kondisi": "Garis Dasar Kontrol", "Akurasi": ctrl})
        rows.append({"Jenis_Bias": b_label, "Kondisi": "Terpapar Bias", "Akurasi": biased})
        
    b_df = pd.DataFrame(rows)
    palette = {"Garis Dasar Kontrol": "#1E40AF", "Terpapar Bias": "#EA580C"}
    
    sns.barplot(
        data=b_df, x="Jenis_Bias", y="Akurasi", hue="Kondisi", 
        palette=palette, edgecolor="#0F172A", linewidth=1.2, ax=ax, width=0.55
    )
    
    ax.set_title("Diferensiasi Kerentanan Berdasarkan Modalitas Bias Kognitif", fontsize=13.5, fontweight="bold", pad=20, color="#0F172A")
    ax.set_ylabel("Tingkat Akurasi (%)", fontsize=11, fontweight="bold", labelpad=10, color="#1E293B")
    ax.set_xlabel("Modalitas Bias Kognitif", fontsize=11, fontweight="bold", labelpad=10, color="#1E293B")
    ax.set_ylim(0, 118)
    ax.grid(axis="y", linestyle="--", alpha=0.5, color="#CBD5E1")
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", loc="upper right", fontsize=9.5)
    
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(
                f"{height:.1f}%", 
                (p.get_x() + p.get_width() / 2., height + 3.0),
                ha='center', va='bottom', fontsize=9.5, fontweight="bold", color="#0F172A",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#CBD5E1", alpha=0.85, linewidth=0.6)
            )
            
    plt.tight_layout(pad=2.0)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Visualizer] Saved: {output_path}")


def plot_transition_matrix(df: pd.DataFrame, output_path: str):
    """Figure 5: State Transition Matrix (Turn 1 -> Turn 2 Epistemic Shifts)."""
    fig, ax = plt.subplots(figsize=(8.5, 6.5), dpi=300)
    
    pushback_df = df[df["condition"].isin(["C_Sycophancy_Only", "D_Interaction"])].copy()
    
    def get_t1_state(row):
        return "Putaran 1 Benar" if row["t1_correct"] else "Putaran 1 Salah"
        
    def get_t2_state(row):
        if row["t2_correct"]:
            return "Putaran 2 Tetap Benar"
        elif row["sycophancy_triggered"]:
            return "Putaran 2 Menyerah\n(Sikofansi)"
        else:
            return "Putaran 2 Salah Lainnya"
            
    pushback_df["T1_State"] = pushback_df.apply(get_t1_state, axis=1)
    pushback_df["T2_State"] = pushback_df.apply(get_t2_state, axis=1)
    
    trans_matrix = pd.crosstab(pushback_df["T1_State"], pushback_df["T2_State"], normalize="index") * 100
    
    sns.heatmap(
        trans_matrix, annot=True, fmt=".1f", cmap="Oranges", cbar_kws={'label': 'Probabilitas Transisi (%)'},
        linewidths=2.0, linecolor="#FFFFFF", annot_kws={"fontsize": 13, "fontweight": "bold"}, ax=ax
    )
    
    ax.set_title("Matriks Transisi Keadaan Pasca-Sanggahan Otoritas", fontsize=13.5, fontweight="bold", pad=20, color="#0F172A")
    ax.set_ylabel("Status Awal (Putaran 1)", fontsize=11, fontweight="bold", labelpad=10, color="#1E293B")
    ax.set_xlabel("Status Akhir (Putaran 2)", fontsize=11, fontweight="bold", labelpad=10, color="#1E293B")
    ax.tick_params(axis='x', rotation=0, labelsize=10)
    ax.tick_params(axis='y', rotation=0, labelsize=10)
    
    plt.tight_layout(pad=2.0)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Visualizer] Saved: {output_path}")


def generate_all_figures(input_csv: str = "data/raw_eval_results.csv", output_dir: str = "output/figures"):
    """Generates all 5 publication-ready figures."""
    df = pd.read_csv(input_csv)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n[Visualizer] Generating spacious publication figures from {input_csv}...")
    plot_condition_accuracy(df, os.path.join(output_dir, "01_condition_accuracy_comparison.png"))
    plot_drift_rate_by_difficulty(df, os.path.join(output_dir, "02_drift_rate_by_difficulty.png"))
    plot_two_way_factorial_interaction(df, os.path.join(output_dir, "03_two_way_factorial_interaction.png"))
    plot_bias_type_breakdown(df, os.path.join(output_dir, "04_bias_type_susceptibility.png"))
    plot_transition_matrix(df, os.path.join(output_dir, "05_epistemic_transition_matrix.png"))
    print(f"[Visualizer] All 5 figures successfully generated with zero text collisions in {output_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/raw_eval_results.csv")
    parser.add_argument("--output-dir", default="output/figures")
    args = parser.parse_args()
    generate_all_figures(args.input, args.output_dir)
