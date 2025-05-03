from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Claim, ClaimCreate, ClaimSchema

router = APIRouter(
    prefix="/api/claims",
    tags=["claims"]
)

@router.post("/", response_model=ClaimSchema)
def create_claim(claim: ClaimCreate, db: Session = Depends(get_db)):
    """
    Create a new claim
    """
    # Check if claim already exists
    db_claim = db.query(Claim).filter(Claim.claim_number == claim.claim_number).first()
    if db_claim:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Claim with number {claim.claim_number} already exists"
        )
    
    # Create new claim
    db_claim = Claim(**claim.dict())
    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)
    return db_claim

@router.get("/", response_model=List[ClaimSchema])
def read_claims(skip: int = 0, limit: int = 100, search: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all claims with optional search
    """
    query = db.query(Claim)
    
    if search:
        # Search by claim number or company
        query = query.filter(
            (Claim.claim_number.ilike(f"%{search}%")) | 
            (Claim.company.ilike(f"%{search}%"))
        )
    
    return query.offset(skip).limit(limit).all()

@router.get("/{claim_id}", response_model=ClaimSchema)
def read_claim(claim_id: int, db: Session = Depends(get_db)):
    """
    Get a specific claim by ID
    """
    db_claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if db_claim is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Claim with id {claim_id} not found"
        )
    return db_claim

@router.delete("/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_claim(claim_id: int, db: Session = Depends(get_db)):
    """
    Delete a claim
    """
    db_claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if db_claim is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Claim with id {claim_id} not found"
        )
    
    db.delete(db_claim)
    db.commit()
    return None 