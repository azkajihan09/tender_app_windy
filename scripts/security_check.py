#!/usr/bin/env python3
"""Security check script for SecureKit project."""

import json
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str]) -> tuple[int, str, str]:
    """Run a command and return returncode, stdout, stderr."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"


def run_bandit() -> bool:
    """Run bandit security scanner."""
    print("🔍 Running Bandit security scanner...")

    # Run bandit with JSON output
    returncode, stdout, stderr = run_command(
        ["bandit", "-r", "src", "-f", "json", "-o", "bandit-report.json"]
    )

    if returncode != 0 and returncode != 1:  # 1 means issues found but not fatal
        print(f"❌ Bandit failed to run: {stderr}")
        return False

    # Check for HIGH/CRITICAL issues
    try:
        with open("bandit-report.json") as f:
            data = json.load(f)

        high_critical = [
            r
            for r in data.get("results", [])
            if r.get("issue_severity") in ["HIGH", "CRITICAL"]
        ]

        if high_critical:
            print(f"❌ Found {len(high_critical)} HIGH/CRITICAL security issues:")
            for issue in high_critical:
                print(f"  - {issue.get('test_name')}: {issue.get('issue_text')}")
                print(f"    File: {issue.get('filename')}:{issue.get('line_number')}")
            return False
        else:
            print("✅ No HIGH/CRITICAL security issues found by Bandit")
            return True

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error reading bandit report: {e}")
        return False


def run_pip_audit() -> bool:
    """Run pip-audit vulnerability scanner."""
    print("🔍 Running pip-audit vulnerability scanner...")

    # Run pip-audit with JSON output
    returncode, stdout, stderr = run_command(
        ["pip-audit", "--format=json", "--output=pip-audit-report.json"]
    )

    if returncode != 0:
        print(f"❌ pip-audit failed: {stderr}")
        return False

    # Check for vulnerabilities
    try:
        with open("pip-audit-report.json") as f:
            data = json.load(f)

        vulnerabilities = data.get("vulnerabilities", [])

        if vulnerabilities:
            print(f"❌ Found {len(vulnerabilities)} vulnerabilities:")
            for vuln in vulnerabilities:
                package = vuln.get("package", "unknown")
                installed = vuln.get("installed_version", "unknown")
                fixed = (
                    vuln.get("fixed_versions", ["unknown"])[0]
                    if vuln.get("fixed_versions")
                    else "unknown"
                )
                print(f"  - {package} {installed} -> {fixed}")
                print(f"    {vuln.get('description', 'No description')}")
            return False
        else:
            print("✅ No vulnerabilities found by pip-audit")
            return True

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error reading pip-audit report: {e}")
        return False


def run_safety_checks() -> bool:
    """Run basic safety checks on the codebase."""
    print("🔍 Running basic safety checks...")

    issues = []

    # Check for common dangerous patterns
    dangerous_patterns = [
        ("eval(", "Avoid using eval()"),
        ("exec(", "Avoid using exec()"),
        ("pickle.loads", "Be careful with pickle.loads()"),
        ("yaml.load", "Use yaml.safe_load() instead of yaml.load()"),
    ]

    for py_file in Path("src").rglob("*.py"):
        with open(py_file, "r", encoding="utf-8") as f:
            content = f.read()

        for pattern, message in dangerous_patterns:
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                if pattern in line:
                    # Skip comments, docstrings, and string literals
                    stripped_line = line.strip()
                    if (stripped_line.startswith('#') or 
                        stripped_line.startswith('"""') or
                        stripped_line.startswith("'''") or
                        '"""' in line or 
                        "'''" in line):
                        continue
                        
                    issues.append(f"{py_file}:{i} - {message}")
                    break

    if issues:
        print("⚠️  Found potential security issues:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ No dangerous patterns found")
        return True


def main():
    """Main security check function."""
    print("🛡️  SecureKit Security Check")
    print("=" * 40)

    all_passed = True

    # Run security scanners
    if not run_bandit():
        all_passed = False

    print()

    if not run_pip_audit():
        all_passed = False

    print()

    if not run_safety_checks():
        all_passed = False

    print()
    print("=" * 40)

    if all_passed:
        print("✅ All security checks passed!")
        sys.exit(0)
    else:
        print("❌ Security checks failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
