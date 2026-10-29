import sqlite3

from fastapi import APIRouter

from app.api.errors import persistence_error, validation_error
from app.api.schemas import DayResponse
from app.domain.meals import InputValidationError, make_day_response, validate_entry_date
from app.storage.meals import list_meals
from app.storage.targets import get_targets


router = APIRouter()


@router.get("/days/{entry_date}", response_model=DayResponse)
def get_day(entry_date: str):
    try:
        valid_date = validate_entry_date(entry_date)
        meals = list_meals(valid_date)
        targets = get_targets()
        return make_day_response(
            valid_date,
            meals,
            targets["calorie_target_hundredths"],
            targets["protein_target_hundredths"],
        )
    except InputValidationError as error:
        raise validation_error({error.field: str(error)}) from error
    except (sqlite3.Error, OSError):
        raise persistence_error() from None