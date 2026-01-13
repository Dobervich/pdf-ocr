"""Entry point for running as a module: python -m pdf_ocr"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
