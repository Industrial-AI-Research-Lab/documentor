"""Load environment variables from .env file."""

import os
from pathlib import Path
from typing import Optional


def load_env_file(env_file: Optional[Path] = None) -> None:
    """
    Load environment variables from .env file.
    
    Args:
        env_file: Path to .env file. If None, searches for .env in current directory and parent directories.
    """
    if env_file is None:
        # Search for .env file in current directory and parent directories
        current_dir = Path.cwd()
        for parent in [current_dir] + list(current_dir.parents):
            env_file = parent / ".env"
            if env_file.exists():
                break
        else:
            # No .env file found
            return
    
    if not env_file.exists():
        return
    
    # Load .env file
    with open(env_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse key=value pairs
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                # Set environment variable if not already set
                if key not in os.environ:
                    os.environ[key] = value
            else:
                print(f"Warning: Invalid line {line_num} in {env_file}: {line}")


# Auto-load .env file when module is imported
load_env_file()
