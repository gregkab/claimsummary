from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import claims, action_items, summarizer

app = FastAPI(title="Claim Action Intelligence API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(claims.router)
app.include_router(action_items.router)
app.include_router(summarizer.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Claim Action Intelligence API"} 