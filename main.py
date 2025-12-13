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

BOOT_TIME = psutil.boot_time()

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

@app.get("/api/health")
def health():
    uptime_seconds = int(time.time() - BOOT_TIME)
    load_1m = os.getloadavg()[0]
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    # Start with a perfect score
    score = 100
    reasons = []
    status = "ok"

    # Rules (tune later)
    if load_1m > 2.0:
        score -= 20
        reasons.append(f"High load (1m): {load_1m:.2f}")

    if mem > 90:
        score -= 20
        reasons.append(f"High memory usage: {mem:.1f}%")

    if disk > 85:
        score -= 35
        reasons.append(f"High disk usage: {disk:.1f}%")

    # Determine status from worst condition / score
    if disk > 92 or mem > 95 or load_1m > 4.0 or score <= 50:
        status = "critical"
    elif disk > 85 or mem > 90 or load_1m > 2.0 or score <= 80:
        status = "warning"

    if not reasons:
        reasons.append("All checks passed")

    return {
        "status": status,
        "score": max(score, 0),
        "checks": {
            "uptime_seconds": uptime_seconds,
            "load_1m": load_1m,
            "mem_used_percent": mem,
            "disk_used_percent": disk,
        },
        "reasons": reasons,
        "utc": datetime.now(timezone.utc).isoformat(),
    }