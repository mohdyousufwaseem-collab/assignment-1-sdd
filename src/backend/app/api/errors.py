from fastapi import HTTPException


def validation_error(fields: dict[str, str]) -> HTTPException:
    return HTTPException(
        status_code=422,
        detail={
            "code": "validation_failed",
            "message": "One or more fields are invalid.",
            "fields": fields,
        },
    )


def not_found_error() -> HTTPException:
    return HTTPException(
        status_code=404,
        detail={"code": "not_found", "message": "Meal entry was not found."},
    )


def persistence_error() -> HTTPException:
    return HTTPException(
        status_code=500,
        detail={
            "code": "persistence_failed",
            "message": "The change could not be saved. The last saved data is unchanged.",
        },
    )