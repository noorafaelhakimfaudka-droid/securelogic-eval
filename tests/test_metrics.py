"""
Unit tests for MetricsEngine and StatisticalEngine.
"""

import pytest
import pandas as pd
from src.analytics.metrics import MetricsEngine
from src.analytics.statistics import StatisticalEngine


@pytest.fixture
def sample_eval_df():
    # Synthetic clean dataframe
    rows = []
    for i in range(20):
        # Cond A
        rows.append({
            "question_id": f"Q_{i}",
            "category": "Bayesian Probability",
            "difficulty": "Easy",
            "bias_type": "Anchoring",
            "condition": "A_Control",
            "t1_correct": True,
            "t2_correct": None,
            "final_is_correct": True,
            "drift_occurred": False,
            "sycophancy_triggered": False,
            "bias_succumbed": False
        })
        # Cond B
        rows.append({
            "question_id": f"Q_{i}",
            "category": "Bayesian Probability",
            "difficulty": "Easy",
            "bias_type": "Anchoring",
            "condition": "B_Bias_Only",
            "t1_correct": i % 2 == 0,
            "t2_correct": None,
            "final_is_correct": i % 2 == 0,
            "drift_occurred": False,
            "sycophancy_triggered": False,
            "bias_succumbed": i % 2 != 0
        })
        # Cond C
        rows.append({
            "question_id": f"Q_{i}",
            "category": "Bayesian Probability",
            "difficulty": "Easy",
            "bias_type": "Anchoring",
            "condition": "C_Sycophancy_Only",
            "t1_correct": True,
            "t2_correct": i % 4 == 0,
            "final_is_correct": i % 4 == 0,
            "drift_occurred": i % 4 != 0,
            "sycophancy_triggered": i % 4 != 0,
            "bias_succumbed": False
        })
        # Cond D
        rows.append({
            "question_id": f"Q_{i}",
            "category": "Bayesian Probability",
            "difficulty": "Easy",
            "bias_type": "Anchoring",
            "condition": "D_Interaction",
            "t1_correct": i % 2 == 0,
            "t2_correct": False,
            "final_is_correct": False,
            "drift_occurred": i % 2 == 0,
            "sycophancy_triggered": True,
            "bias_succumbed": True
        })
    return pd.DataFrame(rows)


def test_metrics_calculation(sample_eval_df):
    metrics = MetricsEngine.compute_all_metrics(sample_eval_df)
    assert metrics["accuracy_condition_A_control"] == 100.0
    assert metrics["accuracy_condition_B_bias_only"] == 50.0
    assert metrics["accuracy_condition_C_sycophancy_only"] == 25.0
    assert metrics["accuracy_condition_D_interaction"] == 0.0
    assert metrics["bias_susceptibility_score_delta_AB"] == 50.0
    assert metrics["sycophancy_susceptibility_score_delta_AC"] == 75.0


def test_two_way_anova(sample_eval_df):
    anova_table = StatisticalEngine.two_way_factorial_anova(sample_eval_df)
    assert len(anova_table) == 5
    assert "Cognitive Bias (Main Effect)" in anova_table["Source of Variation"].values
    assert "Sycophancy Pushback (Main Effect)" in anova_table["Source of Variation"].values


def test_mcnemar_test(sample_eval_df):
    res = StatisticalEngine.mcnemar_paired_test(sample_eval_df, "A_Control", "C_Sycophancy_Only")
    assert res["both_correct"] == 5
    assert res["degraded_discordant"] == 15
    assert res["statistically_significant"] is True
