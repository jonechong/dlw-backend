import os
import json
import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# Instantiate the OpenAI client.
client = OpenAI(api_key=openai_api_key)

def clean_json_string(s: str) -> str:
    """
    Remove markdown code fences and extra characters if present.
    """
    s = s.strip()
    if s.startswith("```json"):
        s = s[len("```json"):].strip()
    if s.startswith("```"):
        s = s[3:].strip()
    if s.endswith("```"):
        s = s[:-3].strip()
    return s

def balance_braces(s: str) -> str:
    """
    A simple heuristic to balance curly braces by counting and appending missing "}".
    """
    open_braces = s.count("{")
    close_braces = s.count("}")
    while open_braces > close_braces:
        s += "}"
        close_braces += 1
    return s

def parse_current_time(time_str: str) -> datetime.time:
    """
    Parse a time string in the format "HH:MM AM/PM" into a datetime.time object.
    """
    return datetime.datetime.strptime(time_str, "%I:%M %p").time()

def determine_meal_context(current_time: str) -> str:
    """
    Determines the meal context based on the current time.
    - Before 11:00 AM: "breakfast" (leave enough calories for lunch and dinner).
    - From 11:00 AM to before 4:00 PM: "lunch" (leave enough calories for dinner).
    - From 4:00 PM to before 9:00 PM: "dinner" (use full remaining budget).
    - From 9:00 PM to before 5:00 AM: "supper".
    """
    try:
        t = parse_current_time(current_time)
    except Exception:
        # If parsing fails, use host time.
        t = datetime.datetime.now().time()
    hour = t.hour
    if hour < 11:
        return "breakfast"
    elif hour < 16:
        return "lunch"
    elif hour < 21:
        return "dinner"
    else:
        return "supper"

