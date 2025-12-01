# Layer 1 — System Prompt (Soft Policy)

Layer 1 defines the **initial agent intent and scope** using system prompts.

These prompts do **not** enforce security.  
They are *soft policies* — easily bypassed — but essential for defining each agent persona.

## Included Prompts

### `investigator_prompt.txt`
Read-only analysis role. No write actions allowed.

### `coordinator_prompt.txt`
Manages task flow and escalations between agents.

### `remediator_prompt.txt`
Authorized to take corrective actions, subject to Layer 5 policy approval.

## Purpose

These prompts demonstrate how F7-LAS begins with **intent shaping**, but does not rely on it for security.  
Actual enforcement occurs in **Layer 5 (PDP/PEP)**.
