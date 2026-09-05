"""
MIT Recursive Language Model (RLM) Scaffolding Simulator
LLMOps & Agentic Engineering Masterclass - Module 1 Lesson 4 Demo

Demonstrates mitigating context rot by storing long context inside
a Python REPL environment variable rather than the LLM prompt window.
"""

import re
import time

class RLMSimulator:
    def __init__(self, raw_corpus: str):
        # Store context in the environment (never feed the full raw string to the model)
        self.env = {"document": raw_corpus}
        print(f"[REPL Sandbox Initialized] Loaded corpus of {len(raw_corpus):,} characters into variable 'document'.")

    def grep_tool(self, pattern: str):
        print(f"  --> [REPL TOOL] Running regex grep for: '{pattern}'")
        time.sleep(0.2)
        lines = [line.strip() for line in self.env["document"].split("\n") if re.search(pattern, line, re.IGNORECASE)]
        print(f"  --> [REPL TOOL] Found {len(lines)} matching lines.")
        return lines

    def chunk_tool(self, size: int = 500):
        print(f"  --> [REPL TOOL] Partitioning context into blocks of {size} characters...")
        time.sleep(0.2)
        doc = self.env["document"]
        chunks = [doc[i:i+size] for i in range(0, len(doc), size)]
        print(f"  --> [REPL TOOL] Created {len(chunks)} sub-chunks.")
        return chunks

    def recursive_eval(self, query: str):
        print(f"\n[User Query Received]: '{query}'")
        print("[Agent Logic] Instead of loading all 100K tokens into prompt, generating programmatic inspection plan...")
        time.sleep(0.4)
        
        # Step 1: Programmatic filter
        extracted_pattern = "User 12345"
        print(f"[Agent Execution] Programmatically calling grep_tool('{extracted_pattern}')...")
        matches = self.grep_tool(extracted_pattern)
        
        # Step 2: Recursive sub-call on targeted context
        print("\n[Targeted Sub-Context for Recursive LLM Reasoning]:")
        for m in matches:
            print(f"   * {m}")
        
        print("\n[Recursive Child LLM Evaluation]: Analyzing 2 extracted lines (Tokens: ~35)...")
        time.sleep(0.3)
        return "User 12345 submitted two tickets: TICKET_101 regarding billing issues, and TICKET_104 requesting a refund for a billing error."

def main():
    print("=" * 75)
    print("MIT RECURSIVE LANGUAGE MODEL (RLM) SIMULATOR - CONTEXT ROT DEFENSE")
    print("=" * 75)

    # Simulated large text database
    tickets_database = """
    TICKET_098: User 99999 reported slow database queries in Europe-West.
    TICKET_099: User 88888 asked about SOC-2 compliance certification.
    TICKET_100: User 77777 updated their organization payment method to Mastercard.
    TICKET_101: User 12345 complained about unexpected billing charges on August 14.
    TICKET_102: User 67890 reported a critical bug in the JWT authentication gateway.
    TICKET_103: User 11111 requested custom enterprise workspace pricing for 500 seats.
    TICKET_104: User 12345 requested a full refund of $420 for the billing calculation error.
    TICKET_105: User 55555 reported intermittent timeouts when using Web MCP scraper.
    """

    rlm = RLMSimulator(tickets_database)
    answer = rlm.recursive_eval("What were the specific complaints and requests made by User 12345?")
    print(f"\n[Final Verified Answer]:\n{answer}")
    print("\n" + "=" * 75)
    print("SUCCESS: Zero Context Rot | Active Prompt Footprint Kept Flat (<500 tokens)")
    print("=" * 75)

if __name__ == "__main__":
    main()
