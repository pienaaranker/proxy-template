from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import google.generativeai as genai
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.error("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=api_key)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://squabbl.vercel.app",
        "http://localhost:3000",  # For local development
        "https://*.ngrok.io",     # For ngrok.io domains
        "https://*.ngrok-free.app",  # For newer ngrok-free.app domains
    ],
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
        raise HTTPException(status_code=500, detail="API key not configured")
    return {"message": "This is a protected route"}

@app.post("/api/gemini")
async def gemini_completion(request: GeminiRequest):
    try:
        logger.info(f"Received request with prompt: {request.prompt[:100]}...")
        
        # Get the API key from environment variables
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("Gemini API key not configured")
            raise HTTPException(
                status_code=500,
                detail="Gemini API key not configured"
            )

        # Configure the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        logger.info(f"Generating content with temperature={request.temperature}, max_tokens={request.max_tokens}")
        
        # Generate the response
        generation_config = genai.types.GenerationConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_tokens,
        )
        
        response = model.generate_content(
            request.prompt,
            generation_config=generation_config
        )
        
        # Log the response
        logger.info(f"Generated response: {str(response.text)[:500]}...")
        
        if not response.text:
            logger.error("Empty response received from Gemini API")
            raise HTTPException(
                status_code=500,
                detail="Empty response received from Gemini API"
            )
            
        # Return the response
        return {
            "response": response.text,
            "status": "success",
            "prompt": request.prompt,
            "model": "gemini-pro"
        }
        
    except Exception as e:
        logger.error(f"Error in gemini_completion: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )