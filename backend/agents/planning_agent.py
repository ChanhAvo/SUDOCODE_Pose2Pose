"""
Planning Agent - Part of A2A Multi-Agent System
Responsible for creating personalized learning plans based on assessment results
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json


class PlanningAgentHelper:
    """
    Helper class for the Planning/Teaching Agent
    Provides structured learning plan generation logic
    """

    DIFFICULTY_LEVELS = {
        "beginner": {
            "duration_weeks": 8,
            "signs_per_week": 5,
            "practice_minutes_per_day": 15
        },
        "intermediate": {
            "duration_weeks": 12,
            "signs_per_week": 8,
            "practice_minutes_per_day": 25
        },
        "advanced": {
            "duration_weeks": 16,
            "signs_per_week": 10,
            "practice_minutes_per_day": 35
        }
    }

    VSL_CURRICULUM = {
        "beginner": [
            "Greetings", "Basic Emotions", "Family Members", "Numbers 1-10",
            "Colors", "Daily Activities", "Common Objects", "Yes/No Questions"
        ],
        "intermediate": [
            "Complex Emotions", "Time Expressions", "Weather", "Food & Drink",
            "Transportation", "Workplace Communication", "Medical Terms", "Directions"
        ],
        "advanced": [
            "Abstract Concepts", "Idioms", "Professional Vocabulary", "Storytelling",
            "Debate Expressions", "Cultural References", "Regional Variations", "Speed Signing"
        ]
    }

    @staticmethod
    def generate_learning_plan(
        current_level: str,
        strengths: List[str],
        weaknesses: List[str],
        user_goals: str
    ) -> Dict:
        """
        Generate a structured learning plan

        Args:
            current_level: User's proficiency level
            strengths: Areas where user excels
            weaknesses: Areas needing improvement
            user_goals: User's stated learning objectives

        Returns:
            Comprehensive learning plan dictionary
        """
        level_config = PlanningAgentHelper.DIFFICULTY_LEVELS.get(
            current_level.lower(),
            PlanningAgentHelper.DIFFICULTY_LEVELS["beginner"]
        )

        curriculum = PlanningAgentHelper.VSL_CURRICULUM.get(
            current_level.lower(),
            PlanningAgentHelper.VSL_CURRICULUM["beginner"]
        )

        # Calculate milestones
        total_weeks = level_config["duration_weeks"]
        signs_per_week = level_config["signs_per_week"]

        milestones = []
        for week in range(1, total_weeks + 1, 4):
            milestone = {
                "week": week,
                "goal": f"Master {curriculum[(week-1)//4] if (week-1)//4 < len(curriculum) else 'Advanced topics'}",
                "assessment": "Practice test at end of milestone"
            }
            milestones.append(milestone)

        plan = {
            "user_level": current_level,
            "generated_at": datetime.now().isoformat(),
            "duration": {
                "weeks": total_weeks,
                "estimated_completion": (datetime.now() + timedelta(weeks=total_weeks)).strftime("%Y-%m-%d")
            },
            "daily_practice": {
                "minutes_per_day": level_config["practice_minutes_per_day"],
                "recommended_times": ["Morning", "Evening"]
            },
            "curriculum": {
                "topics": curriculum,
                "signs_per_week": signs_per_week,
                "total_signs": total_weeks * signs_per_week
            },
            "personalization": {
                "focus_areas": weaknesses or ["General improvement"],
                "build_on_strengths": strengths or ["Will assess during first week"],
                "user_goals": user_goals
            },
            "milestones": milestones,
            "resources": [
                {"type": "video", "title": "VSL Basics Introduction",
                    "duration": "15min"},
                {"type": "interactive", "title": "Hand Shape Practice",
                    "duration": "10min"},
                {"type": "quiz", "title": "Weekly Assessment", "duration": "5min"}
            ],
            "success_criteria": {
                "accuracy_threshold": 80,
                "consistency_requirement": "3 consecutive correct demonstrations",
                "completion_rate": "Complete 90% of weekly practice sessions"
            }
        }

        return plan

    @staticmethod
    def adjust_plan_based_on_progress(
        current_plan: Dict,
        recent_performance: Dict
    ) -> Dict:
        """
        Adjust learning plan based on actual progress

        Args:
            current_plan: Existing learning plan
            recent_performance: Recent performance metrics

        Returns:
            Updated learning plan
        """
        avg_accuracy = recent_performance.get("average_accuracy", 0)

        if avg_accuracy > 90:
            # User is excelling, can accelerate
            current_plan["curriculum"]["signs_per_week"] += 2
            current_plan["recommendation"] = "Excellent progress! Increased difficulty."
        elif avg_accuracy < 70:
            # User needs more time
            current_plan["daily_practice"]["minutes_per_day"] += 5
            current_plan["recommendation"] = "Let's focus on fundamentals. Added practice time."
        else:
            current_plan["recommendation"] = "Good progress! Keep up the current pace."

        return current_plan


# Example usage for testing
if __name__ == "__main__":
    helper = PlanningAgentHelper()

    # Test plan generation
    plan = helper.generate_learning_plan(
        current_level="beginner",
        strengths=["Good hand-eye coordination"],
        weaknesses=["Finger dexterity", "Memorization"],
        user_goals="Learn basic VSL for family communication"
    )

    print(json.dumps(plan, indent=2))
