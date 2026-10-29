import sqlite3

from fastapi import APIRouter

from app.api.errors import persistence_error, validation_error
from app.api.schemas import Targets, TargetsInput
from app.domain.meals import InputValidationError
from app.domain.targets import serialize_targets, validate_targets
from app.storage.targets import get_targets, replace_targets


router = APIRouter()


@router.get("/targets", response_model=Targets)
def read_targets():
    try:
        return serialize_targets(get_targets())
    except (sqlite3.Error, OSError, RuntimeError):
        raise persistence_error() from None


@router.put("/targets", response_model=Targets)
def put_targets(targets_input: TargetsInput):
    try:
        calories, protein = validate_targets(targets_input)
    except InputValidationError as error:
        raise validation_error({error.field: str(error)}) from error
    try:
        return serialize_targets(replace_targets(calories, protein))
    except (sqlite3.Error, OSError, RuntimeError):
        raise persistence_error() from None