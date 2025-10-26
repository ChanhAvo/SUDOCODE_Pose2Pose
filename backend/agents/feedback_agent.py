"""
Feedback Agent - Part of A2A Multi-Agent System
Provides constructive feedback on user's sign language poses
Communicates with Teaching Agent for pedagogical consistency
"""

from typing import Dict, List, Optional
from pydantic import BaseModel
import json


class PoseFeedback(BaseModel):
    """Structured feedback model"""
    accuracy_percentage: float
    overall_assessment: str
    positive_aspects: List[str]
    corrections_needed: List[Dict[str, str]]
    practice_recommendations: List[str]
    estimated_practice_time: int  # minutes
    difficulty_adjustment: Optional[str] = None


class FeedbackAgentHelper:
    """
    Helper class for the Feedback Agent
    Translates technical CV output into user-friendly, actionable feedback
    """

    ENCOURAGEMENT_MESSAGES = {
        "excellent": [
            "Outstanding! Your form is nearly perfect! 🌟",
            "Incredible work! You've mastered this sign! 👏",
            "Perfect execution! You're a natural! ✨"
        ],
        "good": [
            "Great job! You're very close to perfect form! 👍",
            "Well done! Just a few minor adjustments needed! 💪",
            "Nice work! You're making excellent progress! 🎯"
        ],
        "needs_improvement": [
            "Good effort! Let's work on refining your technique! 📚",
            "You're on the right track! Keep practicing! 🔄",
            "Don't worry, with practice you'll get there! 💡"
        ],
        "keep_trying": [
            "Remember, every expert was once a beginner! 🌱",
            "Progress takes time. Let's break this down together! 🔍",
            "You're learning! Let's focus on the fundamentals! 📖"
        ]
    }

    @staticmethod
    def generate_feedback(
        validation_results: Dict,
        user_level: str,
        target_sign: str
    ) -> PoseFeedback:
        """
        Generate constructive feedback from validation results

        Args:
            validation_results: Technical output from pose validation
            user_level: User's proficiency level
            target_sign: The sign being practiced

        Returns:
            Structured PoseFeedback object
        """
        accuracy = validation_results.get("accuracy", 0)
        technical_corrections = validation_results.get(
            "feedback", {}).get("improvements", [])
        correct_aspects = validation_results.get(
            "feedback", {}).get("correct_aspects", [])

        # Determine encouragement level
        if accuracy >= 90:
            level = "excellent"
        elif accuracy >= 80:
            level = "good"
        elif accuracy >= 65:
            level = "needs_improvement"
        else:
            level = "keep_trying"

        # Generate overall assessment
        import random
        overall = random.choice(
            FeedbackAgentHelper.ENCOURAGEMENT_MESSAGES[level])
        overall += f"\n\nYour '{target_sign}' sign scored {accuracy:.1f}% accuracy."

        # Format corrections in user-friendly way
        corrections = []
        for correction in technical_corrections:
            corrections.append({
                "issue": correction,
                "how_to_fix": FeedbackAgentHelper._get_correction_tip(correction),
                "priority": "high" if "critical" in correction.lower() else "medium"
            })

        # Generate practice recommendations
        recommendations = FeedbackAgentHelper._generate_recommendations(
            accuracy, user_level, technical_corrections
        )

        # Estimate practice time needed
        if accuracy >= 85:
            practice_time = 5
        elif accuracy >= 70:
            practice_time = 10
        else:
            practice_time = 15

        # Difficulty adjustment suggestion
        difficulty_adjustment = None
        if accuracy >= 95 and user_level == "beginner":
            difficulty_adjustment = "consider_intermediate"
        elif accuracy < 60 and user_level != "beginner":
            difficulty_adjustment = "review_basics"

        return PoseFeedback(
            accuracy_percentage=accuracy,
            overall_assessment=overall,
            positive_aspects=correct_aspects or ["You attempted the sign!"],
            corrections_needed=corrections,
            practice_recommendations=recommendations,
            estimated_practice_time=practice_time,
            difficulty_adjustment=difficulty_adjustment
        )

    @staticmethod
    def _get_correction_tip(technical_correction: str) -> str:
        """
        Convert technical correction to user-friendly instruction

        Args:
            technical_correction: Technical description of issue

        Returns:
            User-friendly instruction
        """
        correction_tips = {
            "hand": "Focus on hand positioning. Watch yourself in a mirror.",
            "wrist": "Pay attention to wrist rotation. Move slowly and deliberately.",
            "finger": "Practice finger movements separately before combining.",
            "shoulder": "Check your shoulder alignment. Keep them relaxed.",
            "elbow": "Adjust your elbow angle. Try practicing against a wall.",
            "angle": "Work on the angle of movement. Review the reference video.",
            "position": "Double-check your starting position before signing.",
            "movement": "Focus on the smoothness of your movement path.",
            "speed": "Try slowing down to ensure accuracy first, then increase speed."
        }

        correction_lower = technical_correction.lower()
        for keyword, tip in correction_tips.items():
            if keyword in correction_lower:
                return tip

        return "Practice this aspect slowly and check against reference materials."

    @staticmethod
    def _generate_recommendations(
        accuracy: float,
        user_level: str,
        corrections: List[str]
    ) -> List[str]:
        """
        Generate practice recommendations based on performance

        Args:
            accuracy: Accuracy percentage
            user_level: User's level
            corrections: List of corrections needed

        Returns:
            List of practice recommendations
        """
        recommendations = []

        if accuracy >= 80:
            recommendations.append("✅ You're ready to move to the next sign!")
            recommendations.append(
                "📹 Record yourself and compare with reference video")
        else:
            recommendations.append("🎯 Practice this sign 10 more times")
            recommendations.append(
                "🔄 Break down the sign into smaller movements")
            recommendations.append("📺 Watch the tutorial video again")

        if len(corrections) > 3:
            recommendations.append(
                "💡 Focus on one correction at a time, not all at once")

        if user_level == "beginner":
            recommendations.append("📚 Review the beginner fundamentals guide")

        recommendations.append(
            "⏰ Practice for 5-10 minutes daily for best results")

        return recommendations

    @staticmethod
    def format_feedback_for_display(feedback: PoseFeedback) -> str:
        """
        Format feedback object into readable text for display

        Args:
            feedback: PoseFeedback object

        Returns:
            Formatted string for display
        """
        output = []
        output.append("=" * 60)
        output.append("POSE FEEDBACK REPORT")
        output.append("=" * 60)
        output.append(f"\n{feedback.overall_assessment}\n")

        output.append("\n✅ What you did well:")
        for aspect in feedback.positive_aspects:
            output.append(f"  • {aspect}")

        if feedback.corrections_needed:
            output.append("\n🔧 Areas to improve:")
            for i, correction in enumerate(feedback.corrections_needed, 1):
                output.append(f"  {i}. {correction['issue']}")
                output.append(f"     💡 {correction['how_to_fix']}")

        output.append("\n📋 Practice Recommendations:")
        for rec in feedback.practice_recommendations:
            output.append(f"  {rec}")

        output.append(
            f"\n⏱️  Recommended practice time: {feedback.estimated_practice_time} minutes")

        if feedback.difficulty_adjustment:
            if feedback.difficulty_adjustment == "consider_intermediate":
                output.append("\n🎉 You're ready for intermediate level!")
            elif feedback.difficulty_adjustment == "review_basics":
                output.append("\n📖 Consider reviewing basic techniques")

        output.append("\n" + "=" * 60)

        return "\n".join(output)


# Example usage
if __name__ == "__main__":
    # Simulate validation results from CV model
    mock_validation = {
        "accuracy": 82.5,
        "feedback": {
            "correct_aspects": [
                "Hand position is accurate",
                "Shoulder alignment is good"
            ],
            "improvements": [
                "Adjust wrist angle by 10 degrees",
                "Maintain finger spread more consistently"
            ]
        }
    }

    helper = FeedbackAgentHelper()
    feedback = helper.generate_feedback(
        validation_results=mock_validation,
        user_level="beginner",
        target_sign="greeting"
    )

    print(helper.format_feedback_for_display(feedback))
    print("\n\nJSON Output:")
    print(feedback.model_dump_json(indent=2))
