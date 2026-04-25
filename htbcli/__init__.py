"""
HTB CLI - A command-line interface for HackTheBox API

A comprehensive CLI tool for interacting with the HackTheBox API v4 and v5,
providing easy access to machines, challenges, users, teams, and more.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("htbcli")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

__author__ = "HTB CLI Team"
__description__ = "A comprehensive command-line interface for HackTheBox API v4 and v5"
