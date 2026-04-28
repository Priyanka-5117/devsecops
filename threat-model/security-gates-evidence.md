# Security Gates — Pass/Fail Evidence

## What is a Security Gate?
A security gate is a checkpoint in the pipeline that
STOPS deployment if a security threshold is exceeded.

---

## Gate 1 — Secret Detection (Gitleaks)
Threshold : ANY secret found = FAIL
Tool      : Gitleaks v8.18.2
Evidence  : reports/gitleaks-before.json
Finding:
File    : src/app.py
Line    : 6
Secret  : SECRET_KEY = "super_secret_key_12345"
Rule    : generic-api-key
GATE RESULT: ❌ FAIL — Secret detected in source code
ACTION     : Pipeline should stop here
---

## Gate 2 — SAST (Semgrep)
Threshold : Any ERROR severity = FAIL
Tool      : Semgrep
Evidence  : reports/semgrep-before.json
Findings  : 7 total

SQL Injection     (ERROR)    → FAIL
Debug mode ON     (WARNING)  → WARN
Hardcoded secret  (ERROR)    → FAIL
Host 0.0.0.0      (WARNING)  → WARN

GATE RESULT: ❌ FAIL — Critical code vulnerabilities found
ACTION     : Developer must fix before proceeding
---

## Gate 3 — SCA (OSV-Scanner)
Threshold : CVSS >= 9.0 = FAIL
Tool      : OSV-Scanner
Evidence  : reports/osv-scanner-before.json
Critical Finding:
Package : pyyaml 5.3.1
CVE     : PYSEC-2021-142
CVSS    : 9.8 ← CRITICAL!
Issue   : Arbitrary code execution
Total CVEs: 28 across 5 packages
GATE RESULT: ❌ FAIL — Critical CVE in dependencies
ACTION     : Update pyyaml to latest version
---

## Gate 4 — Container Scan (Trivy)
Threshold : CRITICAL CVE = FAIL
Tool      : Trivy
Evidence  : reports/trivy-before.json
Findings:
Critical CVEs : Multiple in python:3.9-slim
Running as    : root (misconfiguration)
Base image    : Outdated with known CVEs
GATE RESULT: ❌ FAIL — Critical CVEs in container
ACTION     : Update base image, add non-root user
---

## Gate 5 — Artifact Signing (Cosign)
Threshold : Unsigned image = FAIL
Tool      : Cosign
Evidence  : reports/cosign-evidence.txt
reports/devsecops-app.sig
Result:
Image signed    : YES ✅
Signature file  : devsecops-app.sig
Verified        : YES ✅
GATE RESULT: ✅ PASS — Image is signed and verified
ACTION     : Proceed to deployment
---

## Gate 6 — DAST (OWASP ZAP)
Threshold : HIGH risk finding = FAIL
Tool      : OWASP ZAP
Evidence  : reports/zap-before.html
Findings (6 warnings):
WARN: X-Content-Type-Options Missing
WARN: Server Version Leaked
WARN: CSP Header Not Set
WARN: Storable Cacheable Content
WARN: Permissions Policy Missing
WARN: Cross-Origin-Resource-Policy Missing
GATE RESULT: ⚠️ WARN — Medium findings, no critical
ACTION     : Add missing security headers
---

## Overall Gates Summary

| Gate | Tool | Threshold | Result |
|------|------|-----------|--------|
| 1 | Gitleaks | No secrets | ❌ FAIL |
| 2 | Semgrep | No ERROR findings | ❌ FAIL |
| 3 | OSV-Scanner | No CVSS 9+ | ❌ FAIL |
| 4 | Trivy | No CRITICAL CVEs | ❌ FAIL |
| 5 | Cosign | Must be signed | ✅ PASS |
| 6 | OWASP ZAP | No HIGH findings | ⚠️ WARN |

