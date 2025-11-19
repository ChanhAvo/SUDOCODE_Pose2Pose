"""
Learning Plan Generator service for creating personalized learning paths.

This module uses LLM to generate customized learning plans with modules
and lessons tailored to user profiles and quiz results.
"""

import json
import logging
import os
import uuid
from pathlib import Path
from typing import Optional

from langchain_openai import ChatOpenAI
from pydantic import ValidationError

from backend.assessment.database import get_learning_plan_db
from backend.assessment.prompts import get_learning_plan_generator_prompt
from backend.assessment.schemas import (
    LearningPlan,
    Module,
    ProficiencyLevel,
    QuizResult,
    UserProfile,
)
from backend.config import config

logger = logging.getLogger(__name__)


class LearningPlanGenerator:
    """
    Service for generating personalized learning plans using LLM.

    This class creates comprehensive learning paths with modules and lessons
    tailored to user profiles, quiz results, and learning goals.
    """

    def __init__(self, llm: ChatOpenAI):
        """
        Initialize learning plan generator.

        Args:
            llm: Configured ChatOpenAI instance
        """
        self._llm = llm
        self._ensure_plans_directory()

    def _ensure_plans_directory(self) -> None:
        """Ensure user plans directory exists."""
        plans_dir = Path(config.user_plans_directory)
        plans_dir.mkdir(parents=True, exist_ok=True)

    def generate_plan(
        self,
        user_profile: UserProfile,
        quiz_result: QuizResult,
        max_retries: int = 2,
    ) -> LearningPlan:
        """
        Generate personalized learning plan using structured output.

        Args:
            user_profile: Validated user profile
            quiz_result: Quiz scoring result
            max_retries: Maximum retry attempts

        Returns:
            Complete LearningPlan object
        """
        logger.info(f"Generating learning plan for {user_profile.name} ({quiz_result.level})")

        for attempt in range(max_retries):
            try:
                # Generate prompt
                prompt = get_learning_plan_generator_prompt(
                    user_profile.model_dump(), quiz_result.model_dump()
                )

                # Configure LLM with structured output
                structured_llm = self._llm.with_structured_output(LearningPlan)

                # Call LLM
                logger.info(f"Calling LLM for plan generation (attempt {attempt + 1}/{max_retries})")
                learning_plan = structured_llm.invoke(prompt)

                # Add user_id if not present (structured output should include it)
                if not learning_plan.user_id:
                    # Create new plan with user_id
                    plan_dict = learning_plan.model_dump()
                    plan_dict["user_id"] = self._generate_user_id(user_profile)
                    learning_plan = LearningPlan(**plan_dict)

                logger.info(f"Successfully generated plan with {len(learning_plan.modules)} modules")

                # Auto-save to database
                db = get_learning_plan_db()
                db.update_plan(learning_plan)
                logger.info(f"Plan auto-saved to database for user {learning_plan.user_id}")

                return learning_plan

            except ValidationError as e:
                logger.error(f"Plan validation failed: {e}")
                if attempt < max_retries - 1:
                    continue
                else:
                    return self._get_fallback_plan(user_profile, quiz_result)

            except Exception as e:
                logger.error(f"Unexpected error in plan generation: {e}", exc_info=True)
                return self._get_fallback_plan(user_profile, quiz_result)

        return self._get_fallback_plan(user_profile, quiz_result)

    def save_plan(self, learning_plan: LearningPlan) -> Optional[str]:
        """
        Save learning plan to JSON file.

        Args:
            learning_plan: LearningPlan to save

        Returns:
            File path if successful, None otherwise
        """
        try:
            # Ensure directory exists
            self._ensure_plans_directory()

            # Generate file path
            file_path = Path(config.user_plans_directory) / f"{learning_plan.user_id}.json"

            # Save with atomic write
            temp_path = file_path.with_suffix(".tmp")
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(learning_plan.model_dump(), f, indent=2, ensure_ascii=False, default=str)

            # Atomic rename
            os.replace(temp_path, file_path)

            logger.info(f"Learning plan saved to {file_path}")
            return str(file_path)

        except OSError as e:
            logger.error(f"Failed to save plan: {e}")
            return None

        except Exception as e:
            logger.error(f"Unexpected error saving plan: {e}", exc_info=True)
            return None

    def _generate_user_id(self, user_profile: UserProfile) -> str:
        """
        Generate user ID from email or create UUID.

        Args:
            user_profile: User profile

        Returns:
            User ID string
        """
        if user_profile.email:
            # Use email as base (sanitized)
            user_id = user_profile.email.replace("@", "_at_").replace(".", "_")
        else:
            # Generate UUID based on name and timestamp
            name_slug = user_profile.name.lower().replace(" ", "_")
            unique_id = str(uuid.uuid4())[:8]
            user_id = f"{name_slug}_{unique_id}"

        return user_id

    def _get_fallback_plan(
        self, user_profile: UserProfile, quiz_result: QuizResult
    ) -> LearningPlan:
        """
        Generate simple fallback plan when LLM fails.

        Args:
            user_profile: User profile
            quiz_result: Quiz result

        Returns:
            Basic LearningPlan
        """
        logger.info("Using fallback learning plan")

        user_id = self._generate_user_id(user_profile)
        level = quiz_result.level

        # Create basic modules based on level
        if level == ProficiencyLevel.BEGINNER:
            modules = self._get_beginner_fallback_modules()
        elif level == ProficiencyLevel.INTERMEDIATE:
            modules = self._get_intermediate_fallback_modules()
        else:
            modules = self._get_advanced_fallback_modules()

        learning_plan = LearningPlan(
            user_id=user_id,
            level=level,
            created_at=None,  # Let LLM generate or leave as None
            time_commitment=user_profile.time_commitment,
            learning_goal=user_profile.learning_goal,
            modules=modules,
        )

        # Auto-save fallback plan to database
        db = get_learning_plan_db()
        db.update_plan(learning_plan)
        logger.info(f"Fallback plan auto-saved to database for user {user_id}")

        return learning_plan

    def _get_beginner_fallback_modules(self) -> list:
        """Get fallback modules for beginner level."""
        from backend.assessment.schemas import Difficulty, Lesson, LessonType

        return [
            Module(
                id="mod_fallback_1",
                title="Nền tảng Ngôn ngữ Ký hiệu Việt Nam",
                description="Học các kiến thức cơ bản về VSL, bao gồm bảng chữ cái, số đếm, và các dấu hiệu hàng ngày.",
                difficulty=Difficulty.BEGINNER,
                duration="2 weeks",
                lessons_count=8,
                estimated_hours=12,
                skills=[
                    "Bảng chữ cái VSL",
                    "Số đếm và màu sắc",
                    "Chào hỏi cơ bản",
                    "Từ vựng hàng ngày",
                ],
                lessons=[
                    Lesson(title="Giới thiệu về VSL", duration="60 min", type=LessonType.VIDEO),
                    Lesson(title="Bảng chữ cái VSL", duration="90 min", type=LessonType.INTERACTIVE),
                    Lesson(title="Thực hành đánh vần", duration="60 min", type=LessonType.PRACTICE),
                    Lesson(title="Số đếm 1-100", duration="75 min", type=LessonType.INTERACTIVE),
                    Lesson(title="Chào hỏi cơ bản", duration="60 min", type=LessonType.VIDEO),
                    Lesson(title="Thực hành hội thoại đơn giản", duration="75 min", type=LessonType.PRACTICE),
                    Lesson(title="Từ vựng gia đình", duration="90 min", type=LessonType.INTERACTIVE),
                    Lesson(title="Kiểm tra module", duration="30 min", type=LessonType.QUIZ),
                ],
            ),
            Module(
                id="mod_fallback_2",
                title="Giao tiếp Hàng ngày",
                description="Phát triển kỹ năng giao tiếp cơ bản cho các tình huống hàng ngày trong gia đình và cộng đồng.",
                difficulty=Difficulty.BEGINNER,
                duration="2 weeks",
                lessons_count=8,
                estimated_hours=12,
                skills=[
                    "Hội thoại đơn giản",
                    "Biểu đạt cảm xúc",
                    "Đặt câu hỏi",
                    "Từ vựng sinh hoạt",
                ],
                lessons=[
                    Lesson(title="Cảm xúc và tâm trạng", duration="75 min", type=LessonType.VIDEO),
                    Lesson(title="Thực hành biểu đạt cảm xúc", duration="60 min", type=LessonType.INTERACTIVE),
                    Lesson(title="Đặt câu hỏi Yes/No", duration="75 min", type=LessonType.INTERACTIVE),
                    Lesson(title="Hoạt động hàng ngày", duration="90 min", type=LessonType.VIDEO),
                    Lesson(title="Thực hành hội thoại", duration="90 min", type=LessonType.PRACTICE),
                    Lesson(title="Thời gian và ngày tháng", duration="75 min", type=LessonType.INTERACTIVE),
                    Lesson(title="Tổng hợp thực hành", duration="60 min", type=LessonType.PRACTICE),
                    Lesson(title="Kiểm tra module", duration="35 min", type=LessonType.QUIZ),
                ],
            ),
        ]

    def _get_intermediate_fallback_modules(self) -> list:
        """Get fallback modules for intermediate level."""
        from backend.assessment.schemas import Difficulty, Lesson, LessonType

        return [
            Module(
                id="mod_fallback_3",
                title="Hội thoại Nâng cao",
                description="Nâng cao kỹ năng hội thoại với cấu trúc câu phức tạp và ngữ cảnh đa dạng.",
                difficulty=Difficulty.INTERMEDIATE,
                duration="3 weeks",
                lessons_count=10,
                estimated_hours=15,
                skills=[
                    "Cấu trúc câu phức",
                    "Kể chuyện",
                    "Thảo luận chủ đề",
                    "Biến thể vùng miền",
                ],
                lessons=[
                    Lesson(title="Cấu trúc câu phức tạp", duration="90 min", type=LessonType.VIDEO),
                    Lesson(title="Thực hành câu ghép", duration="75 min", type=LessonType.INTERACTIVE),
                    Lesson(title="Kỹ thuật kể chuyện", duration="90 min", type=LessonType.VIDEO),
                    Lesson(title="Thực hành kể chuyện", duration="90 min", type=LessonType.PRACTICE),
                    Lesson(title="Thảo luận chủ đề xã hội", duration="75 min", type=LessonType.INTERACTIVE),
                    Lesson(title="Biến thể Miền Bắc/Nam/Trung", duration="90 min", type=LessonType.VIDEO),
                    Lesson(title="Thực hành theo vùng miền", duration="75 min", type=LessonType.PRACTICE),
                    Lesson(title="Hội thoại mở rộng", duration="90 min", type=LessonType.INTERACTIVE),
                    Lesson(title="Tổng hợp thực hành", duration="105 min", type=LessonType.PRACTICE),
                    Lesson(title="Kiểm tra module", duration="40 min", type=LessonType.QUIZ),
                ],
            ),
        ]

    def _get_advanced_fallback_modules(self) -> list:
        """Get fallback modules for advanced level."""
        from backend.assessment.schemas import Difficulty, Lesson, LessonType

        return [
            Module(
                id="mod_fallback_4",
                title="VSL Chuyên nghiệp",
                description="Làm chủ từ vựng chuyên ngành và kỹ thuật giao tiếp chuyên nghiệp trong VSL.",
                difficulty=Difficulty.ADVANCED,
                duration="4 weeks",
                lessons_count=12,
                estimated_hours=20,
                skills=[
                    "Từ vựng chuyên ngành",
                    "Giao tiếp công việc",
                    "Ngôn ngữ học VSL",
                    "Phiên dịch cơ bản",
                ],
                lessons=[
                    Lesson(title="Từ vựng chuyên ngành", duration="90 min", type=LessonType.VIDEO),
                    Lesson(title="Thuật ngữ y tế", duration="90 min", type=LessonType.INTERACTIVE),
                    Lesson(title="Thuật ngữ pháp lý", duration="90 min", type=LessonType.INTERACTIVE),
                    Lesson(title="Giao tiếp công việc", duration="75 min", type=LessonType.VIDEO),
                    Lesson(title="Thực hành môi trường công sở", duration="90 min", type=LessonType.PRACTICE),
                    Lesson(title="Ngôn ngữ học VSL", duration="90 min", type=LessonType.VIDEO),
                    Lesson(title="Phân tích cấu trúc ngữ pháp", duration="90 min", type=LessonType.INTERACTIVE),
                    Lesson(title="Kỹ thuật phiên dịch cơ bản", duration="90 min", type=LessonType.VIDEO),
                    Lesson(title="Thực hành phiên dịch", duration="105 min", type=LessonType.PRACTICE),
                    Lesson(title="Tình huống thực tế", duration="90 min", type=LessonType.INTERACTIVE),
                    Lesson(title="Dự án tổng hợp", duration="120 min", type=LessonType.PRACTICE),
                    Lesson(title="Kiểm tra module", duration="50 min", type=LessonType.QUIZ),
                ],
            ),
        ]

    def _parse_json_response(self, content: str) -> dict:
        """Parse JSON response from LLM."""
        # Remove markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        return json.loads(content)

    def save_and_return(
        self, learning_plan: LearningPlan
    ) -> tuple[LearningPlan, Optional[str]]:
        """
        Save learning plan and return both plan and file path.

        Args:
            learning_plan: LearningPlan to save

        Returns:
            Tuple of (learning_plan, file_path)
        """
        file_path = self.save_plan(learning_plan)
        return learning_plan, file_path
