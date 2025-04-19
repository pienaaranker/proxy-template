from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import google.generativeai as genai
from pydantic import BaseModel

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GeminiRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 1000

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

@app.post("/api/gemini")
async def gemini_completion(request: GeminiRequest):
    try:
        # Get the API key from environment variables
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Gemini API key not configured")

        # Configure the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Generate the response
        response = model.generate_content(
            request.prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=request.temperature,
                max_output_tokens=request.max_tokens,
            )
        )
        
        return {
            "response": response.text,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))