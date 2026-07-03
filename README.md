# Slidessibility - Accessibility Checker for PowerPoint Presentations

## Overview
Tooling to treat accessibility as continuous engineering for .pptx files, focused on WCAG 2.2 compliance for public-sector presentations (Dutch government requirements via EN 301 549 and Tijdelijk besluit digitale toegankelijkheid overheid).

**Core Features:**
- CLI for inspecting .pptx files
- Severity-ranked accessibility findings
- Actionable fix hints tied to WCAG success criteria
- Baseline mechanism for managing pre-existing issues
- Future: PowerPoint Add-in for in-app checking

## Project Structure
```
slidessibility/
├── README.md
├── pyproject.toml          # or requirements.txt
├── src/
│   └── slidessibility/
        | /templates
            |__ index.html
│       ├── __init__.py
│       ├── cli.py
        |__ app.py
│       ├── checker.py      # Core accessibility checks
│       ├── rules/          # WCAG-inspired rules
│       └── reports/        # Report generation
├── tests/
├── examples/
│   └── sample.pptx
├── docs/
└── .github/workflows/      # CI integration
```

## Quick Start
```bash
install the following extensions:
pip install typer 
pip install pdfplumber pypdf 
pip install -e .
pip install flask python-pptx

After the extensions, run the following command:
python app.py

after that, open the website and you can use it
```

## Inspiration
- axe-core (web)
- python-pptx for PPTX parsing
- WCAG 2.2, ARIA practices adapted to slides
```

## Installation
1. Clone the repo
2. `pip install -e .`
3. Run checks on your slides

## WCAG Focus Areas for Slides
- 1.1 Text Alternatives (alt text for images)
- 1.3 Adaptable (reading order, structure)
- 1.4 Distinguishable (color contrast, text resize)
- 2.4 Navigable (slide titles, logical order)
- 3.1 Readable
- And more...
