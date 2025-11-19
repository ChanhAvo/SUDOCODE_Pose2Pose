"""
Pydantic schemas for assessment domain.

This module defines all data models for the dynamic quiz and learning plan
generation system with comprehensive validation.
"""

from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field, field_validator


class AgeGroup(str, Enum):
    """Age group options."""

    UNDER_18 = "Under 18"
    AGE_18_24 = "18-24"
    AGE_25_34 = "25-34"
    AGE_35_44 = "35-44"
    AGE_45_54 = "45-54"
    AGE_55_PLUS = "55+"


class PriorExperience(str, Enum):
    """Prior sign language experience levels."""

    NONE = "None - Complete beginner"
    SOME = "Some exposure (watched videos, met deaf people)"
    CLASS = "Taken a class or course before"
    FLUENT = "Fluent or near-fluent"


class LearningGoal(str, Enum):
    """Learning goal options."""

    PERSONAL = "Personal interest"
    FAMILY = "Communicate with deaf family/friends"
    PROFESSIONAL = "Professional development"
    ACADEMIC = "Academic requirement"
    COMMUNITY = "Community involvement"


class TimeCommitment(str, Enum):
    """Time commitment per week options."""

    LESS_THAN_2 = "Less than 2 hours"
    TWO_TO_FIVE = "2-5 hours"
    FIVE_TO_TEN = "5-10 hours"
    MORE_THAN_TEN = "More than 10 hours"


class UserProfile(BaseModel):
    """User profile from basic info collection."""

    name: str = Field(..., min_length=1, max_length=100)
    email: Optional[str] = Field(default=None)
    age_group: AgeGroup
    prior_experience: PriorExperience
    learning_goal: LearningGoal
    time_commitment: TimeCommitment
    motivation: str = Field(..., min_length=10, max_length=2000)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        """Validate email format if provided."""
        if v and "@" not in v:
            raise ValueError("Invalid email format")
        return v

    class Config:
        use_enum_values = True


class QuestionType(str, Enum):
    """Quiz question types."""

    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"


