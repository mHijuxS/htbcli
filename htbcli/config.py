"""
Configuration module for HTB CLI
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from . import __version__

# Load environment variables in priority order:
#   1. $HTBCLI_ENV_FILE (explicit override)
#   2. ./.env (current working directory)
#   3. ~/.htbcli/.env (user home — works for globally installed binaries)
# `load_dotenv` does not overwrite values already set in the environment,
# so an existing HTB_TOKEN in the shell wins, and the first file found wins
# over later ones.
_ENV_FILE = os.getenv("HTBCLI_ENV_FILE")
if _ENV_FILE:
    load_dotenv(_ENV_FILE)
load_dotenv()
load_dotenv(Path.home() / ".htbcli" / ".env")


class Config:
    """Configuration class for HTB CLI"""

    # API Configuration
    BASE_URL_V4 = "https://labs.hackthebox.com/api/v4"
    BASE_URL_V5 = "https://labs.hackthebox.com/api/v5"
    AVATAR_BASE_URL = "https://htb-mp-prod-public-storage.s3.eu-central-1.amazonaws.com"

    # Authentication
    API_TOKEN = os.getenv("HTB_TOKEN")

    # Default settings
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100

    # Config directory (used for the user-level .env file above)
    CONFIG_DIR = Path.home() / ".htbcli"

    @classmethod
    def ensure_config_dir(cls):
        """Ensure the user-level configuration directory exists."""
        cls.CONFIG_DIR.mkdir(exist_ok=True)
        return cls.CONFIG_DIR

    @classmethod
    def get_auth_headers(cls):
        """Get authentication headers for API requests"""
        if not cls.API_TOKEN:
            raise ValueError("HTB_TOKEN environment variable not set")

        return {
            "Authorization": f"Bearer {cls.API_TOKEN}",
            "Content-Type": "application/json",
            "accept": "application/json",
            "User-Agent": f"HTB-CLI/{__version__}",
        }
