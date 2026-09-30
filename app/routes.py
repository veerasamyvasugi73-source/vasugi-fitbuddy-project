import os
from typing import Optional, List
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
# pyrefly: ignore [missing-import]
from fastapi.responses import HTMLResponse, RedirectResponse
# pyrefly: ignore [missing-import]
from fastapi.templating import Jinja2Templates
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from app.database import (
    get_db,
    save_user,
    save_plan,
    update_plan,
    get_user,
    get_original_plan,
    get_plan_by_user,
    get_all_users,
    get_all_plans,
    delete_user,
    User,
    WorkoutPlan
)
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

# Resolve templates directory relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

router = APIRouter()


# Pydantic Schemas for Validation and API
class UserInput(BaseModel):
    username: str = Field(..., min_length=2, max_length=100, description="Full name or nickname of user")
    user_id: str = Field(..., min_length=2, max_length=50, description="Unique User ID")
    age: int = Field(..., ge=10, le=120, description="Age in years")
    weight: float = Field(..., ge=20.0, le=350.0, description="Weight in kg")
    goal: str = Field(..., description="Fitness goal, e.g., Weight Loss, Muscle Gain, Endurance")
    intensity: str = Field(..., description="Intensity: Low, Medium, High")


class FeedbackRequest(BaseModel):
    user_id: str = Field(..., description="Unique User ID")
    feedback: str = Field(..., min_length=3, description="Feedback or adjustments requested")


# ==============================================================================
# HTML Web Routes
# ==============================================================================

@router.get("/", response_class=HTMLResponse)
async def home_route(request: Request):
    """Activity 3.1: Displays the user form via index.html."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "FitBuddy – AI Fitness Plan Generator"}
    )


@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout_route(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Activity 3.1 & 2.2:
    Receives user input from HTML form, validates, calls Gemini Pro & Flash,
    persists in SQLite database, and renders result.html.
    """
    # Clean inputs
    username = username.strip()
    user_id = user_id.strip()
    goal = goal.strip()
    intensity = intensity.strip().capitalize()

    # Save / Update User in DB
    user = save_user(
        db=db,
        username=username,
        user_id=user_id,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    # Call Gemini 1.5 Pro for 7-day Workout Plan
    workout_plan = generate_workout_gemini(
        goal=goal,
        intensity=intensity,
        age=age,
        weight=weight,
        username=username
    )

    # Call Gemini Flash for concise Nutrition / Recovery Tip
    nutrition_tip = generate_nutrition_tip_with_flash(
        goal=goal,
        weight=weight
    )

    # Save Workout Plan in DB
    save_plan(
        db=db,
        user_id=user_id,
        original_plan=workout_plan,
        nutrition_tip=nutrition_tip
    )

    # Render result template
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": user,
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip,
            "is_updated": False,
            "feedback": None,
            "updated_plan": None
        }
    )


