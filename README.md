
# F7-LAS™ — Fuller 7-Layer Agentic AI Security Framework

*A layered, control-centric security architecture for agentic and multi-agent AI systems.*

[![F7-LAS CI](https://img.shields.io/badge/F7--LAS_CI-passing-brightgreen)](#)
[![Status](https://img.shields.io/badge/status-passing-brightgreen)](#)
[![Version](https://img.shields.io/badge/version-v3.1-blue)](#)
[![License](https://img.shields.io/badge/license-Proprietary-lightgrey)](#license--disclaimer)
[![Maturity](https://img.shields.io/badge/maturity-Stage%200%20%E2%80%94%20Experimental-yellow)](#maturity-roadmap)

---

## 🌐 Overview

**F7-LAS™** (Fuller 7-Layer Agentic AI Security Framework) defines a layered control model for securing AI agents that can plan, reason, call tools, modify systems, and interact with enterprise environments.

It provides:

- ✅ A 7-layer control stack (L1–L7)
- 🔐 Prompt, tool, policy, and execution-level safeguards
- 📊 CI pipeline and golden dataset evaluation
- 🧩 Modular implementation guide, engineering checklists, and playbooks
- 🏗️ Vendor-neutral design

---

## What F7-LAS™ Solves

Modern AI agents are powerful — but risky. They can access tools, plan autonomously, and act in ways that pose enterprise threats.

**F7-LAS™** addresses:
- Tool misuse and overreach
- Unchecked reasoning loops
- Prompt injection and data leakage
- Missing auditability, drift, or policy compliance

This repo proves that securing agentic systems is possible *by design*.

---

## 📐 Architecture

![Multi-Agent F7-LAS Architecture](docs/Multi-Agent-F7-LAS_Architecture.png)

---

## 🚀 Quickstart

```bash
git clone https://github.com/<your-org>/F7-LAS.git
cd F7-LAS

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run tests:

```bash
pytest -q tests/test_agents_basic.py
```

Run the golden evaluator:

```bash
python scripts/check_golden_thresholds.py tests/golden_dataset/golden_eval_results.json
```

---

## 🧪 Maturity Roadmap

| Stage | Label         | Description                                      | Use Readiness             |
|-------|---------------|--------------------------------------------------|----------------------------|
| 0     | Experimental  | Design, scaffolding, early controls and docs.   | Evaluation, learning, PoC  |
| 1     | Alpha         | Core logic working end-to-end with gaps.        | Internal sandbox only      |
| 2     | Beta          | CI + tests in place, coverage improving.        | Controlled pilot / lab     |
| 3     | Stable        | Versioned, test-covered, documented patterns.   | Production-ready           |

Current Stage: **Stage 0 — Experimental**

---

## 🧪 Try It / Demo

Basic placeholder CI is in place. Try the system prompt evaluator:

```bash
python scripts/validate-prompts.py
```

More scenarios and golden dataset examples will be added in future stages.

---

## 📂 Repository Structure

```
F7-LAS/
├── .github/workflows/f7las-ci.yml
├── config/
│   ├── prompts/
│   ├── policies/
│   └── settings.yaml
├── docs/
│   ├── Security-Agentic-AI-The-7-Layer-Model-v2.4.pdf
│   └── F7-LAS-Implementation-Guide-v3.1/
├── scripts/
├── src/
│   └── demo-runner/
├── tests/
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! This is an evolving framework.

To contribute:
- Follow the [Engineering Review Checklist](docs/Engineering-Review-Checklist.md)
- Align with prompt security structure
- Respect repo CI and formatting

---

## 📄 License & Disclaimer

© 2025 Anthony L. Fuller. All rights reserved.  
**F7-LAS™** is a trademark of Anthony L. Fuller. *Trademark application pending.*

> This project was created independently by the author and is **not affiliated with, endorsed by, or associated with Microsoft or any other employer**. All opinions, design patterns, and documentation reflect the author's personal work.

---

## 🔖 GitHub Tags (suggested)

`#agentic-ai` `#ai-security` `#prompt-security` `#governance` `#open-security`

---

## ⭐ Support the Project

If this work helps you explore safer AI architectures — **star the repo** to show your support.
