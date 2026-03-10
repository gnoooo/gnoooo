#!/usr/bin/env python3
"""
CLI for the GitHub Contribution Snake Generator
Run this locally to generate your contribution snake animation
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the scripts directory to the path
sys.path.append(str(Path(__file__).parent))

from scripts.snake_generator import ContributionSnake
from scripts.config import validate_config

# ANSI color codes for console output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Professional CLI header
HEADER = f"""
{BOLD}{CYAN}
╔════════════════════════════════════════════════════════╗
║           GitHub Contribution Snake Generator          ║
╚════════════════════════════════════════════════════════╝{RESET}
"""

# Debug: print the GitHub username and token from environment variables
print(HEADER)
print(f"{CYAN}[DEBUG]{RESET} GITHUB_USERNAME: {BOLD}{os.environ.get('GITHUB_USERNAME') or 'Not set'}{RESET}")
print(f"{CYAN}[DEBUG]{RESET} GITHUB_TOKEN:    {BOLD}{'***' if os.environ.get('GITHUB_TOKEN') else 'Not set'}{RESET}")
print(f"{YELLOW}{'-'*56}{RESET}")

def run_snake_cli():
    """Run the snake generation CLI"""
    
    # Load from .env (already loaded at top)
    username = os.getenv('GITHUB_USERNAME')
    token = os.getenv('GITHUB_TOKEN')
    
    if not username or not token:
        print(f"{RED}{BOLD}🔧 SETUP REQUIRED{RESET}")
        print(f"{YELLOW}{'='*56}{RESET}")
        print(f"{YELLOW}Please set your GitHub credentials in the .env file at the project root:{RESET}")
        print(f"  {CYAN}GITHUB_USERNAME=your_username{RESET}")
        print(f"  {CYAN}GITHUB_TOKEN=your_token{RESET}")
        print(f"\nThen run: {BOLD}python run_snake_cli.py{RESET}\n")
        print(f"{YELLOW}{'='*56}{RESET}")
        return
    
    # Create output directory
    output_dir = Path('dist')
    output_dir.mkdir(exist_ok=True)
    
    try:
        print(f"{CYAN}🐍 Starting snake generation for user: {BOLD}{username}{RESET}")
        print(f"{YELLOW}{'-'*56}{RESET}")
        # Initialize and run snake generator
        snake = ContributionSnake(username, token)
        
        # Generate all animations
        success = snake.generate_all(output_dir)
        
        if success:
            print(f"{GREEN}{BOLD}✔ Snake generation complete!{RESET} Check the '{CYAN}dist{RESET}' folder for generated files:")
            print(f"  {CYAN}• github-contribution-grid-snake.svg{RESET}       (light theme SVG)")
            print(f"  {CYAN}• github-contribution-grid-snake-dark.svg{RESET}  (dark theme SVG)")
            print(f"  {CYAN}• github-contribution-grid-snake-light.gif{RESET} (light theme GIF)")
            print(f"  {CYAN}• github-contribution-grid-snake.gif{RESET}       (dark theme GIF)")
            print(f"{GREEN}{'='*56}{RESET}")
        else:
            print(f"{RED}{BOLD}✖ Snake generation failed!{RESET}")
            print(f"{RED}{'='*56}{RESET}")
            
    except Exception as e:
        print(f"{RED}{BOLD}‼ Error during snake generation:{RESET} {e}")
        print(f"{RED}{'='*56}{RESET}")

if __name__ == "__main__":
    run_snake_cli()
