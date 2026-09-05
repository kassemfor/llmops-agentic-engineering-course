# Episode M06_L02: Out-of-Process AI Gateways: Multi-Agent Routing with Plano Proxy

**Series:** LLMOps & Agentic Engineering: From Foundation to Production-Scale Systems  
**Module:** 06 — Secure Workflows, Monitoring & Governance  
**Target Duration:** 14:30  
**Format:** YouTube Masterclass Systems Architecture (Envoy Topology, Dynamic Routing, Grafana Dashboards)  
**Tone:** High-scale infrastructure architect perspective. Decoupling application logic from AI networking.

---

## Technical Overview & Pedagogical Objectives
- **The Core Problem:** The "In-Process Gateway" Anti-Pattern. When enterprise teams scale multi-agent systems, developers embed API keys, model retry loops, rate-limit handlers, fallback cascades (`if openai_fails: try_anthropic()`), and Prometheus metrics instrumentation directly inside application Python code. When an API key rotates, a provider experiences an outage, or cost governance rules change, dozens of production microservice containers must be recompiled and redeployed.
- **The First-Principles Solution:** Out-of-Process AI Reverse Proxies with Plano (Envoy-based AI Gateway). Moving traffic management, authentication, provider failover, load balancing, and OpenTelemetry observability out of the application code and into an ultra-high-performance C++ proxy layer.
- **The Working Demonstration:** Deploying Plano Proxy in Docker Compose. Routing multi-agent queries between a local fast 4B/8B model (for simple classification) and an external reasoning frontier model (for complex tasks), observing automatic circuit breaking on simulated provider outages, and inspecting distributed trace spans in Grafana.

---

## Script & Production Timeline

### 00:00 - 00:45 | ACT I: The Spaghetti Gateway Collapse (The Hook)
**[VISUAL]** High-contrast dark room (`#0B0F17`). 
Screen displays a catastrophic production incident:
- Incident: OpenAI API experiences a 15-minute global outage (HTTP 503).
- Grafana dashboard shows 24 microservices crashing simultaneously.
- Code review displays a horrifying 800-line Python file full of nested `try-except` blocks, hardcoded API keys, and custom token counters.
- An engineer's Slack message: *"We need to redeploy all 24 services to switch to Anthropic, but the Docker builds will take 45 minutes."*
- High-contrast text: **"STOP HARDCODING LLM CALLS IN YOUR APPLICATION CODE."**

**[AUDIO]** Heavy digital alarms, followed by the sound of a server fan dropping to zero RPM. Voice enters authoritative, architectural.

**[NARRATOR (VO)]**
> "If you have Python code in your production microservices that directly imports `openai` or `anthropic`, instantiates client objects, and hardcodes fallback logic—you are committing the exact same architectural sin that web engineers solved fifteen years ago.
> 
> Imagine if every single endpoint in your backend had to manually implement TLS termination, TCP keep-alives, rate limiting, and DDoS protection.
> 
> You wouldn't do that. You put NGINX or Envoy in front of your servers.
> 
> Yet right now, enterprise AI teams are embedding API keys, retry loops, rate-limit backoffs, and fallback cascades directly inside their agent code.
> 
> When your primary model provider goes down, your entire company goes dark.
> When an API key rotates, you have to rebuild twenty Docker containers.
> When your CFO asks: 'Which agent spent ten thousand dollars yesterday?', nobody knows.
> 
> In this video, we deploy **Plano Proxy**—the Envoy-powered, out-of-process AI gateway. You will learn how to decouple your agent code from LLM providers, implement sub-millisecond dynamic model routing, and get complete OpenTelemetry observability with zero code changes."

---

### 00:45 - 04:15 | ACT II: The Out-of-Process Architecture (The Envoy AI Proxy)
**[VISUAL]** Architectural schematic: In-Process vs. Out-of-Process AI Gateways.
- **Top (In-Process Anti-Pattern):**
  - Application Agent $\to$ [Python SDK] $\to$ [Hardcoded Retry / Failover] $\to$ [Direct Internet to OpenAI/Anthropic].
- **Bottom (Out-of-Process Plano Architecture):**
  - Application Agent $\to$ Calls local endpoint: `http://plano:8080/v1/chat/completions`.
  - Application code uses standard universal OpenAI API schema, has ZERO knowledge of providers, keys, or retries.
  - **Plano Proxy Layer (Envoy Core):**
    - Secret Injection: Injects provider API keys from vault at the edge.
    - Smart Router: Classifies prompt complexity; routes simple queries to local small models, complex queries to frontier models.
    - Circuit Breaker: Automatically diverts traffic to secondary provider within 5ms of an outage.
    - Zero-Code OpenTelemetry: Emits standard spans (TTFT, input tokens, output tokens, cost) to Prometheus & Jaeger.

