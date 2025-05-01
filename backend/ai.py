import openai
from .config import settings

openai.api_key = settings.OPENAI_API_KEY

def evaluate_submission(code: str, challenge_description: str) -> dict:
    prompt = f\"\"\"
You are an expert coding evaluator. Evaluate the following student submission code for the challenge described below. Provide constructive feedback and a score from 0 to 100.

Challenge Description:
{challenge_description}

Student Submission:
{code}

Please provide your response in JSON format with keys: "feedback" and "score".
\"\"\"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.3,
    )
    content = response.choices[0].message.content.strip()
    # Expecting JSON response, parse it
    import json
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        # fallback if parsing fails
        result = {"feedback": content, "score": None}
    return result
