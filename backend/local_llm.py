import ollama
import json
import re

# Optional but strongly recommended
# pip install json-repair
from json_repair import repair_json


def generate_mcqs_local(content, num_questions):
    prompt = f"""
Generate exactly {num_questions} multiple-choice questions from the text below.

Rules:
- Exactly 4 options: A, B, C, D
- One correct answer only
- No explanations
- Output STRICTLY valid JSON
- No markdown, no comments, no trailing commas

JSON format:
{{
  "questions": [
    {{
      "question": "string",
      "options": {{
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
      }},
      "answer": "A"
    }}
  ]
}}

TEXT:
{content[:3000]}
"""

    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}]
    )

    text = response["message"]["content"]
    text = re.sub(r"```json|```", "", text).strip()

    print("----- RAW MODEL OUTPUT -----")
    print(text)
    print("----------------------------")

    # Step 1: Try direct JSON load
    try:
        return json.loads(text)

    # Step 2: Repair JSON if invalid
    except json.JSONDecodeError:
        print("⚠️ JSON invalid, attempting repair...")
        try:
            repaired = repair_json(text)
            return json.loads(repaired)
        except Exception as e:
            print("❌ JSON REPAIR FAILED:", e)
            print("❌ FINAL RAW TEXT:\n", text)
            raise ValueError("LLM returned irreparable JSON")
