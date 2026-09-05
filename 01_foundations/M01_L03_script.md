# SCRIPT: M01_L03
## Stop Wasting GPUs: Multi-Model Serving with Superlinked (SIE)

**Course:** LLMOps & Agentic Engineering  
**Module 1:** Foundations of MLOps & LLMOps  
**Episode:** 03  
**Target Duration:** ~14 Minutes  
**Target Audience:** Infrastructure Engineers, Platform Architects, Backend Developers  

---

### [00:00 - 00:35] THE HOOK

**VISUAL CUE:**
Presenter on camera looking at an AWS / GCP cloud billing dashboard. The monthly line item for GPU instances flashes in bright red: **$4,250.00 / Month**. On the left, four separate cloud instances are running, but their GPU utilization gauges are hovering at a pathetic **4% to 8%**.

**PRESENTER (Spoken to Camera):**
"Look at this cloud compute bill. Four thousand two hundred dollars a month. 

Why? Because an engineering team wanted to build an agentic search system. They spun up one GPU instance for their dense embedding model. Another GPU instance for their cross-encoder reranker. A third instance for an entity extractor. And a fourth instance for content moderation.

Four separate A10G instances burning money 24 hours a day, while their actual GPU compute utilization never exceeds eight percent!

This is the **GPU Resource Fragmentation Trap**.

Today, we are eliminating that waste. We are deploying the open-source **Superlinked Inference Engine (SIE)** to pack dozens of specialized AI models onto a **single shared GPU** using on-demand lazy loading and Least Recently Used memory eviction. Let's inspect the architecture."

---

### [00:35 - 04:15] SECTION 1: THE MULTI-MODEL FRAGMENTATION TRAP

**VISUAL CUE:**
Diagram showing the anti-pattern:
`Cloud Cluster: [Instance A: MiniLM Embeddings] + [Instance B: BGE Reranker] + [Instance C: GLiNER NER] + [Instance D: Granite Guardian] = 4 GPUs ($4,000/mo)`.
Contrast with:
`SIE Unified Architecture: Single GPU (24GB VRAM) hosting all 4 models via dynamic LRU eviction = 1 GPU ($950/mo)`.

**PRESENTER (Spoken):**
"In any modern agentic application, your primary large language model is only the tip of the iceberg. Behind the scenes, you need an entire symphony of small, specialized models:
1. An embedding model like `all-MiniLM-L6-v2` or `BGE-M3` to generate search vectors.
2. A cross-encoder model like `ms-marco-MiniLM` to rerank search results with extreme precision.
3. A zero-shot Named Entity Recognition model like `GLiNER` to pull variables and dates out of raw text.
4. A safety guardrail model like `Granite Guardian 2B` to block toxic outputs.

None of these models need a massive cluster on their own. Most of them have fewer than four billion parameters and consume less than two gigabytes of VRAM.

If you deploy each one as an isolated microservice, you pay a massive operational tax in hardware costs, networking latency, and cold-start synchronization.

If you try to run them all on the same GPU using standard Python scripts, PyTorch crashes with an out-of-memory error because both frameworks compete for static VRAM allocation.

We need an operating-system-level memory manager for GPU workloads."

---

### [04:15 - 08:30] SECTION 2: THE SUPERLINKED INFERENCE ENGINE (SIE) ARCHITECTURE

**VISUAL CUE:**
3D graphic of the SIE Architecture. Incoming HTTP requests hit a unified REST gateway exposing three uniform primitives:
`1. /encode (Vectors)`  
`2. /score (Reranking)`  
`3. /extract (Entities)`  
Below, the SIE Memory Controller dynamically manages a shared VRAM pool using an LRU eviction queue.

**PRESENTER (Spoken):**
"Enter the **Superlinked Inference Engine (SIE)**—an Apache 2.0 open-source inference server designed specifically for shared-GPU multi-model packing.

SIE solves the fragmentation crisis through three architectural pillars:
First: **Uniform Functional Primitives**. 
Instead of learning custom API schemas for twenty different libraries, SIE standardizes model interaction into three universal verbs:
* `encode`: Converts text or images to vectors for semantic search.
* `score`: Computes relevance scores between query-document pairs for reranking.
* `extract`: Pulls structured entities and classifications from unstructured text.

Second: **On-Demand Lazy Loading**.
Models are not loaded into VRAM until an API request actually requires them. If your system hasn't performed entity extraction in an hour, GLiNER sleeps on host RAM.

Third: **Least Recently Used (LRU) Memory Eviction**.
When an incoming request requires a model that exceeds remaining VRAM, the SIE controller identifies the model with the oldest access timestamp, gracefully unloads its weights back to host RAM or disk cache, and loads the active model in milliseconds.

You get the flexibility of dozens of models with the hardware footprint of a single GPU."

---

### [08:30 - 12:00] SECTION 3: LIVE TERMINAL LAB WALKTHROUGH

**VISUAL CUE:**
Split-screen terminal recording running `08_VIDEO_PROJECTS/sie_pipeline.py`.
Presenter inspects the code in VS Code, executes the script, and tracks the telemetry logs.

**PRESENTER (Voiceover over Terminal Demo):**
"Let's look at the Python client code:
We import `SIEClient` and initialize it against our local endpoint: `http://localhost:8080`.

Notice how clean this pipeline is:
Step one: We call `client.encode()` with `all-MiniLM-L6-v2`. In twelve milliseconds, we receive a normalized 384-dimensional embedding vector.

Step two: We execute cross-encoder document reranking. We pass our query: 'What causes the 5-second TTFT latency in RAG?', along with three candidate chunks. We call `client.score()`. SIE scores the candidates, placing our prefill attention explanation at rank one with a 0.96 relevance score.

Step three: We run zero-shot entity extraction. We pass a raw press release about DFlash and SGLang, and specify our target labels: organization, technology, model, and framework. We call `client.extract()`. GLiNER returns structured entities with 98% confidence.

Three distinct models, three distinct tasks, all executed on a single GPU without a single memory conflict or OOM error."

---

### [12:00 - 14:00] SUMMARY & CHALLENGE

**PRESENTER (Spoken to Camera):**
"By deploying the Superlinked Inference Engine, we reduced our monthly hardware footprint from four instances down to one, slashing our infrastructure spend by over seventy-five percent.

In our repository under `08_VIDEO_PROJECTS/sie_pipeline.py`, you can download the exact script and docker configuration.

Your challenge for this episode:
Deploy `sie-server` locally using Docker or Metal on Apple Silicon, add a sentiment classification model to the pipeline, and measure the warm latency when switching between embedding and classification tasks.

In Episode 4, we solve another massive bottleneck: **Context Rot in 100K+ token prompts**, using MIT's Recursive Language Models. Subscribe, and I'll see you in the next lesson."
