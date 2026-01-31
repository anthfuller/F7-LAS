from src.policy import PolicyEnforcementPoint
from src.policy.pep_opa import OPAPolicyEngine


def test_policy_pep_instantiation():
    """
    Ensures the Policy Enforcement Point can be instantiated
    with the existing OPA policy engine.
    """
    engine = OPAPolicyEngine(
        policy_path="config/policies/15/opa/agent_security_enforcement.rego"
    )
    pep = PolicyEnforcementPoint(policy_engine=engine)

    assert pep is not None