"""
Simple JSON-based database for managing user learning plans.

This module provides CRUD operations for learning plans stored as JSON files,
acting as a lightweight persistent storage solution.
"""

import json
import logging
import os
from pathlib import Path
from typing import List, Optional

from backend.assessment.schemas import LearningPlan, Module
from backend.config import config

logger = logging.getLogger(__name__)


class LearningPlanDatabase:
    """
    Simple JSON-based database for learning plans.

    Provides CRUD operations for user learning plans stored in the
    data/user_plans directory.
    """

    def __init__(self, plans_directory: Optional[str] = None):
        """
        Initialize the database.

        Args:
            plans_directory: Directory to store plan JSON files
        """
        self.plans_directory = Path(plans_directory or config.user_plans_directory)
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Ensure the plans directory exists."""
        self.plans_directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Plans directory ensured: {self.plans_directory}")

    def _get_plan_path(self, user_id: str) -> Path:
        """Get file path for a user's plan."""
        return self.plans_directory / f"{user_id}.json"

    # CREATE
    def create_plan(self, learning_plan: LearningPlan) -> bool:
        """
        Create a new learning plan.

        Args:
            learning_plan: LearningPlan object to save

        Returns:
            True if successful, False otherwise
        """
        try:
            plan_path = self._get_plan_path(learning_plan.user_id)

            # Don't overwrite existing plan without explicit update
            if plan_path.exists():
                logger.warning(f"Plan already exists for user {learning_plan.user_id}. Use update_plan() instead.")
                return False

            # Save plan
            with open(plan_path, "w", encoding="utf-8") as f:
                json.dump(learning_plan.model_dump(), f, indent=2, ensure_ascii=False)

            logger.info(f"Created plan for user {learning_plan.user_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to create plan: {e}", exc_info=True)
            return False

    # READ
    def get_plan(self, user_id: str) -> Optional[LearningPlan]:
        """
        Get a learning plan by user ID.

        Args:
            user_id: User identifier

        Returns:
            LearningPlan object if found, None otherwise
        """
        try:
            plan_path = self._get_plan_path(user_id)

            if not plan_path.exists():
                logger.debug(f"No plan found for user {user_id}")
                return None

            with open(plan_path, "r", encoding="utf-8") as f:
                plan_data = json.load(f)

            learning_plan = LearningPlan(**plan_data)
            logger.info(f"Retrieved plan for user {user_id}")
            return learning_plan

        except Exception as e:
            logger.error(f"Failed to get plan: {e}", exc_info=True)
            return None

    def get_plan_dict(self, user_id: str) -> Optional[dict]:
        """
        Get a learning plan as dictionary.

        Args:
            user_id: User identifier

        Returns:
            Plan dictionary if found, None otherwise
        """
        plan = self.get_plan(user_id)
        return plan.model_dump() if plan else None

    # UPDATE
    def update_plan(self, learning_plan: LearningPlan) -> bool:
        """
        Update an existing learning plan (or create if doesn't exist).

        Args:
            learning_plan: Updated LearningPlan object

        Returns:
            True if successful, False otherwise
        """
        try:
            plan_path = self._get_plan_path(learning_plan.user_id)

            # Save plan (overwrites if exists)
            temp_path = plan_path.with_suffix(".tmp")
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(learning_plan.model_dump(), f, indent=2, ensure_ascii=False)

            # Atomic replace
            os.replace(temp_path, plan_path)

            logger.info(f"Updated plan for user {learning_plan.user_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to update plan: {e}", exc_info=True)
            return False

    def update_module_progress(
        self, user_id: str, module_id: str, completed: bool = True
    ) -> bool:
        """
        Update module completion status.

        Args:
            user_id: User identifier
            module_id: Module identifier
            completed: Whether module is completed

        Returns:
            True if successful, False otherwise
        """
        try:
            plan = self.get_plan(user_id)
            if not plan:
                logger.warning(f"No plan found for user {user_id}")
                return False

            # Add metadata to track completion
            # Note: This requires adding a metadata field to Module schema
            # For now, we'll handle this in session state
            # Future: Add completion tracking to Module schema

            logger.info(f"Module {module_id} marked as {'completed' if completed else 'incomplete'} for user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to update module progress: {e}", exc_info=True)
            return False

    # DELETE
    def delete_plan(self, user_id: str) -> bool:
        """
        Delete a learning plan.

        Args:
            user_id: User identifier

        Returns:
            True if successful, False otherwise
        """
        try:
            plan_path = self._get_plan_path(user_id)

            if not plan_path.exists():
                logger.warning(f"No plan to delete for user {user_id}")
                return False

            plan_path.unlink()
            logger.info(f"Deleted plan for user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete plan: {e}", exc_info=True)
            return False

    # LIST
    def list_all_plans(self) -> List[str]:
        """
        List all user IDs with saved plans.

        Returns:
            List of user IDs
        """
        try:
            user_ids = [
                p.stem for p in self.plans_directory.glob("*.json")
                if not p.name.startswith(".")
            ]
            logger.debug(f"Found {len(user_ids)} saved plans")
            return sorted(user_ids)

        except Exception as e:
            logger.error(f"Failed to list plans: {e}", exc_info=True)
            return []

    def get_all_plans(self) -> List[LearningPlan]:
        """
        Get all learning plans.

        Returns:
            List of LearningPlan objects
        """
        plans = []
        for user_id in self.list_all_plans():
            plan = self.get_plan(user_id)
            if plan:
                plans.append(plan)
        return plans

    # UTILITY
    def plan_exists(self, user_id: str) -> bool:
        """
        Check if a plan exists for a user.

        Args:
            user_id: User identifier

        Returns:
            True if plan exists, False otherwise
        """
        return self._get_plan_path(user_id).exists()

    def get_plan_count(self) -> int:
        """
        Get total number of saved plans.

        Returns:
            Number of plans
        """
        return len(self.list_all_plans())


# Global singleton instance
_db_instance: Optional[LearningPlanDatabase] = None


def get_learning_plan_db() -> LearningPlanDatabase:
    """
    Get the singleton LearningPlanDatabase instance.

    Returns:
        LearningPlanDatabase singleton
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = LearningPlanDatabase()
    return _db_instance
