from fastapi import FastAPI
from datetime import datetime
import os
import socket

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Hello from FastAPI in Docker on EC2"}

@app.get("/api/status")
def status():
	return {
        "status": "ok",
        "service": "fastapi",
        "host": socket.gethostname(),
        "utc": dateime.now(timezone.utc).isoformat(),
        "version": os.getenv ("APP_VERSION", "v1"),
        }
