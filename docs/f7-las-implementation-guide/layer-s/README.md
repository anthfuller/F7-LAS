# Supplemental Layer S — Software Supply-Chain Security

Layer S provides the **software integrity foundation** that all other F7-LAS™ layers depend on.  
It applies **horizontally across Layers 1–7** and governs SBOM generation, dependency integrity, plugin/tool vetting, runtime attestation, and supply-chain policy enforcement.

This folder is part of the **F7-LAS Implementation Guide** and is intended for **security engineers, platform teams, and DevSecOps practitioners**.

---

## Goals of Layer S

Layer S focuses on:

- Ensuring every component (agents, tools, plug-ins, runtimes) has **traceable provenance**
- Enforcing **SBOM generation and validation** as part of CI/CD
- Applying **Software Composition Analysis (SCA)** gates for dependencies
- Vetting and approving **agent-exposed tools and plug-ins**
- Providing **schemas and checklists** that can be integrated into pipelines
- Supporting **runtime integrity** and **policy-based allowlists**

Layer S is not a runtime layer like L3–L7, but a **foundational control plane** that reduces the chance that compromised or unvetted software ever reaches the agent.

---

## Folder Contents

- **checklist.md**  
  A concise, engineer-friendly checklist that summarizes required controls for Layer S, including:
  - SBOM requirements and publication
  - SCA gating for dependencies
  - Tool / plug-in vetting steps
  - Runtime attestation hooks (where applicable)
  - CI/CD enforcement guidance

- **sbom-guidance.md**  
  Guidance for producing, storing, and validating SBOMs:
  - Recommended tools (e.g., Syft, Trivy, Microsoft / cloud-native SBOM tasks)
  - Required SBOM fields and formats
  - Storage conventions (e.g., artifact registries, build logs)
  - Release-time SBOM artifacts
  - Example patterns for failing builds on SBOM/SCA violations

- **vetting-workflow.md**  
  A reference workflow for **vetting tools and plug-ins** before exposing them to the agent planner, including:
  - Security review steps and ownership
  - Risk tiering (Tier 1–3) based on blast radius and privileges
  - Required metadata (owner, purpose, scope, permissions, data access)
  - Credential and permission checks
  - Approval and documentation requirements

- **allowlist-schema.json**  
  A JSON Schema describing the structure of a **valid F7-LAS tool allowlist**, used to:
  - Validate tool metadata in CI
  - Enforce consistent formatting and required fields
  - Capture risk tiers, owners, and permission scopes
  - Prevent unvetted tools from silently entering the agent surface

- **README.md** (this file)  
  High-level overview, context, and how Layer S connects to the rest of F7-LAS.

---

## Relationship to the Runtime Allowlist

The **operational allowlist** used by the agent lives outside this documentation folder:

```text
config/tools/allowlist.json
```

- `layer-s/` → defines **schemas, guidance, and checklists**.
- `config/tools/allowlist.json` → defines the **actual tools** available to the agent at runtime.

The `allowlist-schema.json` in this folder is intended to be referenced by CI scripts (for example, `scripts/validate-policies.py`) to validate that the runtime allowlist conforms to Layer-S requirements.

---

## How Layer S Connects to the 7 Layers

Layer S supports and constrains other layers as follows:

- **Layer 1–2 (Prompts & Grounding)**  
  - Ensures that any system prompts, RAG connectors, and retrieval sources are coming from vetted code paths and maintained packages.

- **Layer 3–4 (Planner & Tools)**  
  - Ensures that planners and tools are built from known-good dependencies with SBOMs and SCA checks.
  - All tools exposed in L4 must appear in the **tool allowlist** validated by Layer S.

- **Layer 5 (Policy Engine)**  
  - Ensures the PDP/PEP stack is built from vetted components and policy bundles with known provenance.

- **Layer 6 (Sandbox)**  
  - Ensures container images, base OS layers, and runtime components are tracked, scanned, and governed via SBOMs and supply-chain policy.

- **Layer 7 (Monitoring)**  
  - Ensures observability agents, log forwarders, and telemetry SDKs are part of the same SBOM + supply-chain controls.

---

## How to Use This Folder

For a Stage-1 / Stage-2 adoption of F7-LAS:

1. **Adopt the checklist**  
   - Use `checklist.md` as a working document in design and security reviews.

2. **Wire SBOM guidance into CI**  
   - Implement the patterns in `sbom-guidance.md` in your build pipelines.

3. **Apply the vetting workflow**  
   - Before adding new tools, follow `vetting-workflow.md` and record approvals.

4. **Validate allowlists in CI**  
   - Use `allowlist-schema.json` with a simple validation script to ensure `config/tools/allowlist.json` remains compliant.

Layer S is designed to be **incrementally adoptable**: you can start with SBOMs and allowlists, then grow into full supply-chain governance across all agent and tool components.
