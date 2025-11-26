# Example: Simple RAG-Governed Query with F7-LAS

This example shows how F7-LAS artifacts (prompts, policies, and settings) can be
used to **govern a simple RAG-style query**, even before a full demo runner is built.

> This is a *conceptual* example for Stage 0 — it describes how to use the repo,
> not a ready-made application.

---

## 1. Prepare the Environment

```bash
git clone https://github.com/anthfuller/F7-LAS.git
cd F7-LAS

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
