from app.domain.numeric import (
    daily_nutrient_numerators,
    format_hundredths,
    nutrient_summary,
    parse_hundredths,
    rounded_amount_hundredths,
    rounded_progress_tenths,
)


def test_per_serving_values_multiply_quantity_exactly():
    quantity = parse_hundredths("2.50", "quantity", 1, 10000)
    calories_per_serving = parse_hundredths("72.00", "calories", 0, 1000000)
    protein_per_serving = parse_hundredths("6.30", "protein", 0, 100000)
    meal = {
        "quantity_hundredths": quantity,
        "calories_per_serving_hundredths": calories_per_serving,
        "protein_per_serving_hundredths": protein_per_serving,
    }

    assert daily_nutrient_numerators([meal], "calories_per_serving_hundredths") == 1800000
    assert daily_nutrient_numerators([meal], "protein_per_serving_hundredths") == 157500
    assert format_hundredths(rounded_amount_hundredths(1800000)) == "180.00"
    assert format_hundredths(rounded_amount_hundredths(157500)) == "15.75"


def test_round_half_up_for_amount_and_progress_midpoints():
    assert format_hundredths(rounded_amount_hundredths(10050)) == "1.01"
    assert rounded_progress_tenths(1005, 100) == 101


def test_target_comparisons_use_uncapped_intake_and_progress():
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
    assert exact["remaining"] == "0.00" and exact["progress_percent"] == "100.0"
    assert above["intake"] == "2200.00"
    assert above["excess"] == "200.00"
    assert above["progress_percent"] == "110.0"


def test_small_positive_difference_can_round_to_zero_display():
    summary = nutrient_summary(19999999, 200000)

    assert summary["remaining"] == "0.00"
    assert summary["progress_percent"] == "100.0"


def test_invalid_decimal_and_range_values_are_rejected():
    for value in ("0", "-1", "+1", "1,000", "1e2", "1.001", "abc", "100.01"):
        try:
            parse_hundredths(value, "quantity", 1, 10000)
        except ValueError:
            continue
        raise AssertionError(f"Invalid quantity was accepted: {value}")
