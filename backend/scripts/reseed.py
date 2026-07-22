#!/usr/bin/env python3
"""Reset database content and reseed from PHP PDF data."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.bootstrap import init_db


if __name__ == "__main__":
    init_db(force_reseed=True)
    print("Database reseeded with Zend PHP quiz (themes on questions).")
