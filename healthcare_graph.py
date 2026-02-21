# healthcare_graph.py
from typing import TypedDict
from langgraph.graph import StateGraph, END
from db_utils import get_patient_data, get_prescriptions, book_appointment

import dateparser
from langchain_community.llms import Ollama

# Local LLM (No OpenAI Key Required)
llm = Ollama(model="llama3")


# -----------------------------
# 1️⃣ Define State Structure
# -----------------------------
class HealthcareState(TypedDict):
    patient_id: str
    user_input: str
    intent: str
    response: str


# -----------------------------
# 2️⃣ Detect User Intent (LLM Enhanced)
# -----------------------------
def detect_intent(state: HealthcareState):

    text = state["user_input"].lower()

    if "medicine" in text or "prescription" in text:
        state["intent"] = "prescriptions"

    elif "profile" in text:
        state["intent"] = "profile"

    elif "book" in text or "appointment" in text:
        state["intent"] = "appointment"

    else:
        state["intent"] = "unknown"

    return state


# -----------------------------
# 3️⃣ Profile Node
# -----------------------------
def profile_node(state: HealthcareState):

    data = get_patient_data(state["patient_id"])

    if not data:
        state["response"] = "Patient not found."
        return state

    state["response"] = f"""
Patient Profile
---------------
Name: {data.get('name')}
Age: {data.get('age')}
Blood Group: {data.get('blood_group')}
"""

    return state


# -----------------------------
# 4️⃣ Prescription Node
# -----------------------------
def prescription_node(state: HealthcareState):

    meds = get_prescriptions(state["patient_id"])

    if not meds:
        state["response"] = "No prescriptions found."
        return state

    formatted = "Prescriptions:\n----------------\n"

    for med in meds:
        formatted += f"- {med.get('medicine')} ({med.get('dosage')})\n"

    state["response"] = formatted

    return state


# -----------------------------
# 5️⃣ Appointment Node (Natural Language AI Booking)
# -----------------------------
def appointment_node(state: HealthcareState):

    user_text = state["user_input"]

    # Extract date & time using NLP parsing
    parsed_date = dateparser.parse(user_text)

    if parsed_date:
        date_str = parsed_date.strftime("%Y-%m-%d")
        time_str = parsed_date.strftime("%I:%M %p")
    else:
        # Default demo values
        date_str = "2026-03-10"
        time_str = "10:00 AM"

    message = book_appointment(
        state["patient_id"],
        "Dr Smith",
        date_str,
        time_str
    )

    state["response"] = f"""
✅ Appointment Booking Result

Doctor: Dr Smith
Date: {date_str}
Time: {time_str}

{message}
"""

    return state


# -----------------------------
# 6️⃣ Route Intent
# -----------------------------
def route_intent(state: HealthcareState):

    if state["intent"] == "profile":
        return "profile_node"

    elif state["intent"] == "prescriptions":
        return "prescription_node"

    elif state["intent"] == "appointment":
        return "appointment_node"

    return END


# -----------------------------
# 7️⃣ Build Graph
# -----------------------------
builder = StateGraph(HealthcareState)

builder.add_node("detect_intent", detect_intent)
builder.add_node("profile_node", profile_node)
builder.add_node("prescription_node", prescription_node)
builder.add_node("appointment_node", appointment_node)

builder.set_entry_point("detect_intent")

builder.add_conditional_edges(
    "detect_intent",
    route_intent
)

builder.add_edge("profile_node", END)
builder.add_edge("prescription_node", END)
builder.add_edge("appointment_node", END)

app = builder.compile()