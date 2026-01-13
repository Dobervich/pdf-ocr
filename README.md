# pdf-ocr

Scan directories for PDFs and add OCR text layer to scanned documents.

## Features

- Process single PDF files or entire directories
- Smart detection of PDFs needing OCR (checks for pages without text)
- Creates searchable `_ocr.pdf` files alongside originals
- Python API for programmatic use from other tools
- Progress bars for scanning, analyzing, and processing
- Dry-run mode to preview changes before processing

## Requirements

- Python 3.10+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system

### Installing Tesseract

**Windows:**
```bash
winget install tesseract
```

**macOS:**
```bash
brew install tesseract
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install tesseract-ocr
```

## Installation

```bash
pip install git+https://github.com/Dobervich/pdf-ocr.git
```

Or clone and install locally:
```bash
git clone https://github.com/Dobervich/pdf-ocr.git
cd pdf-ocr
pip install .
```

## Usage

### Command Line

```bash
# Process a single PDF file
pdf-ocr document.pdf

# Scan a directory and OCR any PDFs that need it
pdf-ocr "C:\Documents\Scanned"

# Preview what would be processed (no changes made)
pdf-ocr "C:\Documents\Scanned" --dry-run

# Force reprocess even if _ocr.pdf already exists
pdf-ocr document.pdf --force

# Use a different output suffix
pdf-ocr document.pdf --suffix "_searchable"

# Specify OCR language (default: eng)
pdf-ocr document.pdf --language "eng+fra"
```

### Python API

```python
from pdf_ocr import ocr_file, needs_ocr

# Check if a PDF needs OCR
if needs_ocr("document.pdf"):
    print("This PDF needs OCR")

# Process a single file
result = ocr_file("document.pdf")
if result.success:
    print(f"Created: {result.output_path}")

# With custom output path
result = ocr_file("input.pdf", output_path="output.pdf")

# Force reprocess
result = ocr_file("document.pdf", force=True)

# Specify language
result = ocr_file("document.pdf", language="eng+fra")
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Analyze only, don't process any files |
| `--force` | Reprocess PDFs even if output already exists |
| `--suffix SUFFIX` | Suffix for output files (default: `_ocr`) |
| `--language LANG` | Tesseract language code(s) (default: `eng`) |
| `--empty-ratio RATIO` | Fraction of empty pages to trigger OCR (default: `0.5`) |

## How It Works

1. **Scan**: Recursively finds all PDF files in the directory
2. **Analyze**: Checks each PDF for text content per page
3. **Detect**: Flags PDFs where 50%+ of pages have minimal text (<10 characters)
4. **Process**: Runs OCR on flagged PDFs using Tesseract via ocrmypdf
5. **Output**: Creates `filename_ocr.pdf` alongside each original

## License

MIT
