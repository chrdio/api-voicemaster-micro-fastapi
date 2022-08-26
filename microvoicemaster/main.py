import json
import time
from fastapi import FastAPI, BackgroundTasks, Request
from voicemaster import perform
from chrdiotypes.transport import CheetSheet

from transport import ensure_voices_bg
from logsetup import get_logger

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    TITLE = config["title"]
    PORT = config["port"]
    HOST = config["host"]
    RELOAD = config["reload"]

app = FastAPI(
    docs_url="/",
    title=TITLE,
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


if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=RELOAD)
