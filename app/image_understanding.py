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


def identify_food_from_image(image_path: str) -> dict:
    """
    Identifies the food dish in an image using GPT‑4o.
    The model is instructed to output a valid JSON object with keys:
      name, grain_starch, base, meats, vegetables, additional_ingredients, portion_size.
    """
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
                                "Identify the dish in this image, assuming it is a Singaporean dish "
                                "commonly found at hawker centers or local restaurants. "
                                "Output your answer as a valid JSON object with the following keys: "
                                "name, grain_starch, base, meats, vegetables, additional_ingredients, portion_size. "
                                "Ensure your output is strictly valid JSON without any extra text."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
        )
        dish_str = completion.choices[0].message.content.strip()
        output = json.loads(dish_str)
        return output
    except Exception as e:
        return {"error": f"Error identifying food: {str(e)}"}


def get_nutrition_info_gpt4o(dish: str, portion: float = 1.0) -> dict:
    """
    Retrieves nutritional information for the given dish using GPT‑4o.
    The prompt instructs the model to output valid JSON.
    The JSON output now includes a "sodium" key (total sodium in milligrams).
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "You are my food-tracking assistant. Your role is to help me identify "
                                "the nutritional information of the food I eat. I usually eat Singaporean dishes "
                                "from hawker centers and restaurants. "
                                "Output your answer as a valid JSON object."
                            ),
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Food: {dish}\nPortion: {portion}"}
                    ],
                },
            ],
            response_format={"type": "json_object"},
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "analyze_nutrients",
                        "strict": True,
                        "parameters": {
                            "type": "object",
                            "required": [
                                "calories",
                                "carbs",
                                "protein",
                                "fats",
                                "sodium",
                                "vitamins",
                                "fiber",
                                "other_nutrients",
                            ],
                            "properties": {
                                "calories": {
                                    "type": "number",
                                    "description": "Total calories",
                                },
                                "carbs": {
                                    "type": "number",
                                    "description": "Total carbohydrates in grams",
                                },
                                "protein": {
                                    "type": "number",
                                    "description": "Total protein in grams",
                                },
                                "fats": {
                                    "type": "number",
                                    "description": "Total fat in grams",
                                },
                                "sodium": {
                                    "type": "number",
                                    "description": "Total sodium in milligrams",
                                },
                                "fiber": {
                                    "type": "number",
                                    "description": "Total dietary fiber in grams",
                                },
                                "vitamins": {
                                    "type": "object",
                                    "required": ["vitamin_a", "vitamin_c", "vitamin_d"],
                                    "properties": {
                                        "vitamin_a": {
                                            "type": "number",
                                            "description": "Vitamin A in micrograms",
                                        },
                                        "vitamin_c": {
                                            "type": "number",
                                            "description": "Vitamin C in milligrams",
                                        },
                                        "vitamin_d": {
                                            "type": "number",
                                            "description": "Vitamin D in international units",
                                        },
                                    },
                                    "description": "Vitamins in the food",
                                    "additionalProperties": False,
                                },
                                "other_nutrients": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "description": "Additional nutritional information",
                                    },
                                    "description": "List of other nutritional details",
                                },
                            },
                            "additionalProperties": False,
                        },
                        "description": "JSON output of a food nutrient analyser.",
                    },
                }
            ],
            tool_choice={"type": "function", "function": {"name": "analyze_nutrients"}},
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        json_output = response.choices[0].message.tool_calls[0].function.arguments
        output = json.loads(json_output)
        return output
    except Exception as e:
        return {"error": f"Error retrieving nutritional info: {str(e)}"}
