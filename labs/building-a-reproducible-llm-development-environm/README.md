# Reproducible LLM Development Environment with Docker

This project demonstrates how Docker can package a Python-based
LLM application into a reproducible runtime environment.

## Project Files

- `app.py` - Python LLM application
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container definition
- `.dockerignore` - Files excluded from the Docker build
- `.env` - Local environment variables

## Run Locally

Create and activate a virtual environment.

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate