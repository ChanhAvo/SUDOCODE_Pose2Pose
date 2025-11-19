"""
Quiz Scorer service for evaluating quiz answers.

This module uses LLM to score quiz answers, particularly for
evaluating subjective short answer questions.
"""

import logging
from typing import Any, Dict, List

from langchain_openai import ChatOpenAI
from pydantic import ValidationError

from backend.assessment.prompts import get_quiz_scorer_prompt
from backend.assessment.schemas import (
    MultipleChoiceQuestion,
    ProficiencyLevel,
    QuestionScore,
    QuizQuestion,
    QuizResult,
    QuizScoringResponse,
    ShortAnswerQuestion,
)

logger = logging.getLogger(__name__)


class QuizScorer:
    """
    Service for scoring quiz answers using LLM.

    This class evaluates both multiple choice and short answer questions,
    providing detailed feedback and determining proficiency level.
    """

    def __init__(self, llm: ChatOpenAI):
        """
        Initialize quiz scorer.

        Args:
            llm: Configured ChatOpenAI instance
        """
        self._llm = llm

    def score_quiz(
        self,
        questions: List[QuizQuestion],
        answers: Dict[str, Any],
        max_retries: int = 2,
    ) -> QuizResult:
        """
        Score quiz answers and determine proficiency level using structured output.

        Args:
            questions: List of quiz questions
            answers: Dictionary mapping question_id to user answer
            max_retries: Maximum retry attempts

        Returns:
            QuizResult with detailed scoring and feedback
        """
        logger.info(f"Scoring quiz with {len(questions)} questions")

        # Convert questions to dicts for prompt
        questions_dict = [self._question_to_dict(q) for q in questions]

        for attempt in range(max_retries):
            try:
                # Generate prompt
                prompt = get_quiz_scorer_prompt(questions_dict, answers)

                # Configure LLM with structured output
                structured_llm = self._llm.with_structured_output(QuizScoringResponse)

                # Call LLM
                logger.info(f"Calling LLM for quiz scoring (attempt {attempt + 1}/{max_retries})")
                response = structured_llm.invoke(prompt)

                # Convert question_scores list to dict
                question_scores_dict = {
                    score.question_id: score for score in response.question_scores
                }

                # Convert QuizScoringResponse to QuizResult
                quiz_result = QuizResult(
                    question_scores=question_scores_dict,
                    total_score=response.total_score,
                    total_possible=response.total_possible,
                    percentage=response.percentage,
                    level=response.level,
                    overall_feedback=response.overall_feedback,
                    strengths=response.strengths,
                    areas_for_improvement=response.areas_for_improvement,
                )

                logger.info(f"Quiz scored successfully: {quiz_result.percentage}% ({quiz_result.level})")
                return quiz_result

            except ValidationError as e:
                logger.error(f"Result validation failed: {e}")
                if attempt < max_retries - 1:
                    continue
                else:
                    return self._simple_scoring_fallback(questions, answers)

            except Exception as e:
                logger.error(f"Unexpected error in quiz scoring: {e}", exc_info=True)
                return self._simple_scoring_fallback(questions, answers)

        return self._simple_scoring_fallback(questions, answers)

    def _question_to_dict(self, question: QuizQuestion) -> dict:
        """Convert QuizQuestion to dictionary."""
        if isinstance(question, dict):
            return question
        return question.model_dump()

    def _simple_scoring_fallback(
        self, questions: List[QuizQuestion], answers: Dict[str, Any]
    ) -> QuizResult:
        """
        Simple scoring fallback when LLM fails.

        Args:
            questions: List of quiz questions
            answers: User answers

        Returns:
            Basic QuizResult with simple scoring
        """
        logger.info("Using simple scoring fallback")

        question_scores = {}
        total_score = 0.0
        total_possible = 0.0

        for question in questions:
            q_dict = self._question_to_dict(question)
            q_id = q_dict["id"]
            user_answer = answers.get(q_id)

            points_possible = 100.0
            points_earned = 0.0
            feedback = ""

            if q_dict["type"] == "multiple_choice":
                # Simple MC scoring
                if user_answer == q_dict["correct_answer"]:
                    points_earned = 100.0
                    feedback = "Chính xác! Câu trả lời đúng."
                else:
                    points_earned = 0.0
                    feedback = f"Không chính xác. Đáp án đúng là: {q_dict['options'][q_dict['correct_answer']]}"

            else:  # short_answer
                # Simple SA scoring based on length
                if user_answer and isinstance(user_answer, str):
                    word_count = len(user_answer.split())
                    if word_count >= 20:
                        points_earned = 80.0
                        feedback = "Câu trả lời chi tiết. Cảm ơn bạn đã chia sẻ suy nghĩ."
                    elif word_count >= 10:
                        points_earned = 60.0
                        feedback = "Câu trả lời tốt. Hãy thử mở rộng thêm ý tưởng của bạn."
                    else:
                        points_earned = 40.0
                        feedback = "Câu trả lời ngắn. Hãy cung cấp thêm chi tiết."
                else:
                    points_earned = 0.0
                    feedback = "Chưa có câu trả lời."

            percentage = (points_earned / points_possible) * 100

            question_scores[q_id] = QuestionScore(
                question_id=q_id,
                points_earned=points_earned,
                points_possible=points_possible,
                percentage=percentage,
                feedback=feedback,
            )

            total_score += points_earned
            total_possible += points_possible

        # Calculate overall percentage and determine level
        overall_percentage = (total_score / total_possible) * 100 if total_possible > 0 else 0

        if overall_percentage >= 71:
            level = ProficiencyLevel.ADVANCED
        elif overall_percentage >= 41:
            level = ProficiencyLevel.INTERMEDIATE
        else:
            level = ProficiencyLevel.BEGINNER

        # Generate simple feedback
        overall_feedback = (
            f"Điểm của bạn là {overall_percentage:.1f}%. "
            f"Dựa trên kết quả này, trình độ hiện tại của bạn là {level.value}. "
            "Hãy tiếp tục học tập và thực hành để nâng cao kỹ năng!"
        )

        strengths = ["Hoàn thành bài kiểm tra", "Thể hiện sự cam kết học tập"]
        areas_for_improvement = [
            "Tìm hiểu thêm về ngôn ngữ ký hiệu Việt Nam",
            "Thực hành thường xuyên để cải thiện kỹ năng",
        ]

        return QuizResult(
            question_scores=question_scores,
            total_score=total_score,
            total_possible=total_possible,
            percentage=overall_percentage,
            level=level,
            overall_feedback=overall_feedback,
            strengths=strengths,
            areas_for_improvement=areas_for_improvement,
        )