class Difficulty(str, Enum):
    """Difficulty levels."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class MultipleChoiceQuestion(BaseModel):
    """Multiple choice quiz question."""

    id: str = Field(..., pattern=r"^q\d+$")
    question: str = Field(..., min_length=10, max_length=500)
    type: QuestionType = QuestionType.MULTIPLE_CHOICE
    options: List[str] = Field(..., min_length=2, max_length=6)
    correct_answer: int = Field(..., ge=0)
    difficulty: Difficulty
    explanation: str = Field(..., min_length=10, max_length=500)

    @field_validator("correct_answer")
    @classmethod
    def validate_correct_answer(cls, v: int, info) -> int:
        """Ensure correct_answer is valid index."""
        if "options" in info.data and v >= len(info.data["options"]):
            raise ValueError("correct_answer index out of range")
        return v

    class Config:
        use_enum_values = True


class ShortAnswerQuestion(BaseModel):
    """Short answer quiz question."""

    id: str = Field(..., pattern=r"^q\d+$")
    question: str = Field(..., min_length=10, max_length=500)
    type: QuestionType = QuestionType.SHORT_ANSWER
    scoring_rubric: str = Field(..., min_length=20, max_length=1000)
    difficulty: Difficulty
    sample_answer: str = Field(..., min_length=20, max_length=1000)

    class Config:
        use_enum_values = True


# Union type for quiz questions
QuizQuestion = Union[MultipleChoiceQuestion, ShortAnswerQuestion]


class QuestionScore(BaseModel):
    """Score for an individual question."""

    question_id: str
    points_earned: float = Field(..., ge=0)
    points_possible: float = Field(..., gt=0)
    percentage: float = Field(..., ge=0, le=100)
    feedback: str = Field(..., min_length=10, max_length=1000)

    @field_validator("percentage")
    @classmethod
    def validate_percentage(cls, v: float, info) -> float:
        """Validate percentage matches points."""
        if "points_earned" in info.data and "points_possible" in info.data:
            expected = (info.data["points_earned"] / info.data["points_possible"]) * 100
            if abs(v - expected) > 0.1:  # Allow small rounding errors
                raise ValueError("Percentage mismatch with points")
        return v


class ProficiencyLevel(str, Enum):
    """Proficiency levels."""

    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class QuizResult(BaseModel):
    """Complete quiz scoring result."""

    question_scores: dict[str, QuestionScore]
    total_score: float = Field(..., ge=0)
    total_possible: float = Field(..., gt=0)
    percentage: float = Field(..., ge=0, le=100)
    level: ProficiencyLevel
    overall_feedback: str = Field(..., min_length=20, max_length=2000)
    strengths: List[str] = Field(..., min_length=1, max_length=10)
    areas_for_improvement: List[str] = Field(..., min_length=1, max_length=10)

    @field_validator("percentage")
    @classmethod
    def validate_percentage(cls, v: float, info) -> float:
        """Validate percentage calculation."""
        if "total_score" in info.data and "total_possible" in info.data:
            expected = (info.data["total_score"] / info.data["total_possible"]) * 100
            if abs(v - expected) > 0.1:
                raise ValueError("Percentage mismatch with scores")
        return v

    class Config:
        use_enum_values = True


class LessonType(str, Enum):
    """Lesson types matching existing frontend."""

    VIDEO = "Video"
    INTERACTIVE = "Interactive"
    PRACTICE = "Practice"
    QUIZ = "Quiz"


class Lesson(BaseModel):
    """Individual lesson within a module."""

    title: str = Field(..., min_length=5, max_length=200)
    duration: str = Field(..., pattern=r"^\d+ min$")
    type: LessonType

    class Config:
        use_enum_values = True


class Module(BaseModel):
    """Learning module matching MODULES_DATABASE structure."""

    id: str = Field(..., pattern=r"^mod_\w+$")
    title: str = Field(..., min_length=10, max_length=200)
    description: str = Field(..., min_length=20, max_length=1000)
    difficulty: Difficulty
    duration: str = Field(..., pattern=r"^\d+ weeks?$")
    lessons_count: int = Field(..., ge=5, le=20)
    estimated_hours: int = Field(..., ge=5, le=50)
    skills: List[str] = Field(..., min_length=3, max_length=8)
    lessons: List[Lesson] = Field(..., min_length=5)

    @field_validator("lessons_count")
    @classmethod
    def validate_lessons_count(cls, v: int, info) -> int:
        """Ensure lessons_count matches actual lessons."""
        if "lessons" in info.data and v != len(info.data["lessons"]):
            raise ValueError("lessons_count must match number of lessons")
        return v

    class Config:
        use_enum_values = True


class LearningPlan(BaseModel):
    """Complete personalized learning plan."""

    user_id: str = Field(..., min_length=1, max_length=100)
    level: ProficiencyLevel
    created_at: Optional[str] = None  # ISO format string instead of datetime
    time_commitment: TimeCommitment
    learning_goal: LearningGoal
    modules: List[Module] = Field(..., min_length=2, max_length=6)

    class Config:
        use_enum_values = True


# Structured output wrapper models for LLM responses
class QuizQuestionsResponse(BaseModel):
    """Wrapper model for quiz questions structured output."""

    questions: List[Union[MultipleChoiceQuestion, ShortAnswerQuestion]] = Field(
        ..., min_length=5, max_length=5
    )


class QuizScoringResponse(BaseModel):
    """Wrapper model for quiz scoring structured output."""

    question_scores: List[QuestionScore] = Field(..., min_length=1, max_length=10)
    total_score: float = Field(..., ge=0)
    total_possible: float = Field(..., gt=0)
    percentage: float = Field(..., ge=0, le=100)
    level: ProficiencyLevel
    overall_feedback: str = Field(..., min_length=20, max_length=2000)
    strengths: List[str] = Field(..., min_length=1, max_length=10)
    areas_for_improvement: List[str] = Field(..., min_length=1, max_length=10)

    class Config:
        use_enum_values = True


# Helper types for frontend integration
class QuizGenerationResult(BaseModel):
    """Result from quiz generation."""

    success: bool
    questions: List[dict]  # Serialized QuizQuestion objects
    source: str = Field(..., pattern=r"^(dynamic|static_fallback)$")
    error: Optional[str] = None


class QuizScoringResult(BaseModel):
    """Result from quiz scoring."""

    success: bool
    result: Optional[dict] = None  # Serialized QuizResult
    error: Optional[str] = None


class LearningPlanResult(BaseModel):
    """Result from learning plan generation."""

    success: bool
    plan: Optional[dict] = None  # Serialized LearningPlan
    file_path: Optional[str] = None
    error: Optional[str] = None
