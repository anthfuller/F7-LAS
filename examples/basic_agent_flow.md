# Basic Agent Flow Example (F7-LAS Aligned)

This is a minimal conceptual example showing how an agent would flow through  
Layers 1–7 in the F7-LAS model.

## Goal
"Summarize a PDF using an external tool."

## Flow
1. **Layer 1 — System Prompt**
   - Defines role, constraints, tone.
   - Example: "You are a constrained assistant. Only use approved tools."

2. **Layer 2 — RAG/Grounding**
   - Retrieves metadata from the PDF index to avoid hallucination.

3. **Layer 3 — Planner/Controller**
   - Decides: “Use `pdf_reader` tool → summarize → return output.”

4. **Layer 4 — Tools & Integrations**
   - Executes: `pdf_reader(filepath="report.pdf")`.

5. **Layer 5 — Policy Engine**
   - Approves tool call based on rules:
     - File type is approved
     - Path is within allowed sandbox scope

6. **Layer 6 — Sandbox**
   - Tool runs in restricted container.

7. **Layer 7 — Monitoring**
   - Logs:
     - tool name
     - argument hash
     - timestamp
     - policy decision
     - sandbox outcome

## Output
A grounded, policy-approved summary of the document.
