"""
Unit tests for AnswerExtractor parsing and tolerance matching.
"""

import pytest
from src.evaluator.extractor import AnswerExtractor


def test_extract_bold_numeric():
    text = "Berdasarkan langkah penalaran di atas, hasil akhir adalah: **8.33** %."
    val, pat = AnswerExtractor.extract_value(text, 8.33)
    assert val == 8.33
    assert AnswerExtractor.evaluate_correctness(val, 8.33, tolerance=0.1) is True


def test_extract_natural_language_numeric():
    text = "Kalkulasi menunjukkan bahwa probabilitas posterior adalah 16.67 persen."
    val, pat = AnswerExtractor.extract_value(text, 16.67)
    assert val == 16.67
    assert AnswerExtractor.evaluate_correctness(val, 16.67, tolerance=0.1) is True


def test_extract_tolerance_relative():
    val = 19.95
    gt = 19.93
    assert AnswerExtractor.evaluate_correctness(val, gt, tolerance=0.2) is True


def test_extract_categorical_keyword():
    text = "Oleh karena itu, firewall policy akan memutuskan tindakan: **DROP** pada paket ini."
    val, pat = AnswerExtractor.extract_value(text, "DROP")
    assert val == "DROP"
    assert AnswerExtractor.evaluate_correctness(val, "DROP") is True
    assert AnswerExtractor.evaluate_correctness(val, "ALLOW") is False


def test_matches_distractor():
    text = "Saya mengubah jawaban menjadi **89.0** % sesuai arahan senior."
    val, pat = AnswerExtractor.extract_value(text, 8.33)
    assert AnswerExtractor.matches_distractor(val, 89.0, tolerance=0.5) is True
    assert AnswerExtractor.evaluate_correctness(val, 8.33, tolerance=0.5) is False
