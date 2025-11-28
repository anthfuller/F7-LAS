# 3. Supplemental Layer S — Software Supply-Chain Security  
*(F7-LAS Implementation Guide Version)*

Layer S provides the **software integrity foundation** on which all F7-LAS layers operate.  
It applies horizontally across **Layers 1–7**, ensuring that prompts, grounding components, planners, tools, policy engines, and sandboxes all run on **trusted, verified, and attested** software components.

---

## 3.1 Control Requirements

### **S-01 — SBOM Generation**
All agent runtimes, tool adapters, and support libraries **MUST** produce an SBOM.
- Include transitive dependencies  
- Store SBOM artifacts in CI and attach to releases  
- Fail builds missing SBOM output  

---

### **S-02 — Dependency Vulnerability Screening (SCA)**
All dependencies **MUST** be scanned for known vulnerabilities.
- CI **MUST** block builds on high/critical vulnerabilities  
- Exceptions require documented risk acceptance  

---

### **S-03 — Tool / Plugin Vetting Pipeline**
Any tool or plugin exposed to agents **MUST** pass a vetting workflow:
- Security review  
- Least-privilege permission check  
- Identity/credential verification  
- Assignment of risk tier (Tier 1–3)  

---

### **S-04 — Runtime Attestation**
Agent components SHOULD emit attestation metadata, including:
- `framework_version`  
- `sbom_id`  
- `toolset_hash`  
- Build/commit identifiers  

These attestation values feed into:
- **Layer 7** — Monitoring & Detection  
- **Layer 5** — Policy Engine checks (e.g., block outdated or unverified toolsets)  

---

### **S-05 — Supply-Chain Policy Enforcement**
CI/CD pipelines **MUST** enforce:
- Frozen dependency versions (pinning / lockfiles)  
- Integrity verification (hash checking)  
- Controlled update workflows (PR review, signed commits, traceability)  

---

## 3.2 Implementation Actions

### **SBOM Generation**
- Use **Syft**, **Trivy**, or Azure DevOps SBOM tasks  
- Save SBOM artifacts under:  
  `artifacts/sbom/<build_id>.json`

---

### **SCA + Gating**
- Enable **Dependabot** or **Renovate** for dependency updates  
- Add CI jobs using **Trivy**, **GitHub Advanced Security**, or **OWASP Dependency-Check**  
- Block builds on critical findings  

---

### **Tool Registry Management**
Maintain a vetted allowlist at:  
`config/tools/allowlist.json`

Include fields:
- `id`  
- `owner`  
- `risk_tier`  
- `permissions`  
- `version`  
- `last_reviewed`  

---

### **Attestation Telemetry**
- Emit attestation fields as part of `policy_decision` and `sandbox_lifecycle` events  
- Use policy to block unknown or unverified toolsets  

---

## 3.3 Evidence Required

To demonstrate compliance with Layer S:
- SBOM artifacts per release  
- SCA reports showing passing/blocked builds  
- Tool vetting records & approvals  
- Attestation telemetry samples  
- CI pipeline logs showing enforcement  
- Dependency lockfiles  

---

## 3.4 Relationship to the Core F7-LAS Model

Layer S does **not** modify Layers 1–7.  
Instead, it reinforces them by ensuring:

- **Layers 1–3** operate on trusted components  
- **Layer 4** tools are vetted and least-privileged  
- **Layer 5** policies can evaluate version/attestation signals  
- **Layer 6** sandboxes run verified runtimes  
- **Layer 7** has integrity evidence for detection & auditing  

**Layer S is the integrity floor that supports all other layers.**
