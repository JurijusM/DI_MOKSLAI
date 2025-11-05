"""
Streamlit Application Package
"""

import sys
from pathlib import Path

# Add ITER directory to path when imported
ITER_DIR = Path(__file__).parent.parent
if str(ITER_DIR) not in sys.path:
    sys.path.insert(0, str(ITER_DIR))

