"""
Configuration Utilities Module

This module provides utilities for loading and managing configuration settings.
"""

import os
import yaml
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary containing the configuration
    """
    # Check if file exists
    if not os.path.exists(config_path):
        logger.warning(f"Configuration file not found: {config_path}")
        return {}
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"Loaded configuration from {config_path}")
        return config or {}
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        return {}

def get_config_value(config: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    Get a value from a nested configuration dictionary using a dot-separated path.
    
    Args:
        config: Configuration dictionary
        key_path: Dot-separated path to the desired value (e.g., "ai.model")
        default: Default value to return if the path doesn't exist
        
    Returns:
        The value at the specified path, or the default if not found
    """
    if not config:
        return default
    
    keys = key_path.split('.')
    current = config
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current 