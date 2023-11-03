import logging
import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

logger = logging.getLogger("uvicorn")
router = APIRouter(prefix="/play", tags=["play"])


@router.get("", response_class=HTMLResponse)
async def render_pipeline_play():
    with open(
        os.path.join("/app/pipeline/container/frontend", "index.html"), "r"
    ) as file:
        ts_code = file.read()

    return f"""{ts_code}"""
