import os
import json
import google.generativeai as genai
from core.models import Recipe

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash"
)

def generate_recipe(dish: str, persons: int) -> Recipe:
    prompt = f"""
    Create a cooking recipe for {persons} people.

    Dish: {dish}

    Respond ONLY with valid JSON:
    {{
      "title": "",
      "servings": {persons},
      "ingredients": [
        {{
          "name": "",
          "quantity": 0,
          "unit": ""
        }}
      ]
    }}
    """

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "response_mime_type": "application/json"
        }
    )

    return Recipe.model_validate(json.loads(response.text))
