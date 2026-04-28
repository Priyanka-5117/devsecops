
# STRIDE Threat Model — DevSecOps CI/CD Pipeline

## Project: DevSecOps CI/CD Pipeline Security Assessment
## Date: 2026-04-28
## Author: Security Assessment Team

---

## Pipeline Overview
[Developer] → [GitHub Repo] → [GitHub Actions]
→ [Artifact Registry] → [Staging Server]
→ [Running Application]
---

## Trust Boundaries
TB-1: Developer Machine ←→ GitHub Repository
TB-2: GitHub Repository ←→ GitHub Actions Runner
TB-3: GitHub Actions    ←→ Docker Registry
TB-4: Docker Registry   ←→ Deployment Target
TB-5: Deployment Target ←→ End Users
---

## STAGE 1 — SOURCE REPOSITORY (GitHub)

| STRIDE | Threat | Attack Scenario | Tool Mitigation | Status |
|--------|--------|-----------------|-----------------|--------|
| Spoofing | Attacker pushes code pretending to be developer | Stolen GitHub credentials used to push malicious code | Branch protection rules | ⚠️ Partial |
| Tampering | Source code modified after commit | Man in the middle attack on git push | SSH key authentication | ✅ Mitigated |
| Repudiation | Developer denies pushing malicious code | No audit trail of who changed what | GitHub audit logs | ✅ Mitigated |
| Info Disclosure | Secrets hardcoded in source code | API keys committed accidentally | Gitleaks ✅ | ✅ Mitigated |
| Denial of Service | Repository made unavailable | GitHub DDoS or account suspension | GitHub SLA | ⚠️ Partial |
| Elevation of Privilege | Attacker gains admin access to repo | Social engineering or token theft | MFA on GitHub | ⚠️ Partial |

### Findings at This Stage:
- Gitleaks detected: SECRET_KEY hardcoded in app.py
- Gitleaks detected: DB_PASSWORD hardcoded in app.py
- Risk Level: 🔴 CRITICAL

---

## STAGE 2 — BUILD SYSTEM (GitHub Actions)

| STRIDE | Threat | Attack Scenario | Tool Mitigation | Status |
|--------|--------|-----------------|-----------------|--------|
| Spoofing | Malicious GitHub Action used | Attacker publishes fake action with same name | Pin actions to SHA | ⚠️ Partial |
| Tampering | Build script modified to inject malware | Compromised dependency in pipeline | OSV-Scanner ✅ | ✅ Mitigated |
| Repudiation | No record of what ran in pipeline | Build logs deleted or not retained | GitHub Actions logs | ✅ Mitigated |
| Info Disclosure | Secrets leaked in build logs | Environment variables printed to console | GitHub Secrets masking | ✅ Mitigated |
| Denial of Service | Pipeline flooded with fake PRs | Automated PR spam exhausting runners | Rate limiting | ⚠️ Partial |
| Elevation of Privilege | Build script runs as root | Container escape from runner | Sandboxed runners | ✅ Mitigated |

### Findings at This Stage:
- Semgrep detected: SQL Injection in app.py line 18
- Semgrep detected: Debug mode enabled in production
- Semgrep detected: Hardcoded credentials
- Risk Level: 🔴 CRITICAL

---

## STAGE 3 — ARTIFACT REGISTRY (Docker Images)

| STRIDE | Threat | Attack Scenario | Tool Mitigation | Status |
|--------|--------|-----------------|-----------------|--------|
| Spoofing | Fake image pushed with same name | Attacker replaces legitimate image | Cosign signing ✅ | ✅ Mitigated |
| Tampering | Image modified after build | Layer injection attack | Cosign verification ✅ | ✅ Mitigated |
| Repudiation | No record of who pushed image | Unsigned image deployed | Cosign audit trail ✅ | ✅ Mitigated |
| Info Disclosure | Sensitive data baked into image | Secrets in environment variables | Trivy secret scan ✅ | ✅ Mitigated |
| Denial of Service | Registry made unavailable | Docker Hub outage | Local registry fallback | ⚠️ Partial |
| Elevation of Privilege | Container runs as root user | Privilege escalation via CVE | Trivy scan ✅ | ✅ Mitigated |

