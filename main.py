from fastapi import FastAPI, Response # type: ignore
from datetime import datetime, timezone
import os
import socket
from pydantic import BaseModel # type: ignore
from openai import OpenAI # type: ignore

app = FastAPI()
STARTED_AT = datetime.now(timezone.utc)

class ExplainIn(BaseModel):
    health: dict
    status: dict

def get_client():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")
    return OpenAI()  # reads OPENAI_API_KEY from env  [oai_citation:0‡OpenAI Platform](https://platform.openai.com/docs/quickstart?utm_source=chatgpt.com)

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



@app.post("/api/ai/health-explain")
def ai_health_explain(payload: ExplainIn):
    health = payload.health
    status = payload.status

    if len(str(health)) > 2000 or len(str(status)) > 2000:
        return {"reply": "Health data too large to summarize safely."}

    if not os.getenv("OPENAI_API_KEY"):
        return {"reply": "AI service unavailable (missing API key)."}

    prompt = f"""Explain this service health in plain English.
Use 6–10 short bullets.
Include overall status, uptime, hostname, version, and any red flags.
If everything looks normal, say so.

health.json: {health}
status.json: {status}
"""

    client = OpenAI()
    resp = client.responses.create(
        model=os.getenv("AI_MODEL", "gpt-4.1-mini"),
        input=[
            {"role": "system", "content": "You are an SRE summarizing service health for operators."},
            {"role": "user", "content": prompt}
        ],
    )

    return {"reply": resp.output_text}

