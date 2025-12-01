# Layer 3 — Planner (Reasoning & Control Logic)

Layer 3 converts natural-language input into a structured **tool call**.

This example includes a minimal deterministic planner that:
- inspects user input  
- selects an allowed tool  
- produces `{ tool_name, action, arguments }`

## File

### `simple_planner.py`
A tiny stub demonstrating:
- intent parsing  
- defaulting to read-only actions  
- proposing high-risk actions (e.g., terminate_instance) that must pass Layer 5

## Purpose

Layer 3 shapes *what the agent wants to do* —  
but **Layer 5 determines whether it is allowed**.
