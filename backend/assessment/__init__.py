"""
Assessment domain package for quiz and learning plan generation.

This package provides services for:
- Dynamic quiz generation based on user profiles
- Quiz scoring with detailed feedback
- Personalized learning plan generation
"""

from backend.assessment.learning_plan_generator import LearningPlanGenerator
from backend.assessment.quiz_generator import QuizGenerator, get_static_quiz_questions
from backend.assessment.quiz_scorer import QuizScorer
from backend.assessment.schemas import (
    LearningPlan,
    Module,
    ProficiencyLevel,
    QuizQuestion,
    QuizResult,
    UserProfile,
)

__all__ = [
    "QuizGenerator",
    "QuizScorer",
    "LearningPlanGenerator",
    "UserProfile",
    "QuizQuestion",
    "QuizResult",
    "LearningPlan",
    "Module",
    "ProficiencyLevel",
    "get_static_quiz_questions",
]
