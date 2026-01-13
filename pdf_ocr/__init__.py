"""PDF OCR Tool - Analyze and OCR PDFs."""

from pathlib import Path

from .analyzer import needs_ocr, scan_directory
from .processor import process_pdf, get_output_path, ProcessResult

__version__ = "0.1.0"

__all__ = [
    "ocr_file",
    "needs_ocr",
    "scan_directory",
    "process_pdf",
    "get_output_path",
    "ProcessResult",
]


def ocr_file(
    input_path: str | Path,
    output_path: str | Path | None = None,
    force: bool = False,
    language: str = "eng",
) -> ProcessResult:
    """
    Add OCR to a PDF file.

    This is the main API for programmatic use.

    Args:
        input_path: Path to the input PDF file
        output_path: Path for output file. If None, creates input_ocr.pdf
        force: If True, reprocess even if output exists
        language: Tesseract language code(s), e.g., 'eng' or 'eng+fra'

    Returns:
        ProcessResult with success status and output path

    Example:
        >>> from pdf_ocr import ocr_file
        >>> result = ocr_file("document.pdf")
        >>> if result.success:
        ...     print(f"Created: {result.output_path}")
    """
    input_path = Path(input_path)

    if output_path is not None:
        # Custom output path - need to compute suffix
        output_path = Path(output_path)
        # Extract what the suffix would be
        suffix = output_path.stem.replace(input_path.stem, "")
        if not suffix:
            suffix = "_ocr"
    else:
        suffix = "_ocr"

    result = process_pdf(input_path, suffix, force, language)

    # If custom output path was specified and differs, rename
    if output_path is not None and result.success and not result.skipped:
        actual_output = get_output_path(input_path, suffix)
        if actual_output != output_path:
            actual_output.rename(output_path)
            result = ProcessResult(
                input_path=result.input_path,
                output_path=output_path,
                success=True,
                skipped=False,
                error=None
            )

    return result
