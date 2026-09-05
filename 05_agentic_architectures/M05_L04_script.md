# Episode M05_L04: The 100% Offline AI Second Brain: Rowboat & Ollama Knowledge Graphs

**Series:** LLMOps & Agentic Engineering: From Foundation to Production-Scale Systems  
**Module:** 05 — Agentic Architectures & Semantic Backends  
**Target Duration:** 13:30  
**Format:** YouTube Masterclass Deep-Dive (Offline Workstations, Markdown Graph Traversal, Local Inference)  
**Tone:** Privacy-focused, cybernetic, empowering engineers working with strict air-gapped security.

---

## Technical Overview & Pedagogical Objectives
- **The Core Problem:** The Air-Gapped Enterprise Privacy Dilemma. Defense contractors, healthcare institutions, and proprietary hedge funds sit on petabytes of high-value internal documentation, architectural blueprints, and source code. They are legally or contractually forbidden from sending a single byte of this data to third-party cloud LLM APIs (OpenAI, Anthropic). Naive local vector databases (Chroma/FAISS with arbitrary 500-token chunking) fail completely on complex relational queries ("Which microservices depend on the Auth v1 schema?").
- **The Architectural Solution:** Local-First Plain-Markdown Knowledge Graphs with Rowboat and Ollama. Storing institutional knowledge as human-readable, Git-versioned Markdown files, building a local semantic entity-relationship graph, and querying it entirely on local GPU/CPU hardware.
- **The Working Demonstration:** Disabling Wi-Fi on an Apple Silicon / Linux workstation, ingesting an internal software engineering wiki into Rowboat, and executing complex architectural queries using a local quantized reasoning model via Ollama.

---

## Script & Production Timeline

### 00:00 - 00:45 | ACT I: The Air-Gapped Reality (The Hook)
**[VISUAL]** High-contrast dark room (`#0B0F17`). 
Screen displays a laptop network panel:
- Wi-Fi: **DISCONNECTED**.
- Ethernet: **DISCONNECTED**.
- Bluetooth: **DISABLED**.
- The engineer pastes an internal architectural blueprint containing proprietary cryptographic keys and proprietary schemas.
- A terminal prompt queries: *"Trace all downstream dependencies of our proprietary settlement engine."*
- Instantly, an offline local agent streams a comprehensive response, citing exact markdown files and graph nodes.
- High-contrast text: **"ZERO BYTES TO THE CLOUD: THE 100% OFFLINE AGENTIC BRAIN."**

**[AUDIO]** Muffled, pressurized silence, then the hum of a local laptop fan accelerating. Voice enters calm, conspiratorial, authoritative.

**[NARRATOR (VO)]**
> "If you work at a defense contractor, a top-tier hedge fund, or a healthcare enterprise, you already know the painful truth about modern AI:
> 
> You cannot use ChatGPT.
> You cannot use Claude API.
> You cannot send your company's proprietary IP, patient data, or trade secrets over the public internet to someone else's server.
> 
> But your engineers are drowning in ten thousand internal documentation pages, Notion wikis, and legacy codebase files.
> 
> When teams try to solve this with naive local RAG, it fails miserably. They chop documents into arbitrary 500-token chunks, stuff them into a local vector store, and ask a question.
> The vector search finds three disconnected paragraphs, misses the overall architecture, and hallucinates.
> 
> What if you could build a second brain that understands the entire relational topology of your enterprise knowledge—
> Stored entirely in plain Markdown files,
> Traversed as a local knowledge graph,
> And powered 100% offline by open-source models?
> 
> In this video, we build an offline AI second brain using **Rowboat** and **Ollama**. You will learn how plain text beats proprietary databases, how to navigate knowledge graphs with local LLMs, and how to operate in strict air-gapped environments."

---

### 00:45 - 04:15 | ACT II: Why Plain Markdown Beats Proprietary Vector Stores
**[VISUAL]** High-contrast comparison:
- **Approach A: Proprietary Black-Box Vector Databases**
  - Data locked in binary vector indices (`.bin`, proprietary cloud formats).
  - Unreadable by humans.
  - Hard to version control in Git.
  - Chunk boundaries slice sentences and code functions in half.
- **Approach B: Rowboat Plain-Markdown Knowledge Graph**
  - Source files are standard `.md` files in a Git repo.
  - Frontmatter metadata (`tags`, `dependencies`, `owner`).
  - Bi-directional wikilinks: `[[AuthService]] -> [[PostgresCluster]]`.
  - Human readable, 100% editable in Obsidian or VS Code, zero vendor lock-in.

**[NARRATOR (VO)]**
> "Let's discuss data durability.
> 
> If you store your enterprise knowledge in a proprietary vector database format, what happens five years from now when that startup goes out of business or changes its API?
> Your knowledge is trapped.
> 
> Plain text Markdown has survived for twenty years. It will survive for the next fifty.
> 
> Rowboat's architecture is built on a radical principle: **Your Markdown files are the single source of truth**.
> 
> You don't export your docs into a database. You keep your docs in a standard Git repository—written in standard Markdown, linked with Obsidian-style wikilinks.
> 
> Rowboat parses those Markdown files, extracts entities and relationships, and builds a lightweight graph index on top of your local files.
> 
> When an agent needs context, it doesn't just pull random chunks based on cosine similarity. It traverses the graph:
> It finds the target document, inspects its parent modules, and walks the dependency links to assemble a coherent, structured sub-graph of context before generating an answer."

