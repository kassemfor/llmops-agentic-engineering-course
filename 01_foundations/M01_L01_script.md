# SCRIPT: M01_L01
## MLOps is Dead: The Trillion-Parameter Paradigm Shift

**Course:** LLMOps & Agentic Engineering  
**Module 1:** Foundations of MLOps & LLMOps  
**Episode:** 01 (Series Premiere)  
**Target Duration:** ~12 Minutes  
**Target Audience:** Senior Software Engineers, DevOps Engineers, Enterprise Architects  

---

### [00:00 - 00:35] THE HOOK

**VISUAL CUE:**
Presenter on camera looking direct, sharp, authoritative. In the lower-third, a glowing cyan tag fades in: **"EPISODE 01: THE PARADIGM SHIFT"**. Behind the presenter, a graphic shows a standard 2020 ML pipeline (scikit-learn / XGBoost tabular model) being consumed by an enormous, spinning 3D galaxy of parameters.

**PRESENTER (Spoken to Camera):**
"If you are still treating Large Language Models like standard machine learning models, your production systems are going to fail.

For ten years, MLOps gave us a playbook: train a churn model or fraud predictor with fifty million parameters on a single GPU, validate binary accuracy or F1 score, containerize it in Docker, and retrain the whole thing overnight when the data drifts.

That playbook is officially obsolete.

We are no longer managing models with millions of parameters. We are deploying foundational systems with **hundreds of billions to trillions of parameters**. You don't retrain a 70-billion parameter model overnight because fresh transaction logs arrived. 

The hardware, the data pipelines, the monitoring metrics, and the failure modes have fundamentally mutated. Welcome to **LLMOps and Agentic Engineering**."

---

### [00:35 - 03:30] SECTION 1: THE FOUR DIVERGENCES OF SCALE

**VISUAL CUE:**
A high-contrast side-by-side comparison table enters with smooth deceleration:

```text
+-----------------------+-----------------------------+-----------------------------+
| OPERATIONAL DIMENSION | TRADITIONAL MLOps           | MODERN LLMOps               |
+-----------------------+-----------------------------+-----------------------------+
| Parameter Scale       | 10M – 100M parameters       | 7B – 400B+ parameters       |
| Data Types            | Tabular rows, clean columns | Petabyte unstructured text  |
| Retraining Cadence    | Full model retraining       | PEFT (LoRA), RLHF, GRPO     |
| Evaluation Focus      | Accuracy, Precision, AUC    | Perplexity, Hallucinations  |
| Physical Compute      | Single machine / edge node  | Distributed GPU clusters    |
+-----------------------+-----------------------------+-----------------------------+
```

**PRESENTER (Spoken):**
"Let's look at the numbers. 

In traditional MLOps, a telecom churn prediction model managed ten to fifty million parameters. The model weights were two hundred megabytes. You could fit the entire model and the training batch onto an ordinary laptop GPU.

In LLMOps, our baseline open-weights models start at seven billion parameters and scale past four hundred billion. A single model checkpoint in half-precision requires hundreds of gigabytes of raw VRAM just to exist in memory—before you process a single token!

This leads directly to divergence number two: **Data Complexity**. 
Traditional pipelines handled clean relational tables with known schemas. LLMOps feeds on petabytes of unstructured text, markdown, scraped HTML, and code repositories.

Divergence number three: **Tuning Mechanics**. 
In MLOps, when data drifts, your automated CI/CD pipeline triggers a full retraining run. In LLMOps, pre-training a frontier model costs tens of millions of dollars in compute. You cannot simply 'retrain' Llama or Qwen. Instead, we use Parameter-Efficient Fine-Tuning—primarily LoRA and QLoRA—to freeze ninety-nine percent of the weights and train tiny low-rank adapter matrices.

And divergence number four: **Evaluation**. 
You cannot calculate an F1-score on an open-ended conversational agent. If a user asks 'What is MLOps?' and the model responds with two different grammatically valid paragraphs, traditional exact-match metrics score zero. We must monitor generative quality: perplexity, hallucination rates, semantic drift, and policy compliance."

