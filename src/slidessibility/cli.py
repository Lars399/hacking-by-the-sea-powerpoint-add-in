import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

from .checker import AccessibilityChecker
from .reports import generate_report

console = Console()

def main():
    parser = argparse.ArgumentParser(
        description="Slidessibility: Accessibility checker for .pptx files"
    )
    parser.add_argument("pptx_file", type=Path, help="Path to the .pptx file to check")
    parser.add_argument("--baseline", type=Path, help="Path to baseline JSON file")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--output", type=Path, help="Output file for report")

    args = parser.parse_args()

    if not args.pptx_file.exists():
        console.print(f"[red]Error: File {args.pptx_file} not found[/red]")
        sys.exit(1)

    checker = AccessibilityChecker()
    findings = checker.check_pptx(args.pptx_file)

    # TODO: Apply baseline filtering

    if args.format == "json":
        import json
        report = generate_report(findings, "json")
        if args.output:
            args.output.write_text(json.dumps(report, indent=2))
        else:
            print(json.dumps(report, indent=2))
    else:
        report_text = generate_report(findings, args.format)
        if args.output:
            args.output.write_text(report_text)
        else:
            console.print(report_text)

if __name__ == "__main__":
    main()
