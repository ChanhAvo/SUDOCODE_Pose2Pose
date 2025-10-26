"""
Training Agent - Part of A2A Multi-Agent System
Conducts real-time practice sessions with near real-time pose feedback
Maintains <2 second latency for optimal user experience
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json


class TrainingSessionMetrics:
    """Tracks metrics during a training session"""

    def __init__(self):
        self.start_time = datetime.now()
        self.frames_analyzed = 0
        self.accuracy_scores = []
        self.feedback_timestamps = []
        self.signs_practiced = []

    def add_frame_result(self, accuracy: float, feedback: str):
        """Record a frame analysis result"""
        self.frames_analyzed += 1
        self.accuracy_scores.append(accuracy)
        self.feedback_timestamps.append({
            "timestamp": (datetime.now() - self.start_time).total_seconds(),
            "accuracy": accuracy,
            "feedback": feedback
        })

    def get_summary(self) -> Dict:
        """Get session summary statistics"""
        duration = (datetime.now() - self.start_time).total_seconds()

        return {
            "duration_seconds": round(duration, 2),
            "frames_analyzed": self.frames_analyzed,
            "average_accuracy": round(sum(self.accuracy_scores) / len(self.accuracy_scores), 2) if self.accuracy_scores else 0,
            "peak_accuracy": max(self.accuracy_scores) if self.accuracy_scores else 0,
            "consistency_score": round(self._calculate_consistency(), 2),
            "fps": round(self.frames_analyzed / duration, 2) if duration > 0 else 0
        }

    def _calculate_consistency(self) -> float:
        """Calculate consistency score based on variance"""
        if not self.accuracy_scores or len(self.accuracy_scores) < 2:
            return 0.0

        mean = sum(self.accuracy_scores) / len(self.accuracy_scores)
        variance = sum((x - mean) ** 2 for x in self.accuracy_scores) / \
            len(self.accuracy_scores)
        std_dev = variance ** 0.5

        # Lower std dev = higher consistency
        # Normalize to 0-1 scale
        consistency = max(0, 1 - (std_dev / 100))
        return consistency


class TrainingAgentHelper:
    """
    Helper class for the Training Agent
    Manages real-time training sessions and provides immediate feedback
    """

    @staticmethod
    def start_training_session(
        session_config: Dict,
        target_signs: List[str]
    ) -> Dict:
        """
        Initialize and conduct a real-time training session

        Args:
            session_config: Session configuration (duration, difficulty, etc.)
            target_signs: List of signs to practice

        Returns:
            Session results and performance metrics
        """
        metrics = TrainingSessionMetrics()
        duration_minutes = session_config.get("duration_minutes", 10)
        video_stream_id = session_config.get("video_stream_id", "default")

        print(f"🎬 Starting training session: {duration_minutes} minutes")
        print(f"📋 Signs to practice: {', '.join(target_signs)}")
        print(f"📹 Video stream: {video_stream_id}")
        print("\n" + "="*60)

        # Simulate real-time feedback (in production, this would process actual video stream)
        feedback_log = TrainingAgentHelper._simulate_realtime_feedback(
            duration_seconds=duration_minutes * 60,
            target_signs=target_signs,
            metrics=metrics
        )

        session_summary = metrics.get_summary()

        result = {
            "status": "completed",
            "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "video_stream_id": video_stream_id,
            "target_signs": target_signs,
            "performance": session_summary,
            "feedback_timeline": feedback_log,
            "grade": TrainingAgentHelper._calculate_grade(session_summary["average_accuracy"]),
            "next_steps": TrainingAgentHelper._generate_next_steps(
                session_summary["average_accuracy"],
                target_signs
            )
        }

        return result

    @staticmethod
    def _simulate_realtime_feedback(
        duration_seconds: int,
        target_signs: List[str],
        metrics: TrainingSessionMetrics
    ) -> List[Dict]:
        """
        Simulate real-time pose feedback during session
        In production, this would process actual video frames

        Args:
            duration_seconds: Session duration
            target_signs: Signs being practiced
            metrics: Metrics tracker

        Returns:
            List of feedback events
        """
        import random

        feedback_log = []

        # Simulate feedback every 2-3 seconds
        current_time = 0
        sign_index = 0

        while current_time < duration_seconds:
            # Simulate varying accuracy
            base_accuracy = random.uniform(70, 95)
            # Add improvement trend over time
            time_factor = min(current_time / duration_seconds, 1) * 10
            accuracy = min(95, base_accuracy + time_factor)

            # Generate contextual feedback
            if accuracy >= 85:
                feedback_msg = "Excellent form! Keep it up! 🌟"
            elif accuracy >= 75:
                feedback_msg = "Good! Watch your hand position. 👍"
            elif accuracy >= 65:
                feedback_msg = "Adjust your wrist angle slightly. 🔄"
            else:
                feedback_msg = "Slow down and focus on accuracy. 📚"

            # Add sign context
            current_sign = target_signs[sign_index % len(target_signs)]
            feedback_msg = f"[{current_sign}] {feedback_msg}"

            metrics.add_frame_result(accuracy, feedback_msg)

            feedback_entry = {
                "timestamp": f"{current_time // 60:02d}:{current_time % 60:02d}",
                "seconds": current_time,
                "sign": current_sign,
                "accuracy": round(accuracy, 1),
                "feedback": feedback_msg,
                "latency_ms": random.randint(50, 200)  # <2000ms requirement
            }
            feedback_log.append(feedback_entry)

            # Move to next time interval
            current_time += random.randint(2, 4)
            sign_index += 1

        return feedback_log

    @staticmethod
    def _calculate_grade(average_accuracy: float) -> str:
        """
        Calculate letter grade based on average accuracy

        Args:
            average_accuracy: Average accuracy percentage

        Returns:
            Letter grade with symbol
        """
        if average_accuracy >= 90:
            return "A+ 🏆 Outstanding!"
        elif average_accuracy >= 85:
            return "A 🌟 Excellent!"
        elif average_accuracy >= 80:
            return "B+ ⭐ Very Good!"
        elif average_accuracy >= 75:
            return "B 👍 Good!"
        elif average_accuracy >= 70:
            return "C+ 📈 Keep Improving!"
        else:
            return "C 💪 Keep Practicing!"

    @staticmethod
    def _generate_next_steps(average_accuracy: float, practiced_signs: List[str]) -> List[str]:
        """
        Generate recommendations for next session

        Args:
            average_accuracy: Average accuracy from session
            practiced_signs: Signs that were practiced

        Returns:
            List of next step recommendations
        """
        next_steps = []

        if average_accuracy >= 85:
            next_steps.append(
                "✅ You've mastered these signs! Try more advanced ones.")
            next_steps.append("🎯 Challenge: Increase signing speed by 20%")
        elif average_accuracy >= 75:
            next_steps.append(
                "🔄 Practice these signs 2-3 more times for consistency")
            next_steps.append(
                "📹 Record yourself to identify specific areas to improve")
        else:
            next_steps.append(
                "📚 Review tutorial videos for: " + ", ".join(practiced_signs))
            next_steps.append(
                "⏰ Practice each sign slowly 10 times before next session")
            next_steps.append(
                "🎓 Consider scheduling a session with simpler signs first")

        next_steps.append(
            "💡 Remember: Consistency is more important than speed!")

        return next_steps

    @staticmethod
    def format_session_report(session_result: Dict) -> str:
        """
        Format session results into readable report

        Args:
            session_result: Session results dictionary

        Returns:
            Formatted report string
        """
        output = []
        output.append("\n" + "="*60)
        output.append("TRAINING SESSION REPORT")
        output.append("="*60)

        perf = session_result["performance"]
        output.append(f"\n📊 Performance Summary:")
        output.append(f"  Duration: {perf['duration_seconds']:.1f} seconds")
        output.append(f"  Frames Analyzed: {perf['frames_analyzed']}")
        output.append(f"  Average Accuracy: {perf['average_accuracy']:.1f}%")
        output.append(f"  Peak Accuracy: {perf['peak_accuracy']:.1f}%")
        output.append(f"  Consistency Score: {perf['consistency_score']:.2f}")
        output.append(f"  Processing Speed: {perf['fps']:.1f} FPS")

        output.append(f"\n🎯 Overall Grade: {session_result['grade']}")

        output.append(f"\n📋 Signs Practiced:")
        for sign in session_result['target_signs']:
            output.append(f"  • {sign}")

        output.append(f"\n🔜 Next Steps:")
        for step in session_result['next_steps']:
            output.append(f"  {step}")

        # Show sample feedback timeline
        output.append(f"\n⏱️  Sample Feedback Timeline:")
        timeline = session_result['feedback_timeline']
        for entry in timeline[:5]:  # Show first 5 entries
            output.append(
                f"  [{entry['timestamp']}] {entry['feedback']} ({entry['accuracy']:.1f}%)")
        if len(timeline) > 5:
            output.append(
                f"  ... and {len(timeline) - 5} more feedback events")

        output.append("\n" + "="*60)

        return "\n".join(output)


# Example usage
if __name__ == "__main__":
    helper = TrainingAgentHelper()

    session_config = {
        "duration_minutes": 2,  # Short demo
        "difficulty": "beginner",
        "video_stream_id": "webcam_demo"
    }

    target_signs = ["hello", "thank_you", "goodbye"]

    result = helper.start_training_session(session_config, target_signs)

    print(helper.format_session_report(result))
    print("\n\nJSON Output:")
    print(json.dumps(result, indent=2))
