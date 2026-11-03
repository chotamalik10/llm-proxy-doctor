#!/usr/bin/env python3
"""Backward-compatible entry point. Prefer running doctor.py."""
from doctor import main

if __name__ == "__main__":
    raise SystemExit(main())
