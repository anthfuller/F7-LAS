# Security Policy

## Project scope

F7-LAS is a security reference model with a **prototype reference implementation**. It is not a hosted service or production control plane. No repository artifact is supported for direct production deployment.

Security reports may cover source code, policy examples, schemas, validators, workflows, documentation, dependency configuration, or repository integrity.

## Reporting a vulnerability

Do not disclose a suspected vulnerability in a public issue. Use GitHub's private vulnerability-reporting channel when it is available. If it is unavailable, contact the repository owner privately through the contact method published on the owner's GitHub profile.

Include:

- affected file and revision,
- impact and preconditions,
- minimal reproduction steps using synthetic data,
- suggested mitigation, if known.

Do not test against real third-party systems, accounts, identities, cloud resources, or security platforms.

## Supported claims

Only behavior covered by executable tests and identified evidence may be described as implemented and automatically verified. Illustrative material, manual controls, external dependencies, and planned work must retain those classifications.

## Out of scope

- production deployment support,
- real-world attack or remediation execution,
- third-party platform vulnerabilities,
- claims that example prompts, containers, or policies provide hardened isolation or complete enforcement.
