# FitBuddy 🏋️‍♂️🥗

FitBuddy is an AI-powered fitness and meal planning web application built with FastAPI, SQLite, and Google Gemini AI.

## Features

- 🎯 **Personalized Fitness & Diet Plans**: Generated dynamically based on your fitness goals, preferences, and biometric inputs using Google Gemini.
- 📊 **Interactive Dashboard**: Track workouts, nutrition, daily progress, and water intake.
- ⚡ **Fast & Lightweight**: Built with FastAPI and SQLAlchemy for responsive performance.
- 🎨 **Modern UI**: Clean, interactive interface for seamless tracking.

## Getting Started

### Prerequisites

- Python 3.10+
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/veerasamyvasugi73-source/vasugi-fitbuddy-project.git
   cd vasugi-fitbuddy-project
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Add your Gemini API key in `.env`:
     ```env
     GOOGLE_API_KEY=your_gemini_api_key_here
     ```

5. **Run the application:**
   ```bash
   python main.py
   ```
   Or with uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

6. Open your browser and navigate to `http://127.0.0.1:8000`.
