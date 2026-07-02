from typing import List
from .checker import Finding

def generate_report(findings: List[Finding], format: str = "text"):
    if format == "json":
        return [f.__dict__ for f in findings]

    if format == "markdown":
        md = "# Accessibility Report\n\n"
        for f in findings:
            md += f"## {f.severity.upper()}: {f.rule_id} (Slide {f.slide_number})\n"
            md += f"**WCAG**: {f.wcag_criterion}\n"
            md += f"{f.message}\n"
            md += f"**Fix**: {f.fix_hint}\n\n"
        return md

    # Rich text / plain
    lines = ["Accessibility Findings:", "="*30, ""]
    for f in findings:
        lines.append(f"[{f.severity.upper()}] Slide {f.slide_number}: {f.message}")
        lines.append(f"   WCAG: {f.wcag_criterion}")
        lines.append(f"   Fix: {f.fix_hint}")
        lines.append("")
    return "\n".join(lines)
