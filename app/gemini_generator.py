import os
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Configure Google Generative AI
API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")


def _get_fallback_workout(goal: str, intensity: str, age: Optional[int] = None, weight: Optional[float] = None, username: Optional[str] = None) -> str:
    """Intelligent fallback workout generator when Gemini API key is unavailable or during rate limits."""
    name_str = f" for {username}" if username else ""
    weight_str = f" (Weight: {weight}kg)" if weight else ""
    age_str = f" (Age: {age})" if age else ""

    goal_lower = goal.lower()
    intensity_upper = intensity.capitalize()

    if "muscle" in goal_lower or "bulk" in goal_lower or "strength" in goal_lower:
        plan_content = f"""================================================================================
🏋️ FITBUDDY 7-DAY PERSONALIZED WORKOUT PLAN{name_str.upper()}
Goal: {goal} | Intensity: {intensity_upper} {age_str}{weight_str}
================================================================================

DAY 1: CHEST & TRICEPS HYPERTROPHY
--------------------------------------------------
🔥 Warm-up (7 mins):
  - Arm circles & chest cross stretches (2 mins)
  - Light incline push-ups: 2 sets x 12 reps
  - Banded pull-aparts: 2 sets x 15 reps

⚡ Main Workout:
  1. Barbell Bench Press: 4 sets x 8-10 reps (Rest: 90s)
  2. Incline Dumbbell Press: 3 sets x 10-12 reps (Rest: 75s)
  3. Cable Chest Flyes: 3 sets x 12-15 reps (Rest: 60s)
  4. Tricep Rope Pushdowns: 3 sets x 12-15 reps (Rest: 60s)
  5. Overhead Dumbbell Tricep Extension: 3 sets x 10 reps (Rest: 60s)

🧘 Cooldown: 5 mins light triceps and pec door-frame stretch. Stay hydrated!


DAY 2: BACK & BICEPS STRENGTH
--------------------------------------------------
🔥 Warm-up (8 mins):
  - Scapular pull-ups: 2 sets x 8 reps
  - Cat-cow spinal mobility (2 mins)
  - Light lat pulldowns: 2 sets x 12 reps

⚡ Main Workout:
  1. Barbell Deadlifts / Rack Pulls: 4 sets x 6-8 reps (Rest: 120s)
  2. Lat Pulldowns (Wide Grip): 4 sets x 10-12 reps (Rest: 75s)
  3. Seated Cable Rows: 3 sets x 10-12 reps (Rest: 60s)
  4. Barbell Bicep Curls: 3 sets x 10 reps (Rest: 60s)
  5. Hammer Curls: 3 sets x 12 reps (Rest: 60s)

🧘 Cooldown: Lat hangs and bicep wall stretches for 5 minutes.


DAY 3: LOWER BODY POWER & QUAD FOCUS
--------------------------------------------------
🔥 Warm-up (10 mins):
  - Bodyweight squats & leg swings: 2 sets x 15 reps
  - World's greatest stretch (3 mins)
  - Light goblet squats: 2 sets x 10 reps

⚡ Main Workout:
  1. Barbell Back Squats: 4 sets x 8-10 reps (Rest: 90-120s)
  2. Romanian Deadlifts (RDLs): 3 sets x 10-12 reps (Rest: 90s)
  3. Leg Press: 3 sets x 12 reps (Rest: 75s)
  4. Walking Dumbbell Lunges: 3 sets x 12 steps per leg (Rest: 60s)
  5. Standing Calf Raises: 4 sets x 15-20 reps (Rest: 45s)

🧘 Cooldown: Foam roll quads, hamstrings, and hip flexors for 7 mins.


DAY 4: ACTIVE RECOVERY & CORE CONDITIONING
--------------------------------------------------
🔥 Warm-up: 5 mins gentle breathing and mobility.
⚡ Routine:
  - 30-minute brisk incline walk or light cycling (Zone 2)
  - Hanging Knee Raises: 3 sets x 12 reps
  - Plank Hold: 3 sets x 45-60 seconds
  - Bird-Dog: 3 sets x 10 per side
🧘 Cooldown: Full-body yoga flow and deep hamstring stretch.


DAY 5: SHOULDERS & UPPER BODY SCULPT
--------------------------------------------------
🔥 Warm-up (7 mins):
  - Shoulder dislocates with PVC pipe / resistance band (2 mins)
  - Dumbbell lateral raises (ultra-light warm-up): 2 sets x 15 reps

⚡ Main Workout:
  1. Standing Overhead Barbell / Dumbbell Press: 4 sets x 8-10 reps (Rest: 90s)
  2. Dumbbell Lateral Raises: 4 sets x 12-15 reps (Rest: 60s)
  3. Face Pulls: 4 sets x 15 reps (Rest: 60s)
  4. Dumbbell Shrugs: 3 sets x 12 reps (Rest: 60s)
  5. Close-Grip Pushups: 3 sets to failure (Rest: 60s)

🧘 Cooldown: Shoulder cross-arm stretches and neck mobility.


DAY 6: POSTERIOR CHAIN & HAMSTRING / GLUTE FOCUS
--------------------------------------------------
🔥 Warm-up (8 mins):
  - Glute bridges: 2 sets x 15 reps
  - Hip mobility drills (3 mins)

⚡ Main Workout:
  1. Barbell Hip Thrusts: 4 sets x 10-12 reps (Rest: 90s)
  2. Dumbbell Step-Ups: 3 sets x 10 reps per leg (Rest: 60s)
  3. Lying Hamstring Leg Curls: 3 sets x 12 reps (Rest: 60s)
  4. Leg Extensions: 3 sets x 12-15 reps (Rest: 60s)
  5. Hanging Leg Raises: 3 sets x 12 reps (Rest: 60s)

🧘 Cooldown: Piriformis and lower back gentle stretching for 5 mins.


DAY 7: REST, RECOVERY & NUTRITION ALIGNMENT
--------------------------------------------------
🌿 Complete rest day.
- Light 20-30 min casual walking outdoors.
- Focus on hydration (minimum 3L water) and high-protein intake to repair muscle fibers.
- Sleep for 8+ hours.
================================================================================"""
    elif "loss" in goal_lower or "fat" in goal_lower or "burn" in goal_lower or "lean" in goal_lower:
        plan_content = f"""================================================================================
🔥 FITBUDDY 7-DAY WEIGHT LOSS & FAT BURN PLAN{name_str.upper()}
Goal: {goal} | Intensity: {intensity_upper} {age_str}{weight_str}
================================================================================

DAY 1: FULL BODY METABOLIC RESISTANCE
--------------------------------------------------
🔥 Warm-up (7 mins):
  - Jumping jacks: 2 sets x 30s
  - Mountain climbers: 2 sets x 20s
  - Dynamic arm & leg swings: 2 mins

⚡ Main Workout (Circuit style - rest 45s between rounds):
  1. Goblet Squats: 4 sets x 15 reps
  2. Push-ups (Standard or Knee): 4 sets x 12 reps
  3. Dumbbell Bent-Over Rows: 4 sets x 12 reps
  4. Kettlebell / Dumbbell Swings: 4 sets x 20 reps
  5. Bicycle Crunches: 4 sets x 20 reps per side

🧘 Cooldown: 5 mins slow walking + static hamstring & chest stretches.


DAY 2: CARDIO HIIT & CORE BLAST
--------------------------------------------------
🔥 Warm-up (5 mins):
  - Light jog in place & high knees (3 mins)
  - Torso twists and hip openers (2 mins)

⚡ Main Workout (HIIT Intervals: 40s Work / 20s Rest x 5 Rounds):
  1. Burpees or Modified Step-Burpees
  2. Mountain Climbers
  3. Jump Squats or Bodyweight Air Squats
  4. Russian Twists
  5. High Plank Hold

🧘 Cooldown: 5 mins deep breathing and quad stretches. Drink electrolyte water!


DAY 3: LOWER BODY & GLUTE TONE
--------------------------------------------------
🔥 Warm-up (8 mins):
  - Bodyweight lunges: 10 per leg
  - Glute bridges: 15 reps
  - Hip circles: 10 each direction

⚡ Main Workout:
  1. Dumbbell Romanian Deadlifts: 4 sets x 12 reps (Rest: 60s)
  2. Walking Lunges: 3 sets x 12 steps per leg (Rest: 45s)
  3. Dumbbell Sumo Squats: 3 sets x 15 reps (Rest: 60s)
  4. Step-Ups on Box/Bench: 3 sets x 10 per leg (Rest: 45s)
  5. Calf Raises: 3 sets x 20 reps (Rest: 30s)

🧘 Cooldown: 6 mins foam rolling IT band, quads, and calves.


DAY 4: ACTIVE RECOVERY & MOBILITY
--------------------------------------------------
🌿 Rest & Regeneration:
  - 40-minute moderate outdoor walk or light swimming.
  - 15 minutes of full-body dynamic stretching and yoga sun salutations.
  - Hydration check: Sip water consistently throughout the day.


DAY 5: UPPER BODY SCULPT & CARDIO FINISHER
--------------------------------------------------
🔥 Warm-up (6 mins):
  - Arm circles & light jumping jacks (3 mins)
  - Incline push-ups (2 sets x 10 reps)

⚡ Main Workout:
  1. Dumbbell Shoulder Press: 4 sets x 12 reps (Rest: 60s)
  2. Lat Pulldowns or Assisted Pull-ups: 3 sets x 12 reps (Rest: 60s)
  3. Dumbbell Chest Press: 3 sets x 12 reps (Rest: 60s)
  4. Bicep Curl to Overhead Press: 3 sets x 10 reps (Rest: 45s)
  5. CARDIO FINISHER: 10 minutes treadmill incline walk (12% incline, 4.5 km/h).

🧘 Cooldown: 5 mins chest and lat stretches.


DAY 6: HIGH-ENERGY FUNCTIONAL CIRCUIT
--------------------------------------------------
🔥 Warm-up (7 mins):
  - Skipping rope (or phantom jumps): 3 mins
  - Bodyweight squats & lateral lunges: 2 sets x 10 reps

⚡ Main Workout (3 Rounds for Time):
  1. Box Jumps or Step-ups: 15 reps
  2. Kettlebell Deadlifts: 15 reps
  3. Renegade Rows: 10 reps per side
  4. Wall Sit: 45 seconds
  5. Plank with Shoulder Taps: 20 taps

🧘 Cooldown: 5 mins deep stretching and child's pose.


DAY 7: MINDFUL RECOVERY & MEAL PREP
--------------------------------------------------
🌿 Total rest and recharge.
  - Light casual movement (e.g. 20 min neighborhood walk).
  - Prepare high-protein, fiber-rich whole food meals for the upcoming week.
  - Prioritize 8 hours of restorative sleep.
================================================================================"""
    else:
        plan_content = f"""================================================================================
🌟 FITBUDDY 7-DAY GENERAL FITNESS & WELLNESS PLAN{name_str.upper()}
Goal: {goal} | Intensity: {intensity_upper} {age_str}{weight_str}
================================================================================

DAY 1: FULL BODY FUNCTIONAL STRENGTH
--------------------------------------------------
🔥 Warm-up (7 mins): Dynamic joint rotations, arm sweeps, and 20 bodyweight squats.
⚡ Main Workout:
  1. Goblet Squats: 3 sets x 12 reps (Rest: 60s)
  2. Dumbbell Chest Press: 3 sets x 12 reps (Rest: 60s)
  3. One-Arm Dumbbell Rows: 3 sets x 10 reps per side (Rest: 60s)
  4. Dumbbell Overhead Press: 3 sets x 10 reps (Rest: 60s)
  5. Standard Plank: 3 sets x 40 seconds (Rest: 45s)
🧘 Cooldown: 5 mins full body hamstring and pectoral stretch.

DAY 2: CARDIO ENDURANCE & POSTURAL CORE
--------------------------------------------------
🔥 Warm-up: 5 mins brisk walking or stationary cycling.
⚡ Main Workout:
  - 30 minutes continuous Zone 2 cardio (Jogging, Rowing, or Cycling).
  - Bird-Dog: 3 sets x 12 per side.
  - Dead Bug: 3 sets x 12 reps.
  - Glute Bridge Holds: 3 sets x 30s.
🧘 Cooldown: 5 mins breathing focus and cobra pose.

DAY 3: LOWER BODY MOBILITY & BALANCE
--------------------------------------------------
🔥 Warm-up: 5 mins ankle and hip mobility drills.
⚡ Main Workout:
  1. Reverse Lunges: 3 sets x 10 reps per leg (Rest: 60s)
  2. Romanian Deadlifts (Light to Moderate): 3 sets x 12 reps (Rest: 60s)
  3. Step-Ups: 3 sets x 10 reps per leg (Rest: 45s)
  4. Side Lying Clamshells: 3 sets x 15 reps (Rest: 30s)
  5. Standing Calf Raises: 3 sets x 15 reps (Rest: 30s)
🧘 Cooldown: 7 mins foam rolling and quad stretch.

DAY 4: ACTIVE RECOVERY & YOGA FLOW
--------------------------------------------------
🌿 Rest & Mobility:
  - 30-40 mins light yoga or nature walk.
  - Hydrate with mineral water and herbal tea.

DAY 5: UPPER BODY & POSTURAL STRENGTH
--------------------------------------------------
🔥 Warm-up: 6 mins band pull-aparts and arm circles.
⚡ Main Workout:
  1. Lat Pulldown or Resistance Band Pulldowns: 3 sets x 12 reps
  2. Incline Push-ups: 3 sets x 12 reps
  3. Dumbbell Lateral Raises: 3 sets x 12 reps
  4. Bicep Curls: 3 sets x 12 reps
  5. Tricep Overhead Extension: 3 sets x 12 reps
🧘 Cooldown: 5 mins shoulder and chest opening stretches.

DAY 6: DYNAMIC INTERVALS & AGILITY
--------------------------------------------------
🔥 Warm-up: 6 mins jumping jacks, high knees, butt kicks.
⚡ Main Workout:
  - 20 mins Interval Training: 1 min fast run/row + 1 min moderate pace (10 rounds).
  - Russian Twists: 3 sets x 20 reps.
  - Superman Lower Back Extensions: 3 sets x 12 reps.
🧘 Cooldown: 6 mins slow cool-down walk and total-body stretch.

DAY 7: RECHARGING & REST
--------------------------------------------------
🌿 Complete rest day. Rest, hydrate, and prepare mind & body for next week!
================================================================================"""

    return plan_content


