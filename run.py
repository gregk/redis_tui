#!/usr/bin/env python3
"""
Run script for Redis TUI.

This script provides a convenient way to run the Redis TUI application
directly from the project root directory.
"""

from redis_tui.app import RedisTUI

def main():
    """Run the Redis TUI application with sample data."""
    app = RedisTUI(load_samples=True)
    app.run()

if __name__ == "__main__":
    main() 