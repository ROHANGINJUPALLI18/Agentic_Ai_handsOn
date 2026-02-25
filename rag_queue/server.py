from dotenv import load_dotenv
from fastapi import FastAPI, Query, Path
from client.rq_client import queue
from queues.worker import process_query

load_dotenv()


app = FastAPI()


@app.get("/")
def root():
    return {"status":"server is up and running"}

@app.post("/chat")
def chat(
    quer: str = Query(..., description="The chat query from the user")
):
    job = queue.enqueue(process_query, quer)
    return {"job_id": job.id, "status": "queued"}

@app.get("/job-status/{job_id}")
def get_job_status(job_id: str = Path(..., description="The job id to check the status of the job")):
    job = queue.fetch_job(job_id)
    res = job.return_value()
    return{"result":res}