from fastapi import FastAPI
from healthcare_graph import app

api = FastAPI()

@api.get("/")
def home():
    return {"message": "Healthcare AI API running"}

@api.post("/chat")
def chat(request: dict):

    try:
        result = app.invoke({
            "patient_id": request["patient_id"],
            "user_input": request["user_input"]
        })

        return {
            "response": result.get("response", "No response")
        }

    except Exception as e:
        return {
            "response": str(e)
        }