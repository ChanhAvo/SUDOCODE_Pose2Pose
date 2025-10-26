"""
Main entry point for Vietnamese Sign Language Learning A2A System
Demonstrates the multi-agent collaboration using CrewAI
"""

from backend.crew.sign_language_crew import SignLanguageCrew, create_sign_language_crew
from typing import Dict, Optional
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SignLanguageLearningApp:
    """
    Main application orchestrating the A2A multi-agent system
    """
    
    def __init__(self):
        self.crew = create_sign_language_crew()
        self.current_user_level = None
        self.learning_plan = None
        
    def onboard_new_user(self, user_name: str) -> Dict:
        """
        Onboard a new user: assess level and create learning plan
        
        Args:
            user_name: User's name
            
        Returns:
            Dict containing assessment and learning plan
        """
        print(f"\n{'='*60}")
        print(f"Welcome {user_name} to Vietnamese Sign Language Learning!")
        print(f"{'='*60}\n")
        
        # Initial questions for assessment
        print("Let's assess your current level...")
        user_responses = input("Tell us about your VSL experience (or press Enter for demo): ")
        if not user_responses:
            user_responses = "I'm a complete beginner with no prior sign language experience"
            
        user_goals = input("What are your learning goals? (or press Enter for demo): ")
        if not user_goals:
            user_goals = "I want to learn basic Vietnamese Sign Language for daily communication"
        
        print("\n🤖 Assessment and Planning Agents are working...\n")
        
        result = self.crew.run_assessment_and_planning(
            user_responses=user_responses,
            user_goals=user_goals
        )
        
        print(f"\n✅ Assessment Complete!")
        print(f"📊 Your Level: {result.get('level', 'Beginner')}")
        print(f"📚 Learning plan has been created!\n")
        
        self.current_user_level = result.get('level', 'Beginner')
        self.learning_plan = result
        
        return result
    
    def practice_with_feedback(self, image_path: str, target_sign: str) -> Dict:
        """
        Upload pose and get feedback from agents
        
        Args:
            image_path: Path to uploaded image/video
            target_sign: The sign user is attempting
            
        Returns:
            Dict with validation and feedback
        """
        print(f"\n{'='*60}")
        print(f"Analyzing your '{target_sign}' sign...")
        print(f"{'='*60}\n")
        
        print("🤖 Feedback Agent is analyzing your pose...\n")
        
        result = self.crew.run_pose_feedback(
            media_input=image_path,
            target_sign=target_sign,
            user_level=self.current_user_level or "beginner"
        )
        
        print(f"\n✅ Analysis Complete!")
        print(f"📈 Accuracy: {result.get('accuracy', 'N/A')}%")
        print(f"💡 Feedback ready!\n")
        
        return result
    
    def start_training_session(self, duration_minutes: int = 10) -> Dict:
        """
        Start a real-time training session
        
        Args:
            duration_minutes: Session duration in minutes
            
        Returns:
            Dict with session results and progress
        """
        print(f"\n{'='*60}")
        print(f"Starting {duration_minutes}-minute Training Session")
        print(f"{'='*60}\n")
        
        session_config = {
            "duration_minutes": duration_minutes,
            "difficulty": self.current_user_level or "beginner",
            "video_stream_id": "webcam_001"
        }
        
        target_signs = ["greeting", "thank_you", "hello"]
        
        print("🤖 Trainer Agent is ready!")
        print("📹 Prepare your camera for real-time feedback...\n")
        
        result = self.crew.run_realtime_training(
            session_config=session_config,
            target_signs=target_signs,
            user_history={"previous_sessions": 0}
        )
        
        print(f"\n✅ Training Session Complete!")
        print(f"⭐ Great work!\n")
        
        return result
    
    def query_learning_materials(self, query: str) -> Dict:
        """
        Search for learning resources using MCP RAG
        
        Args:
            query: User's search query
            
        Returns:
            Dict with relevant resources
        """
        print(f"\n{'='*60}")
        print(f"Searching for: '{query}'")
        print(f"{'='*60}\n")
        
        print("🤖 Teaching Agent is searching knowledge base...\n")
        
        learning_context = {
            "user_level": self.current_user_level or "beginner",
            "current_topic": "basics"
        }
        
        result = self.crew.query_learning_resources(
            user_query=query,
            learning_context=learning_context
        )
        
        print(f"\n✅ Found relevant materials!\n")
        
        return result


def interactive_menu():
    """
    Interactive command-line menu for testing the A2A system
    """
    app = SignLanguageLearningApp()
    user_name = None
    
    while True:
        print("\n" + "="*60)
        print("Vietnamese Sign Language Learning - A2A System")
        print("="*60)
        print("\n1. Onboard New User (Assessment + Learning Plan)")
        print("2. Practice with Feedback (Upload Pose)")
        print("3. Real-time Training Session")
        print("4. Search Learning Materials (MCP RAG)")
        print("5. Demo Full A2A Workflow")
        print("6. Exit")
        print()
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice == "1":
            name = input("Enter your name: ").strip() or "Student"
            user_name = name
            result = app.onboard_new_user(user_name)
            print(f"\n📄 Result:\n{json.dumps(result, indent=2, default=str)}")
            
        elif choice == "2":
            if not user_name:
                print("\n⚠️  Please complete onboarding first (Option 1)")
                continue
            image_path = input("Enter image path (or press Enter for demo): ").strip()
            if not image_path:
                image_path = "./uploads/demo_pose.jpg"
            target_sign = input("Which sign are you practicing? (or press Enter for 'greeting'): ").strip()
            if not target_sign:
                target_sign = "greeting"
            result = app.practice_with_feedback(image_path, target_sign)
            print(f"\n📄 Result:\n{json.dumps(result, indent=2, default=str)}")
            
        elif choice == "3":
            if not user_name:
                print("\n⚠️  Please complete onboarding first (Option 1)")
                continue
            duration = input("Session duration in minutes (default 10): ").strip()
            duration = int(duration) if duration.isdigit() else 10
            result = app.start_training_session(duration)
            print(f"\n📄 Result:\n{json.dumps(result, indent=2, default=str)}")
            
        elif choice == "4":
            query = input("What would you like to learn about? ").strip()
            if not query:
                query = "How to sign 'hello' in Vietnamese Sign Language"
            result = app.query_learning_materials(query)
            print(f"\n📄 Result:\n{json.dumps(result, indent=2, default=str)}")
            
        elif choice == "5":
            print("\n🚀 Running Full A2A Demonstration...")
            from backend.crew.sign_language_crew import demo_a2a_workflow
            demo_a2a_workflow()
            
        elif choice == "6":
            print("\n👋 Thank you for using VSL Learning System!")
            print("Keep practicing! 🤟\n")
            break
            
        else:
            print("\n❌ Invalid option. Please select 1-6.")
        
        input("\nPress Enter to continue...")


def main():
    """
    Main entry point
    """
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  WARNING: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
        print("Example: OPENAI_API_KEY=sk-...")
        print("\nContinuing with demo mode...\n")
    
    try:
        interactive_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
