import os
import json

reports_dir = 'reports'

def load_json(filename):
    path = os.path.join(reports_dir, filename)
    if os.path.exists(path):
        with open(path) as f:
            try:
                return json.load(f)
            except:
                return {}
    return None

def count_issues(data):
    if not data:
        return 'N/A'
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        for key in ['results', 'findings', 'vulnerabilities', 'runs']:
            if key in data:
                val = data[key]
                if isinstance(val, list):
                    if key == 'runs' and val:
                        results = val[0].get('results', [])
                        return len(results)
                    return len(val)
    return 'N/A'

gitleaks_before = load_json('gitleaks-before.json')
gitleaks_after  = load_json('gitleaks-after.json')
osv_before      = load_json('osv-scanner-before.json')
osv_after       = load_json('osv-scanner-after.json')
semgrep_before  = load_json('semgrep-before.json')
semgrep_after   = load_json('semgrep-after.json')
trivy_before    = load_json('trivy-before.json')
trivy_after     = load_json('trivy-after.json')

report = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<title>DevSecOps Final Report</title>
<style>
  body {{ font-family: Arial, sans-serif; background: #0d1117; color: #e6edf3; padding: 30px; }}
  h1 {{ color: #58a6ff; text-align: center; }}
  h2 {{ color: #79c0ff; border-bottom: 1px solid #30363d; padding-bottom: 8px; }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
  th {{ background: #161b22; color: #58a6ff; padding: 10px; text-align: left; }}
  td {{ padding: 10px; border-bottom: 1px solid #21262d; }}
  .good {{ color: #3fb950; font-weight: bold; }}
  .bad  {{ color: #f85149; font-weight: bold; }}
  .summary {{ background: #161b22; border-radius: 8px; padding: 20px; margin-bottom: 30px; }}
</style>
</head>
<body>
<h1>🛡️ DevSecOps Security Report — Before vs After</h1>
<div class='summary'>
  <h2>📋 Summary</h2>
  <p>This report compares the security posture of the application before and after DevSecOps pipeline integration.</p>
</div>
<h2>🔍 Tool-wise Comparison</h2>
<table>
  <tr><th>Tool</th><th>Before (Issues)</th><th>After (Issues)</th><th>Status</th></tr>
  <tr>
    <td>GitLeaks (Secret Scanning)</td>
    <td class='bad'>{count_issues(gitleaks_before)}</td>
    <td class='good'>{count_issues(gitleaks_after)}</td>
    <td>{'✅ Improved' if str(count_issues(gitleaks_after)) < str(count_issues(gitleaks_before)) else '🔄 Check Manually'}</td>
  </tr>
  <tr>
    <td>OSV Scanner (Dependencies)</td>
    <td class='bad'>{count_issues(osv_before)}</td>
    <td class='good'>{count_issues(osv_after)}</td>
    <td>🔄 Review</td>
  </tr>
  <tr>
    <td>Semgrep (SAST)</td>
    <td class='bad'>{count_issues(semgrep_before)}</td>
    <td class='good'>{count_issues(semgrep_after)}</td>
    <td>🔄 Review</td>
  </tr>
  <tr>
    <td>Trivy (Container/IaC Scan)</td>
    <td class='bad'>{count_issues(trivy_before)}</td>
    <td class='good'>{count_issues(trivy_after)}</td>
    <td>🔄 Review</td>
  </tr>
  <tr>
    <td>ZAP (DAST)</td>
    <td>See zap-before.html</td>
    <td>See zap-after.html</td>
    <td>🔄 Review</td>
  </tr>
</table>
<h2>✅ Conclusion</h2>
<p>The DevSecOps pipeline successfully integrates security scanning at every stage — secret detection, dependency checks, static analysis, container scanning, and dynamic testing — reducing the attack surface before code reaches production.</p>
</body>
</html>"""

os.makedirs('reports', exist_ok=True)
with open('reports/final-report.html', 'w') as f:
    f.write(report)

print("✅ Final report generated!")
print("   Open: reports/final-report.html")
