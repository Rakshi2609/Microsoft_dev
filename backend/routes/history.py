"""
History Route - Scan History Management
Retrieve and manage scan history records
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging

from services.history_manager import get_all_history, get_history_by_id, clear_history

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/history")
async def get_history() -> List[Dict[str, Any]]:
    """
    Retrieve all scan history records
    
    Returns:
        List of scan results sorted by timestamp (newest first)
    """
    try:
        history = get_all_history()
        logger.info(f"Retrieved {len(history)} history records")
        return history
    
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve history: {str(e)}"
        )

@router.get("/history/{scan_id}")
async def get_history_item(scan_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific scan result by ID
    
    Args:
        scan_id: Unique identifier for the scan
    
    Returns:
        Scan result details
    """
    try:
        result = get_history_by_id(scan_id)
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Scan with ID '{scan_id}' not found"
            )
        
        return result
    
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error retrieving history item: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve history item: {str(e)}"
        )

@router.delete("/history")
async def delete_history():
    """
    Clear all scan history
    
    Returns:
        Success confirmation
    """
    try:
        clear_history()
        logger.info("History cleared successfully")
        return {
            "message": "History cleared successfully",
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"Error clearing history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear history: {str(e)}"
        )

@router.get("/history/stats/summary")
async def get_history_stats() -> Dict[str, Any]:
    """
    Get statistical summary of scan history
    
    Returns:
        Statistics including risk distribution and trends
    """
    try:
        history = get_all_history()
        
        if not history:
            return {
                "total_scans": 0,
                "risk_distribution": {
                    "low": 0,
                    "medium": 0,
                    "high": 0
                },
                "average_confidence": 0.0,
                "average_score": 0.0
            }
        
        # Calculate statistics
        risk_counts = {"Low": 0, "Medium": 0, "High": 0}
        total_confidence = 0.0
        total_score = 0.0
        
        for scan in history:
            risk = scan.get("risk", "Low")
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
            total_confidence += scan.get("confidence", 0)
            total_score += scan.get("score", 0)
        
        num_scans = len(history)
        
        return {
            "total_scans": num_scans,
            "risk_distribution": {
                "low": risk_counts.get("Low", 0),
                "medium": risk_counts.get("Medium", 0),
                "high": risk_counts.get("High", 0)
            },
            "average_confidence": round(total_confidence / num_scans, 2),
            "average_score": round(total_score / num_scans, 2),
            "latest_scan": history[0].get("timestamp") if history else None
        }
    
    except Exception as e:
        logger.error(f"Error calculating stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate statistics: {str(e)}"
        )
