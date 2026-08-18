"""
SecureLogic Eval - Inferential Statistical Testing Engine
Provides 2-Way Factorial ANOVA, McNemar's Paired Test, Odds Ratios with 95% CI,
and Non-parametric Bootstrap Confidence Intervals.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from scipy import stats


class StatisticalEngine:
    """Rigorous statistical hypothesis testing for behavioral benchmark results."""

    @staticmethod
    def two_way_factorial_anova(df: pd.DataFrame) -> pd.DataFrame:
        """
        Conducts a 2x2 Factorial ANOVA on Accuracy.
        Factor 1: Bias Factor (0 = Neutral, 1 = Biased)
        Factor 2: Pushback Factor (0 = No Pushback, 1 = Pushback)
        """
        # Assign numeric factors
        df_anova = df.copy()
        df_anova["bias_factor"] = df_anova["condition"].apply(lambda c: 1 if "Bias" in c or "Interaction" in c else 0)
        df_anova["pushback_factor"] = df_anova["condition"].apply(lambda c: 1 if "Sycophancy" in c or "Interaction" in c else 0)
        df_anova["y"] = df_anova["final_is_correct"].astype(float)

        grand_mean = df_anova["y"].mean()
        N = len(df_anova)

        # Main effect of Bias
        mean_b0 = df_anova[df_anova["bias_factor"] == 0]["y"].mean()
        mean_b1 = df_anova[df_anova["bias_factor"] == 1]["y"].mean()
        n_b = len(df_anova) / 2
        ss_bias = n_b * ((mean_b0 - grand_mean)**2 + (mean_b1 - grand_mean)**2)
        df_bias = 1

        # Main effect of Pushback
        mean_p0 = df_anova[df_anova["pushback_factor"] == 0]["y"].mean()
        mean_p1 = df_anova[df_anova["pushback_factor"] == 1]["y"].mean()
        n_p = len(df_anova) / 2
        ss_pushback = n_p * ((mean_p0 - grand_mean)**2 + (mean_p1 - grand_mean)**2)
        df_pushback = 1

        # Cell Means for Interaction
        cell_means = df_anova.groupby(["bias_factor", "pushback_factor"])["y"].mean()
        n_cell = len(df_anova) / 4
        ss_cells = n_cell * sum((mean - grand_mean)**2 for mean in cell_means)
        ss_interaction = max(0.0, ss_cells - ss_bias - ss_pushback)
        df_interaction = 1

        # Error / Residual Sum of Squares
        ss_total = ((df_anova["y"] - grand_mean)**2).sum()
        ss_error = max(1e-6, ss_total - (ss_bias + ss_pushback + ss_interaction))
        df_error = N - 4

        # Mean Squares
        ms_bias = ss_bias / df_bias
        ms_pushback = ss_pushback / df_pushback
        ms_interaction = ss_interaction / df_interaction
        ms_error = ss_error / df_error

        # F-statistics and p-values
        f_bias = ms_bias / ms_error
        p_bias = 1.0 - stats.f.cdf(f_bias, df_bias, df_error)

        f_pushback = ms_pushback / ms_error
        p_pushback = 1.0 - stats.f.cdf(f_pushback, df_pushback, df_error)

        f_interaction = ms_interaction / ms_error
        p_interaction = 1.0 - stats.f.cdf(f_interaction, df_interaction, df_error)

        anova_table = pd.DataFrame([
            {"Source of Variation": "Cognitive Bias (Main Effect)", "Sum of Squares": round(ss_bias, 4), "df": df_bias, "Mean Square": round(ms_bias, 4), "F-Statistic": round(f_bias, 3), "p-Value": f"{p_bias:.4e}" if p_bias < 0.0001 else f"{p_bias:.4f}"},
            {"Source of Variation": "Sycophancy Pushback (Main Effect)", "Sum of Squares": round(ss_pushback, 4), "df": df_pushback, "Mean Square": round(ms_pushback, 4), "F-Statistic": round(f_pushback, 3), "p-Value": f"{p_pushback:.4e}" if p_pushback < 0.0001 else f"{p_pushback:.4f}"},
            {"Source of Variation": "Bias x Sycophancy Interaction", "Sum of Squares": round(ss_interaction, 4), "df": df_interaction, "Mean Square": round(ms_interaction, 4), "F-Statistic": round(f_interaction, 3), "p-Value": f"{p_interaction:.4e}" if p_interaction < 0.0001 else f"{p_interaction:.4f}"},
            {"Source of Variation": "Residual Error", "Sum of Squares": round(ss_error, 4), "df": df_error, "Mean Square": round(ms_error, 4), "F-Statistic": "-", "p-Value": "-"},
            {"Source of Variation": "Total", "Sum of Squares": round(ss_total, 4), "df": N - 1, "Mean Square": "-", "F-Statistic": "-", "p-Value": "-"}
        ])

        return anova_table

    @staticmethod
    def mcnemar_paired_test(df: pd.DataFrame, cond1: str, cond2: str) -> Dict[str, Any]:
        """
        Executes McNemar's exact test for paired binary correctness between two conditions.
        """
        pivot = df.pivot(index="question_id", columns="condition", values="final_is_correct")
        
        # Contingency counts
        # b: Correct in Cond1, Incorrect in Cond2 (Degraded)
        # c: Incorrect in Cond1, Correct in Cond2 (Improved)
        both_correct = ((pivot[cond1] == True) & (pivot[cond2] == True)).sum()
        degraded_b = ((pivot[cond1] == True) & (pivot[cond2] == False)).sum()
        improved_c = ((pivot[cond1] == False) & (pivot[cond2] == True)).sum()
        both_incorrect = ((pivot[cond1] == False) & (pivot[cond2] == False)).sum()

        discordant = degraded_b + improved_c
        if discordant == 0:
            stat, p_val = 0.0, 1.0
        else:
            # Edwards continuity correction
            stat = ((abs(degraded_b - improved_c) - 1)**2) / discordant
            p_val = 1.0 - stats.chi2.cdf(stat, df=1)

        return {
            "comparison": f"{cond1} vs {cond2}",
            "both_correct": int(both_correct),
            "degraded_discordant": int(degraded_b),
            "improved_discordant": int(improved_c),
            "both_incorrect": int(both_incorrect),
            "mcnemar_chi2": round(float(stat), 3),
            "p_value": f"{p_val:.4e}" if p_val < 0.0001 else f"{p_val:.4f}",
            "statistically_significant": bool(p_val < 0.05)
        }

    @staticmethod
    def calculate_odds_ratio(df: pd.DataFrame, cond_exposure: str, cond_control: str) -> Dict[str, Any]:
        """Calculates Odds Ratio (OR) of failing in exposure condition vs control."""
        acc_exp = df[df["condition"] == cond_exposure]["final_is_correct"].mean()
        acc_ctrl = df[df["condition"] == cond_control]["final_is_correct"].mean()

        odds_err_exp = (1.0 - acc_exp) / max(1e-6, acc_exp)
        odds_err_ctrl = (1.0 - acc_ctrl) / max(1e-6, acc_ctrl)

        odds_ratio = odds_err_exp / max(1e-6, odds_err_ctrl)

        # Standard error of log odds ratio
        n1 = len(df[df["condition"] == cond_exposure])
        n2 = len(df[df["condition"] == cond_control])
        
        a = (1.0 - acc_exp) * n1
        b = acc_exp * n1
        c = (1.0 - acc_ctrl) * n2
        d = acc_ctrl * n2

        se_log_or = np.sqrt(1/max(1, a) + 1/max(1, b) + 1/max(1, c) + 1/max(1, d))
        ci_lower = float(np.exp(np.log(max(1e-6, odds_ratio)) - 1.96 * se_log_or))
        ci_upper = float(np.exp(np.log(max(1e-6, odds_ratio)) + 1.96 * se_log_or))

        return {
            "exposure_condition": cond_exposure,
            "control_condition": cond_control,
            "odds_ratio_of_error": round(float(odds_ratio), 2),
            "ci_95_lower": round(ci_lower, 2),
            "ci_95_upper": round(ci_upper, 2)
        }

    @staticmethod
    def bootstrap_ci_by_condition(df: pd.DataFrame, n_resamples: int = 1000, seed: int = 42) -> Dict[str, Tuple[float, float, float]]:
        """Calculates 95% Bootstrap Confidence Interval for accuracy per condition."""
        rng = np.random.RandomState(seed)
        ci_dict = {}
        for cond in ["A_Control", "B_Bias_Only", "C_Sycophancy_Only", "D_Interaction"]:
            sub = df[df["condition"] == cond]["final_is_correct"].values
            if len(sub) == 0:
                continue
            boot_means = []
            for _ in range(n_resamples):
                sample = rng.choice(sub, size=len(sub), replace=True)
                boot_means.append(sample.mean() * 100)
            mean_est = float(np.mean(boot_means))
            ci_low = float(np.percentile(boot_means, 2.5))
            ci_high = float(np.percentile(boot_means, 97.5))
            ci_dict[cond] = (round(mean_est, 2), round(ci_low, 2), round(ci_high, 2))
        return ci_dict
