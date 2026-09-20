#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python_bin="${PYTHON_BIN:-python}"
opa_candidate="${OPA_BIN:-opa}"
expected_python="3.12.14"
expected_opa="1.20.2"
expected_opa_sha256="69da5179ee403d10fa11bab6cfb4ffb0d23dba5f9b682fa977db772a1da5670f"

fail() {
  echo "clean-user acceptance failed: $*" >&2
  exit 1
}

command -v "$python_bin" >/dev/null 2>&1 || fail "Python executable not found: $python_bin"
opa_bin="$(command -v "$opa_candidate" 2>/dev/null || true)"
[[ -n "$opa_bin" ]] || fail "OPA executable not found: $opa_candidate"
opa_bin="$(cd "$(dirname "$opa_bin")" && pwd)/$(basename "$opa_bin")"

python_version="$($python_bin -c 'import platform; print(platform.python_version())')"
[[ "$python_version" == "$expected_python" ]] || \
  fail "Python $expected_python is required; found $python_version"

opa_version="$($opa_bin version | awk '/^Version:/ {print $2; exit}')"
[[ "$opa_version" == "$expected_opa" ]] || \
  fail "OPA $expected_opa is required; found ${opa_version:-unknown}"

opa_sha256="$($python_bin -c 'import hashlib, pathlib, sys; print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())' "$opa_bin")"
[[ "$opa_sha256" == "$expected_opa_sha256" ]] || \
  fail "OPA binary digest does not match the reviewed Linux x86_64 static binary"

acceptance_root="$(mktemp -d "${TMPDIR:-/tmp}/f7las-clean-user.XXXXXX")"
if [[ "${KEEP_CLEAN_USER_WORKDIR:-0}" != "1" ]]; then
  trap 'rm -rf "$acceptance_root"' EXIT
else
  echo "Retaining clean-user workspace: $acceptance_root"
fi

checkout="$acceptance_root/F7-LAS"
venv="$acceptance_root/venv"
mkdir -p "$checkout"

tar \
  --exclude='./.git' \
  --exclude='./.venv' \
  --exclude='./.pytest_cache' \
  --exclude='*/__pycache__' \
  -cf - -C "$repo_root" . | tar -xf - -C "$checkout"

cd "$checkout"
unset PYTHONPATH

echo "[clean-user] Create isolated Python environment"
"$python_bin" -m venv "$venv"
python="$venv/bin/python"
pip_audit="$venv/bin/pip-audit"

echo "[clean-user] Install the hash-locked dependency graph"
"$python" -m pip install --require-hashes -r requirements-ci.lock

echo "[clean-user] Validate documentation and repository invariants"
"$python" scripts/validate-documentation.py
"$python" scripts/validate-supply-chain.py
"$python" scripts/validate-prompts.py config/prompts
"$python" scripts/validate-policies.py
"$python" scripts/allowlist-validator.py
"$python" scripts/validate-settings.py config/settings.yaml
"$python" scripts/validate-contracts.py
"$opa_bin" check --strict config/policies/canonical-workflow.rego

echo "[clean-user] Run the complete automated test suite"
OPA_BIN="$opa_bin" "$python" -m pytest -q

evidence="$acceptance_root/canonical-evidence.json"
replayed="$acceptance_root/replayed-evidence.json"
golden="$acceptance_root/golden-results.json"
sbom="$acceptance_root/f7las-python.cdx.json"

echo "[clean-user] Execute, verify, and replay the canonical walkthrough"
"$python" -m src.canonical.cli \
  --input examples/canonical-workflow/request.json \
  --output "$evidence" \
  --opa-binary "$opa_bin"
"$python" -m src.canonical.evidence --evidence "$evidence"
"$python" -m src.canonical.replay \
  --input examples/canonical-workflow/request.json \
  --evidence "$evidence" \
  --output "$replayed" \
  --opa-binary "$opa_bin"

echo "[clean-user] Run and enforce the golden structural evaluation"
"$python" -m src.demo_runner.run_golden_dataset \
  --scenarios tests/golden_dataset/scenarios.json \
  --rubric tests/golden_dataset/rubric.json \
  --output "$golden" \
  --strict
"$python" scripts/check_golden_thresholds.py "$golden"

echo "[clean-user] Audit the locked graph and generate a CycloneDX SBOM"
"$pip_audit" \
  --require-hashes \
  --disable-pip \
  --strict \
  --progress-spinner off \
  --requirement requirements-ci.lock \
  --format cyclonedx-json \
  --output "$sbom"
test -s "$sbom" || fail "CycloneDX SBOM was not generated"

echo "Clean-user acceptance PASSED: Python $python_version, OPA $opa_version."