@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback_route(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Activity 3.1 & 2.2:
    Captures feedback and user_id, retrieves original plan from DB,
    revises plan using Gemini 1.5 Pro, updates DB, and renders updated result on result.html.
    """
    user_id = user_id.strip()
    feedback = feedback.strip()

    user = get_user(db=db, user_id=user_id)
    plan_record = get_plan_by_user(db=db, user_id=user_id)

    if not user or not plan_record:
        # If user not found, render error on result or redirect
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "error_message": f"User ID '{user_id}' not found. Please create a plan first from the home page.",
                "user": None,
                "username": None,
                "user_id": user_id,
                "age": 0,
                "weight": 0,
                "goal": "N/A",
                "intensity": "N/A",
                "workout_plan": "",
                "nutrition_tip": "",
                "is_updated": False
            },
            status_code=404
        )

    # Retrieve original plan
    original_plan = plan_record.original_plan

    # Use Gemini 1.5 Pro to update plan
    revised_plan = update_workout_plan(
        original_plan=original_plan,
        feedback=feedback,
        goal=user.goal,
        intensity=user.intensity
    )

    # Update the revised plan and feedback in the database
    updated_record = update_plan(
        db=db,
        user_id=user_id,
        updated_plan=revised_plan,
        feedback=feedback
    )

    assert updated_record is not None
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": user,
            "username": user.username,
            "user_id": user.user_id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": original_plan,
            "updated_plan": revised_plan,
            "nutrition_tip": updated_record.nutrition_tip or "Keep fueling your workouts with proper hydration and balanced macros!",
            "is_updated": True,
            "feedback": feedback,
            "success_message": "Workout plan successfully updated with your feedback!"
        }
    )


@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users_route(request: Request, db: Session = Depends(get_db)):
    """Activity 3.1 & Scenario 4: Admin dashboard displaying all users and their workout plans."""
    users = get_all_users(db=db)
    plans = get_all_plans(db=db)
    plans_by_user = {plan.user_id: plan for plan in plans}

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users,
            "plans_by_user": plans_by_user,
            "total_users": len(users),
            "updated_count": sum(1 for p in plans if p.updated_plan)
        }
    )


@router.post("/delete-user/{user_id}")
async def delete_user_route(user_id: str, db: Session = Depends(get_db)):
    """Admin action to delete a user profile and associated plans."""
    delete_user(db=db, user_id=user_id)
    return RedirectResponse(url="/view-all-users", status_code=status.HTTP_303_SEE_OTHER)


# ==============================================================================
# REST API Endpoints (For testing, Swagger /docs, and external clients)
# ==============================================================================

@router.post("/api/generate-plan")
async def api_generate_plan(payload: UserInput, db: Session = Depends(get_db)):
    """REST API endpoint to generate workout plan and nutrition tip."""
    user = save_user(
        db=db,
        username=payload.username,
        user_id=payload.user_id,
        age=payload.age,
        weight=payload.weight,
        goal=payload.goal,
        intensity=payload.intensity
    )

    workout_plan = generate_workout_gemini(
        goal=payload.goal,
        intensity=payload.intensity,
        age=payload.age,
        weight=payload.weight,
        username=payload.username
    )

    nutrition_tip = generate_nutrition_tip_with_flash(
        goal=payload.goal,
        weight=payload.weight
    )

    plan = save_plan(
        db=db,
        user_id=payload.user_id,
        original_plan=workout_plan,
        nutrition_tip=nutrition_tip
    )

    return {
        "status": "success",
        "user": {
            "username": user.username,
            "user_id": user.user_id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity
        },
        "workout_plan": workout_plan,
        "nutrition_tip": nutrition_tip
    }


@router.post("/api/submit-feedback")
async def api_submit_feedback(payload: FeedbackRequest, db: Session = Depends(get_db)):
    """REST API endpoint to revise workout plan based on feedback."""
    user = get_user(db=db, user_id=payload.user_id)
    plan_record = get_plan_by_user(db=db, user_id=payload.user_id)

    if not user or not plan_record:
        raise HTTPException(status_code=404, detail="User or workout plan not found.")

    revised_plan = update_workout_plan(
        original_plan=plan_record.original_plan,
        feedback=payload.feedback,
        goal=user.goal,
        intensity=user.intensity
    )

    updated_record = update_plan(
        db=db,
        user_id=payload.user_id,
        updated_plan=revised_plan,
        feedback=payload.feedback
    )

    assert updated_record is not None
    return {
        "status": "success",
        "user_id": payload.user_id,
        # pyrefly: ignore [missing-attribute]
        "original_plan": updated_record.original_plan,
        "updated_plan": updated_record.updated_plan,
        "feedback": updated_record.feedback
    }


@router.get("/api/users")
async def api_get_users(db: Session = Depends(get_db)):
    """REST API endpoint to fetch all users and their plan summaries."""
    users = get_all_users(db=db)
    plans = get_all_plans(db=db)
    plans_by_user = {plan.user_id: plan for plan in plans}

    results = []
    for u in users:
        p = plans_by_user.get(u.user_id)
        results.append({
            "user_id": u.user_id,
            "username": u.username,
            "age": u.age,
            "weight": u.weight,
            "goal": u.goal,
            "intensity": u.intensity,
            "has_original_plan": bool(p and p.original_plan),
            "has_updated_plan": bool(p and p.updated_plan),
            "created_at": u.created_at.isoformat() if u.created_at else None
        })
    return {"users": results}
