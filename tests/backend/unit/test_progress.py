from app.domain.numeric import nutrient_summary, parse_hundredths


def test_below_equal_and_above_target_summaries():
    below = nutrient_summary(12000000, 200000)
    exact = nutrient_summary(20000000, 200000)
    above = nutrient_summary(22000000, 200000)

    assert below == {
        "intake": "1200.00",
        "target": "2000.00",
        "remaining": "800.00",
        "excess": "0.00",
        "progress_percent": "60.0",
    }
    assert exact["remaining"] == "0.00"
    assert exact["excess"] == "0.00"
    assert exact["progress_percent"] == "100.0"
    assert above["intake"] == "2200.00"
    assert above["excess"] == "200.00"
    assert above["progress_percent"] == "110.0"


def test_protein_progress_and_round_half_up_boundaries():
    protein_target = parse_hundredths("50.00", "protein", 1, 1000000)
    assert nutrient_summary(400000, protein_target)["progress_percent"] == "80.0"
    assert nutrient_summary(650000, protein_target)["progress_percent"] == "130.0"
    assert nutrient_summary(10005000, 100000)["progress_percent"] == "100.1"
    assert nutrient_summary(10050000, 100000)["progress_percent"] == "100.5"
    assert nutrient_summary(10050, 100000)["intake"] == "1.01"


def test_small_positive_remaining_uses_unrounded_comparison():
    summary = nutrient_summary(19999999, 200000)

    assert summary["remaining"] == "0.00"
    assert summary["excess"] == "0.00"
    assert summary["progress_percent"] == "100.0"
