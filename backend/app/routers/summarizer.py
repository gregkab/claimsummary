from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..models import Claim, EmailThread, ActionItem, EmailThreadCreate, SummaryResponse
from ..utils.email_parser import parse_email_content
from ..utils.openai_helper import claims_agent

router = APIRouter(
    prefix="/api/summarize",
    tags=["summarizer"]
)

@router.post("/", response_model=SummaryResponse)
async def summarize_email(
    raw_email: str, 
    claim_number: str,
    db: Session = Depends(get_db)
):
    """
    Process an email, extract action items, and save to database
    """
    # Find or create the claim
    claim = db.query(Claim).filter(Claim.claim_number == claim_number).first()
    if not claim:
        # Create new claim if it doesn't exist
        claim = Claim(claim_number=claim_number)
        db.add(claim)
        db.commit()
        db.refresh(claim)
    
    # Parse the email
    email_data = parse_email_content(raw_email)
    
    # Create an email thread record
    email_thread = EmailThread(
        claim_id=claim.id,
        subject=email_data["subject"],
        raw_body=email_data["raw_body"],
        clean_body=email_data["clean_body"],
        timestamp=email_data["timestamp"]
    )
    db.add(email_thread)
    db.commit()
    db.refresh(email_thread)
    
    # Extract action items using OpenAI via the claims agent
    result = claims_agent.extract_action_items(email_data["clean_body"], claim.id)
    
    # Save action items to database
    for item_data in result.get("action_items", []):
        action_item = ActionItem(
            claim_id=claim.id,
            thread_id=email_thread.id,
            description=item_data["description"],
            assignee=item_data.get("assignee"),
            due_date=item_data.get("due_date"),
            confidence=item_data.get("confidence", 1.0),
        )
        db.add(action_item)
    
    db.commit()
    
    # Return summary and action items
    return {
        "summary": result.get("summary", "No summary available"),
        "action_items": result.get("action_items", [])
    } 