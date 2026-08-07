"""Acceptance entry point: python scripts/run_tests.py

Unit tests resolve ``pricing_core`` from the frozen contract stub in ``contract/``
so this repository can be verified independently. A joint test overrides it with
the producer's candidate revision through ``PRICING_CORE_SRC``.
"""

import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

producer = os.environ.get("PRICING_CORE_SRC", "").strip()
sys.path.insert(0, str(Path(producer) if producer else ROOT / "contract"))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

if __name__ == "__main__":
    print(f"pricing_core resolved from: {sys.path[2] if producer else ROOT / 'contract'}")
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
