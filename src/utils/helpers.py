"""
Utility functions for the project
"""

import logging
from datetime import datetime
from pathlib import Path

def setup_logger(name, log_file=None):
    """Configure logger for the module"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def validate_date(date_str):
    """Check if date is in YYYY-MM-DD format"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False

def map_risk_to_string(risk_code):
    """Convert numeric risk (0,1,2) to string label"""
    mapping = {0: 'Low', 1: 'Medium', 2: 'High'}
    return mapping.get(risk_code, 'Unknown')

def ensure_dir(path):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path

def calculate_heat_index(temp, humidity):
    """Calculate heat index from temperature and humidity"""
    return temp + (0.12 * humidity)