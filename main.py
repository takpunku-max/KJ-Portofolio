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

client = OpenAI()  # reads OPENAI_API_KEY from env  [oai_citation:0‡OpenAI Platform](https://platform.openai.com/docs/quickstart?utm_source=chatgpt.com)

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
    # Basic guardrail: don’t send secrets/logs/etc.
    health = payload.health
    status = payload.status

    prompt = f"""You are an SRE assistant. Explain this service health in plain English.
Be concise (6-10 bullets), include: overall status, uptime, hostname, version, and any red flags.
If everything looks normal, say so.

health.json: {health}
status.json: {status}
"""

    resp = client.responses.create(
        model=os.getenv("AI_MODEL", "gpt-4.1-mini"),
        input=prompt,
    )  # Responses API  [oai_citation:1‡OpenAI Platform](https://platform.openai.com/docs/api-reference/responses?utm_source=chatgpt.com)

    return {"reply": resp.output_text}

