# Episode M05_L03: Enterprise AI Standards: Hardening Claude Code with CLAUDE.md

**Series:** LLMOps & Agentic Engineering: From Foundation to Production-Scale Systems  
**Module:** 05 — Agentic Architectures & Semantic Backends  
**Target Duration:** 12:30  
**Format:** YouTube Masterclass Deep-Dive (Repository Audits, Config Deconstructions, Hook Pipelines)  
**Tone:** Senior Engineering Manager / Staff Architect perspective. Taming AI chaos in enterprise codebases.

---

## Technical Overview & Pedagogical Objectives
- **The Core Problem:** The "Context Drift & Style Rot" of AI Coding Assistants. When engineers use AI tools like Claude Code without guardrails, the agent hallucinates deprecated APIs, introduces random third-party dependencies, writes code in incompatible paradigms (e.g., mixing class components with React server components), and declares tasks "Done" without running the test suite.
- **The Architectural Solution:** Production-Grade Repository Hardening using `CLAUDE.md` and automated tool hooks. Defining deterministic constraints, architecture rules, verification commands, and forbidden patterns that the agent loads automatically into its root system prompt.
- **The Working Demonstration:** Auditing an enterprise repository before and after configuring a bulletproof `CLAUDE.md` and automated linting hooks, demonstrating how PostToolUse verification blocks faulty code before it ever reaches a commit.

---

## Script & Production Timeline

### 00:00 - 00:45 | ACT I: The Junior Engineer with Root Privileges (The Hook)
**[VISUAL]** High-contrast dark room (`#0B0F17`). 
Screen displays a catastrophic GitHub Pull Request:
- Author: `AI Assistant (Claude Code)`
- Files changed: 42 files, +3,800 lines.
- PR Description: *"I fixed the bug by rewriting your authentication system, switching your testing framework from Vitest to Jest, installing 14 new NPM packages, and disabling TypeScript strict mode."*
- CI Status: 18 failing checks.
- High-contrast text: **"STOP TREATING YOUR AI LIKE A MAGICIAN. TREAT IT LIKE AN INTERN."**

**[AUDIO]** Dramatic glitch sound, followed by a heavy mechanical drop. Voice enters crisp, authoritative.

**[NARRATOR (VO)]**
> "Anthropic's Claude Code is arguably the most capable agentic coding assistant ever created.
> 
> But if you run Claude Code inside a multi-million-dollar enterprise repository without configuring guardrails, you have just handed root access to a hyperactive junior engineer who has read every programming book on earth, but doesn't know your company's coding rules.
> 
> In thirty seconds, it will introduce five new dependencies to solve a problem that your standard library already handles.
> It will mix functional patterns with object-oriented boilerplate.
> And it will confidently tell you: 'I have finished the task,' without ever running your test suite.
> 
> How do elite engineering teams tame this chaos?
> 
> They don't write endless repetitive prompts.
> 
> They configure **`CLAUDE.md`**.
> 
> In this video, we deconstruct the anatomy of a production-grade `CLAUDE.md`. You will learn how to enforce architectural boundaries, configure automated post-tool verification hooks, and force your AI assistant to practice strict Test-Driven Development on every line of code."

---

### 00:45 - 04:00 | ACT II: What is CLAUDE.md? (The Root System Context)
**[VISUAL]** High-contrast architectural diagram showing how Claude Code loads context:
1. Engineer invokes `claude` in terminal.
2. Claude Code scans the current workspace root for `CLAUDE.md` (or `.claude/rules/`).
3. It parses the Markdown file and injects it at the highest priority level into its system prompt.
4. Every reasoning step, file edit, and bash execution is permanently conditioned on these instructions throughout the entire session.

**[NARRATOR (VO)]**
> "To understand `CLAUDE.md`, you have to understand how Claude Code thinks.
> 
> When you launch the CLI, Claude Code looks for a file named `CLAUDE.md` at the root of your project.
> 
> This is not standard user documentation. This is **operational firmware for the AI**.
> 
> Whatever you put in `CLAUDE.md` becomes part of the model's core system prompt for every tool call it makes.
> 
> If you tell it: 'Never install an NPM package without asking,' it will not install an NPM package.
> If you tell it: 'Our test runner is `pnpm test:unit`,' it knows the exact command to verify its work.
> 
> But most developers write terrible `CLAUDE.md` files. They write five pages of philosophical ramblings about their product vision, which clutters the context window with useless tokens.
> 
> A production `CLAUDE.md` must be lean, deterministic, and operational."

---

### 04:00 - 08:30 | ACT III: The Anatomy of a Bulletproof CLAUDE.md
**[VISUAL]** Visual Studio Code screen displaying a production-grade `CLAUDE.md` template with glowing section highlights:

