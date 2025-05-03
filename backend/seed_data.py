"""
Seed data generator for the Claim Action Intelligence application.
Creates sample claims, email threads, and action items for demo purposes.
"""
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# Add the parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models.models import Base, Claim, EmailThread, ActionItem, ClaimStatus, ActionItemStatus

load_dotenv()

def create_seed_data():
    """Create sample data for the application"""
    db = SessionLocal()
    try:
        print("Creating sample data...")
        
        # Create sample claims
        claims = [
            Claim(claim_number="CL-2023-001", company="Acme Insurance", status=ClaimStatus.OPEN),
            Claim(claim_number="CL-2023-002", company="Beta Protection", status=ClaimStatus.PENDING),
            Claim(claim_number="CL-2023-003", company="Century Assurance", status=ClaimStatus.OPEN)
        ]
        
        for claim in claims:
            db.add(claim)
        
        db.commit()
        
        # Sample email threads
        email_threads = [
            # Claim 1 emails
            EmailThread(
                claim_id=1,
                subject="Re: Initial assessment for claim CL-2023-001",
                raw_body="Hi Team,\n\nI've completed the initial assessment for claim CL-2023-001. The property damage is estimated at $15,000. We need to schedule an adjuster visit by next week.\n\nRegards,\nSarah",
                clean_body="Hi Team,\n\nI've completed the initial assessment for claim CL-2023-001. The property damage is estimated at $15,000. We need to schedule an adjuster visit by next week.\n\nRegards,\nSarah",
                timestamp=datetime.utcnow() - timedelta(days=10)
            ),
            EmailThread(
                claim_id=1,
                subject="Documentation needed for claim CL-2023-001",
                raw_body="Hello,\n\nWe need additional documentation for this claim. Please provide photos of the damage and the original purchase receipts by Friday.\n\nThanks,\nMike",
                clean_body="Hello,\n\nWe need additional documentation for this claim. Please provide photos of the damage and the original purchase receipts by Friday.\n\nThanks,\nMike",
                timestamp=datetime.utcnow() - timedelta(days=5)
            ),
            
            # Claim 2 emails
            EmailThread(
                claim_id=2,
                subject="Claim CL-2023-002 - Medical evaluation required",
                raw_body="Dear Dr. Johnson,\n\nWe would like to request a medical evaluation for the claimant in case CL-2023-002. Please let us know your availability in the next two weeks.\n\nBest regards,\nClaire Williams\nBeta Protection",
                clean_body="Dear Dr. Johnson,\n\nWe would like to request a medical evaluation for the claimant in case CL-2023-002. Please let us know your availability in the next two weeks.\n\nBest regards,\nClaire Williams\nBeta Protection",
                timestamp=datetime.utcnow() - timedelta(days=8)
            ),
            
            # Claim 3 emails
            EmailThread(
                claim_id=3,
                subject="Update on claim CL-2023-003",
                raw_body="Hi team,\n\nJust an update on CL-2023-003: We've received all required documentation. We need to review and approve the claim by next Monday. Also, we need to notify the policyholder about the deductible amount.\n\nCheers,\nDavid",
                clean_body="Hi team,\n\nJust an update on CL-2023-003: We've received all required documentation. We need to review and approve the claim by next Monday. Also, we need to notify the policyholder about the deductible amount.\n\nCheers,\nDavid",
                timestamp=datetime.utcnow() - timedelta(days=3)
            ),
            EmailThread(
                claim_id=3,
                subject="Re: Update on claim CL-2023-003",
                raw_body="David,\n\nI've started reviewing the documentation. There are some inconsistencies in the repair estimates. Let's schedule a call with the contractor to discuss.\n\nRegards,\nEmily",
                clean_body="David,\n\nI've started reviewing the documentation. There are some inconsistencies in the repair estimates. Let's schedule a call with the contractor to discuss.\n\nRegards,\nEmily",
                timestamp=datetime.utcnow() - timedelta(days=1)
            ),
        ]
        
        for email in email_threads:
            db.add(email)
        
        db.commit()
        
        # Sample action items
        action_items = [
            # Claim 1 actions
            ActionItem(
                claim_id=1,
                thread_id=1,
                description="Schedule adjuster visit for claim CL-2023-001",
                assignee="Sarah",
                due_date=datetime.utcnow() + timedelta(days=7),
                status=ActionItemStatus.TODO,
                confidence=0.95
            ),
            ActionItem(
                claim_id=1,
                thread_id=2,
                description="Collect photos of property damage",
                assignee="Claimant",
                due_date=datetime.utcnow() + timedelta(days=2),
                status=ActionItemStatus.IN_PROGRESS,
                confidence=0.92
            ),
            ActionItem(
                claim_id=1,
                thread_id=2,
                description="Gather original purchase receipts",
                assignee="Claimant",
                due_date=datetime.utcnow() + timedelta(days=2),
                status=ActionItemStatus.TODO,
                confidence=0.88
            ),
            
            # Claim 2 actions
            ActionItem(
                claim_id=2,
                thread_id=3,
                description="Schedule medical evaluation with Dr. Johnson",
                assignee="Claire",
                due_date=datetime.utcnow() + timedelta(days=14),
                status=ActionItemStatus.TODO,
                confidence=0.96
            ),
            ActionItem(
                claim_id=2,
                thread_id=3,
                description="Confirm claimant availability for medical evaluation",
                assignee="Claire",
                due_date=datetime.utcnow() + timedelta(days=3),
                status=ActionItemStatus.COMPLETED,
                completed_at=datetime.utcnow() - timedelta(days=1),
                confidence=0.90
            ),
            
            # Claim 3 actions
            ActionItem(
                claim_id=3,
                thread_id=4,
                description="Review and approve claim CL-2023-003",
                assignee="David",
                due_date=datetime.utcnow() + timedelta(days=5),
                status=ActionItemStatus.IN_PROGRESS,
                confidence=0.97
            ),
            ActionItem(
                claim_id=3,
                thread_id=4,
                description="Notify policyholder about deductible amount",
                assignee="David",
                due_date=datetime.utcnow() + timedelta(days=7),
                status=ActionItemStatus.TODO,
                confidence=0.94
            ),
            ActionItem(
                claim_id=3,
                thread_id=5,
                description="Schedule call with contractor to discuss repair estimates",
                assignee="Emily",
                due_date=datetime.utcnow() + timedelta(days=3),
                status=ActionItemStatus.TODO,
                confidence=0.91
            ),
        ]
        
        for item in action_items:
            db.add(item)
        
        db.commit()
        
        print(f"Successfully created {len(claims)} claims, {len(email_threads)} email threads, and {len(action_items)} action items.")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating seed data: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables first (if they don't exist)
    Base.metadata.create_all(bind=engine)
    
    # Create seed data
    create_seed_data() 