---

### 04:15 - 08:30 | ACT III: The Rowboat + Ollama Offline Architecture
**[VISUAL]** High-contrast architecture schematic: The Offline Air-Gapped Stack:
1. **Physical Layer:** Local Workstation (MacBook Pro M-Series / Linux RTX 4090 / A100).
2. **Model Serving Layer:** Ollama serving quantized open-source models locally:
   - Reasoning Model: `deepseek-r1:14b` or `qwen2.5-coder:14b` (Q4_K_M).
   - Embedding Model: `nomic-embed-text` or `bge-m3` (local CPU/GPU).
3. **Knowledge Engine:** Rowboat CLI:
   - Markdown Watcher: Tracks changes in `.md` files in real-time.
   - Graph Store: SQLite / DuckDB local edge graph.
   - Context Packer: Selects subgraphs and formats them as a prompt prefix.

**[NARRATOR (VO)]**
> "Look at the offline stack on screen.
> 
> At the base: your local machine. With Apple Silicon unified memory or a single workstation GPU, you can run a 14-billion or 32-billion parameter model at 40 tokens per second using Ollama.
> 
> In our setup, we use **Ollama** serving `qwen2.5-coder:14b` or `deepseek-r1:14b` for reasoning, and `nomic-embed-text` for local vector embeddings.
> 
> Above that sits **Rowboat**.
> 
> When you point Rowboat at your local documentation directory:
> 1. It reads the files.
> 2. It parses markdown headings and frontmatter.
> 3. It identifies cross-references: `[[DatabaseSchema]]`, `[[BillingService]]`.
> 4. It constructs an in-memory directed graph of your company's architecture.
> 
> When you ask: 'If we upgrade the Billing Service database, what APIs break?', Rowboat doesn't search for the words 'upgrade' and 'break'.
> 
> It looks up the `BillingService` node in the graph, queries its outbound edges to identify dependent services, loads the exact markdown specs for those specific services, and passes them to your local Ollama instance."

---

### 08:30 - 11:45 | ACT IV: Live Air-Gapped Demonstration
**[VISUAL]** Screencast: Terminal showing network interfaces being disabled (`sudo ifconfig en0 down`).
Terminal executes:
```bash
# Verify no internet connectivity
$ ping -c 1 8.8.8.8
ping: sendto: No route to host

# Launch Rowboat with local Ollama backend
$ rowboat index ./internal-engineering-wiki --backend ollama --model deepseek-r1:14b
[ROWBOAT] Parsed 482 markdown files.
[ROWBOAT] Extracted 1,240 entities, 3,890 relationships.
[ROWBOAT] Graph initialized in 3.4 seconds.

$ rowboat query "What security precautions must be taken when modifying the payment queue?"
```
The terminal streams a fast, step-by-step reasoning trace from `deepseek-r1:14b`, quoting exact internal guidelines and file paths: `docs/architecture/payment_queue.md#L45`.

**[NARRATOR (VO)]**
> "Look at the terminal.
> 
> We ping Google DNS: 'No route to host.' The network is dead.
> 
> We point Rowboat at 480 internal architecture markdown files. In three seconds, it extracts over three thousand relationships.
> 
> We ask our query.
> 
> Look at the local reasoning trace streaming in real-time from our local DeepSeek model:
> It doesn't guess. It quotes line 45 of `payment_queue.md`. It highlights the exact dead-letter-queue configuration required by internal company policy.
> 
> All of this happened on a local laptop sitting on a plane at 35,000 feet.
> 
> Zero cloud API fees. Zero risk of data breach. Zero reliance on third-party uptime."

---

### 11:45 - 13:30 | ACT V: Module 5 Synthesis & Module 6 Teaser
**[VISUAL]** Full-screen summary graphic of Module 5:
- Durable State Graphs (ADK 2.0) -> Agent-Native Backend (InsForge) -> Enterprise Standards (`CLAUDE.md`) -> Offline Knowledge Graphs (Rowboat).
- Next preview: **Module 6 — Secure Workflows, Monitoring & Governance**.
- Teaser visual: SonarQube CLI blocking `.env` credential leaks and Plano AI Edge Proxy routing traffic.

**[NARRATOR (VO)]**
> "This concludes Module 5: Agentic Architectures and Semantic Backends.
> 
> We have elevated our agentic systems from fragile in-memory while-loops to durable, stateful graphs; connected them to real cloud backends with InsForge; hardened their development rules with `CLAUDE.md`; and established complete local data sovereignty with Rowboat.
> 
> But as your autonomous agents gain more power—as they read files, query databases, and execute code—a terrifying new threat emerges:
> 
> **How do you stop an agent from secretly exfiltrating your API keys and credentials?**
> 
> In Module 6, we enter the final frontier of production LLMOps: **Security, Monitoring, and Governance**.
> 
> In Episode 1, we expose: **The Silent AI Leak: Stopping Agents from Exfiltrating Secrets with SonarQube CLI**.
> 
> Check out the Rowboat setup instructions in the description, subscribe, and I'll see you in Module 6."
