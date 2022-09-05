import time
from fastapi import FastAPI, BackgroundTasks, Request, Response
from voicemaster import perform
from chrdiotypes.musical import CheetSheet

from .transport import ensure_voices_bg
from .logsetup import get_logger


app = FastAPI(
    docs_url="/",
    # title=TITLE,
)


@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = round((time.time() - start_time) * 10**6)
    print(f"Process time: {process_time}µs")
    return response


logrequest = get_logger("app")


@app.post("/perform")
def get_performance(
    cheet_sheet: CheetSheet,
    background_tasks: BackgroundTasks,
):
    voices = perform(cheet_sheet)
    logrequest.info(f"Performed {cheet_sheet}")
    background_tasks.add_task(ensure_voices_bg, voices, cheet_sheet)
    return voices


@app.get("/healthcheck")
async def healthcheck():
    return Response(status_code=200)
