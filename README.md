# Food Recommendation App

This project is a full-stack application that uses a **React frontend** and a **FastAPI backend** to analyze food images, retrieve nutritional information using GPT‑4o, and generate personalized food recommendations based on user profiles and daily food intake.

---

## Overview

### Frontend:
- Built with **React** and **Material-UI**.
- Allows users to add food items (**via image upload or manual input**).
- Displays nutritional totals and **shows personalized recommendations**.

### Backend:
- Developed with **FastAPI**.
- Uses **GPT‑4o** for two main functions:
  1. **Analyzing food images** to extract dish identification and nutritional information.
  2. **Generating personalized recommendations** based on the user's daily food totals and profile.

### Environment:
- The React app runs on **port 3000**.
- The FastAPI backend runs on **port 8000**.
- These defaults simplify setup and ensure quick deployment.

---

## Prerequisites

Before running the project, make sure you have the following installed:

- **Node.js & npm** → Required for the React frontend.
- **Python 3.8+ & pip** → Required for the FastAPI backend.
- **Uvicorn** → ASGI server to run FastAPI.

---

## Setup

### Clone the Repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

### Configure the Backend:

Create a `.env` file in the root of the backend directory with the following content:

```ini
OPENAI_API_KEY=your_openai_api_key_here
```

> Replace `your_openai_api_key_here` with your actual GPT‑4o API key.

### Install Python Dependencies:

```bash
pip install -r requirements.txt
```

> Ensure that **FastAPI, Uvicorn, and any other required packages** are listed in your `requirements.txt`.

### Install Node Dependencies for the Frontend:

```bash
cd frontend
npm install
```

---

## Running the Server

### Backend:
Use Uvicorn to run the FastAPI backend on port **8000**:

```bash
uvicorn app.main:app --reload
```

### Frontend:
In a separate terminal, start the React app on port **3000**:

```bash
npm start
```

---

## Project Structure

```bash
├── app
│   ├── main.py              # FastAPI application entry point
│   ├── get_food_info.py     # Module for analyzing food images using GPT‑4o
│   └── get_personalized_recommendations.py  # Module for generating recommendations
├── frontend                 # React application source code
│   └── src
│       └── pages
│           └── MainPage.js  # Main React component with UI and API calls
├── .env                     # Environment file with OPENAI_API_KEY (for backend)
├── requirements.txt         # Python dependencies list
└── README.md                # Project documentation (this file)
```

---

## Notes

### Ports:
- The application uses **default ports**:
  - **FastAPI runs on port 8000**.
  - **React frontend runs on port 3000**.

### Environment Variables:
- The backend **requires** a `.env` file with your OpenAI API key (`OPENAI_API_KEY`) to function correctly.

### Running the Application:
- Once both servers are running, you can **interact with the React frontend** in your browser.
- The frontend makes API calls to the **FastAPI backend on port 8000**.

---

