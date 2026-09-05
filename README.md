# LLMOps & Agentic Engineering: From Foundation to Production-Scale Systems

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 2.2+](https://img.shields.io/badge/PyTorch-2.2+-ee4c2c.svg)](https://pytorch.org/)
[![Docker Compose](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://docs.docker.com/compose/)
[![Substack](https://img.shields.io/badge/Substack-Technical_Ledger-FF6719.svg)](https://engineeringledger.substack.com/)

> **The definitive 50-hour open-source systems engineering curriculum and 24-episode YouTube masterclass transforming raw AI source materials into production-scale distributed infrastructure.**

Created & Instructed by **Kris Kassem**  
Official YouTube Channel: [LLMOps & Agentic Engineering Masterclass](https://www.youtube.com/@AgenticEngineeringMasterclass)  
Substack Technical Ledger: [The LLMOps Ledger](https://engineeringledger.substack.com/)  
Community & Architecture Office Hours: [Discord Community](https://discord.gg/agentic-engineering)

---

## 🏛️ Course Architectural Blueprint

```
+---------------------------------------------------------------------------------------------------+
|                        4 PILLARS OF PRODUCTION AGENTIC SYSTEMS                                   |
+----------------------------------+----------------------------------------------------------------+
| 1. DATA INGESTION & CONTEXT      | 2. POST-TRAINING & REINFORCEMENT LEARNING                      |
| • Anti-Bot Web Scraping (MCP)    | • The Death of the Critic (DeepSeek-R1 GRPO)                   |
| • 40% Token Cut (Strip-Markdown) | • Deterministic Verifiable Rewards (Compilers & AST)          |
| • TimescaleDB + pgvectorscale    | • Multi-Turn Trajectory Rollouts (OpenPipe ART)                |
| • LakeFS & DVC Git-for-Data      | • PEFT & QLoRA Low-Rank Adaptation                             |
+----------------------------------+----------------------------------------------------------------+
| 3. HIGH-PERFORMANCE SERVING      | 4. MULTI-AGENT ORCHESTRATION & GOVERNANCE                      |
| • Prefill Latency & Attention    | • Google ADK 2.0 Durable State Graphs                          |
| • KV Cache Physics & MLA/GQA     | • In-Process PreToolUse Secret Shielding (SonarQube)           |
| • DFlash Block Diffusion (16 tok)| • Out-of-Process Envoy Gateways (Plano AI Edge Proxy)          |
| • Superlinked Engine (SIE LRU)   | • CI/CD Auto-Documentation (Doc Holiday)                       |
+----------------------------------+----------------------------------------------------------------+
```

---

## 📚 Complete 24-Class Curriculum Syllabus

### [Module 1: Foundations of MLOps & LLMOps](./01_foundations/)
| Class ID | Title | Key Architectural Focus | Code Project |
| :--- | :--- | :--- | :--- |
| **Trailer** | [The End of Brute Force AI](./07_capstone/TRAILER_script.md) | Why pretraining scaling laws hit physical walls | [Cluster Architecture](./diagrams/CAPSTONE_enterprise_cluster_architecture.png) |
| **M01_L01** | [MLOps is Dead](./01_foundations/M01_L01_script.md) | The Trillion-Parameter Paradigm Shift & 4 Divergences | [Memory Physics](./diagrams/M04_L01_kv_cache_memory_breakdown.png) |
| **M01_L02** | [The RAG Latency Lie](./01_foundations/M01_L02_script.md) | Prefill vs. Decode, $O(T^2)$ Attention & Speculative Decoding | [`projects/sie_pipeline.py`](./projects/sie_pipeline.py) |
| **M01_L03** | [Stop Wasting GPUs](./01_foundations/M01_L03_script.md) | Superlinked Inference Engine (SIE) Shared GPU LRU Packing | [`projects/sie_pipeline.py`](./projects/sie_pipeline.py) |
| **M01_L04** | [Defeating Context Rot](./01_foundations/M01_L04_script.md) | MIT Recursive Language Models (RLMs) for 10M Context | [`projects/rlm_simulator.py`](./projects/rlm_simulator.py) |

### [Module 2: The Modern LLMOps Data Pipeline](./02_data_pipelines/)
| Class ID | Title | Key Architectural Focus | Code Project |
| :--- | :--- | :--- | :--- |
| **M02_L01** | [Web Scraping for AI](./02_data_pipelines/M02_L01_script.md) | Model Context Protocol (MCP) Anti-Bot Ingestion | [`projects/strip_markdown_optimizer.py`](./projects/strip_markdown_optimizer.py) |
| **M02_L02** | [The 40% Token Cut](./02_data_pipelines/M02_L02_script.md) | Context Optimization & Markdown AST Sanitization | [`projects/strip_markdown_optimizer.py`](./projects/strip_markdown_optimizer.py) |
| **M02_L03** | [One Database to Rule All](./02_data_pipelines/M02_L03_script.md) | TimescaleDB Hypertables + pgvectorscale + BM25 | [`projects/docker-compose.enterprise-cluster.yml`](./projects/docker-compose.enterprise-cluster.yml) |
| **M02_L04** | [Data Versioning for LLMs](./02_data_pipelines/M02_L04_script.md) | LakeFS Zero-Copy Branching & DVC Rollback Audits | [`projects/lakefs_dvc_pipeline.py`](./projects/lakefs_dvc_pipeline.py) |

### [Module 3: Post-Training & Reinforcement Learning](./03_post_training_rl/)
| Class ID | Title | Key Architectural Focus | Code Project |
| :--- | :--- | :--- | :--- |
| **M03_L01** | [Why SFT Fails](./03_post_training_rl/M03_L01_script.md) | Exposure Bias, Teacher Forcing & Quadratic Compounding | [`projects/grpo_loss_engine.py`](./projects/grpo_loss_engine.py) |
| **M03_L02** | [The Death of the Critic](./03_post_training_rl/M03_L02_script.md) | DeepSeek-R1 GRPO: 4 Models -> 2 Models ($A_i$ Advantage) | [`projects/grpo_loss_engine.py`](./projects/grpo_loss_engine.py) |
| **M03_L03** | [You Can't Smooth Talk a Compiler](./03_post_training_rl/M03_L03_script.md) | Deterministic Verifiable Rewards vs Neural Reward Models | [`projects/verifiable_reward_evaluator.py`](./projects/verifiable_reward_evaluator.py) |
| **M03_L04** | [Multi-Turn Agent RL](./03_post_training_rl/M03_L04_script.md) | OpenPipe ART Trajectory Rollouts & W&B Tracking | [`projects/verifiable_reward_evaluator.py`](./projects/verifiable_reward_evaluator.py) |

### [Module 4: High-Performance Inference & Speculative Decoding](./04_inference_serving/)
| Class ID | Title | Key Architectural Focus | Code Project |
| :--- | :--- | :--- | :--- |
| **M04_L01** | [Mathematics of the KV Cache](./04_inference_serving/M04_L01_script.md) | VRAM Sizing Formula, GQA (87.5% cut) & DeepSeek MLA | [`projects/kv_cache_calculator.py`](./projects/kv_cache_calculator.py) |
| **M04_L02** | [Why Prefix Caching Fails](./04_inference_serving/M04_L02_script.md) | Dynamic Timestamps vs Strict Canonical Prompt Ordering | [`projects/kv_cache_calculator.py`](./projects/kv_cache_calculator.py) |
| **M04_L03** | [4.3x Faster Inference](./04_inference_serving/M04_L03_script.md) | DFlash Block Diffusion: 16 Draft Tokens in Parallel | [`diagrams/M01_L02_dflash_spec_decoding.png`](./diagrams/M01_L02_dflash_spec_decoding.png) |

### [Module 5: Agentic Architectures & Semantic Backends](./05_agentic_architectures/)
| Class ID | Title | Key Architectural Focus | Code Project |
| :--- | :--- | :--- | :--- |
| **M05_L01** | [Beyond Vibe Coding](./05_agentic_architectures/M05_L01_script.md) | Google ADK 2.0 Durable State Graphs & Suspend/Resume | [`projects/adk_durable_graph.py`](./projects/adk_durable_graph.py) |
| **M05_L02** | [The Agent-Native Backend](./05_agentic_architectures/M05_L02_script.md) | InsForge BaaS: Auth, Storage & DB over MCP | [`projects/docker-compose.enterprise-cluster.yml`](./projects/docker-compose.enterprise-cluster.yml) |
| **M05_L03** | [Enterprise AI Standards](./05_agentic_architectures/M05_L03_script.md) | Hardening Claude Code with Root CLAUDE.md Governance | [`projects/sonarqube_leak_shield.py`](./projects/sonarqube_leak_shield.py) |
| **M05_L04** | [The 100% Offline AI Second Brain](./05_agentic_architectures/M05_L04_script.md) | Plain-Markdown Knowledge Graphs with Rowboat & Ollama | [`projects/rlm_simulator.py`](./projects/rlm_simulator.py) |

### [Module 6: Security, Monitoring & Enterprise Governance](./06_security_governance/)
| Class ID | Title | Key Architectural Focus | Code Project |
| :--- | :--- | :--- | :--- |
| **M06_L01** | [The Silent AI Leak](./06_security_governance/M06_L01_script.md) | In-Process PreToolUse Secret Scanning (SonarQube) | [`projects/sonarqube_leak_shield.py`](./projects/sonarqube_leak_shield.py) |
| **M06_L02** | [Out-of-Process AI Gateways](./06_security_governance/M06_L02_script.md) | Plano AI Edge Proxy (Envoy 4B Router & OpenTelemetry) | [`projects/docker-compose.enterprise-cluster.yml`](./projects/docker-compose.enterprise-cluster.yml) |
| **M06_L03** | [Zero-Maintenance Release Notes](./06_security_governance/M06_L03_script.md) | Automated CI/CD Release Notes & Docs via Doc Holiday | [`projects/docker-compose.enterprise-cluster.yml`](./projects/docker-compose.enterprise-cluster.yml) |

### [Grand Capstone: The Autonomous Enterprise Swarm](./07_capstone/)
| Class ID | Title | Key Architectural Focus | Code Project |
| :--- | :--- | :--- | :--- |
| **CAPSTONE** | [The Autonomous Enterprise Swarm](./07_capstone/CAPSTONE_script.md) | Full-Stack Orchestrated Production Cluster | [`projects/docker-compose.enterprise-cluster.yml`](./projects/docker-compose.enterprise-cluster.yml) |

---

## 💻 Verified Code Projects (`projects/`)

Every project has been tested and verified to run with zero external proprietary dependencies:

1. **`projects/sie_pipeline.py`**: Multi-model serving simulation implementing Superlinked's Least-Recently-Used (LRU) GPU memory packing.
2. **`projects/rlm_simulator.py`**: MIT Recursive Language Model (RLM) simulator splitting 10M token inputs into recursive query graphs.
3. **`projects/strip_markdown_optimizer.py`**: High-speed AST token sanitizer reducing prompt tokens by 40%.
4. **`projects/lakefs_dvc_pipeline.py`**: Git-for-data pipeline demonstrating atomic data branching, commits, and instant rollback.
5. **`projects/grpo_loss_engine.py`**: DeepSeek-R1 Group Relative Policy Optimization (GRPO) implementation in pure PyTorch with Schulman KL divergence.
6. **`projects/verifiable_reward_evaluator.py`**: Deterministic compiler reward engine validating agent code outputs in isolated sandbox environments.
7. **`projects/kv_cache_calculator.py`**: Transformer inference memory calculator computing VRAM requirements across MHA, GQA, and DeepSeek MLA.
8. **`projects/adk_durable_graph.py`**: Google ADK 2.0 directed state graph demonstrating event-sourced checkpointing, state serialization, and `suspend()/resume()`.
9. **`projects/sonarqube_leak_shield.py`**: In-process PreToolUse interception shield preventing LLMs from reading `.env` files or API secrets.
10. **`projects/docker-compose.enterprise-cluster.yml`**: Production Docker Compose topology orchestrating TimescaleDB, Plano Proxy, SIE Serving, ADK Swarm, and Doc Holiday.

---

## 🚀 Quickstart: Running the Code

### 1. Clone the Repository
```bash
git clone https://github.com/kassemfor/llmops-agentic-engineering-course.git
cd llmops-agentic-engineering-course
```

### 2. Set Up Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Any Project Demo
```bash
# Test the DeepSeek GRPO loss engine
python3 projects/grpo_loss_engine.py

# Calculate KV Cache memory bounds for 70B models
python3 projects/kv_cache_calculator.py

# Simulate Google ADK 2.0 durable state graph with human-in-the-loop gate
python3 projects/adk_durable_graph.py

# Test the in-process SonarQube secret shield
python3 projects/sonarqube_leak_shield.py
```

---

## 📄 License & Attribution
This repository and curriculum are distributed under the [MIT License](LICENSE).  
Authored by **Kris Kassem** © 2026.
