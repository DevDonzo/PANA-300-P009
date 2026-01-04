"""Entry point for running calculator package as a module."""

import sys
from pathlib import Path

# Add parent src directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.main import main

if __name__ == "__main__":
    sys.exit(main())
