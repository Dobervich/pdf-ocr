"""PDF analysis module for detecting OCR status."""

from pathlib import Path
from typing import Generator

import fitz  # PyMuPDF


def needs_ocr(
    pdf_path: Path,
    empty_page_threshold: int = 10,
    empty_page_ratio: float = 0.5
) -> bool:
    """
    Determine if a PDF needs OCR by checking for pages with no text.

    A PDF needs OCR if most of its pages have little to no extractable text,
    indicating they are likely scanned images.

    Args:
        pdf_path: Path to the PDF file
        empty_page_threshold: Characters below which a page is considered "empty" (default: 10)
        empty_page_ratio: Fraction of pages that must be empty to trigger OCR (default: 0.5)

    Returns:
        True if the PDF needs OCR (majority of pages have no text), False otherwise
    """
    try:
        doc = fitz.open(pdf_path)
        page_count = doc.page_count

        if page_count == 0:
            doc.close()
            return False

        empty_pages = 0
        for page in doc:
            char_count = len(page.get_text())
            if char_count < empty_page_threshold:
                empty_pages += 1

        doc.close()

        # Needs OCR if more than half the pages are empty
        return (empty_pages / page_count) >= empty_page_ratio
    except Exception as e:
        print(f"Error analyzing {pdf_path}: {e}")
        return False


def scan_directory(directory: Path) -> Generator[Path, None, None]:
    """
    Recursively scan a directory for PDF files.

    Args:
        directory: Directory path to scan

    Yields:
        Path objects for each PDF file found
    """
    directory = Path(directory)
    for pdf_path in directory.rglob("*.[pP][dD][fF]"):
        if pdf_path.is_file():
            yield pdf_path


def analyze_directory(
    directory: Path,
    empty_page_threshold: int = 10,
    empty_page_ratio: float = 0.5
) -> tuple[list[Path], list[Path]]:
    """
    Analyze all PDFs in a directory and categorize by OCR status.

    Args:
        directory: Directory path to scan
        empty_page_threshold: Characters below which a page is considered "empty"
        empty_page_ratio: Fraction of pages that must be empty to trigger OCR

    Returns:
        Tuple of (needs_ocr_list, has_ocr_list)
    """
    needs_ocr_list = []
    has_ocr_list = []

    for pdf_path in scan_directory(directory):
        if needs_ocr(pdf_path, empty_page_threshold, empty_page_ratio):
            needs_ocr_list.append(pdf_path)
        else:
            has_ocr_list.append(pdf_path)

    return needs_ocr_list, has_ocr_list
