# DevSecops CI/CD Pipeline Security Assessment
## Overview
This project implements a complete DevSecOps pipeline that automatically scans for security vulnerabilities at every stage of the CI/CD
## Tools used
- **Gitleaks** - Secret detection
- **Semgrep** - Static code analysis (SAST)
- **Snyk** - Dependency scanning (SCA)
- **Trivy** - Container Image Scanning
- **Checkov** - IaC misconfiguration scanning 
- **OWASP ZAP** - Dynamic app testing (DAST)
##Pipeline Stages
1. Secret Scanning
2. SAST 
3. SCA
4.Build
5.Container Scan
6.IaC Scan
7.DAST
8.report generation

See docs/ folder for detailed setup instructions.
