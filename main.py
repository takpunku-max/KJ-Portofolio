from fastapi import FastAPI # type: ignore
from datetime import datetime, timezone
import os
import socket

app = FastAPI()
STARTED_AT = datetime.now(timezone.utc)

@app.get("/")
def root():
    return {"status": "ok", "message": "Hello from FastAPI in Docker on EC2"}

@app.get("/api/status")
def status():
    return {
        "status": "ok",
        "service": "fastapi",
        "host": socket.gethostname(),
        "utc": datetime.now(timezone.utc).isoformat(),
        "version": os.getenv("APP_VERSION", "v1"),
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "fastapi-app",
        "time_utc": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": int((datetime.now(timezone.utc) - STARTED_AT).total_seconds()),
        "hostname": os.uname().nodename,
    }

