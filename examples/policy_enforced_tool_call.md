# Policy-Enforced Tool Call Example

Demonstrates a simple "allow/deny" tool call checked at Layer 5.

## Tool Call

{
"tool_name": "web_search",
"arguments": { "query": "confidential_sales_data" }
}

## Policy Evaluation (Layer 5)
- Rule: "Deny search queries containing sensitive terms."
- Result: ❌ Denied

## Sandbox (Layer 6)
- No execution occurs.

## Monitoring (Layer 7)
Log entry:

{
"tool": "web_search",
"allowed": false,
"reason": "Sensitive keyword",
"timestamp": "2025-01-10T10:24:18Z"
}


