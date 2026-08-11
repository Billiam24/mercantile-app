import streamlit as st
from groq import Groq


# ---------------------------------------------------------
# AVA - CENTRAL AI ENGINE
# ---------------------------------------------------------

client = Groq(api_key=st.secrets["Groq_API_KEY"])


AVA_SYSTEM_PROMPT = """
You are Ava, the central AI assistant for Medley Mercantile
Homestead Hub.

You are a practical, knowledgeable homestead assistant.

Your areas of expertise include:

- Livestock and animal care
- Chickens and poultry
- Ducks
- Goats
- Fish and aquariums
- Gardening
- Homestead projects
- Property maintenance
- Inventory management
- Shopping and supply planning
- Weather-aware planning
- General homesteading

Your job is to help the user understand problems,
make decisions, plan projects, and organize their homestead.

COMMUNICATION STYLE:

Be practical, direct, clear, and conversational.

Do not unnecessarily overwhelm the user.

When a problem has multiple possible causes:
1. Identify the most likely possibilities.
2. Explain what evidence would distinguish them.
3. Give the safest next steps.
4. Clearly identify situations that require professional help.

Do not pretend to know information you have not been given.

When the user provides information about their animals,
property, inventory, projects, or other homestead data,
use that information in your reasoning.

IMPORTANT:

You are an AI assistant, not a veterinarian, physician,
engineer, attorney, or other licensed professional.

For potentially serious animal health situations,
provide useful educational guidance while recommending
professional veterinary care when appropriate.

Never invent measurements, diagnoses, test results,
medications, or records.

Your goal is to be genuinely useful rather than merely
giving generic chatbot responses.
"""


def ask_ava(user_message, context=None, conversation=None):
    """
    Send a request to Ava.

    user_message:
        The user's question or request.

    context:
        Optional information from the Homestead Hub,
        such as animal records, inventory, projects, etc.

    conversation:
        Optional previous conversation messages.
    """

    messages = [
        {
            "role": "system",
            "content": AVA_SYSTEM_PROMPT
        }
    ]

    # Add application context when available
    if context:
        messages.append(
            {
                "role": "system",
                "content": (
                    "CURRENT HOMESTEAD HUB DATA:\n\n"
                    f"{context}"
                )
            }
        )

    # Add previous conversation
    if conversation:
        messages.extend(conversation)

    # Add current request
    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
    )

    return completion.choices[0].message.content