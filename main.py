from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone
import os, json, socket, time
import psutil
from openai import OpenAI

app = FastAPI()
BOOT_TIME = psutil.boot_time()

def get_openai_client() -> OpenAI:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        # Don't crash the app — only the AI endpoint should fail
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY not set on server")
    return OpenAI(api_key=key)

def format_health_for_ai(health_data: dict) -> str:
    return (
        "Summarize this server health JSON for an operator.\n"
        "Return: 1) overall status, 2) biggest risks, 3) 3 recommended actions.\n\n"
        + json.dumps(health_data, indent=2)
    )

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


@app.get("/api/health/summary")
def health_summary():
    health_data = health()
    prompt = format_health_for_ai(health_data)

    try:
        client = get_openai_client()
    except HTTPException:
        return {
            "summary": "AI summary unavailable (OPENAI_API_KEY not set).",
            "health": health_data,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    resp = client.responses.create(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": "You are a senior site reliability engineer. Be concise and specific."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return {
        "summary": resp.output_text,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

