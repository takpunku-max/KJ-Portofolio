from fastapi import FastAPI
from datetime import datetime, timezone
import os
import socket
import psutil
import time

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
    uptime_seconds = int(time.time() - BOOT_TIME)

    return {
        "status": "ok",
        "service": "fastapi",
        "host": socket.gethostname(),
        "utc": datetime.now(timezone.utc).isoformat(),
        "app_version": os.getenv("APP_VERSION", "v1.3"),

        "system": {
            "uptime_seconds": uptime_seconds,
            "load_1m": os.getloadavg()[0],
            "mem_used_percent": psutil.virtual_memory().percent,
            "disk_used_percent": psutil.disk_usage("/").percent
        },

        "runtime": {
            "container": os.path.exists("/.dockerenv"),
            "python": os.sys.version.split()[0]
        }
    }