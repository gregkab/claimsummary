from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..models import ActionItem, ActionItemUpdate, ActionItemSchema, Claim

router = APIRouter(
    prefix="/api/action-items",
    tags=["action-items"]
)

@router.get("/{claim_id}", response_model=List[ActionItemSchema])
def read_action_items(claim_id: int, status: str = None, db: Session = Depends(get_db)):
    """
    Get action items for a specific claim with optional status filter
    """
    # Check if claim exists
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Claim with id {claim_id} not found"
        )
    
    # Query action items
    query = db.query(ActionItem).filter(ActionItem.claim_id == claim_id)
    
    # Filter by status if provided
    if status:
        query = query.filter(ActionItem.status == status)
    
    return query.all()

@router.patch("/{item_id}", response_model=ActionItemSchema)
def update_action_item(item_id: int, item_update: ActionItemUpdate, db: Session = Depends(get_db)):
    """
    Update an action item (mark complete, change status, update due date, etc.)
    """
    # Find the action item
    db_item = db.query(ActionItem).filter(ActionItem.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action item with id {item_id} not found"
        )
    
    # Update item attributes
    update_data = item_update.dict(exclude_unset=True)
    
    # If status is being changed to COMPLETED, set completed_at timestamp
    if update_data.get("status") == "COMPLETED" and db_item.status != "COMPLETED":
        update_data["completed_at"] = datetime.utcnow()
    
    # Apply updates
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_action_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete an action item
    """
    db_item = db.query(ActionItem).filter(ActionItem.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action item with id {item_id} not found"
        )
    
    db.delete(db_item)
    db.commit()
    return None 