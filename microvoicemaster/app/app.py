import time
from fastapi import FastAPI, BackgroundTasks, Request, Response
from voicemaster import perform
from chrdiotypes.musical import CheetSheet

from ..transport import ensure_voices_bg


app = FastAPI(
    docs_url="/",
)


@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = round((time.time() - start_time) * 10**6)
    print(f"Process time: {process_time}µs")
    return response


@app.post("/perform")
def get_performance(
    cheet_sheet: CheetSheet,
    background_tasks: BackgroundTasks,
):
    voices = perform(cheet_sheet)
    background_tasks.add_task(ensure_voices_bg, voices, cheet_sheet)
    return voices


@app.get("/healthcheck")
async def healthcheck():
    return Response(status_code=200)
