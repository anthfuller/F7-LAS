# Supplemental Layer S — Software Supply-Chain Security  
_F7-LAS Implementation Guide — Layer S Documentation_

Layer S provides the software integrity foundation that all other F7-LAS layers depend on.  
It applies horizontally across Layers 1–7 and governs SBOM generation, dependency integrity,
plugin/tool vetting, runtime attestation, and supply-chain policy enforcement.

This folder contains reference material, schemas, and engineering checklists that support
implementation of Layer S.

---

## Folder Contents

### **1. `checklist.md`**
A concise, engineer-friendly checklist summarizing the required controls for Layer S:
- SBOM requirements  
- SCA gating  
- Tool/plugin vetting  
- Runtime attestation  
- Dependency integrity rules  
- CI/CD enforcement guidance  

Use this file for day-to-day engineering validation and CI hardening.

---

### **2. `sbom-guidance.md`**
Implementation guidance for producing and storing SBOMs:
- Recommended tools (Syft, Trivy, Azure DevOps tasks)  
- Required SBOM fields  
- Storage conventions  
- Release-time SBOM artifacts  
- CI enforcement patterns  

---

### **3. `vetting-workflow.md`**
Defines the workflow for vetting tools/plugins before being exposed to the agent planner:
- Security review steps  
- Risk tiering (Tier 1–3)  
- Required metadata fields  
- Credential & permission checks  
- Approval and documentation process  

This workflow ensures that all agent-accessible tools follow least privilege and meet baseline security expectations.

---

### **4. `allowlist-schema.json`**
A JSON Schema describing the structure of a valid F7-LAS tool allowlist.  
This schema supports:
- Validation in CI  
- Consistent formatting  
- Safety checking of tool metadata  
- Enforcing risk tiers and required fields  

The schema is referenced by the `allowlist-validator.py` script located in `/scripts/`.

---

## Runtime Allowlist (Not in this folder)

The **actual** allowlist used by agents lives here:

`/config/tools/allowlist.json`

This folder (`layer-s/`) only contains documentation, schemas, and guidance — **not** the operational allowlist used at runtime.


