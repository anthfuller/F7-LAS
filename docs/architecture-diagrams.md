# F7-LAS Architecture Diagrams

These diagrams describe the F7-LAS responsibility model and governed execution
flow. They are architecture views, not evidence that every depicted control is
implemented by this repository. The only executable path currently supported
is the bounded synthetic workflow documented under
[`examples/canonical-workflow/`](../examples/canonical-workflow/README.md).

## Executive control loop

![F7-LAS executive control loop for agentic systems](images/F7-LAS-Executive-Control-Loop.png)

This view summarizes the governance path for an executive audience: mission
context, an action proposal, policy decision, conditional human approval,
scoped execution, validation, monitoring, and governed feedback.

## Layer-specific execution control loop

![F7-LAS agentic execution control loop](images/F7-LAS-Agentic-Execution-Control-Loop.png)

This view maps the same control loop to F7-LAS Layers 1–7. Layer numbers name
responsibility domains; they do not require every runtime event to occur in
numeric order. In particular, Layer 4 first defines a proposed tool action as
data before Layer 5 authorization. Actual Layer 4 tool access may occur only
after permit, through an enforcement point and within the applicable Layer 6
execution boundary.

## Canonical implementation alignment

| Diagram concept | Canonical repository behavior |
|---|---|
| Mission request and context | `request` and `context` records establish the fixed mission, actor, evidence, and lab scope. |
| Reasoning and action proposal | A deterministic `plan` produces one `proposed_action`; the proposal has no authority to execute. No LLM or private chain-of-thought is used or recorded. |
| Policy decision point | OPA evaluates the complete action, scope, approval binding, execution time, and policy-bundle digest, then permits or denies fail closed. |
| Conditional human approval | The canonical fixture creates deterministic synthetic approval evidence before the `policy_decision` record. It demonstrates binding and expiry enforcement, not an interactive approval service or verified human identity. |
| Scoped execution and tool access | The permit path invokes one registered, synthetic, read-only in-process executor. It makes no network or external API call and independently rechecks the action, approval, decision, scope, policy, obligations, and expiry. |
| Validation, monitoring, and evaluation | `execution_result` and `audit_event` records preserve the outcome; evidence verification and deterministic replay check their correlations and digests. This is not production telemetry or continuous monitoring. |
| Feedback and continuous assurance | Test, review, policy, prompt, and process changes use the normal governed repository workflow. The implementation does not self-modify. |

The permit flow is therefore:

1. admit a request and context;
2. create a bounded plan and proposed Layer 4 action;
3. bind any required approval to the exact request, action, scope, policy, authority, and validity window;
4. obtain a Layer 5 decision;
5. on permit only, revalidate at the Layer 6 executor and perform the registered synthetic action;
6. emit correlated Layer 7 result and audit evidence.

A denial or invalid prerequisite stops before execution and still preserves
canonical evidence when admission succeeded.

## Assurance boundary

The diagrams express the intended F7-LAS control architecture. In this
repository, Layer 6 is a synthetic in-process executor—not an OS/container
sandbox, network-isolation boundary, or production least-privilege runtime.
The repository does not provide production integrations, autonomous response,
live human approval, external identity proofing, or a deployed monitoring
system. See [QA and current maturity](F7-LAS-QA.md) for the complete boundary.

## Asset integrity and attribution

Both diagrams are authored F7-LAS content by Anthony L. Fuller and are covered
by [CC BY 4.0](../LICENSE-CONTENT.md). Copyright licensing does not grant
F7-LAS trademark rights or imply endorsement.

| File | Dimensions | SHA-256 |
|---|---:|---|
| `images/F7-LAS-Executive-Control-Loop.png` | 1672 × 941 | `e56b99d3811ca36e2c2fa0a3f1ef09ba21297845dc86bc2d4f9d2922596dc252` |
| `images/F7-LAS-Agentic-Execution-Control-Loop.png` | 1672 × 941 | `dd93d67596ef99dc86179097b817735ca4fca9539e47f64b35e378ba9162c480` |

Legacy draft graphics were removed from the current documentation set because
they contained ambiguous execution routing, private-reasoning terminology, or
unsupported active-remediation claims. The immutable whitepaper PDF was not
modified.
