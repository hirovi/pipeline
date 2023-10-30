import asyncio
import logging
import os
import traceback
import uuid

from fastapi import APIRouter, FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from pipeline.container.manager import Manager
from pipeline.container.run import execution_handler
from pipeline.container.run import router as run_router
from pipeline.container.status import router as status_router

logger = logging.getLogger("uvicorn")


def create_app() -> FastAPI:
    app = FastAPI(
        title="pipeline-container",
    )

    setup_oapi(app)
    setup_middlewares(app)

    app.state.execution_queue = asyncio.Queue()
    app.state.manager = Manager(
        pipeline_path=os.environ.get(
            "PIPELINE_PATH",
            "",
        )
    )
    asyncio.create_task(execution_handler(app.state.execution_queue, app.state.manager))

    router = APIRouter(prefix="/v1")

    router.include_router(status_router)
    router.include_router(run_router)

    app.include_router(router)

    return app


def setup_middlewares(app: FastAPI) -> None:
    @app.middleware("http")
    async def _(request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(e)
            return JSONResponse(
                status_code=500,
                content={
                    "traceback": str(traceback.format_exc()),
                },
            )
        return response

    @app.middleware("http")
    async def _(request: Request, call_next):
        request.state.request_id = request.headers.get("X-Request-Id") or str(
            uuid.uuid4()
        )
        response = await call_next(request)
        response.headers["X-Request-Id"] = request.state.request_id
        return response


def setup_oapi(app: FastAPI) -> None:
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="pipeline-container",
            version="1.1.0",
            routes=app.routes,
            servers=[{"url": "http://localhost:14300"}],
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi