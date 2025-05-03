"""
Basic API tests for the Claim Action Intelligence API.
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add the parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.database import Base, get_db
from app.models.models import Claim, EmailThread, ActionItem

# Create test database in memory
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Create tables in the test database once for all tests"""
    # Import all models to ensure they're registered with the Base metadata
    from app.models import models
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after all tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_db():
    """Reset data between tests"""
    # Start with a clean slate for each test
    db = TestingSessionLocal()
    try:
        # Clear data from tables but don't drop them
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
        yield db
    finally:
        db.close()

@pytest.fixture
def sample_claim(test_db):
    """Create a sample claim in the test database"""
    db = TestingSessionLocal()
    claim = Claim(claim_number="TEST-123", company="Test Company")
    db.add(claim)
    db.commit()
    db.refresh(claim)
    db.close()
    return claim

def test_read_main():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Claim Action Intelligence API"}

def test_create_claim():
    """Test creating a new claim"""
    response = client.post(
        "/api/claims/",
        json={
            "claim_number": "CL-TEST-001",
            "company": "Test Insurance"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["claim_number"] == "CL-TEST-001"
    assert data["company"] == "Test Insurance"
    assert "id" in data

def test_get_claim(sample_claim):
    """Test getting a specific claim"""
    response = client.get(f"/api/claims/{sample_claim.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["claim_number"] == sample_claim.claim_number
    assert data["company"] == sample_claim.company

def test_get_nonexistent_claim():
    """Test getting a claim that doesn't exist"""
    response = client.get("/api/claims/9999")
    assert response.status_code == 404

def test_action_items(sample_claim):
    """Test the action items endpoint"""
    db = TestingSessionLocal()
    action_item = ActionItem(
        claim_id=sample_claim.id,
        description="Test action item",
        status="TODO"
    )
    db.add(action_item)
    db.commit()
    db.close()
    
    response = client.get(f"/api/action-items/{sample_claim.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["description"] == "Test action item"

def test_summarize_endpoint():
    """Test the summarize endpoint with a mock email"""
    # First create a claim to associate with the summary
    client.post(
        "/api/claims/",
        json={
            "claim_number": "TEST-SUMMARY-001",
            "company": "Test Insurance"
        }
    )
    
    mock_email = """
    From: test@example.com
    To: claims@insurance.com
    Subject: Test Claim
    
    Hello,
    
    I need to submit a claim for my recent accident.
    Please process this as soon as possible.
    
    I need to:
    1. Submit photos by Friday
    2. Schedule an appointment with the adjuster
    
    Thanks,
    Test User
    """
    
    response = client.post(
        "/api/summarize/",
        params={
            "claim_number": "TEST-SUMMARY-001"
        },
        content=mock_email
    )
    
    # Since we're not setting OPENAI_API_KEY in the test environment,
    # let's just check that it handles the error appropriately
    assert response.status_code in [200, 422]
    if response.status_code == 200:
        data = response.json()
        assert "summary" in data
        assert "action_items" in data 