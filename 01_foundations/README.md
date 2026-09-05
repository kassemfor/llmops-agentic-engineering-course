# Module 1: Foundations of MLOps & LLMOps

## Overview
Module 1 establishes the mathematical and physical divergences between classical 2020 MLOps (50M parameter tabular models) and modern LLMOps (70B–400B+ parameter distributed systems).

## Classes in this Module
* **[M01_L01: MLOps is Dead: The Trillion-Parameter Paradigm Shift](./M01_L01_script.md)**
  * The 4 Operational Divergences (Parameter Scale, Data Complexity, Tuning Mechanics, Generative Evaluation).
* **[M01_L02: The RAG Latency Lie: Why Your AI is Slow (Prefill vs. Decode & Speculative Decoding)](./M01_L02_script.md)**
  * Deriving the (T^2)$ quadratic prefill attention wall.
  * DFlash 16-token parallel diffusion drafting.
* **[M01_L03: Stop Wasting GPUs: Multi-Model Serving with Superlinked (SIE)](./M01_L03_script.md)**
  * Shared GPU multi-model packing and LRU eviction.
* **[M01_L04: Defeating Context Rot: MIT's Recursive Language Models (RLMs)](./M01_L04_script.md)**
  * 10M token context decomposition without attention degradation.

## Runnable Projects
* [](../projects/sie_pipeline.py) — Superlinked LRU serving engine.
* [](../projects/rlm_simulator.py) — MIT recursive language model simulator.
