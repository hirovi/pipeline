import asyncio
import logging

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from pipeline.cloud.schemas import runs as run_schemas
from pipeline.container.manager import Manager

logger = logging.getLogger("uvicorn")
router = APIRouter(prefix="/run")


@router.post(
    "",
    tags=["run"],
    status_code=200,
    # response_model=run_schemas.Run,
)
async def run(run_create: run_schemas.RunCreate, request: Request):
    outputs = await request.app.state.manager.run(run_create.input_data)

    return outputs


async def execution_handler(execution_queue: asyncio.Queue, manager: Manager) -> None:
    while True:
        try:
            args, response_queue, async_run = await execution_queue.get()

            output = await manager.run(*args)
            response_queue.put_nowait(output)
        except Exception:
            logger.exception("Got an error in the execution loop handler")


@router.get("/form", tags=["run"], response_class=HTMLResponse)
async def get_pipeline_form():
    import os

    with open(os.path.join("/app/pipeline/container", "app.tsx"), "r") as file:
        ts_code = file.read()
    return f"""
    <!-- Your code that needs compiling goes in a type="text/babel" `script` tag -->
    <script type="text/babel" data-presets="react,stage-3">
    {ts_code}

    ReactDOM.render(<App />, document.getElementById("root"));
    </script>

    <div id="root"></div>

    <!-- This is what supports JSX compilation (and other transformations) -->

    <script src="https://unpkg.com/@babel/standalone@7.10.3/babel.min.js"></script>

    <link
        href="https://cdn.jsdelivr.net/npm/tailwindcss@2/dist/tailwind.min.css"
        rel="stylesheet"
    >

    <!-- These are for React -->
    <script
    src="https://cdnjs.cloudflare.com/ajax/libs/react/17.0.2/umd/react.development.js"
    ></script>
    <script
    src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/17.0.2/umd/react-dom.development.js"
    ></script>
    """
