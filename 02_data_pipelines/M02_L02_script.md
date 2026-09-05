# SCRIPT: M02_L02
## The 40% Token Cut: Context Optimization with Strip-Markdown

**Course:** LLMOps & Agentic Engineering  
**Module 2:** The Modern LLMOps Data Pipeline  
**Episode:** 06  
**Target Duration:** ~10 Minutes  
**Target Audience:** AI Engineers, Backend Developers, Context Engineers  

---

### [00:00 - 00:35] THE HOOK

**VISUAL CUE:**
Presenter on camera. Split-screen appears: on the left, a wall of raw scraped markdown with image tags, bold links, and markdown table pipes. Token count displays: **12,450 Tokens ($0.04)**. 
With a snap of the presenter's fingers, the right side displays the exact same semantic text, stripped of formatting. Token count drops to: **7,470 Tokens ($0.024)**. A glowing emerald badge flashes: **"40% TOKEN REDUCTION"**.

**PRESENTER (Spoken to Camera):**
"Did you know that forty percent of the tokens inside your RAG pipelines are completely useless to an LLM?

When you scrape an article or index a PDF, your parser outputs markdown: bold asterisks, header hashes, embedded image URLs, bracketed links, and markdown table borders.

To a human reader, that formatting is visually pleasing.
To a Large Language Model calculating multi-head attention, every single bracket, link, and asterisk is a token that burns compute and accelerates the quadratic prefill wall.

Today, we are looking at **Strip-Markdown Context Optimization**. We will write an Abstract Syntax Tree parser that strips formatting syntax while preserving 100% of the underlying semantic data—slashing your token bills by forty percent. Let's inspect the code."

---

### [00:35 - 03:30] SECTION 1: THE FORMATTING TAX IN TRANSFORMERS

**VISUAL CUE:**
Deconstruction of a single markdown link:
`[Read the official documentation here](https://docs.enterprise-ai.com/v2/api/reference/speculative-decoding?utm_source=blog&utm_medium=referral)`

Token breakdown animation:
* Link text (`Read the official documentation here`): 6 Tokens (Useful!)
* Formatting brackets & parentheses (`[` `]` `(` `)`): 4 Tokens (Noise!)
* Massive URL string (`https://docs.enterprise-ai.com/...`): 22 Tokens (Pure Waste!)
Total: 32 Tokens. Useful semantic content: 6 Tokens. **81% of the tokens were formatting overhead!**

**PRESENTER (Spoken):**
"Let's look at what your tokenizer actually sees when you ingest markdown.

Look at this standard hyperlink:
`[Read the official documentation here](https://docs.enterprise-ai.com/...)`

The LLM only needs to know that documentation exists. But because of the URL parameters, UTM tags, and markdown syntax, your tokenizer generates thirty-two discrete tokens. More than eighty percent of those tokens provide zero reasoning value to the model.

Now multiply that by ten retrieved articles in an enterprise RAG query. 
You are throwing thousands of tokens into the prefill attention matrix that do nothing except inflate your Time to First Token and drive up your cloud inference bills.

If we strip that syntax before prompt construction, we reduce our prompt payload from twelve thousand tokens down to seven thousand tokens."

---

### [03:30 - 07:00] SECTION 2: ABSTRACT SYNTAX TREE (AST) TRANSFORMATION

**VISUAL CUE:**
Diagram of the markdown AST (Abstract Syntax Tree) pipeline using `remark` / Python `markdown-it`:
`Raw Markdown Input` -> `AST Parser` -> `Node Filter (Remove Link URLs, Images, Styling)` -> `Clean Text Emitter`.

**PRESENTER (Spoken):**
"How do we strip markdown safely without mangling technical text like code blocks or math formulas?

You cannot use naive regex substitutions. If you write a regex to strip backticks, you will accidentally corrupt executable Python code!

Instead, we parse markdown into an **Abstract Syntax Tree (AST)** using libraries like `remark` or Python's `markdown-it`.

The AST represents the document as a structured hierarchy of nodes:
* `heading` nodes
* `paragraph` nodes
* `code_block` nodes
* `link` nodes
* `image` nodes

Our optimization script traverses the AST with three strict rules:
Rule 1: If a node is a `code_block` or `inline_code`, leave it completely untouched. Code syntax must remain exact.
Rule 2: If a node is a `link`, extract the human-readable text and discard the URL.
Rule 3: If a node is an `image`, discard the entire node unless the alt-text contains descriptive data.
Rule 4: Strip bold asterisks and italics, preserving the raw text strings."

---

### [07:00 - 09:15] SECTION 3: PYTHON DEMO & TOKEN BENCHMARK

**VISUAL CUE:**
Terminal screencast running `08_VIDEO_PROJECTS/strip_markdown_optimizer.py`.
The script processes a raw web-scraped article, displays before-and-after token counts using `tiktoken` (cl100k_base), and outputs the exact percentage savings.

**PRESENTER (Voiceover over Terminal):**
"Let's run our optimization script from `08_VIDEO_PROJECTS/strip_markdown_optimizer.py`:

We load a typical web-scraped markdown article from a tech blog: it contains code snippets, tables, image badges, and twenty links.

Before optimization:
Raw character length: 6,420 characters.
Token count under OpenAI's tokenizer: **1,612 tokens**.

We execute `optimize_markdown_payload(raw_text)`:
The parser strips all link URLs, eliminates formatting markup, but preserves our Python code block with mathematical exactness.

After optimization:
Cleaned token count: **968 tokens**.
**Net Token Reduction: 39.95%**!

That's over six hundred tokens saved on a single article. When your agent processes thousands of queries a day, that 40% cut translates to thousands of dollars saved on your monthly inference bill—and an immediate drop in Time to First Token."

---

### [09:15 - 10:30] SUMMARY & CHALLENGE

**PRESENTER (Spoken to Camera):**
"Context engineering is not just about writing good prompts. It is about treating tokens as expensive computational currency.

Clone `08_VIDEO_PROJECTS/strip_markdown_optimizer.py` from our repository and add it as a preprocessing hook in your ingestion pipeline.

In **Episode 7**, we tackle the storage tier: How to store vectors, telemetry, and relational data in a single unified database using **Tiger Cloud TimescaleDB Postgres**.

Subscribe, and I'll see you in the next lesson."
