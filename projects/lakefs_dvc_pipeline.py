#!/usr/bin/env python3
"""
LakeFS & DVC Isolated Staging, Data Audit, and Rollback Simulator
Episode M02_L04: Data Versioning for LLMs: DVC, LakeFS & Rollback Audits

Demonstrates:
1. Zero-copy metadata branching from 'main'.
2. Ingestion of data batches into isolated staging branches.
3. Automated pre-commit data quality audit hooks (entropy drift & schema validation).
4. Quarantine and abort on poisoned data.
5. Instant rollback to previous commit hashes.
"""

import hashlib
import json
import math
import time
from typing import Dict, List, Any, Optional

class MockGravelerCommit:
    def __init__(self, commit_id: str, message: str, parent_id: Optional[str], data_manifest: Dict[str, str]):
        self.commit_id = commit_id
        self.message = message
        self.parent_id = parent_id
        self.data_manifest = data_manifest # path -> content_hash
        self.timestamp = time.time()

class LakeFSRepository:
    def __init__(self, repo_name: str):
        self.repo_name = repo_name
        self.commits: Dict[str, MockGravelerCommit] = {}
        self.branches: Dict[str, str] = {} # branch_name -> commit_id
        self.staging: Dict[str, Dict[str, str]] = {} # branch_name -> {path: content}
        
        # Initialize main branch with root commit
        root_commit = MockGravelerCommit(
            commit_id="c_init_0000",
            message="Initial repository commit",
            parent_id=None,
            data_manifest={}
        )
        self.commits[root_commit.commit_id] = root_commit
        self.branches["main"] = root_commit.commit_id
        self.staging["main"] = {}

    def create_branch(self, branch_name: str, source_branch: str = "main") -> str:
        if source_branch not in self.branches:
            raise ValueError(f"Source branch '{source_branch}' does not exist.")
        base_commit = self.branches[source_branch]
        self.branches[branch_name] = base_commit
        self.staging[branch_name] = {}
        return f"Created zero-copy branch '{branch_name}' pointing to commit {base_commit} (0 bytes copied)"

    def upload_object(self, branch: str, path: str, content: str):
        if branch not in self.branches:
            raise ValueError(f"Branch '{branch}' does not exist.")
        self.staging[branch][path] = content

    def commit(self, branch: str, message: str) -> str:
        parent_id = self.branches[branch]
        parent_manifest = dict(self.commits[parent_id].data_manifest)
        
        # Merge staged changes into new manifest
        for path, content in self.staging.get(branch, {}).items():
            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
            parent_manifest[path] = content_hash
            
        commit_id = f"c_{hashlib.sha256(f'{parent_id}:{message}:{time.time()}'.encode()).hexdigest()[:8]}"
        new_commit = MockGravelerCommit(commit_id, message, parent_id, parent_manifest)
        self.commits[commit_id] = new_commit
        self.branches[branch] = commit_id
        self.staging[branch] = {}
        return commit_id

    def revert(self, branch: str, target_commit_id: str) -> str:
        if target_commit_id not in self.commits:
            raise ValueError(f"Target commit {target_commit_id} not found.")
        self.branches[branch] = target_commit_id
        return f"Branch '{branch}' rolled back to {target_commit_id} ({self.commits[target_commit_id].message})"

def calculate_token_entropy(text: str) -> float:
    """Calculates Shannon entropy of character/token distribution."""
    if not text:
        return 0.0
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    entropy = 0.0
    length = len(text)
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy

def audit_staging_quality_hook(repo: LakeFSRepository, branch: str) -> bool:
    """Automated pre-commit data audit hook (schema integrity & entropy check)."""
    staged_files = repo.staging.get(branch, {})
    for path, content in staged_files.items():
        lines = content.strip().split("\n")
        total_entropy = 0.0
        for idx, line in enumerate(lines):
            try:
                record = json.loads(line)
                if "text" not in record or "doc_id" not in record:
                    print(f"  ❌ Audit Fail [Schema]: Missing required keys in line {idx+1} of {path}")
                    return False
                total_entropy += calculate_token_entropy(record["text"])
            except json.JSONDecodeError:
                print(f"  ❌ Audit Fail [Syntax]: Malformed JSON on line {idx+1} of {path}")
                return False
                
        avg_entropy = total_entropy / len(lines) if lines else 0.0
        # Normal English / technical corpus typically has Shannon entropy between 3.5 and 5.2
        if avg_entropy < 2.5:
            print(f"  ❌ Audit Fail [Entropy Collapse]: Detected repetitive/corrupted data (Entropy: {avg_entropy:.2f} < 2.5)")
            return False
            
    return True

def main():
    print("=================================================================")
    print(" LAKEFS GIT-FOR-DATA STAGING & AUDIT SIMULATOR (M02_L04)")
    print("=================================================================\n")
    
    repo = LakeFSRepository("enterprise-rag-corpus")
    print(f"[*] Initialized LakeFS Repository: {repo.repo_name} on branch 'main'")
    
    # 1. Baseline good commit on main
    clean_batch = "\n".join([
        json.dumps({"doc_id": "doc_001", "text": "Kubernetes orchestration requires ingress controllers and Calico CNI plugins."}),
        json.dumps({"doc_id": "doc_002", "text": "PostgreSQL TimescaleDB provides hypertables for time-series telemetry compression."})
    ])
    repo.upload_object("main", "raw/batch_01.jsonl", clean_batch)
    v1_commit = repo.commit("main", "feat: Ingest validated Q1 technical manual docs")
    print(f"[*] Committed clean baseline data to main: {v1_commit}")
    print(f"    Manifest: {repo.commits[v1_commit].data_manifest}\n")
    
    # 2. Spawn isolated zero-copy branch for daily crawler ingestion
    branch_status = repo.create_branch("staging-crawler-run-042", source_branch="main")
    print(f"[*] {branch_status}")
    
    # 3. Simulate crawler ingesting POISONED / CORRUPTED data
    print("\n[*] Simulating Crawler Ingestion: Ingesting batch with collapsed entropy (repetition bug)...")
    poisoned_batch = "\n".join([
        json.dumps({"doc_id": "doc_003", "text": "a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a"}),
        json.dumps({"doc_id": "doc_004", "text": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"})
    ])
    repo.upload_object("staging-crawler-run-042", "raw/batch_02.jsonl", poisoned_batch)
    
    # 4. Trigger automated pre-commit hook
    print("[*] Triggering LakeFS Pre-Commit Quality Hook...")
    passed = audit_staging_quality_hook(repo, "staging-crawler-run-042")
    
    if not passed:
        print("\n🚨 AUTOMATED HOOK INTERCEPT: Poisoned data detected!")
        print("[*] Aborting merge into 'main'. Deleting staging branch.")
        del repo.branches["staging-crawler-run-042"]
        print("[+] Main branch remained 100% clean and protected from corruption.")
    
    print(f"\n[*] Current main branch head: {repo.branches['main']} (Commit: {repo.commits[repo.branches['main']].message})")
    print("=================================================================")
    print(" DATA VERSIONING AUDIT SIMULATION COMPLETE - VERIFIED PASS")
    print("=================================================================")

if __name__ == "__main__":
    main()
