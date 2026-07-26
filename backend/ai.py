from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

CATEGORY_OPTIONS = {
    "awaiting_interest": ["product", "support"],
    "awaiting_budget": ["under_1k", "1k_5k", "5k_plus"],
    "awaiting_urgency": ["asap", "this_month", "exploring"],
}


def classify_reply(step_key, text):
    options = CATEGORY_OPTIONS.get(step_key)
    if not options:
        return None

    prompt = (
        f"A customer replied to a qualifying question in free text. "
        f"Classify their reply into exactly one of these categories: {', '.join(options)}. "
        f'If none genuinely fit, respond with "unclear".\n\n'
        f'Customer reply: "{text}"\n\n'
        f"Respond with ONLY the category word, nothing else."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        result = response.text.strip().lower()
    except Exception:
        return None

    return result if result in options else None