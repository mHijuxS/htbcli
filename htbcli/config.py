"""
Configuration module for HTB CLI
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for HTB CLI"""
    
    # API Configuration
    BASE_URL_V4 = "https://labs.hackthebox.com/api/v4"
    BASE_URL_V5 = "https://labs.hackthebox.com/api/v5"
    
    # Authentication
    API_TOKEN = os.getenv("HTB_TOKEN")
    
    # Default settings
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100
    
    # File paths
    CONFIG_DIR = Path.home() / ".htbcli"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    
    @classmethod
    def get_auth_headers(cls):
        """Get authentication headers for API requests"""
        if not cls.API_TOKEN:
            raise ValueError("HTB_TOKEN environment variable not set")
        
        return {
            "Authorization": f"Bearer {cls.API_TOKEN}",
            "Content-Type": "application/json",
            "accept": "application/json",
            "User-Agent": "HTB-CLI/1.0.0"
        }
    
    @classmethod
    def ensure_config_dir(cls):
        """Ensure configuration directory exists"""
        cls.CONFIG_DIR.mkdir(exist_ok=True)
        return cls.CONFIG_DIR
