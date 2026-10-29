from pathlib import Path
from urllib.parse import urlsplit

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.router import router as api_router
from app.config import get_database_path
from app.storage.database import initialize_database


STATIC_DIRECTORY = Path(__file__).with_name("static")
LOCAL_HOSTNAMES = {"127.0.0.1", "localhost"}

app = FastAPI(title="Calorie and Nutrition Tracker Local API", version="1.0.0")


@app.on_event("startup")
def initialize_local_store() -> None:
    initialize_database(get_database_path())


@app.middleware("http")
async def restrict_local_mutations(request: Request, call_next):
    if request.method not in {"GET", "HEAD", "OPTIONS"}:
        host = request.headers.get("host", "").split(":", 1)[0].strip("[]").lower()
        origin = request.headers.get("origin")
        origin_host = urlsplit(origin).hostname.lower() if origin else None
        if host not in LOCAL_HOSTNAMES or (origin_host and origin_host not in LOCAL_HOSTNAMES):
            return JSONResponse(
                status_code=400,
                content={
                    "error": {
                        "code": "validation_failed",
                        "message": "Requests must use the local application origin.",
                        "fields": {"origin": "Only localhost and 127.0.0.1 are accepted."},
                    }
                },
            )
    return await call_next(request)


@app.exception_handler(HTTPException)
@app.exception_handler(StarletteHTTPException)
async def handle_http_error(_request: Request, exception: HTTPException) -> JSONResponse:
    detail = exception.detail
    if isinstance(detail, dict) and "code" in detail:
        payload = {"error": detail}
    else:
        code = "not_found" if exception.status_code == 404 else "request_failed"
        payload = {"error": {"code": code, "message": str(detail)}}
    return JSONResponse(status_code=exception.status_code, content=payload)


@app.exception_handler(RequestValidationError)
async def handle_request_validation(_request: Request, exception: RequestValidationError) -> JSONResponse:
    fields: dict[str, str] = {}
    for error in exception.errors():
        location = error.get("loc", ())
        field = str(location[-1]) if location else "request"
        fields[field] = str(error.get("msg", "Invalid value."))
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "validation_failed",
                "message": "One or more fields are invalid.",
                "fields": fields,
            }
        },
    )


app.include_router(api_router)
app.mount("/", StaticFiles(directory=STATIC_DIRECTORY, html=True), name="frontend")