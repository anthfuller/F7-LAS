from src.policy.pep_opa import OPAPolicyEngine


def test_opa_policy_engine_instantiation():
    """
    Ensures the OPA policy engine can be instantiated
    with the existing Rego policy file.
    """
    engine = OPAPolicyEngine(
        policy_path="config/policies/15/opa/agent_security_enforcement.rego"
    )

    assert engine is not None
