"""
Stage 2 F7-LAS – Local Validation Entry Point
Runs the full multi-agent flow end-to-end.
"""

from orchestrator.orchestrator import Orchestrator


def main():
    orchestrator = Orchestrator()

    test_request = (
        "Suspicious sign-in activity detected for user jdoe. "
        "Investigate and propose appropriate remediation."
    )

    result = orchestrator.run(test_request)

    print("\n=== FINAL RESULT ===")
    print(result)


if __name__ == "__main__":
    main()
