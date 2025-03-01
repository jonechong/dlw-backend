# DLW Backend

This repository contains the backend code for the Food Recommendation App. The backend is built with [FastAPI](https://fastapi.tiangolo.com/) and leverages GPT‑4o to perform two primary functions:

1. **Food Image Analysis:**  
   Analyzes food images to extract dish identification and nutritional information.

2. **Personalized Recommendations:**  
   Generates personalized food recommendations based on the user's daily nutritional totals and profile.

This backend is designed to work with a React frontend, which is maintained in a separate repository ([DLW Frontend](https://github.com/jonechong/dlw-frontend)). For this project, both the backend and frontend use default ports:
- FastAPI backend runs on port **8000**.
- React frontend runs on port **3000**.

## Features

- **Image Analysis:**  
  Uses GPT‑4o to process an image and return a JSON object containing dish identification and nutrition details.
  
- **Personalized Recommendations:**  
  Based on the user's current nutritional totals and profile, returns recommendations tailored to common local Singaporean dishes.  
  - If the recommendation process fails, a placeholder JSON response is returned to ensure the frontend always receives valid data.
  
- **Default Port Usage:**  
  The backend is set to run on port **8000** (enforced for time constraints) without additional configuration.

## Prerequisites

- **Python 3.8+** and **pip**
- **Uvicorn** (ASGI server for FastAPI)
- An OpenAI API key for GPT‑4o

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/jonechong/dlw-backend.git
   cd dlw-backend
Create the .env File

In the root directory, create a file named .env with the following content:

ini
Copy
OPENAI_API_KEY=your_openai_api_key_here
Replace your_openai_api_key_here with your actual GPT‑4o API key.

Install Dependencies

bash
Copy
pip install -r requirements.txt
Ensure that fastapi, uvicorn, and any other required packages are listed in requirements.txt.

Running the Server
Start the backend server using Uvicorn on the default port 8000:

bash
Copy
uvicorn app.main:app --reload
This command runs the FastAPI application with automatic reloading enabled.

Project Structure
bash
Copy
├── app
│   ├── main.py                             # FastAPI application entry point
│   ├── get_food_info.py                    # Module for analyzing food images using GPT‑4o
│   └── get_personalized_recommendations.py  # Module for generating personalized recommendations
├── .env                                    # Environment file with OPENAI_API_KEY
├── requirements.txt                        # Python dependencies list
└── README.md                               # This documentation file
Notes
Ports:
The backend runs on port 8000. The frontend is expected to run on port 3000.

Environment Variables:
Ensure the .env file is present with your OPENAI_API_KEY for GPT‑4o to work.

Starting the Server:
Use the Uvicorn command above to run the backend.

Frontend
The React frontend is maintained separately in the DLW Frontend repository (https://github.com/jonechong/dlw-frontend).
