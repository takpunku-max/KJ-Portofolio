from fastapi import FastAPI
from datime import datetime

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Hello from FastAPI in Docker on EC2"}

@app.get("/api/status")
def status():
	return {"status": "ok"}
