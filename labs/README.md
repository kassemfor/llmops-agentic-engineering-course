# LLMOps Hands-On Labs

Runnable demo projects accompanying the **LLMOps & Agentic Engineering** course and the
**LLMOps & Agentic Engineering: Infrastructure & Delivery** module set on
[Enterprise AI Recovery](https://www.youtube.com/@EnterpriseAIRecovery).

Every lab here is small enough to read in one sitting and real enough to run. They are
the practical half of the course: the videos explain why, these prove it.

---

## Labs

| # | Project | What it demonstrates |
|---|---|---|
| 1 | `demo-1-setting-up-a-local-mlops-workspace-with-mlflow` | Tracking server, experiment runs, artifact logging |
| 2 | `demo-2-tracking-ml-experiments-with-mlflow` | Parameter sweeps and comparing runs |
| 3 | `demo-3-comparing-experiments-and-selecting-the-b` | Choosing a model on evidence, not vibes |
| 4 | `building-a-reproducible-llm-development-environm` | Pinned images, pinned dependencies, why `latest` is a bug |
| 5 | `running-an-open-source-llm-locally-with-ollama` | Local inference, the `/api/generate` contract, when local is wrong |
| 6 | `building-an-llm-application-with-hugging-face-tr` | Tokenizer internals, `pipeline()`, what the abstraction hides |
| 7 | `creating-a-multi-service-llmops-stack-with-docke` | Compose orchestration, healthchecks, the scaling ceiling |
| 8 | `text-data-pipeline` | Versioning a text pipeline, reproducible datasets |
| 9 | `creating-and-validating-synthetic-training-data-` | Generating and validating synthetic training data |
| 10 | `lora-fine-tuning` | Parameter-efficient fine-tuning on a small model |
| 11 | `ci-prompt-evaluation-demo` | Prompt regression testing as a CI gate |
| 12 | `cd-canary-deployment` | Stable/canary releases and rollback as code |
| 13 | `autoscaling-gemini-llm-workloads-with-keda-and-k` | Scaling on queue depth, not CPU |
| 14 | `llm-monitoring` | Performance and quality monitoring |
| 15 | `llm-governance` | Audit logging and access control |
| 16 | `responsible-ai-evaluation` | Evaluating outputs for responsible-AI risk |

---

## Running a lab

Most labs need Python 3.10+ and a virtual environment:

```bash
cd <project>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # then fill in your own keys
python <entrypoint>.py
```

Some need Docker or a Kubernetes cluster:

```bash
# Docker-based labs
docker compose up

# Kubernetes-based labs
kubectl apply -f k8s/
```

If a lab needs a model download or a GPU, the README in that project says so.

---

## Secrets

**Never commit a real API key.** Each project ships a `.env.example`. Copy it to `.env`,
fill in your own keys, and leave `.env` uncommitted — a `.gitignore` is already in place.

The Kubernetes labs expect a Secret named `gemini-api-secret`:

```bash
kubectl create secret generic gemini-api-secret \
  --from-literal=GEMINI_API_KEY="$GEMINI_API_KEY"
```

---

## License

Educational material provided as-is. Run it, break it, adapt it for your own environment.