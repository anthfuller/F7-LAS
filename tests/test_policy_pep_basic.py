from src.policy.pep_opa import OPAPEP


def test_opa_pep_instantiation():
    pep = OPAPEP()
    assert pep is not None
