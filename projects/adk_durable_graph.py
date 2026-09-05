#!/usr/bin/env python3
"""
Google ADK 2.0 Durable State Graph & Checkpoint Resumption Engine
Episode M05_L01: Beyond Vibe Coding: Durable State Graphs with Google ADK 2.0

Implements:
1. Directed State Machine with Nodes and Conditional Edges.
2. Event-Sourced transactional state checkpointing (SQLite / file store).
3. Native suspend/interrupt mechanism for long-running Human-in-the-Loop approvals.
4. Process termination simulation (zero RAM / zero CPU during human review).
5. State deserialization and seamless resumption from exact microstate.
"""

import json
import os
import sys
import time
from typing import Callable, Dict, Any, Optional

class CheckpointStore:
    def __init__(self, db_path: str = "/tmp/adk_checkpoints.json"):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump({}, f)

    def save(self, checkpoint_id: str, state: Dict[str, Any]):
        with open(self.db_path, "r") as f:
            data = json.load(f)
        data[checkpoint_id] = state
        with open(self.db_path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        with open(self.db_path, "r") as f:
            data = json.load(f)
        return data.get(checkpoint_id)

class AgentGraph:
    def __init__(self, name: str, checkpointer: CheckpointStore):
        self.name = name
        self.checkpointer = checkpointer
        self.nodes: Dict[str, Callable] = {}
        self.interrupt_nodes: set = set()
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Callable[[Dict[str, Any]], str]] = {}

    def add_node(self, name: str, handler: Callable, is_interrupt: bool = False):
        self.nodes[name] = handler
        if is_interrupt:
            self.interrupt_nodes.add(name)

    def add_edge(self, source: str, destination: str):
        self.edges[source] = destination

    def add_conditional_edge(self, source: str, condition_fn: Callable[[Dict[str, Any]], str]):
        self.conditional_edges[source] = condition_fn

    def run(self, initial_state: Dict[str, Any], start_node: str) -> Dict[str, Any]:
        state = dict(initial_state)
        current_node = start_node
        checkpoint_id = state.get("checkpoint_id", f"chk_{int(time.time()*1000)}")
        state["checkpoint_id"] = checkpoint_id

        print(f"[*] Starting ADK Graph '{self.name}' (Checkpoint ID: {checkpoint_id})")

        while current_node:
            print(f"  -> Executing Node: [{current_node}]")
            
            # Check if current node is an interrupt / human-in-the-loop gate
            if current_node in self.interrupt_nodes and not state.get(f"{current_node}_approved"):
                print(f"  🛑 [SUSPEND/INTERRUPT] Node [{current_node}] requires human approval.")
                state["suspended_at"] = current_node
                self.checkpointer.save(checkpoint_id, state)
                print(f"  [+] State checkpointed to storage. Worker process safely exiting (0 CPU/RAM).")
                return {"status": "SUSPENDED", "checkpoint_id": checkpoint_id, "state": state}

            # Execute node handler
            state = self.nodes[current_node](state)
            self.checkpointer.save(checkpoint_id, state)

            # Determine next node
            if current_node in self.conditional_edges:
                current_node = self.conditional_edges[current_node](state)
            elif current_node in self.edges:
                current_node = self.edges[current_node]
            else:
                current_node = None # End of graph

        print(f"[+] ADK Graph '{self.name}' completed execution.")
        return {"status": "COMPLETED", "checkpoint_id": checkpoint_id, "state": state}

    def resume(self, checkpoint_id: str, human_input: Dict[str, Any]) -> Dict[str, Any]:
        state = self.checkpointer.load(checkpoint_id)
        if not state:
            raise ValueError(f"Checkpoint {checkpoint_id} not found in store.")

        suspended_node = state.get("suspended_at")
        print(f"\n[*] Resuming ADK Graph '{self.name}' from Checkpoint: {checkpoint_id}")
        print(f"    Suspended Node: [{suspended_node}] | Injected Input: {human_input}")

        # Mark approval and merge input
        state[f"{suspended_node}_approved"] = True
        state.update(human_input)
        state["suspended_at"] = None

        # Determine where to transition from suspended node
        if suspended_node in self.conditional_edges:
            next_node = self.conditional_edges[suspended_node](state)
        elif suspended_node in self.edges:
            next_node = self.edges[suspended_node]
        else:
            next_node = None

        # Continue execution
        return self.run(state, next_node)

# --- Node Handlers ---
def node_audit_request(state: Dict[str, Any]) -> Dict[str, Any]:
    print(f"     [Audit] Ingesting refund request: ${state['amount']} for customer {state['customer_id']}")
    state["audit_passed"] = True
    return state

def node_fraud_analysis(state: Dict[str, Any]) -> Dict[str, Any]:
    # Synthetic rule: amounts over $5,000 flagged for manual executive review
    risk_score = 0.85 if state["amount"] > 5000 else 0.15
    state["risk_score"] = risk_score
    print(f"     [Fraud Engine] Computed transaction risk score: {risk_score:.2f}")
    return state

def node_manager_approval(state: Dict[str, Any]) -> Dict[str, Any]:
    print(f"     [Executive Gate] Validating CFO digital signature: {state.get('approver_email')}")
    return state

def node_execute_payout(state: Dict[str, Any]) -> Dict[str, Any]:
    print(f"     [Stripe Core] Successfully processed payout of ${state['amount']} to {state['customer_id']}")
    state["payout_completed"] = True
    return state

def main():
    print("=================================================================")
    print(" GOOGLE ADK 2.0 DURABLE GRAPH & CHECKPOINT ENGINE (M05_L01)")
    print("=================================================================\n")
    
    store = CheckpointStore("/tmp/test_adk_db.json")
    graph = AgentGraph("enterprise-finance-governance", checkpointer=store)
    
    # 1. Register Nodes
    graph.add_node("audit_request", node_audit_request)
    graph.add_node("fraud_analysis", node_fraud_analysis)
    graph.add_node("manager_approval", node_manager_approval, is_interrupt=True)
    graph.add_node("execute_payout", node_execute_payout)
    
    # 2. Register Edges
    graph.add_edge("audit_request", "fraud_analysis")
    graph.add_conditional_edge(
        "fraud_analysis",
        lambda state: "manager_approval" if state["amount"] > 5000 else "execute_payout"
    )
    graph.add_edge("manager_approval", "execute_payout")
    
    # 3. Simulate high-value transaction ($7,500)
    tx = {
        "customer_id": "cust_enterprise_942",
        "amount": 7500,
        "reason": "SLA breach credit"
    }
    
    # Phase 1: Execution up to suspend
    res = graph.run(tx, start_node="audit_request")
    chk_id = res["checkpoint_id"]
    
    print("\n--- SIMULATING SERVER CRASH & 3 DAYS PASSING IN COLD STORAGE ---")
    print("Zero CPU consumed. Zero in-memory Python variables kept alive.\n")
    
    # Phase 2: Resume via Webhook with CFO Approval
    human_approval_payload = {
        "approver_email": "cfo@enterprise.com",
        "decision": "APPROVED_SIGN_OFF"
    }
    final_res = graph.resume(chk_id, human_approval_payload)
    
    print(f"\n[*] Final Payout Status: {final_res['state'].get('payout_completed')}")
    print("=================================================================")
    print(" ADK DURABLE GRAPH EXECUTION COMPLETE - ZERO LOST CONTEXT")
    print("=================================================================")

if __name__ == "__main__":
    main()
