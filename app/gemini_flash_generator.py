import os
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")


def _get_fallback_nutrition_tip(goal: str, weight: Optional[float] = None) -> str:
    """Fallback nutrition & recovery tip generator."""
    goal_lower = goal.lower()
    weight_str = f" For your body weight of {weight} kg, " if weight else " "

    if "muscle" in goal_lower or "bulk" in goal_lower or "strength" in goal_lower:
        target_protein = f"aim for approximately {int(weight * 1.8)}-{int(weight * 2.2)}g of high-quality protein daily" if weight else "aim for 1.8 to 2.2g of protein per kg of bodyweight"
        return (
            f"🥩 Prioritize Protein & Post-Workout Nutrient Timing:\n"
            f"{weight_str.strip()} {target_protein} spread evenly across 4–5 meals (chicken breast, salmon, eggs, Greek yogurt, or plant-based isolates). "
            f"Within 45 minutes after heavy resistance training, consume a 3:1 carb-to-protein recovery snack (e.g., whey shake + banana) to replenish depleted glycogen stores and kickstart muscle protein synthesis. "
            f"Stay well hydrated with at least 3.5 liters of water daily, adding electrolytes during intense lifting sessions."
        )
    elif "loss" in goal_lower or "fat" in goal_lower or "burn" in goal_lower or "lean" in goal_lower:
        return (
            f"🥗 Optimize Satiety & Caloric Deficit:\n"
            f"{weight_str.strip()} Maintain a sustainable caloric deficit of 300–500 kcal below maintenance while keeping daily protein high (1.6–2.0g per kg) to protect lean muscle mass. "
            f"Fill half of your plate with cruciferous, fiber-rich vegetables (spinach, broccoli, zucchini) to promote fullness and digestive health. "
            f"Drink 500ml of cold water 15 minutes prior to every meal, limit liquid calories, and target 7–8 hours of uninterrupted sleep to keep cortisol and hunger hormones (ghrelin) in check."
        )
    elif "endurance" in goal_lower or "stamina" in goal_lower or "running" in goal_lower:
        return (
            f"⚡ Complex Carbs & Cellular Hydration:\n"
            f"{weight_str.strip()} Fuel aerobic sessions with low-glycemic complex carbohydrates (oatmeal, sweet potatoes, quinoa) 2 hours before long runs or cycling. "
            f"During workouts exceeding 60 minutes, supplement with essential electrolytes (sodium, potassium, magnesium) to prevent cramping and fatigue. "
            f"Post-workout, support tissue recovery with tart cherry juice or omega-3 fatty acids to reduce systemic inflammation."
        )
    else:
        return (
            f"🌱 Balanced Whole-Food Nutrition & Daily Vitality:\n"
            f"{weight_str.strip()} Center your diet around unprocessed whole foods: lean proteins, complex grains, and vibrant colorful fruits and vegetables. "
            f"Target minimum 2.5 to 3 liters of water per day for optimal cognitive focus and cellular metabolism. "
            f"Avoid processed sugars and artificial additives in the evening to optimize your natural melatonin production and deep sleep cycles."
        )


def generate_nutrition_tip_with_flash(goal: str, weight: Optional[float] = None) -> str:
    """Generate a concise, practical nutrition or recovery tip using Gemini Flash."""
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or API_KEY

    if api_key and api_key.strip() and not api_key.startswith("your_"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)

            # Use gemini-1.5-flash as specified
            model = None
            for model_name in ["gemini-1.5-flash", "gemini-flash", "gemini-1.5-pro"]:
                try:
                    model = genai.GenerativeModel(model_name)
                    break
                except Exception:
                    continue

            if model:
                prompt = f"""You are a sports nutritionist and recovery specialist for FitBuddy.
Generate a concise, highly practical, and actionable nutrition or recovery tip for a user with the following fitness profile:
- Primary Fitness Goal: {goal}
- Body Weight: {weight} kg if weight else 'Not specified'

GUIDELINES:
1. Keep the tip concise (2-4 sentences max), punchy, and instantly actionable.
2. Emphasize specific foods, macros (protein, hydration), nutrient timing, or recovery techniques tailored to their goal.
3. Start with an engaging emoji and short header.
4. Output in clean plain text without markdown headers.
"""
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
        except Exception as e:
            logger.warning(f"Gemini Flash API call failed, falling back to smart tip generator: {e}")

    return _get_fallback_nutrition_tip(goal, weight)
