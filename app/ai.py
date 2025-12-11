from fastapi import APIRouter
import ollama

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/chat")
async def chat(prompt: str):
    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"response": response["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}
