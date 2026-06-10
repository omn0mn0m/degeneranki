import os

if not os.environ.get("IN_TEST_SUITE", False):
    from . import main
