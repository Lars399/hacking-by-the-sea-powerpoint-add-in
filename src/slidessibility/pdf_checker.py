from pathlib import Path
from typing import List
from dataclasses import dataclass
import pdfplumber
from pypdf import PdfReader


@dataclass
class Finding:
    severity: str
    rule_id: str
    wcag_criterion: str
    message: str
    page_number: int
    location: str
    fix_hint: str
    confidence: float = 1.0


class PDFAccessibilityChecker:
    def __init__(self):
        self.rules = self._load_rules()

    def _load_rules(self):
        return [
            self._check_alt_text_images,
            self._check_table_structure,
            self._check_reading_order_heuristic,
            self._check_small_text,
            self._check_image_only_pages,
            self._check_headings,
        ]

    def check_pdf(self, pdf_path: Path) -> List[Finding]:
        findings = []
        reader = PdfReader(pdf_path)

        # Metadata checks (run once)
        findings.extend(self._check_metadata(reader))

        # Per-page checks
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                for rule in self.rules:
                    findings.extend(rule(page, page_num, reader))

        return sorted(findings, key=lambda f: self._severity_order(f.severity), reverse=True)

    def _severity_order(self, sev: str) -> int:
        order = {"critical": 4, "serious": 3, "moderate": 2, "minor": 1}
        return order.get(sev, 0)

    # ====================== METADATA ======================
    def _check_metadata(self, reader) -> List[Finding]:
        findings = []
        meta = reader.metadata or {}

        title = meta.get('/Title')
        if not title or len(str(title).strip()) < 5:
            findings.append(Finding(
                severity="serious",
                rule_id="PDF_DOC_TITLE",
                wcag_criterion="2.4.2 Page Titled",
                message="PDF is missing a descriptive document title",
                page_number=0,
                location="Document Properties",
                fix_hint="In Acrobat: File → Properties → Description → Set Title."
            ))

        lang = meta.get('/Lang')
        if not lang:
            findings.append(Finding(
                severity="serious",
                rule_id="PDF_LANGUAGE",
                wcag_criterion="3.1.1 Language of Page",
                message="PDF missing language metadata",
                page_number=0,
                location="Document Properties",
                fix_hint="Set default language in Acrobat Pro."
            ))
        return findings

    # ====================== PAGE RULES ======================
    def _check_alt_text_images(self, page, page_num: int, reader) -> List[Finding]:
        findings = []
        for img in page.images or []:
            findings.append(Finding(
                severity="moderate",
                rule_id="PDF_IMG_ALT",
                wcag_criterion="1.1.1 Non-text Content",
                message=f"Image detected on page {page_num}",
                page_number=page_num,
                location=f"Page {page_num}",
                fix_hint="Add Alt Text using Adobe Acrobat (tagged PDF recommended)."
            ))
        return findings

    def _check_table_structure(self, page, page_num: int, reader) -> List[Finding]:
        findings = []
        tables = page.extract_tables() or []
        for idx, table in enumerate(tables):
            if table and len(table) > 0:
                first_row = table[0]
                if all(not str(cell or "").strip() for cell in first_row):
                    findings.append(Finding(
                        severity="serious",
                        rule_id="PDF_TABLE_HEADERS",
                        wcag_criterion="1.3.1 Info and Relationships",
                        message=f"Table on page {page_num} likely missing headers",
                        page_number=page_num,
                        location=f"Table {idx}",
                        fix_hint="Add header row and ensure proper table tagging."
                    ))
        return findings

    def _check_reading_order_heuristic(self, page, page_num: int, reader) -> List[Finding]:
        return [Finding(
            severity="moderate",
            rule_id="PDF_READING_ORDER",
            wcag_criterion="1.3.2 Meaningful Sequence",
            message=f"Verify reading order on page {page_num}",
            page_number=page_num,
            location=f"Page {page_num}",
            fix_hint="Use Acrobat Pro → Order panel to fix reading order."
        )]

    def _check_small_text(self, page, page_num: int, reader) -> List[Finding]:
        text = page.extract_text() or ""
        if len(text) > 80:
            return [Finding(
                severity="moderate",
                rule_id="PDF_SMALL_TEXT",
                wcag_criterion="1.4.4 Resize Text",
                message=f"Page {page_num} has dense text content",
                page_number=page_num,
                location=f"Page {page_num}",
                fix_hint="Ensure font size is sufficient and PDF is reflowable."
            )]
        return []

    def _check_image_only_pages(self, page, page_num: int, reader) -> List[Finding]:
        text = (page.extract_text() or "").strip()
        if len(page.images or []) > 0 and len(text) < 30:
            return [Finding(
                severity="serious",
                rule_id="PDF_IMAGE_ONLY",
                wcag_criterion="1.1.1 Non-text Content",
                message=f"Page {page_num} appears mostly image-based",
                page_number=page_num,
                location=f"Page {page_num}",
                fix_hint="Add alt text or convert text in images to real selectable text."
            )]
        return []

    def _check_headings(self, page, page_num: int, reader) -> List[Finding]:
        return [Finding(
            severity="moderate",
            rule_id="PDF_HEADING_STRUCTURE",
            wcag_criterion="2.4.6 Headings and Labels",
            message=f"Check heading structure on page {page_num}",
            page_number=page_num,
            location=f"Page {page_num}",
            fix_hint="Use proper heading tags (H1, H2...) in a tagged PDF."
        )]