from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import groq
import os
from dotenv import load_dotenv
import base64
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "AgriConnect Backend Running!"}

@app.post("/chat")
async def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are AgriConnect AI, a helpful farming assistant for beginner farmers in Karnataka, India. Give simple, practical advice about crops, pests, soil, weather and farming. Keep answers short and easy to understand."
            },
            {
                "role": "user",
                "content": req.message
            }
        ]
    )
    return {"reply": response.choices[0].message.content}

@app.post("/disease")
async def detect_disease(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
        
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "You are an expert agriculture assistant. Look at this crop leaf image and tell me the disease and cure. Format your response exactly like this:\nDisease: [Name]\nCure: [Detailed Solution]"
                        }
                    ]
                }
            ]
        )
        
        reply = response.choices[0].message.content
        logger.info(f"AI Response: {reply}")



        # Use regex for more robust parsing
        disease_match = re.search(r"Disease:\s*(.*)", reply, re.IGNORECASE)
        cure_match = re.search(r"Cure:\s*([\s\S]*)", reply, re.IGNORECASE)

        disease = disease_match.group(1).strip() if disease_match else "Unknown Issue"
        cure = cure_match.group(1).strip() if cure_match else reply

        return {"disease": disease, "cure": cure}
    except Exception as e:
        logger.error(f"Error in detect_disease: {str(e)}")
        return {"error": "Failed to process image", "details": str(e)}
