import time
from fastapi import FastAPI, BackgroundTasks, Request, Response
from voicemaster import perform
from chrdiotypes.musical import CheetSheet, PseudoMIDI

from ..transport import register_with_database


app = FastAPI(
    docs_url="/",
)


@app.middleware("http")
async def add_process_time(request: Request, call_next):
    """Spits out the processing time for every request."""

    start_time = time.time()
    response = await call_next(request)
    process_time = round((time.time() - start_time) * 10**6)
    print(f"Process time: {process_time}µs")
    return response


@app.post("/perform")
def get_performance(
    cheet_sheet: CheetSheet,
    background_tasks: BackgroundTasks,
    ) -> PseudoMIDI:
    """Generates a voicemaster-native PseudoMIDI object based on
    an API-native CheetSheet object specified in a request.
    Returns it and then
    registers it with the database microservice.
    """

    voices = perform(cheet_sheet)
    background_tasks.add_task(register_with_database, voices, cheet_sheet)
    return voices


@app.get("/healthcheck")
async def healthcheck():
    """An enpoint to make sure this instance is up-and-running."""
    return Response(status_code=200)
