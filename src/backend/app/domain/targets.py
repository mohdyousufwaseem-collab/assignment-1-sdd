import sqlite3

from app.domain.meals import InputValidationError
from app.domain.numeric import format_hundredths, parse_hundredths


def validate_targets(targets_input) -> tuple[int, int]:
    try:
        calories = parse_hundredths(targets_input.calories, "calories", 100, 10000000)
    except ValueError as error:
        raise InputValidationError("calories", str(error)) from error
    try:
        protein = parse_hundredths(targets_input.protein, "protein", 1, 1000000)
    except ValueError as error:
        raise InputValidationError("protein", str(error)) from error
    return calories, protein


def serialize_targets(targets: dict) -> dict[str, str]:
    return {
        "calories": format_hundredths(targets["calorie_target_hundredths"]),
        "protein": format_hundredths(targets["protein_target_hundredths"]),
    }


def get_target_values(targets: dict) -> tuple[int, int]:
    return (
        targets["calorie_target_hundredths"],
        targets["protein_target_hundredths"],
    )