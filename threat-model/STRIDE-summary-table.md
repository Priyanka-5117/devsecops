# STRIDE Analysis — Quick Reference Table

## Complete Threat Matrix

| # | Stage | STRIDE | Threat Description | Severity | Tool | Gate Status |
|---|-------|--------|--------------------|----------|------|-------------|
| 1 | Source Repo | I | Hardcoded API secret in app.py | 🔴 CRITICAL | Gitleaks | FAIL ❌ |
| 2 | Source Repo | I | Hardcoded DB password in app.py | 🔴 CRITICAL | Gitleaks | FAIL ❌ |
| 3 | Source Repo | S | Unauthorized code push | 🟠 HIGH | Branch Rules | WARN ⚠️ |
| 4 | Build System | T | SQL Injection vulnerability | 🔴 CRITICAL | Semgrep | FAIL ❌ |
| 5 | Build System | T | Debug mode in production | 🟠 HIGH | Semgrep | FAIL ❌ |
| 6 | Build System | I | Host binding 0.0.0.0 | 🟠 HIGH | Semgrep | WARN ⚠️ |
| 7 | Dependencies | T | PyYAML 5.3.1 CVSS 9.8 | 🔴 CRITICAL | OSV-Scanner | FAIL ❌ |
| 8 | Dependencies | T | Jinja2 3.0.1 CVSS 8.8 | 🔴 CRITICAL | OSV-Scanner | FAIL ❌ |
| 9 | Dependencies | T | Flask 2.0.1 CVSS 8.7 | 🟠 HIGH | OSV-Scanner | FAIL ❌ |
| 10 | Dependencies | T | Werkzeug 2.0.1 CVSS 7.5 | 🟠 HIGH | OSV-Scanner | FAIL ❌ |
| 11 | Container | E | Container running as root | 🔴 CRITICAL | Trivy | FAIL ❌ |
| 12 | Container | E | CVEs in python:3.9-slim | 🔴 CRITICAL | Trivy | FAIL ❌ |
| 13 | Artifact | S | Unsigned Docker image | 🟠 HIGH | Cosign | PASS ✅ |
| 14 | Artifact | T | Image tampered after build | 🟠 HIGH | Cosign | PASS ✅ |
| 15 | Runtime | I | Server version leaked in headers | 🟡 MEDIUM | OWASP ZAP | WARN ⚠️ |
| 16 | Runtime | I | Missing security headers | 🟡 MEDIUM | OWASP ZAP | WARN ⚠️ |
| 17 | Runtime | T | Missing CSP header | 🟡 MEDIUM | OWASP ZAP | WARN ⚠️ |
| 18 | Runtime | D | No rate limiting | 🟡 MEDIUM | Manual | ❌ Open |

## Risk Score by Stage

| Stage | Total Threats | Critical | High | Medium | Risk Level |
|-------|--------------|----------|------|--------|------------|
| Source Repo | 3 | 2 | 1 | 0 | 🔴 CRITICAL |
| Build System | 3 | 1 | 2 | 0 | 🔴 CRITICAL |
| Dependencies | 4 | 2 | 2 | 0 | 🔴 CRITICAL |
| Container | 2 | 2 | 0 | 0 | 🔴 CRITICAL |
| Artifact | 2 | 0 | 2 | 0 | ✅ MITIGATED |
| Runtime | 4 | 0 | 0 | 4 | 🟡 MEDIUM |
| **TOTAL** | **18** | **7** | **7** | **4** | **🔴 HIGH** |

