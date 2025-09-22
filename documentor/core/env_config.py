"""Environment configuration management for Documentor."""

import os
from pathlib import Path
from typing import Any, Optional, Union, List
from dataclasses import dataclass


@dataclass
class EnvConfig:
    """Environment configuration manager."""
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get environment variable value."""
        return os.getenv(key, default)
    
    def get_str(self, key: str, default: str = "") -> str:
        """Get string environment variable."""
        return os.getenv(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer environment variable."""
        try:
            return int(os.getenv(key, str(default)))
        except (ValueError, TypeError):
            return default
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get float environment variable."""
        try:
            return float(os.getenv(key, str(default)))
        except (ValueError, TypeError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean environment variable."""
        value = os.getenv(key, "").lower()
        if value in ("true", "1", "yes", "on"):
            return True
        elif value in ("false", "0", "no", "off"):
            return False
        return default
    
    def get_path(self, key: str, default: Optional[Path] = None) -> Optional[Path]:
        """Get path environment variable."""
        value = os.getenv(key)
        if value:
            return Path(value)
        return default
    
    def get_list(self, key: str, separator: str = ",", default: Optional[List[str]] = None) -> List[str]:
        """Get list environment variable."""
        value = os.getenv(key)
        if value:
            return [item.strip() for item in value.split(separator) if item.strip()]
        return default or []
    
    def get_set(self, key: str, separator: str = ",", default: Optional[set] = None) -> set:
        """Get set environment variable."""
        return set(self.get_list(key, separator, list(default or [])))


# Global environment config instance
env = EnvConfig()
