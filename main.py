from fastapi import FastAPI
from datetime import datetime, timezone
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
        "utc": datetime.now(timezone.utc).isoformat(),
        "version": os.getenv("APP_VERSION", "v1"),
    }

@app.get("/api/system")
def system():
    return {
        "status": "ok",
        "service": "fastapi",
        "host": "ip-172-31-xx-xx",
        "utc": "2025-12-13T18:12:01Z",
        "app_version": "v1",

        "system": {
            "uptime_seconds": 123456,
            "load_1m": 0.12,
            "mem_used_percent": 41.3,
            "disk_used_percent": 28.9
        },

        "runtime": {
            "container": true,
            "python": "3.11.6"
        }
    }