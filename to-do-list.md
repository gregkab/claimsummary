# Claim Action Intelligence MVP - To-Do List

## 1. Project Setup
- [x] Initialize GitHub repository
- [x] Create basic README.md
- [x] Set up project structure (backend and frontend folders)
- [x] Configure git ignore files

## 2. Backend Development (FastAPI)
- [x] Set up FastAPI project structure
- [x] Configure PostgreSQL database connection
- [x] Create database models:
  - [x] `Claim`: id, claim_number, external_id, company, status
  - [x] `EmailThread`: id, claim_id, subject, raw_body, clean_body, timestamp
  - [x] `ActionItem`: id, claim_id, thread_id, description, status, assignee, due_date, confidence, created_at, completed_at
- [x] Implement database migrations
- [x] Create API endpoints:
  - [x] `POST /api/claims/` - create/search claims
  - [x] `POST /api/summarize/` - process email and generate action items
  - [x] `GET /api/claims/{id}/action-items/` - retrieve action items for a claim
  - [x] `PATCH /api/action-items/{id}` - update action item status
- [x] Implement email parsing functionality
  - [x] Use `mailparser` or `email.message` to clean forwarded email bodies
  - [x] Normalize timestamps, remove signatures
- [x] Integrate OpenAI GPT-4
  - [x] Create prompt template for email analysis
  - [x] Implement JSON response parsing
  - [x] Add error handling for API calls
- [x] Set up logging for LLM prompts and responses
- [x] Write basic tests for API endpoints
- [x] Create sample seed data (3 claims, 5 emails, 8 action items)

## 3. Frontend Development (React + TailwindCSS)
- [x] Set up React project with TailwindCSS
- [x] Create basic component structure
- [x] Implement pages:
  - [x] Claim List Page
    - [x] Search functionality
    - [x] Claim selection
  - [x] Claim Detail Page
    - [x] Claim metadata display
    - [x] Email thread display (last 3)
    - [x] Action items table with filtering
    - [x] Complete/update action item functionality
  - [x] Email Submission Component
    - [x] Text area for email content
    - [x] Submit button to trigger analysis
- [x] Set up API integration with backend
- [x] Implement responsive design with TailwindCSS
- [x] Add basic error handling and loading states

## 4. Infrastructure Setup
- [ ] Set up backend deployment on Railway or Render
- [ ] Configure PostgreSQL database on Supabase or Neon
- [ ] Deploy frontend to Vercel
- [ ] Configure environment variables:
  - [ ] OpenAI API key
  - [ ] Database URL
  - [ ] Frontend URL

## 5. Integration and Testing
- [ ] Connect frontend to backend API
- [ ] Test complete workflow: email submission → action item extraction → display
- [ ] Debug and fix issues
- [ ] Create Postman collection or curl documentation
- [ ] Perform end-to-end testing

## 6. Documentation and Finalization
- [ ] Update README with setup instructions
- [ ] Document API endpoints
- [ ] Create Loom walkthrough (optional)
- [ ] Prepare demo with sample data
- [ ] Share hosted demo URL

## Optional Stretch Goals (If Time Permits)
- [ ] Implement PDF export of action items
- [ ] Add weekly email digest functionality
- [ ] Add sorting by oldest open task
- [ ] Implement basic authentication 