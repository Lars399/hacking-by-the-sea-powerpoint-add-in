from pathlib import Path
import sys
from .checker import AccessibilityChecker
from .pdf_checker import PDFAccessibilityChecker

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "check":
        print("Usage: slidessibility check <file.pptx or file.pdf>")
        print("Example: slidessibility check examples/Lesson.pptx")
        sys.exit(1)

    file_path = Path(sys.argv[2])

    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        print(f"   Current directory: {Path.cwd()}")
        sys.exit(1)

    suffix = file_path.suffix.lower()

    if suffix == ".pptx":
        checker = AccessibilityChecker()
        findings = checker.check_pptx(file_path)
        tool_name = "PowerPoint"

    elif suffix == ".pdf":
        checker = PDFAccessibilityChecker()
        findings = checker.check_pdf(file_path)
        tool_name = "PDF"

    else:
        print(f"❌ Unsupported file type: {suffix}")
        print("Supported: .pptx and .pdf")
        sys.exit(1)

    # Output
    print(f"\n🔍 {tool_name} Accessibility Findings ({len(findings)} total)")
    print("=" * 70)

    if not findings:
        print("✅ No accessibility issues found!")
        return

    for f in findings:
        print(f"[{f.severity.upper()}] {f.message}")
        print(f"    WCAG: {f.wcag_criterion}")
        print(f"    Fix:  {f.fix_hint}")
        print("-" * 60)


if __name__ == "__main__":
    main()