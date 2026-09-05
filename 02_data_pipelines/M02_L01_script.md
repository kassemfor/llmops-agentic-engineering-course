# SCRIPT: M02_L01
## Web Scraping for AI Without Getting Blocked (Model Context Protocol)

**Course:** LLMOps & Agentic Engineering  
**Module 2:** The Modern LLMOps Data Pipeline  
**Episode:** 05 (Module 2 Premiere)  
**Target Duration:** ~12 Minutes  
**Target Audience:** Data Engineers, Full-Stack Developers, Agent Builders  

---

### [00:00 - 00:35] THE HOOK

**VISUAL CUE:**
Presenter on camera. Behind the presenter, a terminal runs a standard BeautifulSoup / Puppeteer web scraper. The terminal suddenly explodes with red HTTP errors: `403 Forbidden`, `429 Too Many Requests`, and a Cloudflare CAPTCHA challenge screen.

**PRESENTER (Spoken to Camera):**
"If you are trying to feed live web data to your AI agents using traditional web scraping in 2026, you already know the frustration:

You write a scraper with BeautifulSoup or Puppeteer. It runs for three minutes. Then you get hit with IP rate limits, Cloudflare bot-detection firewalls, and CAPTCHAs. 

And even when your scraper does work, it spits out five megabytes of minified Javascript, tracking pixels, and CSS styles that completely destroy your LLM's context window.

Brittle CSS selectors are dead. 

Today, we are connecting our AI agents directly to the live web using the **Model Context Protocol (MCP)** and **Bright Data's Web MCP server**—giving our agents unblockable, real-time web superpowers. Let's inspect the setup."

---

### [00:35 - 04:15] SECTION 1: THE BOT-DETECTION MINEFIELD

**VISUAL CUE:**
Diagram contrasting traditional scraping vs. MCP-based web infrastructure.
Left: `Standard Scraper -> Target Website -> IP Blocked / CAPTCHA Challenge`.
Right: `AI Agent -> Model Context Protocol (MCP) -> Bright Data Proxy Network -> Unblocked Web Data`.

**PRESENTER (Spoken):**
"Why does traditional web scraping fail in production agentic systems?

Because modern websites use sophisticated behavioral fingerprinting. They analyze TLS handshakes, monitor canvas rendering, inspect browser headers, and rate-limit IP ranges. 

If your autonomous agent needs to research live financial filings, track competitor pricing, or verify real-time news, you cannot afford to have your pipeline fail because a website changed its CSS class names from `product-price` to `price-v2`.

We need three enterprise capabilities:
1. **Automated Proxy Rotation:** Routing requests through residential and data center IP networks across the globe.
2. **Automated CAPTCHA Solving & Headless Browser Rendering:** Emulating legitimate user sessions without manual intervention.
3. **Intent-Based Search & Discovery:** Asking high-level semantic questions rather than hand-crafting brittle HTTP GET requests."

---

### [04:15 - 08:30] SECTION 2: BRIGHT DATA WEB MCP ARCHITECTURE

**VISUAL CUE:**
Architectural diagram of the Model Context Protocol (MCP) JSON-RPC bridge between an LLM agent (Claude Desktop, Cursor, or custom Python agent) and the Bright Data hosted server.

**PRESENTER (Spoken):**
"Enter the **Model Context Protocol (MCP)**.
MCP is an open standard that allows Large Language Models to discover and execute external tools through a uniform JSON-RPC protocol.

Bright Data provides an official, enterprise-grade Web MCP server that exposes three foundational tools:
* `search_engine`: Executes optimized web searches across major engines for real-time fact checking and research.
* `scrape_as_markdown`: Ingests any URL, bypasses all anti-bot protections automatically, strips scripts, and converts the clean content into AI-ready markdown.
* `discover`: Runs intent-based discovery, ranking web results based on semantic relevance to the agent's task.

Notice how simple the client configuration is:
Inside your agent's `mcpServers` configuration file, you add a single block:

```json
{
  "mcpServers": {
    "Bright Data": {
      "command": "npx",
      "args": ["@brightdata/mcp"],
      "env": {
        "API_TOKEN": "YOUR_BRIGHT_DATA_TOKEN",
        "GROUPS": "advanced_scraping,code"
      }
    }
  }
}
```

Notice that `GROUPS` environment variable! 
Instead of exposing all sixty-two tools and bloating your agent's prompt window, you scope tool groups to exactly what the agent needs. Setting `GROUPS="code"` exposes npm and PyPI package lookup tools. Setting `GROUPS="advanced_scraping"` gives full web unblocking."

---

### [08:30 - 11:30] SECTION 3: LIVE TERMINAL DEMO & MARGINAL COSTS

**VISUAL CUE:**
Screen recording showing Claude Desktop / Terminal invoking `search_engine` and `scrape_as_markdown` on a complex dynamic web application.

**PRESENTER (Voiceover over Demo):**
"Watch the execution in real-time:
Our agent receives the prompt: *'Analyze the latest architectural features released in SGLang Spec V2 on GitHub.'*

The agent calls `search_engine`. In eight hundred milliseconds, Bright Data routes through an unblocked residential node, executes the search, and returns top results.

The agent selects the official release page and calls `scrape_as_markdown`. 

Notice what happens: No CAPTCHAs, no Cloudflare blocks, and zero raw HTML boilerplate. The agent receives clean, structured markdown containing the release notes, benchmark numbers, and installation commands.

Now let's talk economics: 
Bright Data provides five thousand free credits every month. Base tools like search and markdown extraction cost exactly **one credit per request**. 

You can run thousands of live agentic research queries every month without ever managing a proxy server or maintaining headless browser instances."

---

### [11:30 - 12:30] SUMMARY & NEXT LESSON

**PRESENTER (Spoken to Camera):**
"Now that our agent can ingest the live web without getting blocked, we face our next challenge:
Scraped markdown still contains image URLs, styling tags, and metadata links that burn through expensive context tokens.

In **Episode 6**, we introduce **Strip-Markdown Optimization**, showing how AST parsing strips forty percent of your token payload before it ever reaches the LLM.

Subscribe, check the repo links below, and I'll see you in the next lesson."