**[NARRATOR (VO)]**
> "Look at the architectural transformation on screen.
> 
> Your agent code no longer imports specific vendor SDKs. It connects to a single, standardized endpoint: `http://plano:8080/v1`.
> 
> Your application doesn't know—and doesn't care—whether the underlying model is running on AWS Bedrock, Google Vertex AI, Anthropic, or an open-source vLLM node in your own basement.
> 
> All networking logic is handled by Plano, running on Envoy’s battle-tested C++ networking core.
> 
> When a request enters Plano:
> One: **Zero-Trust Secret Injection**. Your application code never holds third-party API keys. Plano securely injects credentials from HashiCorp Vault or AWS Secrets Manager.
> 
> Two: **Dynamic Semantic Routing**. If an agent sends a 50-token query asking to classify a user intent, Plano routes it to a local 4B model hosted on your shared GPU engine. If the prompt requires deep reasoning, Plano routes it to DeepSeek-R1 or Claude 3.5 Sonnet.
> 
> Three: **Instant Circuit Breaking**. If provider A throws an HTTP 500 or hits a rate limit, Plano diverts the stream to provider B in five milliseconds before your application even notices."

---

### 04:15 - 08:45 | ACT III: The Plano Configuration Matrix
**[VISUAL]** VS Code screen displaying Plano's declarative YAML configuration file (`plano_routing_manifest.yaml`):

**[SCREEN CODE]**:
```yaml
# Plano AI Edge Proxy Configuration
listeners:
  - address: 0.0.0.0:8080
    protocol: HTTP/2

routes:
  - match:
      prefix: "/v1/chat/completions"
    rules:
      - condition: "header['x-agent-tier'] == 'fast'"
        destination: "cluster_local_sie_4b"
      - condition: "header['x-agent-tier'] == 'deep_reasoning'"
        destination: "cluster_deepseek_r1"
      - default:
          primary: "cluster_anthropic_claude"
          fallback: "cluster_openai_gpt4o"
          circuit_breaker:
            consecutive_5xx_errors: 3
            ejection_timestamp: 30s

observability:
  opentelemetry:
    endpoint: "otel-collector:4317"
    metrics:
      - token_usage
      - time_to_first_token
      - financial_cost_usd
```

**[NARRATOR (VO)]**
> "Look at the clarity of this declarative manifest.
> 
> Look at lines 10 through 17:
> We define a routing rule based on agent intent:
> If an agent tags its request as `fast`, Plano directs it to our local Superlinked Inference Engine cluster hosting a 4-billion parameter model.
> Zero external cloud fees.
> 
> Look at line 15:
> If our primary frontier model fails three consecutive times with a 5xx status, the circuit breaker trips. Plano instantly ejects the failing provider for thirty seconds and reroutes 100% of traffic to our fallback cluster.
> 
> And look at the observability block:
> With zero lines of Python instrumentation, Plano captures:
> - Token counts.
> - Time to First Token (TTFT).
> - End-to-end latency.
> - Exact dollar cost calculated down to the micro-cent.
> 
> It streams those metrics directly into your company's existing OpenTelemetry, Datadog, or Grafana infrastructure."

---

### 08:45 - 12:15 | ACT IV: Live Simulation: Outage & Instant Failover
**[VISUAL]** Split-screen screencast:
- Top: An agent script generating requests in an infinite loop.
- Bottom Left: Terminal simulating a provider failure (blocking outbound connections to provider A).
- Bottom Right: Grafana live latency and provider distribution dashboard.

**[NARRATOR (VO)]**
> "Watch what happens in our live test.
> 
> On the top screen, our multi-agent workflow is firing twenty requests per second through Plano Proxy.
> 
> Now, on the bottom left, we simulate an outage: we sever the connection to Provider A.
> 
> Look at the Grafana dashboard:
> Request 1 fails. Request 2 fails. Request 3 fails.
> 
> In **four milliseconds**, Plano’s circuit breaker trips.
> 
> Look at the green line on the dashboard:
> 100% of outbound requests seamlessly shift to Provider B.
> 
> Look at the agent application log:
> Not a single exception was thrown.
> Not a single user request dropped.
> Zero pod restarts. Zero panic.
> 
> That is the power of decoupling your AI systems from external vendors."

---

### 12:15 - 14:30 | ACT V: Summary & Next Episode Teaser
**[VISUAL]** Summary graphic:
- In-Process Spaghetti vs. Out-of-Process Plano AI Gateway.
- Next preview: **Episode M06_L03 — Zero-Maintenance Release Notes: CI/CD Automation with Doc Holiday**.

**[NARRATOR (VO)]**
> "Let's review the architectural rules of AI gateways:
> 
> One: Never embed vendor SDKs, API keys, or fallback loops in your core business logic. Route all AI traffic through an out-of-process reverse proxy.
> 
> Two: Use dynamic semantic routing to offload lightweight agent queries to fast local models, reserving frontier reasoning models for complex tasks.
> 
> Three: Implement circuit breaking and zero-code OpenTelemetry at the proxy tier for bulletproof enterprise reliability.
> 
> Now, once your agents are running, code is being written, models are being served, and features are being shipped at lightning speed:
> **How do you keep your human developers and stakeholders informed without drowning in documentation debt?**
> 
> In Episode 3, we explore **Doc Holiday**: how to automate release notes, changelogs, and architecture docs directly inside your GitHub Actions CI/CD pipeline using specialized agentic hooks.
> 
> Download the Plano Docker Compose setup in the description, subscribe, and I'll see you in Episode 3."
