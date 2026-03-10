#!/usr/bin/env python3
"""
Configuration module for GitHub Contribution Snake
Handles environment variables and settings
"""

import os
import sys

def get_github_username():
    """Get GitHub username from environment variables"""
    username = os.getenv('GITHUB_USERNAME')
    if not username:
        print("Error: GITHUB_USERNAME environment variable is required")
        return None
    return username

def get_github_token():
    """Get GitHub token from environment variables"""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable is required")
        return None
    return token

def validate_config():
    """Validate that all required configuration is present"""
    username = get_github_username()
    token = get_github_token()
    
    if not username or not token:
        print("Missing required environment variables:")
        if not username:
            print("  - GITHUB_USERNAME")
        if not token:
            print("  - GITHUB_TOKEN")
        print("\nTo get a GitHub token:")
        print("  1. Go to: https://github.com/settings/tokens")
        print("  2. Click 'Generate new token (classic)'")
        print("  3. Select 'read:user' scope")
        print("  4. Copy the generated token")
        return False
    
    return True

# Snake configuration
SNAKE_CONFIG = {
    'cell_size': 11,
    'cell_spacing': 3,
    'snake_length': 6,
    'animation_duration': 120,  # milliseconds per frame
    'padding': 30
}

# Color schemes
COLORS = {
    'dark': {
        'background': '#0d1117',
        'grid': '#21262d',
        'levels': ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353'],
        'snake': '#f85149',
        'snake_head': '#ff6b6b'
    },
    'light': {
        'background': '#ffffff',
        'grid': '#ebedf0',
        'levels': ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39'],
        'snake': '#f85149',
        'snake_head': '#ff6b6b'
    }
}
