# Tool & Plugin Vetting Workflow (Layer S)

This workflow ensures any tool exposed to the planner or agents is vetted before use.

## Step 1 — Submission
Developer provides:
- Tool ID  
- Description  
- Owner  
- Required permissions  
- Risk tier request  
- Version range  
- Integration notes  

## Step 2 — Security Review
Security engineering validates:
- Risk tier  
- Credential model  
- Identity mapping  
- Attack surface review  
- Input/output schemas  

## Step 3 — Least-Privilege Check
- Verify the tool operates with minimal required permissions  
- Confirm destructive actions require HITL (Tier-3)

## Step 4 — Approvals & Registration
Approved tools are added to:
