# 3. Supplemental Layer S — Software Supply-Chain Security

Layer S provides supply-chain integrity across all layers.

## Control Requirements
- SBOM generation for all agent runtimes.
- SCA gating in CI.
- Plugin/tool vetting pipeline.
- Runtime attestation: model_version, sbom_id, toolset_hash.

## Implementation Actions
- Generate SBOMs with Syft or Azure DevOps tasks.
- Use Dependabot + SCA scanning.
- Maintain a vetted tool registry in `config/tools/allowlist.json`.
