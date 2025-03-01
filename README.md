# DLW-Backend

**DLW-Backend** is the FastAPI backend for the **DLW project**. It uses **GPT‑4o** to analyze food images and generate personalized food recommendations based on user nutritional intake and profiles. Although the project interacts with a React frontend (available separately), this repository focuses mainly on the backend functionality.

A key differentiator of DLW-Backend is its focus on the **local Singaporean context**. Unlike many existing applications, DLW-Backend **incorporates local food options, cultural dietary preferences, and region-specific nutritional guidelines**, addressing a market gap in food recommendation apps.

---

## Overview

The backend performs two primary functions:

### **Image Analysis:**
- Processes food images to identify the dish and extract nutritional information using **GPT‑4o**.
- Recognizes **local Singaporean dishes**, ensuring culturally relevant nutritional insights.

### **Personalized Recommendations:**
- Generates tailored recommendations based on the user's daily nutritional totals and profile details.
- Enforces a **default meal schedule** (breakfast, lunch, dinner, or supper) based on the current time.
- Considers **user-specific factors**, including:
  - **Height, age, and weight**.
  - **Automatic BMR calculation**.
  - **Daily energy expenditure estimation** (based on step count and activity level).
  - **Target calorie deficit** (user-selectable, constrained to healthy weight loss options).
  - **Medical conditions** (e.g., high cholesterol, dietary restrictions).
- Adapts recommendations to **Singaporean dietary habits**, ensuring they align with local cuisine and availability.

Both functions use **GPT‑4o** and require an **OpenAI API key** to function.

---

## Prerequisites

Before running the project, make sure you have the following installed:

- **Python 3.8+**
- **pip**
- **Uvicorn** (ASGI server)

---

## Setup

### Clone the Repository:

```bash
git clone https://github.com/jonechong/dlw-backend.git
cd dlw-backend
```

### Create a `.env` File:

In the project root, create a file named `.env` with the following content:

```ini
OPENAI_API_KEY=your_openai_api_key_here
```

> Replace `your_openai_api_key_here` with your actual GPT‑4o API key.

### Install Dependencies:

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

---

## Running the Server

To start the FastAPI backend on the default port (**8000**), run:

```bash
uvicorn app.main:app --reload
```

This command starts the server in **development mode** with hot reloading enabled.

---

## Project Structure

```bash
├── app
│   ├── main.py                              # FastAPI application entry point
│   ├── get_food_info.py                     # Module to analyze food images via GPT‑4o
│   └── get_personalized_recommendations.py  # Module to generate personalized recommendations
├── .env                                     # Environment file (must include OPENAI_API_KEY)
├── requirements.txt                         # List of Python dependencies
└── README.md                                # This documentation file
```

---

## Notes

### **Default Ports:**
- The backend uses the **default port 8000**. This is enforced to meet time constraints—no custom configuration is provided in an environment file.

### **Frontend Integration:**
- Although this repository focuses on the backend, the React frontend (which interacts with this backend) is available at:  
  **[DLW-Frontend](https://github.com/jonechong/dlw-frontend)**.

### **Singapore-Specific Features:**
- **Recognizes and provides nutritional analysis for local Singaporean dishes**.
- **Recommends meals based on common Singaporean dietary patterns**.
- **Considers local food availability and cultural eating habits in its recommendations**.

### **Starting the Server:**
- Use the command `uvicorn app.main:app --reload` to run the backend in development mode.
