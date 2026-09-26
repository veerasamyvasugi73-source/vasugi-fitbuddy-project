import os
# pyrefly: ignore [missing-import]
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, SessionLocal, User, WorkoutPlan

client = TestClient(app)

def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "FitBuddy" in response.text
    assert "Generate 7-Day Plan" in response.text
    print("PASS: Home page renders correctly")

def test_generate_workout_scenario_1_and_3():
    payload = {
        "username": "David Miller",
        "user_id": "FB-TEST-001",
        "age": "28",
        "weight": "78.5",
        "goal": "Muscle Gain & Hypertrophy",
        "intensity": "High"
    }
    response = client.post("/generate-workout", data=payload)
    assert response.status_code == 200
    assert "David Miller" in response.text
    assert "FB-TEST-001" in response.text
    assert "DAY 1:" in response.text
    assert "DAY 7:" in response.text
    assert "Protein" in response.text or "Nutrition" in response.text
    print("PASS: Scenario 1 (Workout Generation) & Scenario 3 (Nutrition Tip) successful")

def test_feedback_plan_update_scenario_2():
    feedback_payload = {
        "user_id": "FB-TEST-001",
        "feedback": "Add more cardio at the end of sessions and include yoga on rest days"
    }
    response = client.post("/submit-feedback", data=feedback_payload)
    assert response.status_code == 200
    assert "Plan Successfully Updated!" in response.text
    assert "David Miller" in response.text
    assert "CARDIO" in response.text or "YOGA" in response.text or "FEEDBACK" in response.text
    print("PASS: Scenario 2 (Feedback Plan Updating) successful")

def test_admin_view_scenario_4():
    response = client.get("/view-all-users")
    assert response.status_code == 200
    assert "David Miller" in response.text
    assert "FB-TEST-001" in response.text
    assert "Coach & Admin Management Portal" in response.text
    print("PASS: Scenario 4 (Admin Coach View) successful")

def test_api_endpoints():
    api_payload = {
        "username": "Sarah Connor",
        "user_id": "FB-TEST-002",
        "age": 32,
        "weight": 62.0,
        "goal": "Weight Loss & Fat Reduction",
        "intensity": "Medium"
    }
    res = client.post("/api/generate-plan", json=api_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "DAY 1:" in data["workout_plan"]
    assert "nutrition_tip" in data

    feedback_api = {
        "user_id": "FB-TEST-002",
        "feedback": "More focus on core and lower back"
    }
    res2 = client.post("/api/submit-feedback", json=feedback_api)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["status"] == "success"
    assert data2["updated_plan"] is not None

    res3 = client.get("/api/users")
    assert res3.status_code == 200
    users_data = res3.json()
    assert len(users_data["users"]) >= 2
    print("PASS: REST API endpoints tested successfully")

if __name__ == "__main__":
    print("\n--- Running FitBuddy Comprehensive Test Suite ---")
    test_home_page()
    test_generate_workout_scenario_1_and_3()
    test_feedback_plan_update_scenario_2()
    test_admin_view_scenario_4()
    test_api_endpoints()
    print("\nALL SCENARIOS PASSED WITH 100% SUCCESS!\n")
