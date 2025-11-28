# SBOM Guidance for Layer S

SBOMs provide a machine-verifiable inventory of all software used by agentic components.  
They are mandatory inputs to supply-chain risk management and version attestation.

## SBOM Requirements
- MUST cover agent runtimes, planners, tool adapters, and dependencies  
- MUST include transitive dependency graph  
- SHOULD be generated on every CI build  
- MUST be stored in:  
  `artifacts/sbom/<build_id>.json`

## Recommended Tools
- **Syft** (standard, fast, widely adopted)  
- **Trivy** (SBOM + vulnerability scan)  
- **Azure DevOps SBOM task**  

## Failure Conditions
CI SHOULD fail when:
- SBOM is missing  
- SBOM cannot be parsed  
- SBOM does not match dependency lockfile  

SBOMs feed Layer S → Layer 5 (policy engine) → Layer 7 (monitoring).
