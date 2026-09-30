import datetime
from typing import Optional, List
# pyrefly: ignore [missing-import]
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String(100), nullable=False)
    intensity = Column(String(50), nullable=False)
    # pyrefly: ignore [deprecated]
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationship to workout plans
    plans = relationship("WorkoutPlan", back_populates="user", cascade="all, delete-orphan")


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    # pyrefly: ignore [deprecated]
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    # pyrefly: ignore [deprecated]
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationship to user
    user = relationship("User", back_populates="plans")


def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency generator for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_user(db: Session, username: str, user_id: str, age: int, weight: float, goal: str, intensity: str) -> User:
    """Save or update user details in the database."""
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        # pyrefly: ignore [read-only]
        user.username = username
        # pyrefly: ignore [read-only]
        user.age = age
        # pyrefly: ignore [read-only]
        user.weight = weight
        # pyrefly: ignore [read-only]
        user.goal = goal
        # pyrefly: ignore [read-only]
        user.intensity = intensity
    else:
        user = User(
            user_id=user_id,
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )
        db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_plan(db: Session, user_id: str, original_plan: str, nutrition_tip: Optional[str] = None) -> WorkoutPlan:
    """Save an original workout plan and nutrition tip for a user."""
    # Check if a plan already exists for this user; if so, update its original plan
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
    if plan:
        # pyrefly: ignore [read-only]
        plan.original_plan = original_plan
        # pyrefly: ignore [read-only]
        plan.nutrition_tip = nutrition_tip
        # pyrefly: ignore [read-only]
        plan.updated_plan = None
        # pyrefly: ignore [read-only]
        plan.feedback = None
        # pyrefly: ignore [read-only]
        plan.updated_at = datetime.datetime.utcnow()
    else:
        plan = WorkoutPlan(
            user_id=user_id,
            original_plan=original_plan,
            nutrition_tip=nutrition_tip
        )
        db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def update_plan(db: Session, user_id: str, updated_plan: str, feedback: Optional[str] = None) -> Optional[WorkoutPlan]:
    """Update a user's workout plan with feedback revisions."""
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
    if plan:
        # pyrefly: ignore [read-only]
        plan.updated_plan = updated_plan
        if feedback:
            # pyrefly: ignore [read-only]
            plan.feedback = feedback
        # pyrefly: ignore [read-only]
        plan.updated_at = datetime.datetime.utcnow()
        db.commit()
        db.refresh(plan)
        return plan
    return None


def get_user(db: Session, user_id: str) -> Optional[User]:
    """Retrieve user by user_id."""
    return db.query(User).filter(User.user_id == user_id).first()


def get_original_plan(db: Session, user_id: str) -> Optional[str]:
    """Retrieve original plan text for a user."""
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
    return plan.original_plan if plan else None


def get_plan_by_user(db: Session, user_id: str) -> Optional[WorkoutPlan]:
    """Retrieve the full WorkoutPlan record for a user."""
    return db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()


def get_all_users(db: Session) -> List[User]:
    """Retrieve all users ordered by creation date descending."""
    return db.query(User).order_by(User.created_at.desc()).all()


def get_all_plans(db: Session) -> List[WorkoutPlan]:
    """Retrieve all workout plans ordered by creation date descending."""
    return db.query(WorkoutPlan).order_by(WorkoutPlan.created_at.desc()).all()


def delete_user(db: Session, user_id: str) -> bool:
    """Delete a user and associated plans."""
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