def get_personalized_recommendations(food_totals: dict, user_profile: dict, current_time: str = None) -> dict:
    """
    Uses GPT‑4o to generate personalized recommendations for a specific meal context based on:
      - Nutritional totals consumed so far (calories, carbs, protein, fats, sodium).
      - Key user profile details (age, weight, height, food-related medical conditions,
        daily calorie target or estimated expenditure, target weight, target weight loss, steps per day).
      - The current time, which determines the meal context.
    
    The prompt instructs the model to output a valid JSON object with a key "recommendations"
    whose value is a list (of at most 5 objects). Each recommendation includes:
      - "food": The recommended local Singaporean dish or non-food action (e.g. "Chicken Rice (with less rice)" or "Drink water and sleep early").
      - "estimatedNutrition": An object with estimated values for calories, carbs, protein, fats, and sodium.
      - "explanation": A detailed explanation describing why the option is recommended, including its impact on the remaining calorie budget and variant suggestions if necessary.
      - "remainingAfter": The remaining calorie budget after consuming the recommended food.
    
    The prompt is tailored for the following meal contexts:
      - Breakfast: Recommendations should leave enough calories for both lunch and dinner.
      - Lunch: Recommendations should leave enough calories for dinner.
      - Dinner: Use the full remaining calorie budget.
      - Supper: Provide appropriate options if any budget remains.
    """
    # Use host system time if current_time is not provided.
    if current_time is None:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
    
    meal_context = determine_meal_context(current_time)
    
    # Build a summary of relevant user profile details (excluding name).
    user_details = []
    if user_profile.get("age"):
        user_details.append(f"Age: {user_profile['age']}")
    if user_profile.get("weight"):
        user_details.append(f"Weight: {user_profile['weight']} kg")
    if user_profile.get("height"):
        user_details.append(f"Height: {user_profile['height']} cm")
    if user_profile.get("medicalConditions"):
        user_details.append(f"Medical Conditions: {user_profile['medicalConditions']}")
    if user_profile.get("dailyCalorieTarget"):
        user_details.append(f"Daily Calorie Target: {user_profile['dailyCalorieTarget']}")
    elif user_profile.get("estimatedExpenditure"):
        user_details.append(f"Maintenance Calories: {user_profile['estimatedExpenditure']}")
    if user_profile.get("targetWeight"):
        user_details.append(f"Target Weight: {user_profile['targetWeight']} kg")
    if user_profile.get("targetLoss"):
        user_details.append(f"Target Weight Loss: {user_profile['targetLoss']} kg")
    if user_profile.get("stepsPerDay"):
        user_details.append(f"Average Steps/Day: {user_profile['stepsPerDay']}")
    user_details_str = "; ".join(user_details)
    
    # Calculate remaining calorie budget.
    total_cal = float(food_totals.get("calories", 0))
    if user_profile.get("dailyCalorieTarget"):
        remaining_cal = float(user_profile["dailyCalorieTarget"]) - total_cal
    elif user_profile.get("estimatedExpenditure"):
        remaining_cal = float(user_profile["estimatedExpenditure"]) - total_cal
    else:
        remaining_cal = "unspecified"
    
    # Summarize today's food consumption.
    food_totals_str = (
        f"Consumed today: Calories: {total_cal}, Carbs: {food_totals.get('carbs', 0)}g, "
        f"Protein: {food_totals.get('protein', 0)}g, Fats: {food_totals.get('fats', 0)}g, "
        f"Sodium: {food_totals.get('sodium', 0)}mg. "
        f"Remaining Calorie Budget: {remaining_cal}."
    )
    
    # Build the prompt with meal-specific instructions.
    if meal_context == "breakfast":
        meal_instruction = "You are recommending breakfast options that leave enough calories for both lunch and dinner."
    elif meal_context == "lunch":
        meal_instruction = "You are recommending lunch options that leave enough calories for dinner."
    elif meal_context == "dinner":
        meal_instruction = "You are recommending dinner options using the full remaining calorie budget."
    else:  # supper
        meal_instruction = "You are recommending supper options appropriate for late hours."
    
    prompt = (
        f"Current time: {current_time}. Context: Singapore. "
        f"Meal Context: {meal_context.upper()}. {meal_instruction} "
        f"User Profile: {user_details_str}. {food_totals_str} "
        f"Note that the remaining calorie budget is {remaining_cal} calories. "
        "Based on this information, provide personalized recommendations for the rest of the day to help the user reach their target. "
        "Your answer must be tailored exclusively to common, widely available local Singaporean cuisine—recommend dishes that are easily accessible at hawker centres, food courts, or supermarkets. "
        "Important requirements:\n"
        "1. Provide no more than 5 recommendations.\n"
        "2. For each recommendation, include:\n"
        "   - 'food': the name of the dish or non-food action (e.g. 'Chicken Rice (with less rice)' or 'Drink water and sleep early').\n"
        "   - 'estimatedNutrition': an object with estimated values for calories, carbs, protein, fats, and sodium.\n"
        "   - 'explanation': a detailed explanation of why this option is recommended, including its impact on the remaining calorie budget, variant suggestions (if necessary), and whether it is suitable as a full meal or a snack (e.g. ensuring breakfast leaves room for lunch and dinner).\n"
        "   - 'remainingAfter': the remaining calorie budget after consuming this recommended food (e.g. if the remaining budget is 100 and the food uses 400 calories, this should be -300).\n"
        "3. If the remaining calorie budget is very low or if it is late in the day (e.g., after 10:00 PM), consider recommending a light snack, a home-cooked meal, or even advise the user to drink water and get some rest instead of a full meal.\n"
        "4. Be specific about variants. For example, if recommending Chicken Rice, suggest ordering with white rice or a reduced portion of rice if necessary.\n"
        "Output your answer as a valid JSON object with a key 'recommendations' whose value is a list of objects as specified. "
        "Ensure there is no additional text or markdown formatting in your output."
    )
    
    print("DEBUG: current_time:", current_time)
    print("DEBUG: meal_context:", meal_context)
    print("DEBUG: user_details_str:", user_details_str)
    print("DEBUG: food_totals_str:", food_totals_str)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
            temperature=0.7,
            max_completion_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response_str = completion.choices[0].message.content.strip()
        # Clean the response string to remove markdown fences.
        response_str = clean_json_string(response_str)
        # Heuristically balance braces if needed.
        response_str = balance_braces(response_str)
        # print("DEBUG: Cleaned GPT-4o response:", response_str)
        output = json.loads(response_str)
        return output
    except Exception as e:
        return {"error": f"Error generating personalized recommendations: {str(e)}"}
