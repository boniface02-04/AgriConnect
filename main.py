from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import groq
import os
from dotenv import load_dotenv
import base64

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
        model="llama3-8b-8192",
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
    image_data = await file.read()
    base64_image = base64.b64encode(image_data).decode("utf-8")
    
    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
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
                        "text": "You are an expert agriculture assistant. Look at this crop leaf image and tell me: 1) What disease or problem do you see? 2) What is the cure or solution? Keep it simple and practical for a beginner farmer in India."
                    }
                ]
            }
        ]
    )
    
    reply = response.choices[0].message.content
    parts = reply.split("\n", 1)
    disease = parts[0] if parts else "Unknown"
    cure = parts[1] if len(parts) > 1 else reply
    
    return {"disease": disease, "cure": cure}
