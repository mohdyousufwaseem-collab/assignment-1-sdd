import re


DECIMAL_INPUT = re.compile(r"^[0-9]+(?:\.[0-9]{1,2})?$")


def parse_hundredths(value: str, field: str, minimum: int, maximum: int) -> int:
    if not isinstance(value, str) or not DECIMAL_INPUT.fullmatch(value):
        raise ValueError(f"{field} must be an unsigned decimal with at most two fractional digits.")

    whole, separator, fraction = value.partition(".")
    scaled = int(whole) * 100 + int((fraction + "00")[:2]) if separator else int(whole) * 100
    if not minimum <= scaled <= maximum:
        raise ValueError(f"{field} must be within the inclusive allowed range.")
    return scaled


def format_hundredths(value: int) -> str:
    if value < 0:
        raise ValueError("Amounts must be nonnegative.")
    return f"{value // 100}.{value % 100:02d}"


def format_tenths(value: int) -> str:
    if value < 0:
        raise ValueError("Progress must be nonnegative.")
    return f"{value // 10}.{value % 10}"


def rounded_amount_hundredths(numerator: int) -> int:
    if numerator < 0:
        raise ValueError("Amounts must be nonnegative.")
    return (numerator + 50) // 100


def rounded_progress_tenths(intake_numerator: int, target_hundredths: int) -> int:
    if intake_numerator < 0 or target_hundredths <= 0:
        raise ValueError("Intake must be nonnegative and target must be positive.")
    return (20 * intake_numerator + target_hundredths) // (2 * target_hundredths)


def nutrient_summary(intake_numerator: int, target_hundredths: int) -> dict[str, str]:
    target_numerator = target_hundredths * 100
    remaining_numerator = max(target_numerator - intake_numerator, 0)
    excess_numerator = max(intake_numerator - target_numerator, 0)
    return {
        "intake": format_hundredths(rounded_amount_hundredths(intake_numerator)),
        "target": format_hundredths(target_hundredths),
        "remaining": format_hundredths(rounded_amount_hundredths(remaining_numerator)),
        "excess": format_hundredths(rounded_amount_hundredths(excess_numerator)),
        "progress_percent": format_tenths(rounded_progress_tenths(intake_numerator, target_hundredths)),
    }


def daily_nutrient_numerators(meals: list[dict], nutrient_field: str) -> int:
    return sum(
        meal["quantity_hundredths"] * meal[nutrient_field]
        for meal in meals
    )