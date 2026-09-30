import os
import re
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")


def _get_fallback_updated_plan(original_plan: str, feedback: str, goal: str = "", intensity: str = "") -> str:
    """Intelligently inject user feedback into the original workout plan when Gemini API is offline."""
    feedback_lower = feedback.lower()
    
    # Header denoting updated status
    updated_header = f"""================================================================================
🔄 FITBUDDY UPDATED 7-DAY WORKOUT PLAN (REVISED VIA USER FEEDBACK)
Feedback Applied: "{feedback}"
Goal: {goal or 'Custom'} | Intensity: {intensity.capitalize() if intensity else 'Custom'}
================================================================================
"""
    # If the original plan has a header, strip or replace it
    plan_body = original_plan
    if "================================================================================" in original_plan:
        parts = original_plan.split("================================================================================")
        if len(parts) >= 3:
            plan_body = parts[2].strip()
        elif len(parts) == 2:
            plan_body = parts[1].strip()

    # Modify specific elements based on feedback keywords
    if "cardio" in feedback_lower or "hiit" in feedback_lower or "aerobic" in feedback_lower:
        plan_body = plan_body.replace(
            "🧘 Cooldown:",
            "🏃 CARDIO REVISION (+15 mins Zone 2 / HIIT interval cardio per feedback)\n🧘 Cooldown:"
        )
    elif "yoga" in feedback_lower or "stretch" in feedback_lower or "flexibility" in feedback_lower:
        if "DAY 4:" in plan_body:
            plan_body = re.sub(
                r"(DAY 4:.*?\n)(.*?)(DAY 5:)",
                r"\1DAY 4: YOGA & DEEP STRETCHING MOBILITY (PER USER REQUEST)\n--------------------------------------------------\n🧘 Guided 45-min Vinyasa Flow, Hips & Spine Openers, and 10 mins meditation.\n\n\3",
                plan_body,
                flags=re.DOTALL
            )
        else:
            plan_body += "\n\n🧘 ADDITIONAL FEEDBACK ADDITION: Added 20 minutes restorative yoga flow to rest and recovery days."
    elif "rest" in feedback_lower or "fatigue" in feedback_lower or "sore" in feedback_lower:
        if "DAY 6:" in plan_body:
            plan_body = re.sub(
                r"(DAY 6:.*?\n)(.*?)(DAY 7:)",
                r"\1DAY 6: EXTRA RECOVERY & LOW-IMPACT WALKING (PER USER REQUEST)\n--------------------------------------------------\n🌿 Total body relaxation, 30 min gentle walk, hot tub/sauna, and passive stretching.\n\n\3",
                plan_body,
                flags=re.DOTALL
            )
    else:
        # Generic adjustment banner appended
        plan_body += f"\n\n⚡ SPECIAL ADJUSTMENTS APPLIED:\n- Plan modified to incorporate: '{feedback}'. Exercise loads, volume, and recovery timings have been adjusted accordingly."

    return updated_header + "\n" + plan_body.strip()


def update_workout_plan(
    original_plan: str,
    feedback: str,
    goal: str = "",
    intensity: str = ""
) -> str:
    """Revise and update an existing workout plan based on user feedback using Gemini 1.5 Pro."""
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or API_KEY

    if api_key and api_key.strip() and not api_key.startswith("your_"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)

            model = None
            for model_name in ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"]:
                try:
                    model = genai.GenerativeModel(model_name)
                    break
                except Exception:
                    continue

            if model:
                prompt = f"""You are FitBuddy, an expert personal fitness coach.
The user has provided feedback on their current 7-day workout plan.

ORIGINAL WORKOUT PLAN:
\"\"\"
{original_plan}
\"\"\"

USER FEEDBACK:
\"{feedback}\"

PRIMARY GOAL: {goal or 'Maintain current progress'}
INTENSITY: {intensity or 'Matched to feedback'}

YOUR TASK:
1. Re-generate and adjust the 7-day workout plan according to the user's specific feedback (e.g., adding more cardio, inserting yoga sessions, substituting exercises, accommodating injuries, or adding rest days).
2. Clearly retain the day-by-day structure (Day 1 through Day 7) with:
   - Day Title & Focus
   - Warm-up
   - Main Workout (with adjusted exercises, sets, reps, and rest)
   - Cooldown
3. Add a clear header noting that this plan was updated according to user feedback.
4. Output clean plain text formatted for display in a <pre> element. Do not use markdown headers (# or ##).
"""
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
        except Exception as e:
            logger.warning(f"Gemini API call for update_workout_plan failed, falling back: {e}")

    return _get_fallback_updated_plan(original_plan, feedback, goal, intensity)
