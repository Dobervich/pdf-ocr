"""PDF OCR processing module."""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import ocrmypdf


@dataclass
class ProcessResult:
    """Result of processing a single PDF."""
    input_path: Path
    output_path: Path | None
    success: bool
    skipped: bool
    error: str | None = None


@dataclass
class BatchResult:
    """Result of processing a batch of PDFs."""
    processed: int
    skipped: int
    failed: int
    results: list[ProcessResult]


def get_output_path(input_path: Path, suffix: str = "_ocr") -> Path:
    """
    Generate output path for OCR'd PDF.

    Args:
        input_path: Original PDF path
        suffix: Suffix to add before extension (default: "_ocr")

    Returns:
        Path for the output file (e.g., document.pdf -> document_ocr.pdf)
    """
    return input_path.parent / f"{input_path.stem}{suffix}{input_path.suffix}"


def process_pdf(
    input_path: Path,
    suffix: str = "_ocr",
    force: bool = False,
    language: str = "eng"
) -> ProcessResult:
    """
    Process a single PDF with OCR.

    Args:
        input_path: Path to the input PDF
        suffix: Suffix for output filename
        force: If True, reprocess even if output exists
        language: Tesseract language code(s)

    Returns:
        ProcessResult with status and details
    """
    output_path = get_output_path(input_path, suffix)

    if output_path.exists() and not force:
        return ProcessResult(
            input_path=input_path,
            output_path=output_path,
            success=True,
            skipped=True,
            error=None
        )

    try:
        ocrmypdf.ocr(
            input_path,
            output_path,
            language=language,
            skip_text=True,  # Skip pages that already have text
            deskew=True,     # Straighten skewed pages
        )
        return ProcessResult(
            input_path=input_path,
            output_path=output_path,
            success=True,
            skipped=False,
            error=None
        )
    except Exception as e:
        return ProcessResult(
            input_path=input_path,
            output_path=None,
            success=False,
            skipped=False,
            error=str(e)
        )


def process_batch(
    pdf_list: list[Path],
    suffix: str = "_ocr",
    force: bool = False,
    language: str = "eng",
    progress_callback: Callable[[int, int, Path], None] | None = None
) -> BatchResult:
    """
    Process a batch of PDFs with OCR.

    Args:
        pdf_list: List of PDF paths to process
        suffix: Suffix for output filenames
        force: If True, reprocess even if outputs exist
        language: Tesseract language code(s)
        progress_callback: Optional callback(current, total, path) for progress updates

    Returns:
        BatchResult with counts and individual results
    """
    results = []
    processed = 0
    skipped = 0
    failed = 0
    total = len(pdf_list)

    for i, pdf_path in enumerate(pdf_list):
        if progress_callback:
            progress_callback(i + 1, total, pdf_path)

        result = process_pdf(pdf_path, suffix, force, language)
        results.append(result)

        if result.skipped:
            skipped += 1
        elif result.success:
            processed += 1
        else:
            failed += 1

    return BatchResult(
        processed=processed,
        skipped=skipped,
        failed=failed,
        results=results
    )
