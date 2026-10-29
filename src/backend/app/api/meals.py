import sqlite3

from fastapi import APIRouter, HTTPException, Response, status

from app.api.errors import not_found_error, persistence_error, validation_error
from app.api.schemas import Meal, MealInput
from app.domain.meals import InputValidationError, serialize_meal, validate_and_convert_meal
from app.storage.meals import create_meal, delete_meal, replace_meal


router = APIRouter()


def convert_input(meal_input: MealInput) -> dict:
    try:
        return validate_and_convert_meal(meal_input)
    except InputValidationError as error:
        raise validation_error({error.field: str(error)}) from error


@router.post("/meals", response_model=Meal, status_code=status.HTTP_201_CREATED)
def post_meal(meal_input: MealInput):
    values = convert_input(meal_input)
    try:
        return serialize_meal(create_meal(values))
    except (sqlite3.Error, OSError):
        raise persistence_error() from None


@router.put("/meals/{meal_id}", response_model=Meal)
def put_meal(meal_id: int, meal_input: MealInput):
    values = convert_input(meal_input)
    try:
        updated = replace_meal(meal_id, values)
    except (sqlite3.Error, OSError):
        raise persistence_error() from None
    if updated is None:
        raise not_found_error()
    return serialize_meal(updated)


@router.delete("/meals/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_meal(meal_id: int):
    try:
        deleted = delete_meal(meal_id)
    except (sqlite3.Error, OSError):
        raise persistence_error() from None
    if not deleted:
        raise not_found_error()
    return Response(status_code=status.HTTP_204_NO_CONTENT)