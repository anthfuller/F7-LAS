# Layer S — Software Supply-Chain Security Checklist
Version 0.1 • Engineer-Facing • Applies Across Layers 1–7

Layer S ensures all agentic components run on trusted, verified, and attested software.  
Use this checklist during implementation, PR review, and release preparation.

---

## S-01 — SBOM Generation
- [ ] SBOM generated for agent runtime and tool adapters  
- [ ] Includes transitive dependencies  
- [ ] Saved to CI artifacts  
- [ ] Build fails if SBOM missing  
- [ ] SBOM attached to releases  

Tools: Syft, Trivy, Azure DevOps SBOM task

---

## S-02 — Dependency Vulnerability Screening (SCA)
- [ ] All dependencies scanned for CVEs  
- [ ] CI fails on high/critical issues  
- [ ] Exceptions documented and approved  
- [ ] Auto dependency PRs (Dependabot/Renovate) enabled  

Tools: Trivy, GitHub Advanced Security, OWASP Dependency-Check

---

## S-03 — Tool / Plugin Vetting
- [ ] All tools included in `config/tools/allowlist.json`  
- [ ] Owner & risk tier assigned  
- [ ] Least-privilege review complete  
- [ ] Identity/credential verification done  
- [ ] Deprecated tools marked  
- [ ] Last-reviewed date assigned  

---

## S-04 — Runtime Attestation
- [ ] Runtime emits:  
  - `framework_version`  
  - `sbom_id`  
  - `toolset_hash`  
  - Build/commit identifiers  
- [ ] Telemetry includes attestation fields in:  
  - `policy_decision`  
  - `tool_call`  
  - `sandbox_lifecycle`  
- [ ] Policy engine can block unknown/mismatched builds  

---

## S-05 — Supply Chain Enforcement in CI/CD
- [ ] Dependency pinning (lockfiles)  
- [ ] Hash integrity verification  
- [ ] PR review for dependency changes  
- [ ] CI includes SBOM + SCA + validation  
- [ ] Builds blocked on unvetted tools  

---

## Evidence Required
- [ ] SBOM artifacts  
- [ ] SCA reports  
- [ ] CI logs showing failed/blocked builds  
- [ ] Tool vetting approvals  
- [ ] Attestation telemetry samples  
- [ ] Dependency lockfiles  

---

## Relationship to F7-LAS Layers
Layer S reinforces:

- L1–L3: Agents run on trusted runtime code  
- L4: Tools are vetted and least-privileged  
- L5: Policy engine uses attestation signals  
- L6: Sandboxes run verified images  
- L7: Monitoring includes integrity signals  

Layer S is the **integrity substrate** for all layers.
