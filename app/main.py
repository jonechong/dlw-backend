import os
import uuid
import shutil
import json
from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.get_food_info import get_food_info
from app.get_personalized_recommendations import get_personalized_recommendations

# ----- Monkey-patch json.loads to clean markdown formatting -----
original_json_loads = json.loads

def clean_json_string(s: str) -> str:
    s = s.strip()
    if s.startswith("```json"):
        s = s[len("```json"):].strip()
    if s.startswith("```"):
        s = s[3:].strip()
    if s.endswith("```"):
        s = s[:-3].strip()
    return s

def debug_json_loads(s):
    if isinstance(s, bytes):
        s = s.decode("utf-8")
    s_clean = clean_json_string(s)
    try:
        return original_json_loads(s_clean)
    except Exception as e:
        print("Debug: Failed to parse JSON. Raw response:")
        print(s)
        raise e

json.loads = debug_json_loads
# --------------------------------------------------------------------

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.post("/analyze")
async def analyze_food(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image type. Only JPEG and PNG are allowed.")
    file_id = str(uuid.uuid4())
    file_extension = file.filename.split(".")[-1]
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.{file_extension}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    food_info = get_food_info(file_path)
    os.remove(file_path)
    if "error" in food_info:
        raise HTTPException(status_code=500, detail=food_info["error"])
    output = {
        "name": food_info.get("Dish Identification", {}).get("name"),
        "calories": food_info.get("Nutrition", {}).get("calories"),
        "carbs": food_info.get("Nutrition", {}).get("carbs"),
        "protein": food_info.get("Nutrition", {}).get("protein"),
        "fats": food_info.get("Nutrition", {}).get("fats"),
        "sodium": food_info.get("Nutrition", {}).get("sodium")
    }
    return JSONResponse(content=output)

@app.post("/recommend")
async def personalize(
    food_totals: dict = Body(..., embed=True),
    user_profile: dict = Body(..., embed=True),
    current_time: str = Body(None, embed=True)
):
    recommendations = get_personalized_recommendations(food_totals, user_profile, current_time)
    if "error" in recommendations:
        raise HTTPException(status_code=500, detail=recommendations["error"])
    return JSONResponse(content=recommendations)
