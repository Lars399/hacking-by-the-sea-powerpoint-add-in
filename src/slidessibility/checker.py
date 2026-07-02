from pathlib import Path
from pptx import Presentation
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Finding:
    severity: str  # critical, serious, moderate, minor
    rule_id: str
    wcag_criterion: str
    message: str
    slide_number: int
    location: str  # e.g., "Slide 5 - Shape 3"
    fix_hint: str
    confidence: float = 1.0

class AccessibilityChecker:
    def __init__(self):
        self.rules = self._load_rules()

    def _load_rules(self):
        # TODO: Load modular rules
        return [
            self._check_alt_text,
            self._check_slide_titles,
            # Add more rules
        ]

    def check_pptx(self, pptx_path: Path) -> List[Finding]:
        prs = Presentation(pptx_path)
        findings = []

        for slide_num, slide in enumerate(prs.slides, 1):
            # Run rules on each slide
            for rule in self.rules:
                findings.extend(rule(slide, slide_num))

        return sorted(findings, key=lambda f: self._severity_order(f.severity), reverse=True)

    def _severity_order(self, sev: str) -> int:
        order = {"critical": 4, "serious": 3, "moderate": 2, "minor": 1}
        return order.get(sev, 0)

    def _check_alt_text(self, slide, slide_num: int) -> List[Finding]:
        findings = []
        for shape_idx, shape in enumerate(slide.shapes):
            if shape.has_picture or (hasattr(shape, 'image') and shape.image):
                if not getattr(shape, 'alt_text', None) or not shape.alt_text.strip():
                    findings.append(Finding(
                        severity="serious",
                        rule_id="IMG_ALT",
                        wcag_criterion="1.1.1 Non-text Content",
                        message=f"Image on slide {slide_num} missing alt text",
                        slide_number=slide_num,
                        location=f"Slide {slide_num} - Shape {shape_idx}",
                        fix_hint="Add descriptive alt text via Shape Format > Alt Text. Be concise but informative for screen readers."
                    ))
        return findings

    def _check_slide_titles(self, slide, slide_num: int) -> List[Finding]:
        title = slide.shapes.title
        if not title or not title.text.strip():
            return [Finding(
                severity="critical",
                rule_id="SLIDE_TITLE",
                wcag_criterion="2.4.6 Headings and Labels",
                message=f"Slide {slide_num} has no title",
                slide_number=slide_num,
                location=f"Slide {slide_num}",
                fix_hint="Add a title placeholder or text box as the first element. Ensures proper navigation for screen readers."
            )]
        return []
