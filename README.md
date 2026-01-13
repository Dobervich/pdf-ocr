# pdf-ocr

Scan directories for PDFs and add OCR text layer to scanned documents.

## Features

- Recursively scans directories for PDF files
- Smart detection of PDFs needing OCR (checks for pages without text)
- Creates searchable `_ocr.pdf` files alongside originals
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

```bash
# Scan a directory and OCR any PDFs that need it
pdf-ocr "C:\Documents\Scanned"

# Preview what would be processed (no changes made)
pdf-ocr "C:\Documents\Scanned" --dry-run

# Force reprocess even if _ocr.pdf already exists
pdf-ocr "C:\Documents\Scanned" --force

# Use a different output suffix
pdf-ocr "C:\Documents\Scanned" --suffix "_searchable"

# Specify OCR language (default: eng)
pdf-ocr "C:\Documents\Scanned" --language "eng+fra"
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
