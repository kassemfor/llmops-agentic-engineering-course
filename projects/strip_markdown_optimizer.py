"""
Strip-Markdown Payload Context Optimizer
LLMOps & Agentic Engineering Masterclass - Module 2 Lesson 2 Demo

Demonstrates parsing scraped web markdown to strip non-essential formatting
(hyperlinks, images, bold/italics) while preserving technical code blocks,
achieving an approximate ~40% token payload reduction for RAG prefill.
"""

import re
import time

def optimize_markdown_payload(raw_md: str) -> str:
    """
    Strips non-essential markdown syntax (links, images, styling)
    while strictly preserving code blocks and raw text.
    """
    # 1. Protect code blocks by extracting them into placeholders
    code_blocks = []
    def code_replacer(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"

    # Match fenced code blocks (```...```)
    text = re.sub(r"```[\s\S]*?```", code_replacer, raw_md)

    # 2. Strip images: ![alt](url) -> ""
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)

    # 3. Strip link URLs while keeping anchor text: [Anchor](url) -> Anchor
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)

    # 4. Strip bold and italic symbols (**text** or *text* -> text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)

    # 5. Strip blockquote indicators (> )
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)

    # 6. Clean up excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    # 7. Restore protected code blocks
    for idx, block in enumerate(code_blocks):
        text = text.replace(f"__CODE_BLOCK_{idx}__", block)

    return text

def estimate_tokens(text: str) -> int:
    """Rough estimation of token count (~4 characters per token for English)."""
    return int(len(text) / 3.8)

def main():
    print("=" * 75)
    print("STRIP-MARKDOWN CONTEXT OPTIMIZER (40% TOKEN REDUCTION)")
    print("=" * 75)

    sample_scraped_article = """
# Getting Started with [DFlash Speculative Decoding](https://github.com/z-lab/dflash?utm_source=blog&ref=landing)

![DFlash Banner](https://cdn.enterprise-ai.com/assets/images/banner_v2_hires_2026_speculative_decoding.png)

> **Note:** Speculative decoding is the *definitive* method to slash Time-to-First-Token (TTFT). For more information, visit our [Architecture Guide](https://docs.enterprise-ai.com/spec-decoding/architecture-deep-dive?session=8932478923).

### Key Features
* **Parallel Block Drafting:** Generates a block of **16 tokens** simultaneously. Check our [Paper Review](https://arxiv.org/abs/2401.99999).
* **High Acceptance Rate:** Achieves over **85% token acceptance** on [Qwen-3.5 Benchmarks](https://huggingface.co/Qwen/Qwen3.5-397B).
* **Seamless Integration:** Compatible with [vLLM](https://github.com/vllm-project/vllm) and [SGLang](https://github.com/sgl-project/sglang).

Here is the exact code snippet to launch the server:

```python
# Launch SGLang with DFlash speculative decoding
import sglang as sgl

server = sgl.Server(
    model_path="Qwen/Qwen3.5-27B",
    speculative_algorithm="DFLASH",
    speculative_draft="z-lab/Qwen3.5-27B-DFlash",
    num_speculative_tokens=16
)
server.start()
```

For customer support, reach out to [Support Portal](https://support.enterprise-ai.com/tickets/new) or read our [Terms of Service](https://enterprise-ai.com/legal/tos).
"""

    print("\n1. Processing Raw Scraped Web Payload...")
    raw_chars = len(sample_scraped_article)
    raw_tokens = estimate_tokens(sample_scraped_article)
    print(f"   Raw Payload Length : {raw_chars:,} characters")
    print(f"   Estimated Tokens   : {raw_tokens:,} tokens")

    time.sleep(0.3)
    print("\n2. Executing AST Strip-Markdown Optimization...")
    cleaned = optimize_markdown_payload(sample_scraped_article)
    cleaned_chars = len(cleaned)
    cleaned_tokens = estimate_tokens(cleaned)

    reduction = ((raw_tokens - cleaned_tokens) / raw_tokens) * 100

    print(f"   Cleaned Length     : {cleaned_chars:,} characters")
    print(f"   Cleaned Tokens     : {cleaned_tokens:,} tokens")
    print(f"   Net Token Savings  : {reduction:.2f}% REDUCTION")

    print("\n" + "-" * 75)
    print("CLEANED PAYLOAD PREVIEW (Preserves Code, Strips URLs & Markdown Noise):")
    print("-" * 75)
    print(cleaned[:400] + "\n[...]\n" + cleaned[-250:])
    print("=" * 75)

if __name__ == "__main__":
    main()