def generate_workout_gemini(
    goal: str,
    intensity: str,
    age: Optional[int] = None,
    weight: Optional[float] = None,
    username: Optional[str] = None
) -> str:
    """Generate a structured 7-day workout plan using Gemini 1.5 Pro with fallback."""
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or API_KEY

    if api_key and api_key.strip() and not api_key.startswith("your_"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)

            # Try gemini-1.5-pro first as requested, fallback to gemini-1.5-flash
            model = None
            for model_name in ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"]:
                try:
                    model = genai.GenerativeModel(model_name)
                    break
                except Exception:
                    continue

            if model:
                prompt = f"""You are FitBuddy, an elite personal fitness coach and exercise physiologist.
Create a highly structured, comprehensive, and personalized 7-Day Workout Plan tailored to the user.

USER PROFILE:
- Name: {username or 'Athlete'}
- Age: {age or 'Not specified'}
- Weight: {weight} kg if weight else 'Not specified'
- Primary Fitness Goal: {goal}
- Preferred Workout Intensity: {intensity} (High, Medium, or Low)

REQUIREMENTS:
1. Provide a day-by-day plan from Day 1 to Day 7.
2. For each day, specify:
   - Day Title & Muscle / Training Focus
   - Warm-up (5–10 mins with specific exercises & duration)
   - Main Workout (Curated list of exercises, exact sets, reps/duration, and rest intervals)
   - Cooldown or Recovery guidance (stretching, mobility, or foam rolling)
3. Ensure the intensity and volume match the user's selected intensity ({intensity}) and primary goal ({goal}). Include appropriate rest / active recovery days.
4. Format using clean text with clear separators and bullet points so it displays clearly in a <pre> element. Do not use markdown headers (# or ##); use capital headers and ASCII dividers like '====================' and '--------------------'.
"""
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
        except Exception as e:
            logger.warning(f"Gemini API call failed, falling back to smart generator: {e}")

    # Fallback to high quality tailored plan
    return _get_fallback_workout(goal, intensity, age, weight, username)
