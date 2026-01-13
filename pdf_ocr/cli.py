"""Command-line interface for PDF OCR tool."""

import argparse
import sys
from pathlib import Path

from tqdm import tqdm

from .analyzer import analyze_directory, scan_directory, needs_ocr
from .processor import process_batch, get_output_path


def main(args: list[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Scan a directory for PDFs and add OCR to those that need it.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdf-ocr "C:\\Documents\\Scanned"
  pdf-ocr /path/to/pdfs --suffix "_searchable"
  pdf-ocr ./documents --dry-run
  pdf-ocr ./documents --force
        """
    )

    parser.add_argument(
        "directory",
        type=Path,
        help="Directory to scan for PDFs (recursive)"
    )
    parser.add_argument(
        "--suffix",
        default="_ocr",
        help="Suffix for output files (default: _ocr)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reprocess PDFs even if output already exists"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze only, don't process any files"
    )
    parser.add_argument(
        "--empty-ratio",
        type=float,
        default=0.5,
        help="Fraction of pages that must be empty to trigger OCR (default: 0.5)"
    )
    parser.add_argument(
        "--language",
        default="eng",
        help="Tesseract language code(s), e.g., 'eng' or 'eng+fra' (default: eng)"
    )

    parsed = parser.parse_args(args)

    # Validate directory
    if not parsed.directory.exists():
        print(f"Error: Directory not found: {parsed.directory}")
        return 1

    if not parsed.directory.is_dir():
        print(f"Error: Not a directory: {parsed.directory}")
        return 1

    print(f"Scanning: {parsed.directory}")
    print()

    # Scan and analyze
    all_pdfs = list(tqdm(
        scan_directory(parsed.directory),
        desc="Finding PDFs",
        unit="file"
    ))

    if not all_pdfs:
        print("No PDF files found.")
        return 0

    print(f"\nFound {len(all_pdfs)} PDF(s). Analyzing...")

    needs_ocr_list = []
    has_ocr_list = []

    for pdf_path in tqdm(all_pdfs, desc="Analyzing", unit="file"):
        if needs_ocr(pdf_path, empty_page_ratio=parsed.empty_ratio):
            needs_ocr_list.append(pdf_path)
        else:
            has_ocr_list.append(pdf_path)

    print(f"\nAnalysis complete:")
    print(f"  - Already have OCR: {len(has_ocr_list)}")
    print(f"  - Need OCR:         {len(needs_ocr_list)}")

    if not needs_ocr_list:
        print("\nNo PDFs need OCR processing.")
        return 0

    if parsed.dry_run:
        print("\n[DRY RUN] Files that would be processed:")
        for pdf_path in needs_ocr_list:
            output_path = get_output_path(pdf_path, parsed.suffix)
            exists = " (output exists)" if output_path.exists() else ""
            print(f"  {pdf_path}{exists}")
            print(f"    -> {output_path}")
        return 0

    # Process PDFs
    print(f"\nProcessing {len(needs_ocr_list)} PDF(s)...")

    pbar = tqdm(total=len(needs_ocr_list), desc="OCR Processing", unit="file")

    def progress_callback(current: int, total: int, path: Path) -> None:
        pbar.set_postfix_str(path.name[:30])
        pbar.update(1)

    # Reset for callback (it will call update)
    pbar.reset()

    result = process_batch(
        needs_ocr_list,
        suffix=parsed.suffix,
        force=parsed.force,
        language=parsed.language,
        progress_callback=progress_callback
    )

    pbar.close()

    # Summary
    print(f"\nComplete!")
    print(f"  - Processed: {result.processed}")
    print(f"  - Skipped (already existed): {result.skipped}")
    print(f"  - Failed: {result.failed}")

    # Show failures
    if result.failed > 0:
        print("\nFailed files:")
        for r in result.results:
            if not r.success and not r.skipped:
                print(f"  {r.input_path}")
                print(f"    Error: {r.error}")

    return 0 if result.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
