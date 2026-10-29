from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


MealCategory = Literal["Breakfast", "Lunch", "Dinner", "Snack"]
InputDecimal = str
OutputAmount = str


class MealInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    category: MealCategory
    date: str
    quantity: InputDecimal = Field(pattern=r"^[0-9]+(?:\.[0-9]{1,2})?$")
    calories_per_serving: InputDecimal = Field(pattern=r"^[0-9]+(?:\.[0-9]{1,2})?$")
    protein_per_serving: InputDecimal = Field(pattern=r"^[0-9]+(?:\.[0-9]{1,2})?$")


class Meal(MealInput):
    id: int = Field(ge=1)
    quantity: OutputAmount
    calories_per_serving: OutputAmount
    protein_per_serving: OutputAmount


class TargetsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    calories: InputDecimal = Field(pattern=r"^[0-9]+(?:\.[0-9]{1,2})?$")
    protein: InputDecimal = Field(pattern=r"^[0-9]+(?:\.[0-9]{1,2})?$")


class Targets(TargetsInput):
    calories: OutputAmount
    protein: OutputAmount


class NutrientSummary(BaseModel):
    intake: OutputAmount
    target: OutputAmount
    remaining: OutputAmount
    excess: OutputAmount
    progress_percent: str


class DaySummary(BaseModel):
    calories: NutrientSummary
    protein: NutrientSummary


class DayResponse(BaseModel):
    date: str
    has_entries: bool
    meals: list[Meal]
    summary: DaySummary


class ErrorDetail(BaseModel):
    code: Literal["validation_failed", "not_found", "persistence_failed"]
    message: str
    fields: dict[str, str] | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail