from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Claim Schemas
class ClaimBase(BaseModel):
    claim_number: str
    external_id: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = "OPEN"


class ClaimCreate(ClaimBase):
    pass


class Claim(ClaimBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Email Thread Schemas
class EmailThreadBase(BaseModel):
    subject: Optional[str] = None
    raw_body: str
    clean_body: Optional[str] = None
    timestamp: Optional[datetime] = None


class EmailThreadCreate(EmailThreadBase):
    claim_id: int


class EmailThread(EmailThreadBase):
    id: int
    claim_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Action Item Schemas
class ActionItemBase(BaseModel):
    description: str
    status: Optional[str] = "TODO"
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    confidence: Optional[float] = 1.0


class ActionItemCreate(ActionItemBase):
    claim_id: int
    thread_id: Optional[int] = None


class ActionItemUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class ActionItem(ActionItemBase):
    id: int
    claim_id: int
    thread_id: Optional[int] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Summary Response Schema
class SummaryResponse(BaseModel):
    summary: str
    action_items: List[ActionItemCreate] 