---

### [03:30 - 06:45] SECTION 2: THE PHYSICAL MEMORY WALL & DISTRIBUTED COMPUTE

**VISUAL CUE:**
Architectural 3D animation showing a single NVIDIA H100 GPU (80GB VRAM). A red bar representing model weights exceeds the physical VRAM container and spills over into an out-of-memory error. The camera pulls back to show **Tensor Parallelism** and **Pipeline Parallelism** shattering the model across an 8-GPU cluster.

**PRESENTER (Spoken):**
"Why do traditional software engineers struggle when transitioning to LLMOps? Because they hit **the physical memory wall**.

Let's do the arithmetic:
A 70-billion parameter model stored in standard 16-bit floating point (FP16 or BF16) requires two bytes per parameter:
$$70 \times 10^9 \times 2 \text{ bytes} = 140 \text{ Gigabytes}$$

The largest standard enterprise GPU on the market—an NVIDIA A100 or H100—has eighty gigabytes of VRAM. 

You physically cannot load the model onto a single GPU!

To survive, an LLMOps engineer must master distributed infrastructure:
1. **Model Parallelism (Tensor Parallelism):** Splitting the internal linear weight matrices across multiple GPUs using libraries like Megatron-LM.
2. **Pipeline Parallelism:** Splitting the transformer layers sequentially across separate cards.
3. **Weight Quantization:** Compressing weights down to 8-bit or 4-bit integers (AWQ, GPTQ) to run massive models on cost-effective hardware without losing intelligence.
4. **Data Parallelism with ZeRO (DeepSpeed):** Partitioning optimizer states and gradients across clusters to eliminate redundant memory allocation."

---

### [06:45 - 09:30] SECTION 3: THE NINE-STAGE LLMOps LIFECYCLE

**VISUAL CUE:**
Animated circular workflow showing the 9 stages of the modern LLMOps loop:
`1. Data Sourcing` -> `2. Model Selection` -> `3. Exploratory Data Analysis` -> `4. Review & Alignment` -> `5. Scope & Plan` -> `6. Package & Containerize` -> `7. Release & Serve` -> `8. Predict & Infer` -> `9. Continuous Monitoring`.

**PRESENTER (Spoken):**
"To operationalize this scale, we refine the traditional DevOps infinity loop into the **Nine-Stage LLMOps Lifecycle**.

Notice three critical additions that didn't exist in traditional software:
First, **The Review & Alignment Stage**. Before you write code or train adapters, you must evaluate the base model's zero-shot baseline against domain compliance.
Second, **The Packaging Phase**. We don't just package a Python wheel. We containerize optimized serving engines like vLLM, SGLang, or TensorRT-LLM, configuring memory allocation fractions and KV cache budgets.
And third, **The Continuous Monitoring Stage**. In traditional software, monitoring means tracking HTTP 500 errors and CPU spikes. In LLMOps, you monitor real-time semantic drift, prompt injection attempts, tool-calling failures, and token spend."

---

### [09:30 - 12:00] SUMMARY & LAB 1.0 CHALLENGE

**VISUAL CUE:**
Presenter returns on camera with terminal screen overlay showing Netflix and Uber Michelangelo architecture diagrams.

**PRESENTER (Spoken to Camera):**
"Here is your first homework assignment for the masterclass:
In our GitHub workbook, we have documented the production architectures of two legendary MLOps systems: Netflix's recommendation engine and Uber's Michelangelo platform.

Your task is **Lab 1.0: The Breakpoint Audit**. 
Walk through each architecture and identify the exact points where their data lakes, retraining jobs, and monitoring suites shatter when you swap out their tabular models for a 70B parameter agent.

Submit your audit in the `#lab-submissions` channel on our Discord to earn your Module 1 Architect badge.

In the next episode, we tackle the single biggest complaint in generative AI: **why RAG systems freeze for five seconds before streaming a word**. We are deriving the prefill attention wall and introducing speculative decoding. 

Subscribe, check the repo links below, and I'll see you in Episode Two."
