"""
Sign Language Learning A2A Multi-Agent System
Implements Agent-to-Agent protocol using CrewAI for Vietnamese Sign Language learning
"""

from backend.core.tools import (
    PoseDetectionTool,
    PoseValidationTool,
    RealTimePoseFeedbackTool,
    MCPKnowledgeBaseTool
)
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from pathlib import Path
import yaml
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import custom tools


@CrewBase
class SignLanguageCrew:
    """
    Vietnamese Sign Language Learning Crew
    A2A Multi-Agent System with specialized agents for teaching, assessment, feedback, and progress tracking
    """

    agents_config = Path(__file__).parent / 'agents.yaml'
    tasks_config = Path(__file__).parent / 'tasks.yaml'

    def __init__(self):
        """Initialize the crew with tools"""
        self.pose_detection_tool = PoseDetectionTool()
        self.pose_validation_tool = PoseValidationTool()
        self.realtime_feedback_tool = RealTimePoseFeedbackTool()
        self.mcp_knowledge_tool = MCPKnowledgeBaseTool()

    # ==================== AGENTS ====================

    @agent
    def teaching_agent(self) -> Agent:
        """
        Teaching Agent: Designs lessons and learning pathways
        Can delegate to other agents for specific assessments or feedback
        """
        return Agent(
            config=self.agents_config['teaching_agent'],
            tools=[self.mcp_knowledge_tool],
            allow_delegation=True,
            verbose=True
        )

    @agent
    def assessment_agent(self) -> Agent:
        """
        Assessment Agent: Evaluates user proficiency and provides scoring
        Collaborates with teaching agent for proper level placement
        """
        return Agent(
            config=self.agents_config['assessment_agent'],
            allow_delegation=True,
            verbose=True
        )

    @agent
    def feedback_agent(self) -> Agent:
        """
        Feedback Agent: Provides detailed, constructive pose feedback
        Uses CV tools and coordinates with teaching agent for pedagogical approach
        """
        return Agent(
            config=self.agents_config['feedback_agent'],
            tools=[
                self.pose_detection_tool,
                self.pose_validation_tool,
                self.mcp_knowledge_tool
            ],
            allow_delegation=True,
            verbose=True
        )

    @agent
    def progress_tracking_agent(self) -> Agent:
        """
        Progress Tracking Agent: Monitors and analyzes learning progress
        Coordinates with teaching agent to adjust learning plans
        """
        return Agent(
            config=self.agents_config['progress_tracking_agent'],
            allow_delegation=True,
            verbose=True
        )

    @agent
    def trainer_agent(self) -> Agent:
        """
        Trainer Agent: Conducts real-time practice sessions
        Uses real-time feedback tools for live coaching
        """
        return Agent(
            config=self.agents_config['trainer_agent'],
            tools=[self.realtime_feedback_tool],
            allow_delegation=False,  # Focused on real-time coaching
            verbose=True
        )

    # ==================== TASKS ====================

    @task
    def assess_user_level_task(self) -> Task:
        """Task 1: Initial proficiency assessment"""
        return Task(
            config=self.tasks_config['assess_user_level'],
            agent=self.assessment_agent()
        )

    @task
    def create_learning_plan_task(self) -> Task:
        """Task 2: Create personalized learning plan based on assessment"""
        return Task(
            config=self.tasks_config['create_personalized_learning_plan'],
            agent=self.teaching_agent(),
            context=[self.assess_user_level_task()]
        )

    @task
    def validate_pose_task(self) -> Task:
        """Task 3: Validate user pose using CV tools"""
        return Task(
            config=self.tasks_config['validate_user_pose'],
            agent=self.feedback_agent()
        )

    @task
    def provide_feedback_task(self) -> Task:
        """Task 4: Provide detailed improvement feedback"""
        return Task(
            config=self.tasks_config['provide_improvement_feedback'],
            agent=self.feedback_agent(),
            context=[self.validate_pose_task()]
        )

    @task
    def realtime_training_task(self) -> Task:
        """Task 5: Conduct real-time training session"""
        return Task(
            config=self.tasks_config['conduct_realtime_training'],
            agent=self.trainer_agent()
        )

    @task
    def track_progress_task(self) -> Task:
        """Task 6: Track and analyze learning progress"""
        return Task(
            config=self.tasks_config['track_and_analyze_progress'],
            agent=self.progress_tracking_agent(),
            context=[
                self.create_learning_plan_task(),
                self.realtime_training_task()
            ]
        )

    @task
    def query_resources_task(self) -> Task:
        """Task 7: Query knowledge base for learning resources"""
        return Task(
            config=self.tasks_config['query_learning_resources'],
            agent=self.teaching_agent()
        )

    # ==================== CREW WORKFLOWS ====================

    @crew
    def assessment_and_planning_crew(self) -> Crew:
        """
        Workflow 1: Initial Assessment and Learning Plan Creation
        Used when a new user joins or wants to reassess their level
        """
        return Crew(
            agents=[
                self.assessment_agent(),
                self.teaching_agent()
            ],
            tasks=[
                self.assess_user_level_task(),
                self.create_learning_plan_task()
            ],
            process=Process.sequential,
            verbose=True,
            memory=True,  # Enable memory for agent context sharing
            embedder={
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small"
                }
            }
        )

    @crew
    def pose_feedback_crew(self) -> Crew:
        """
        Workflow 2: Pose Upload and Feedback
        Used when user uploads image/video for feedback
        """
        return Crew(
            agents=[
                self.feedback_agent(),
                self.teaching_agent()
            ],
            tasks=[
                self.validate_pose_task(),
                self.provide_feedback_task()
            ],
            process=Process.sequential,
            verbose=True,
            memory=True
        )

    @crew
    def realtime_training_crew(self) -> Crew:
        """
        Workflow 3: Real-time Training Session
        Used for live practice with immediate feedback
        """
        return Crew(
            agents=[
                self.trainer_agent(),
                self.feedback_agent(),
                self.progress_tracking_agent()
            ],
            tasks=[
                self.realtime_training_task(),
                self.track_progress_task()
            ],
            process=Process.sequential,
            verbose=True,
            memory=True
        )

    @crew
    def full_learning_cycle_crew(self) -> Crew:
        """
        Workflow 4: Complete Learning Cycle (A2A Showcase)
        Demonstrates full agent collaboration: assess -> plan -> practice -> track
        """
        return Crew(
            agents=[
                self.assessment_agent(),
                self.teaching_agent(),
                self.feedback_agent(),
                self.trainer_agent(),
                self.progress_tracking_agent()
            ],
            tasks=[
                self.assess_user_level_task(),
                self.create_learning_plan_task(),
                self.validate_pose_task(),
                self.provide_feedback_task(),
                self.realtime_training_task(),
                self.track_progress_task()
            ],
            process=Process.sequential,  # Can use hierarchical for more complex coordination
            verbose=True,
            memory=True,
            embedder={
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small"
                }
            }
        )

    # ==================== CONVENIENCE METHODS ====================

    def run_assessment_and_planning(self, user_responses: str, user_goals: str) -> Dict:
        """
        Run assessment and create learning plan

        Args:
            user_responses: User's responses to initial questions
            user_goals: User's learning goals

        Returns:
            Dict with assessment results and learning plan
        """
        crew = self.assessment_and_planning_crew()
        result = crew.kickoff(inputs={
            'user_responses': user_responses,
            'user_goals': user_goals
        })
        return result

    def run_pose_feedback(self, media_input: str, target_sign: str, user_level: str) -> Dict:
        """
        Validate pose and provide feedback

        Args:
            media_input: Path to image/video file
            target_sign: Name of the target sign
            user_level: User's proficiency level

        Returns:
            Dict with validation results and feedback
        """
        crew = self.pose_feedback_crew()
        result = crew.kickoff(inputs={
            'media_input': media_input,
            'target_sign': target_sign,
            'user_level': user_level
        })
        return result

    def run_realtime_training(
        self,
        session_config: Dict,
        target_signs: List[str],
        user_history: Optional[Dict] = None
    ) -> Dict:
        """
        Conduct real-time training session with progress tracking

        Args:
            session_config: Configuration for the session (duration, difficulty, etc.)
            target_signs: List of signs to practice
            user_history: Historical performance data

        Returns:
            Dict with session results and progress analysis
        """
        crew = self.realtime_training_crew()
        result = crew.kickoff(inputs={
            'session_config': session_config,
            'target_signs': target_signs,
            'user_history': user_history or {},
            'current_session_data': {}  # Will be populated during session
        })
        return result

    def query_learning_resources(self, user_query: str, learning_context: Dict) -> Dict:
        """
        Query knowledge base for learning resources

        Args:
            user_query: User's search query
            learning_context: Context including user level, current topic, etc.

        Returns:
            Dict with relevant resources from knowledge base
        """
        teaching_agent = self.teaching_agent()
        query_task = self.query_resources_task()

        crew = Crew(
            agents=[teaching_agent],
            tasks=[query_task],
            verbose=True
        )

        result = crew.kickoff(inputs={
            'user_query': user_query,
            'learning_context': learning_context
        })
        return result


# ==================== STANDALONE FUNCTIONS ====================

def create_sign_language_crew() -> SignLanguageCrew:
    """Factory function to create and return a crew instance"""
    return SignLanguageCrew()


def demo_a2a_workflow():
    """
    Demonstration of A2A agent collaboration
    Shows how agents communicate and coordinate
    """
    print("=" * 60)
    print("Vietnamese Sign Language Learning - A2A Demo")
    print("=" * 60)

    crew = SignLanguageCrew()

    # Demo 1: Assessment and Planning
    print("\n[DEMO 1] Assessment and Planning Workflow")
    print("-" * 60)
    result1 = crew.run_assessment_and_planning(
        user_responses="I'm a complete beginner, never learned sign language before",
        user_goals="I want to learn basic VSL for daily communication"
    )
    print("Assessment Result:", result1)

    # Demo 2: Pose Feedback
    print("\n[DEMO 2] Pose Feedback Workflow")
    print("-" * 60)
    result2 = crew.run_pose_feedback(
        media_input="./uploads/user_greeting_pose.jpg",
        target_sign="greeting",
        user_level="beginner"
    )
    print("Feedback Result:", result2)

    print("\n" + "=" * 60)
    print("A2A Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    # Run demo if executed directly
    demo_a2a_workflow()
