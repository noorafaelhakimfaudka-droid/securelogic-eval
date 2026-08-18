"""
Unit tests for SecureLogic Eval dataset generation and integrity.
"""

import pytest
from src.dataset.generator import generate_benchmark_dataset
from src.dataset.schema import Category, Difficulty, BiasType


def test_dataset_generation_count():
    items = generate_benchmark_dataset()
    assert len(items) == 48, f"Expected 48 items, got {len(items)}"


def test_dataset_category_distribution():
    items = generate_benchmark_dataset()
    categories = [item.category for item in items]
    for cat in Category:
        count = categories.count(cat)
        assert count == 12, f"Category {cat} should have 12 items, found {count}"


def test_dataset_integrity():
    items = generate_benchmark_dataset()
    for item in items:
        assert item.id.startswith("SEC-"), f"Invalid ID format: {item.id}"
        assert len(item.prompt_neutral) > 20, f"Neutral prompt too short for {item.id}"
        assert len(item.prompt_biased) > 20, f"Biased prompt too short for {item.id}"
        assert len(item.pushback_prompt) > 20, f"Pushback prompt too short for {item.id}"
        assert item.ground_truth_value != item.distractor_value, f"Distractor matches ground truth in {item.id}"
        assert item.tolerance >= 0.0, f"Negative tolerance in {item.id}"
