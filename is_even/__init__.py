from __future__ import annotations

from math import isinf, isnan
from random import choice
from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi.responses import JSONResponse

if TYPE_CHECKING:
    from typing import Any

app = FastAPI(
    debug=False,
    title="Is Even?",
    version="0.1.0",
    openapi_url=None,
    redoc_url=None,
    docs_url=None,
)

SARCASTIC_RESPONSES: list[str] = [
    "God I wish I was as funny as you.",
    "Wow I hadn't ever thought of that one!!!",
    "Is this how you get your rocks off? Pervert.",
]


@app.get("/{number}")
async def is_even(number: int | float) -> JSONResponse:
    is_even = number % 2 == 0
    response: dict[str, Any] = {"number": number, "is_even": is_even}
    if isinf(number) or isnan(number):
        response["number"] = str(number)
        response["extra"] = choice(SARCASTIC_RESPONSES)

    return JSONResponse(response, status_code=200)
