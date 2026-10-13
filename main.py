import os
import time
import uuid
from typing import Callable, Awaitable

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Scope, Receive, Send, Message

EMAIL = "24f2005619@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-sh27fw.example.com"

api = FastAPI(title="CORS-Aware Metrics API")


@api.get("/stats")
async def stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        parts = values.split(",")
        if not parts or any(part.strip() == "" for part in parts):
            raise ValueError("Empty integer")
        numbers = [int(part.strip()) for part in parts]
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="values must be a comma-separated list of integers",
        )

    count = len(numbers)
    total = sum(numbers)
    return {
        "email": EMAIL,
        "count": count,
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / count,
    }


# Starlette's CORS middleware handles browser preflights. It only grants
# access to the single assigned origin; other origins receive no ACAO header.
cors_app = CORSMiddleware(
    app=api,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


class MetricsHeadersMiddleware:
    """Add request ID and elapsed time to every HTTP response, including CORS preflights."""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        started = time.perf_counter()
        request_id = str(uuid.uuid4())

        async def send_with_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                elapsed = max(0.0, time.perf_counter() - started)
                headers = list(message.get("headers", []))
                headers.extend([
                    (b"x-request-id", request_id.encode("ascii")),
                    (b"x-process-time", f"{elapsed:.6f}".encode("ascii")),
                ])
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_with_headers)


# Wrap CORS with the header middleware so headers are included on preflight
# responses as well as normal endpoint responses.
app = MetricsHeadersMiddleware(cors_app)
