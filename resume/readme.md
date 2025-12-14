# AI Health Summary – FastAPI on AWS

A production-style cloud application that exposes system health metrics and uses AI to translate them into a clear, human-readable summary.

> **Goal:** demonstrate real-world cloud engineering *and* practical AI integration — not just calling an API.

---

## Overview

This project runs a Dockerized **FastAPI** backend on **AWS EC2**, fronted by **Nginx with TLS**, and integrates an AI model to explain service health in plain English.

Raw JSON health data is useful for machines; AI makes it understandable for humans.

---

## Architecture

- **Frontend**: Static HTML (resume site + AI Health page) served by Nginx
- **Backend**: FastAPI app running in Docker
- **AI**: OpenAI API (`gpt-5-nano` by default)
- **Infra**: AWS EC2, Docker, Nginx, Let’s Encrypt TLS
- **CI/CD**: GitHub Actions → SSH deploy to EC2

---

## Key Endpoints

### Health & Status

- `GET /api/health` – runtime health (uptime, hostname)
- `GET /api/status` – service metadata

### AI Integration

- `POST /api/ai/health-explain` – accepts health + status JSON and returns an AI summary
- `GET /api/ai/health-explain` – browser-friendly shortcut that generates the summary automatically

---

## AI Health Page

- **URL:** `/ai-health.html`
- Button-driven UI that:
  - Fetches live health + status
  - Sends data to the AI endpoint
  - Displays a concise operational summary
- Optional toggle to view raw JSON

The OpenAI API key is kept **server-side only**.

---

## Model Choice

Default model: **gpt-5-nano**

Why:

- Structured JSON input
- Deterministic summarization
- Low latency and cost

Model selection is configurable via environment variables:

```bash
AI_MODEL=gpt-5-nano
```

This demonstrates **right-sizing AI models** for the task.

---

## Security

- API keys stored in environment variables
- Secrets injected into Docker at runtime
- No credentials exposed to the browser
- TLS enabled via Let’s Encrypt

---

## Deployment Flow

1. Push to `main`
2. GitHub Actions triggers
3. Workflow SSHs into EC2
4. Server deploy script:
   - `git pull`
   - `docker build`
   - restart container
   - reload Nginx

This provides automated, repeatable deployments.

---

## Why This Project Matters

This project demonstrates:

- Cloud networking and TLS
- Dockerized backend services
- CI/CD pipelines
- Secure secret handling
- Practical, user-facing AI integration

It is designed as a **production-minded portfolio project**, not a tutorial demo.

---

## Future Improvements

- Cache AI summaries
- Rate-limit AI endpoints
- Add authentication
- Add observability (logs/metrics)
- Docker health checks

---

## Author

Built and deployed by **KJ** as part of a long-term cloud and infrastructure learning path.

