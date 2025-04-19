from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API Proxy is running"}

# Example protected endpoint
@app.get("/api/protected")
async def protected_route():
    api_key = os.getenv("EXAMPLE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, message="API key not configured")
    return {"message": "This is a protected route"}