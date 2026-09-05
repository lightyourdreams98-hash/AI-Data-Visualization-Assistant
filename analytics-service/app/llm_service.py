import os

from openai import OpenAI
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# OPENAI CLIENT
# ============================================================

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# ============================================================
# GENERATE AI ANSWER
# ============================================================

def generate_llm_answer(
    question,
    analysis,
    dataset_info
):

    prompt = f"""
You are an AI Data Analysis Assistant.

Your job is to answer questions about a user's dataset.

IMPORTANT RULES:

1. Use ONLY the information provided below.
2. Do not invent values.
3. Do not perform calculations that contradict the
   provided analysis.
4. Explain the result clearly.
5. Keep the answer concise but useful.
6. If the analysis contains an error, explain the error.
7. Do not claim that you analyzed data that is not provided.

USER QUESTION:
{question}

DATASET INFORMATION:
{dataset_info}

ANALYTICAL RESULT:
{analysis}

Generate a natural-language answer to the user's question.
"""


    # ========================================================
    # CALL OPENAI
    # ========================================================

    response = client.responses.create(

        model="gpt-5.6-luna",

        input=prompt

    )


    return response.output_text