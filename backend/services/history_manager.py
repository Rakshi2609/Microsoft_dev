"""
History Manager Service
Manages scan history storage and retrieval
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
import uuid

logger = logging.getLogger(__name__)

# Path to history data file
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def load_history() -> List[Dict[str, Any]]:
    """
    Load scan history from file
    
    Returns:
        List of scan records
    """
    
    try:
        if not os.path.exists(HISTORY_FILE):
            return []
        
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
        
        return history
    
    except json.JSONDecodeError:
        logger.error("Corrupted history file, returning empty list")
        return []
    except Exception as e:
        logger.error(f"Error loading history: {str(e)}")
        return []

def save_history(history: List[Dict[str, Any]]) -> bool:
    """
    Save scan history to file
    
    Args:
        history: List of scan records
    
    Returns:
        Success status
    """
    
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        
        return True
    
    except Exception as e:
        logger.error(f"Error saving history: {str(e)}")
        return False

def save_scan_result(result: Dict[str, Any]) -> bool:
    """
    Save a new scan result to history
    
    Args:
        result: Scan result dictionary
    
    Returns:
        Success status
    """
    
    try:
        # Load existing history
        history = load_history()
        
        # Add unique ID if not present
        if "id" not in result:
            result["id"] = str(uuid.uuid4())
        
        # Add timestamp if not present
        if "timestamp" not in result:
            result["timestamp"] = datetime.now().isoformat()
        
        # Prepend to history (newest first)
        history.insert(0, result)
        
        # Limit history size (keep last 100 scans)
        history = history[:100]
        
        # Save
        success = save_history(history)
        
        if success:
            logger.info(f"Scan result saved: {result['id']}")
        
        return success
    
    except Exception as e:
        logger.error(f"Error saving scan result: {str(e)}")
        return False

def get_all_history() -> List[Dict[str, Any]]:
    """
    Retrieve all scan history records
    
    Returns:
        List of scan records (newest first)
    """
    
    return load_history()

def get_history_by_id(scan_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a specific scan result by ID
    
    Args:
        scan_id: Unique scan identifier
    
    Returns:
        Scan result or None if not found
    """
    
    try:
        history = load_history()
        
        for scan in history:
            if scan.get("id") == scan_id:
                return scan
        
        return None
    
    except Exception as e:
        logger.error(f"Error retrieving scan by ID: {str(e)}")
        return None

def clear_history() -> bool:
    """
    Clear all scan history
    
    Returns:
        Success status
    """
    
    try:
        return save_history([])
    
    except Exception as e:
        logger.error(f"Error clearing history: {str(e)}")
        return False

def get_history_by_risk_level(risk_level: str) -> List[Dict[str, Any]]:
    """
    Filter history by risk level
    
    Args:
        risk_level: Risk level to filter by ("Low", "Medium", "High")
    
    Returns:
        Filtered list of scans
    """
    
    try:
        history = load_history()
        
        filtered = [
            scan for scan in history
            if scan.get("risk", "").lower() == risk_level.lower()
        ]
        
        return filtered
    
    except Exception as e:
        logger.error(f"Error filtering history: {str(e)}")
        return []

def get_recent_scans(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get most recent scans
    
    Args:
        limit: Maximum number of scans to return
    
    Returns:
        List of recent scans
    """
    
    try:
        history = load_history()
        return history[:limit]
    
    except Exception as e:
        logger.error(f"Error retrieving recent scans: {str(e)}")
        return []
