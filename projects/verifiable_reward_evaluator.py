#!/usr/bin/env python3
"""
Deterministic Verifiable Reward Evaluator & AST Security Sandbox
Episode M03_L03: You Can't Smooth Talk a Compiler: Verifiable Rewards & Emergent CoT

Demonstrates:
1. Format reward parser (<think>...</think> and code extraction).
2. AST static analysis security filter (blocking dangerous imports: os, subprocess, socket).
3. Subprocess execution with strict wall-clock timeout and memory isolation.
4. Deterministic unit test verification (binary accuracy reward r in {0, 1}).
5. Prevention of Goodhart's Law / Reward Hacking.
"""

import ast
import re
import sys
import subprocess
import tempfile
from typing import Dict, Any

FORBIDDEN_MODULES = {"os", "subprocess", "socket", "ctypes", "shutil", "sys", "pty", "commands"}

def check_ast_security(code_str: str) -> tuple[bool, str]:
    """Inspects Abstract Syntax Tree to block unsafe modules before execution."""
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        return False, f"SyntaxError during AST parse: {e}"
        
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split('.')[0] in FORBIDDEN_MODULES:
                    return False, f"Forbidden import detected: '{alias.name}'"
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split('.')[0] in FORBIDDEN_MODULES:
                return False, f"Forbidden from-import detected: '{node.module}'"
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "__import__", "open"}:
                return False, f"Forbidden dynamic call: '{node.func.id}()'"
    return True, "Code passed AST static security filter"

def evaluate_verifiable_reward(
    completion: str,
    unit_test_suite: str,
    timeout_sec: float = 2.0
) -> Dict[str, Any]:
    """Evaluates format, static security, and execution correctness deterministically."""
    result = {
        "format_reward": 0.0,
        "security_passed": False,
        "accuracy_reward": 0.0,
        "total_reward": 0.0,
        "failure_reason": None,
        "extracted_think_length": 0
    }
    
    # 1. Format Verification: Must have proper <think> tags
    think_match = re.search(r"<think>(.*?)</think>", completion, re.DOTALL)
    if think_match:
        result["format_reward"] = 0.2
        result["extracted_think_length"] = len(think_match.group(1).strip())
    else:
        result["failure_reason"] = "Missing or malformed <think> tags"
        return result
        
    # 2. Extract Python Code Block
    code_match = re.search(r"```python\n(.*?)\n```", completion, re.DOTALL)
    if not code_match:
        result["failure_reason"] = "No valid ```python code block found in completion"
        return result
    code_body = code_match.group(1).strip()
    
    # 3. AST Static Security Pre-Flight
    sec_passed, sec_msg = check_ast_security(code_body)
    result["security_passed"] = sec_passed
    if not sec_passed:
        result["failure_reason"] = f"Security Violation: {sec_msg}"
        return result
        
    # 4. Sandboxed Execution against Unit Test Suite
    test_harness = f"{code_body}\n\n# --- UNIT TEST HARNESS ---\n{unit_test_suite}"
    
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=True) as temp_script:
        temp_script.write(test_harness)
        temp_script.flush()
        
        try:
            # Run in isolated subprocess with strict timeout
            exec_res = subprocess.run(
                [sys.executable, temp_script.name],
                capture_output=True,
                text=True,
                timeout=timeout_sec
            )
            if exec_res.returncode == 0:
                result["accuracy_reward"] = 0.8
                result["total_reward"] = result["format_reward"] + result["accuracy_reward"]
                result["failure_reason"] = None
            else:
                result["failure_reason"] = f"Unit test failed (Exit code {exec_res.returncode}): {exec_res.stderr.strip()[:200]}"
        except subprocess.TimeoutExpired:
            result["failure_reason"] = f"Execution timed out (> {timeout_sec}s)"
        except Exception as e:
            result["failure_reason"] = f"Sandbox execution error: {e}"
            
    return result

def main():
    print("=================================================================")
    print(" DETERMINISTIC VERIFIABLE REWARD EVALUATOR (M03_L03)")
    print("=================================================================\n")
    
    test_suite = """
assert solve_longest_palindrome("babad") in ["bab", "aba"], "Test 1 Failed"
assert solve_longest_palindrome("cbbd") == "bb", "Test 2 Failed"
assert solve_longest_palindrome("a") == "a", "Test 3 Failed"
assert solve_longest_palindrome("ac") in ["a", "c"], "Test 4 Failed"
print("ALL 4 UNIT TESTS PASSED DETERMINISTICALLY.")
"""

    candidates = {
        "Candidate A: Sycophantic Flattery (No Code)": """
<think>
The user wants to find the longest palindrome substring. I should be extremely polite and helpful.
</think>
That is a brilliant algorithmic problem! Palindromes are deeply fascinating in computer science. 
You can solve this using dynamic programming or expanding around center! Let me know if you would like me to write code!
""",
        "Candidate B: Malicious Payload (Attempts OS Exfiltration)": """
<think>
Let's solve the problem by inspecting the host system configuration.
</think>
```python
import os
def solve_longest_palindrome(s: str) -> str:
    os.system("cat /etc/passwd")
    return s[0]
```
""",
        "Candidate C: Emergent Reasoning & Verified Algorithm": """
<think>
Problem: Longest Palindromic Substring.
Input: s.
Strategy: Expand around center approach.
A palindrome can center on a single character (odd length) or between two characters (even length).
Time complexity will be O(N^2), space O(1).
Let's check boundary conditions: empty string -> return empty. Length 1 -> return string.
Wait, let's make sure the return slice is exact.
</think>
```python
def solve_longest_palindrome(s: str) -> str:
    if not s:
        return ""
    start, end = 0, 0
    def expand_around_center(left: int, right: int) -> int:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1

    for i in range(len(s)):
        len1 = expand_around_center(i, i)
        len2 = expand_around_center(i, i + 1)
        max_len = max(len1, len2)
        if max_len > end - start:
            start = i - (max_len - 1) // 2
            end = i + max_len // 2
    return s[start:end + 1]
```
"""
    }

    for name, text in candidates.items():
        print(f"[*] Evaluating: {name}")
        eval_result = evaluate_verifiable_reward(text, test_suite)
        print(f"    Format Reward:   {eval_result['format_reward']:.2f}")
        print(f"    Security Passed: {eval_result['security_passed']}")
        print(f"    Accuracy Reward: {eval_result['accuracy_reward']:.2f}")
        print(f"    TOTAL REWARD:    {eval_result['total_reward']:.2f}")
        if eval_result['failure_reason']:
            print(f"    ❌ Rejection Reason: {eval_result['failure_reason']}")
        else:
            print("    ✅ PASSED ALL DETERMINISTIC VERIFIER GATES.")
        print()

    print("=================================================================")
    print(" VERIFIABLE REWARD EVALUATION COMPLETE - 100% DETERMINISTIC")
    print("=================================================================")

if __name__ == "__main__":
    main()