### Findings at This Stage:
- Trivy detected: Multiple CVEs in python:3.9-slim
- Trivy detected: Container running as root
- Cosign: Image successfully signed ✅
- Risk Level: 🟠 HIGH

---

## STAGE 4 — DEPLOYMENT TARGET (Staging Server)

| STRIDE | Threat | Attack Scenario | Tool Mitigation | Status |
|--------|--------|-----------------|-----------------|--------|
| Spoofing | Fake deployment trigger | Attacker triggers deployment with malicious image | Signed artifacts required | ✅ Mitigated |
| Tampering | Config changed after approval | IaC drift from approved state | Checkov IaC scan ✅ | ✅ Mitigated |
| Repudiation | No deployment audit trail | Unknown who deployed what version | GitHub Actions logs | ✅ Mitigated |
| Info Disclosure | Env variables exposed in logs | Sensitive config printed to logs | Secrets management | ⚠️ Partial |
| Denial of Service | Container resource exhaustion | No resource limits set | Resource limits needed | ❌ Not mitigated |
| Elevation of Privilege | Container breakout to host | Misconfigured container permissions | Trivy config scan ✅ | ✅ Mitigated |

### Findings at This Stage:
- Checkov detected: Missing resource limits
- Checkov detected: S3 bucket without encryption
- Checkov detected: Security group allows all traffic
- Risk Level: 🟠 HIGH

---

## STAGE 5 — RUNNING APPLICATION

| STRIDE | Threat | Attack Scenario | Tool Mitigation | Status |
|--------|--------|-----------------|-----------------|--------|
| Spoofing | User impersonation | Session hijacking attack | OWASP ZAP ✅ | ✅ Mitigated |
| Tampering | Runtime code injection | SQL injection via HTTP request | OWASP ZAP ✅ | ✅ Mitigated |
| Repudiation | No request logging | Attacker covers tracks | Application logging needed | ⚠️ Partial |
| Info Disclosure | Sensitive data in responses | Server version in HTTP headers | OWASP ZAP ✅ | ✅ Mitigated |
| Denial of Service | Application overwhelmed | DDoS attack on endpoints | Rate limiting needed | ❌ Not mitigated |
| Elevation of Privilege | Privilege escalation via vuln | CVE exploitation at runtime | OWASP ZAP ✅ | ✅ Mitigated |

### Findings at This Stage:
- ZAP detected: X-Content-Type-Options header missing
- ZAP detected: Server version information leaked
- ZAP detected: CSP header not set
- ZAP detected: Storable and cacheable content
- ZAP detected: Permissions policy header missing
- ZAP detected: Cross-Origin-Resource-Policy missing
- Risk Level: 🟡 MEDIUM

---

## Overall Risk Summary

| Stage | Critical | High | Medium | Low | Overall |
|-------|----------|------|--------|-----|---------|
| Source Repo | 2 | 1 | 2 | 1 | 🔴 CRITICAL |
| Build System | 3 | 2 | 1 | 1 | 🔴 CRITICAL |
| Artifact Registry | 1 | 3 | 2 | 0 | 🟠 HIGH |
| Deployment | 0 | 2 | 3 | 1 | 🟠 HIGH |
| Running App | 0 | 0 | 6 | 0 | 🟡 MEDIUM |

---

## Residual Risks (Not Fully Mitigated)

| Risk | Reason | Recommendation |
|------|--------|----------------|
| DDoS on pipeline | No rate limiting on PRs | Add GitHub branch rules |
| Resource exhaustion | No container resource limits | Add CPU/memory limits |
| Application logging | No structured logging | Add logging middleware |
| MFA not enforced | GitHub account security | Enable MFA on GitHub |

