#!/usr/bin/env python
"""
Entry point script for the ResearchFinder system.
This script provides a simple way to run research queries.
"""

import os
import sys

# Add the parent directory to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from federated_query.main import main

if __name__ == "__main__":
    # Pass any command-line arguments to the main function
    main()