**[SCREEN CODE]**:
```markdown
# Enterprise Repository Guidelines

## 1. Build & Test Commands (Mandatory Verification)
- Run unit tests: `pnpm test:unit`
- Run integration tests: `pnpm test:e2e`
- Lint & Typecheck: `pnpm lint && pnpm tsc --noEmit`
- Format check: `pnpm prettier --check .`

## 2. Architectural Boundaries
- Stack: Next.js 15 (App Router), TypeScript (Strict Mode enabled).
- Styling: Tailwind CSS v4. Never use CSS Modules or inline style tags.
- State Management: Zustand for client state; TanStack Query for server state.
- FORBIDDEN: Never import `moment.js` (use `date-fns`), never use `any` type.

## 3. Autonomous Execution Rules
- TDD Enforcement: Write the failing test FIRST before modifying source code.
- Verification Rule: You may NEVER state a task is complete until `pnpm lint && pnpm test:unit` passes with exit code 0.
- Commits: Use Conventional Commits (`feat:`, `fix:`, `refactor:`). Never push directly to `main`.
```

**[NARRATOR (VO)]**
> "Look at the four sections of a battle-tested `CLAUDE.md`:
> 
> **Section One: Explicit Build & Verification Commands.**
> Never assume the LLM knows how to test your code. Specify the exact shell commands for unit testing, linting, and typechecking. When the agent gets stuck or introduces a type error, it can run these commands to self-correct in seconds.
> 
> **Section Two: Architectural Invariants & Forbidden Libraries.**
> This is where you protect your codebase from library bloat. If your team uses `date-fns`, explicitly forbid `moment.js`. If you are on Next.js App Router, explicitly instruct it to never create `pages/` directory files. Be ruthless with negative constraints.
> 
> **Section Three: The 'Verification Gate' Rule.**
> Notice this exact sentence: *'You may NEVER state a task is complete until `pnpm test` passes with exit code 0.'*
> That single line eliminates the most frustrating behavior in AI coding—the premature declaration of victory while code remains broken.
> 
> **Section Four: Atomic Commit Protocols.**
> Define how you want commits structured so your git history remains pristine."

---

### 08:30 - 11:00 | ACT IV: Automated Hooks: The PostToolUse Gate
**[VISUAL]** High-contrast schematic: The Claude Code Tool Hook Pipeline (`.claude/hooks.json`):
- Action: Claude Code executes `edit_file("src/api/auth.ts")`.
- Hook Trigger: `PostToolUse` event fires instantly.
- Hook Script: Runs `ruff check` or `tsc --noEmit` on the modified file.
- If Hook fails (exit code 1): The error output is automatically fed directly back into Claude's context window with message: `"HOOK ERROR: File violates type rules. Fix immediately before proceeding."`

**[NARRATOR (VO)]**
> "Even with a great `CLAUDE.md`, models can occasionally skip instructions.
> 
> That’s why modern AI engineering teams enforce **Automated Tool Hooks**.
> 
> Claude Code supports configuration hooks in `.claude/hooks.json`:
> 
> You can register a `PostToolUse` hook that runs automatically every time the agent edits a file.
> 
> Look at the workflow on screen:
> 1. Claude edits `src/utils/payment.ts`.
> 2. Before Claude can even generate its next sentence, our local hook runs `eslint` and `tsc`.
> 3. If Claude introduced an unused variable or a syntax error, the hook intercepts the agent's turn and injects the compiler error directly into its prompt.
> 
> The agent is forced to fix the lint error before it can move on to the next file!
> 
> Bad code is caught at the microsecond of generation, preventing multi-file syntax rot."

---

### 11:00 - 12:30 | ACT V: Summary & Next Episode Preview
**[VISUAL]** Summary graphic:
- Uncontrolled AI -> Context drift, dependency bloat, failing CI.
- Hardened AI (`CLAUDE.md` + Hooks) -> Strict architectural compliance, 100% test pass rate, clean atomic commits.
- Next preview: **Episode M05_L04 — The 100% Offline AI Second Brain: Rowboat & Ollama**.

**[NARRATOR (VO)]**
> "To summarize our enterprise standards:
> 
> One: Treat `CLAUDE.md` as operational firmware, not general documentation.
> 
> Two: Specify exact build, lint, and test commands, and mandate that tests must pass before task completion.
> 
> Three: Wire up `PostToolUse` hooks to catch type errors and style violations automatically.
> 
> Now, what if your enterprise has sensitive intellectual property, proprietary source code, or internal architecture docs that you CANNOT send to external cloud APIs?
> 
> How do you build a local-first, 100% offline agentic second brain?
> 
> In Episode 4, we explore **Rowboat**: how to combine Ollama, local embeddings, and plain-markdown knowledge graphs to give your agents deep company memory without a single byte leaving your laptop.
> 
> Download our enterprise `CLAUDE.md` template in the description, subscribe, and I'll see you in Episode 4."
