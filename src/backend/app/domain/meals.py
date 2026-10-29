import re
from datetime import date

from app.domain.numeric import (
    daily_nutrient_numerators,
    format_hundredths,
    nutrient_summary,
    parse_hundredths,
)


class InputValidationError(ValueError):
    def __init__(self, field: str, message: str):
        super().__init__(message)
        self.field = field


MEAL_CATEGORIES = {"Breakfast", "Lunch", "Dinner", "Snack"}
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ENTRY_NUMERIC_RULES = {
    "quantity": (1, 10000),
    "calories_per_serving": (0, 1000000),
    "protein_per_serving": (0, 100000),
}


def validate_entry_date(value: str) -> str:
    if not isinstance(value, str) or not ISO_DATE.fullmatch(value):
        raise InputValidationError("date", "Enter a valid calendar date in YYYY-MM-DD format.")
    try:
        parsed_date = date.fromisoformat(value)
    except ValueError as error:
        raise InputValidationError("date", "Enter a real calendar date.") from error
    if parsed_date.isoformat() != value:
        raise InputValidationError("date", "Enter a valid calendar date in YYYY-MM-DD format.")
    if parsed_date > date.today():
        raise InputValidationError("date", "Future dates are not allowed.")
    return value


def validate_and_convert_meal(meal_input) -> dict:
    name = meal_input.name.strip()
    if not name:
        raise InputValidationError("name", "Enter a food name.")
    if len(name) > 80:
        raise InputValidationError("name", "Food name must be at most 80 characters after trimming.")
    if meal_input.category not in MEAL_CATEGORIES:
        raise InputValidationError("category", "Choose Breakfast, Lunch, Dinner, or Snack.")

    converted = {
        "name": name,
        "category": meal_input.category,
        "entry_date": validate_entry_date(meal_input.date),
    }
    for field, (minimum, maximum) in ENTRY_NUMERIC_RULES.items():
        try:
            converted[f"{field}_hundredths"] = parse_hundredths(
                getattr(meal_input, field), field, minimum, maximum
            )
        except ValueError as error:
            raise InputValidationError(field, str(error)) from error
    return converted


def serialize_meal(meal: dict) -> dict:
    return {
        "id": meal["id"],
        "name": meal["name"],
        "category": meal["category"],
        "date": meal["entry_date"],
        "quantity": format_hundredths(meal["quantity_hundredths"]),
        "calories_per_serving": format_hundredths(meal["calories_per_serving_hundredths"]),
        "protein_per_serving": format_hundredths(meal["protein_per_serving_hundredths"]),
    }


def make_day_response(
    entry_date: str,
    meals: list[dict],
    calorie_target: int,
    protein_target: int,
) -> dict:
    calories_numerator = daily_nutrient_numerators(meals, "calories_per_serving_hundredths")
    protein_numerator = daily_nutrient_numerators(meals, "protein_per_serving_hundredths")
    return {
        "date": entry_date,
        "has_entries": bool(meals),
        "meals": [serialize_meal(meal) for meal in meals],
        "summary": {
            "calories": nutrient_summary(calories_numerator, calorie_target),
            "protein": nutrient_summary(protein_numerator, protein_target),
        },
    }