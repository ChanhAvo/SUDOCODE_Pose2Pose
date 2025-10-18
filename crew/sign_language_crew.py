# crew.py
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
import os


class SignLanguageCrew:
    def __init__(self):
        self.agents_config = self.load_config('agents.yaml')
        self.tasks_config = self.load_config('tasks.yaml')

    def testing_agent(self):
        return Agent(
            config=self.agents_config['testing_agent'],
            verbose=True,
            allow_delegation=False
        )

    def learning_planner(self):
        return Agent(
            config=self.agents_config['learning_planner'],
            verbose=True,
            allow_delegation=True  # Can delegate to other agents
        )

    def pose_validator(self):
        return Agent(
            config=self.agents_config['pose_validator'],
            verbose=True,
            tools=[],  # Add your CV tools here
            allow_delegation=False
        )

    def feedback_agent(self):
        return Agent(
            config=self.agents_config['feedback_agent'],
            verbose=True,
            allow_delegation=True
        )

    def trainer_agent(self):
        return Agent(
            config=self.agents_config['trainer_agent'],
            verbose=True,
            allow_delegation=False
        )

    def assess_level_task(self):
        return Task(
            config=self.tasks_config['assess_level'],
            agent=self.testing_agent()
        )

    def create_plan_task(self):
        return Task(
            config=self.tasks_config['create_learning_plan'],
            agent=self.learning_planner()
        )

    def validate_pose_task(self):
        return Task(
            config=self.tasks_config['validate_pose'],
            agent=self.pose_validator()
        )

    def feedback_task(self):
        return Task(
            config=self.tasks_config['provide_feedback'],
            agent=self.feedback_agent()
        )

    def crew(self):
        return Crew(
            agents=[
                self.testing_agent(),
                self.learning_planner(),
                self.pose_validator(),
                self.feedback_agent(),
                self.trainer_agent()
            ],
            tasks=[
                self.assess_level_task(),
                self.create_plan_task(),
                self.validate_pose_task(),
                self.feedback_task()
            ],
            process=Process.sequential,  # Or Process.hierarchical for complex delegation
            verbose=True
        )

    def kickoff(self, inputs):
        return self.crew().kickoff(inputs=inputs)
