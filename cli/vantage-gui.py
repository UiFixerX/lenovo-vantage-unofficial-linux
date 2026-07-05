#!/usr/bin/env python3
"""Thin launcher — real entry point is gui.app.main()"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.app import main

if __name__ == "__main__":
    main()
