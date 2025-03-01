import os
import base64
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# Instantiate the OpenAI client for API calls.
client = OpenAI(api_key=openai_api_key)

def encode_image(image_path: str) -> str:
    """
    Encodes an image to Base64 format.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_food_info(image_path: str, portion: float = 1.0) -> dict:
    image_base64 = encode_image(image_path)
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Identify the dish in this image and provide its nutritional information for one portion. "
                                "Assume it is a Singaporean dish commonly found at hawker centers or local restaurants. "
                                "Output your answer as a valid JSON object with the following keys:\n\n"
                                "Dish Identification: name, grain_starch, base, meats, vegetables, additional_ingredients, portion_size.\n\n"
                                "Nutrition: calories, carbs, protein, fats, sodium, fiber, vitamins (vitamin_a, vitamin_c, vitamin_d), other_nutrients.\n\n"
                                "Ensure your output is strictly valid JSON without any extra text."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                        {
                            "type": "text",
                            "text": f"Portion: {portion}"
                        }
                    ],
                }
            ],
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response_str = completion.choices[0].message.content.strip()
        print("DEBUG: Raw GPT-4o response:", response_str)
        output = json.loads(response_str)
        return output
    except Exception as e:
        return {"error": f"Error in get_food_info: {str(e)}"}
