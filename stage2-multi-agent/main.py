"""
Stage 2 F7-LAS – Local Validation Entry Point
Runs the full multi-agent flow end-to-end.
"""

from orchestrator.orchestrator import Orchestrator


def main():
    orchestrator = Orchestrator()

    # Neutral trigger — no identities, no assumptions
    test_request = "Run baseline log investigation."

    result = orchestrator.run(test_request)

    print("\n=== FINAL RESULT ===")
    print(result)


if __name__ == "__main__":
    main()
