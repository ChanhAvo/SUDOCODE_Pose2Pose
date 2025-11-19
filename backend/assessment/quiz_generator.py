"""
Quiz Generator service for creating personalized quiz questions.

This module uses LLM to generate customized quiz questions based on
user profiles and learning goals.
"""

import logging
from typing import List

from langchain_openai import ChatOpenAI
from pydantic import ValidationError

from backend.assessment.prompts import get_quiz_generator_prompt
from backend.assessment.schemas import (
    MultipleChoiceQuestion,
    QuizQuestion,
    QuizQuestionsResponse,
    ShortAnswerQuestion,
    UserProfile,
)

logger = logging.getLogger(__name__)


# Static fallback quiz for when LLM generation fails
STATIC_FALLBACK_QUIZ = [
    {
        "id": "q1",
        "question": "Ngôn ngữ ký hiệu Việt Nam (VSL) chủ yếu dựa trên yếu tố nào?",
        "type": "multiple_choice",
        "options": [
            "Chỉ đánh vần bằng ngón tay",
            "Cử chỉ bằng tay, chuyển động, và biểu hiện khuôn mặt",
            "Ký hiệu viết",
            "Mã Morse"
        ],
        "correct_answer": 1,
        "difficulty": "beginner",
        "explanation": "VSL là ngôn ngữ trực quan-chuyển động, sử dụng hình dạng tay, chuyển động, vị trí và biểu hiện khuôn mặt để truyền đạt ý nghĩa."
    },
    {
        "id": "q2",
        "question": "Biểu hiện khuôn mặt trong ngôn ngữ ký hiệu đóng vai trò gì?",
        "type": "multiple_choice",
        "options": [
            "Chỉ là tùy chọn để nhấn mạnh",
            "Là dấu hiệu ngữ pháp có thể thay đổi ý nghĩa",
            "Chỉ dùng để thể hiện cảm xúc",
            "Không có ý nghĩa gì"
        ],
        "correct_answer": 1,
        "difficulty": "intermediate",
        "explanation": "Biểu hiện khuôn mặt là một phần quan trọng của ngữ pháp trong ngôn ngữ ký hiệu và có thể thay đổi hoàn toàn ý nghĩa của dấu hiệu."
    },
    {
        "id": "q3",
        "question": "VSL có sự khác biệt theo vùng miền không? Nếu có, hãy giải thích.",
        "type": "short_answer",
        "scoring_rubric": "Điểm cho: Nhắc đến sự khác biệt giữa Miền Bắc/Nam/Trung (40%), Giải thích tại sao có sự khác biệt (30%), Đưa ra ví dụ hoặc so sánh (30%). Tối thiểu 3 câu.",
        "difficulty": "intermediate",
        "sample_answer": "Có, VSL có sự khác biệt theo vùng miền giống như tiếng Việt nói. Có ba phiên bản chính: Miền Bắc (B), Miền Nam (N), và Miền Trung (T). Sự khác biệt này phát triển tự nhiên do khoảng cách địa lý và sự phát triển độc lập của các cộng đồng người Điếc ở các vùng khác nhau."
    },
    {
        "id": "q4",
        "question": "Tại sao việc học ngôn ngữ ký hiệu lại quan trọng?",
        "type": "short_answer",
        "scoring_rubric": "Điểm cho: Đề cập đến khả năng tiếp cận và giao tiếp (40%), Hiểu biết về văn hóa Điếc (30%), Lợi ích cá nhân hoặc xã hội (30%). Tối thiểu 2-3 câu.",
        "difficulty": "beginner",
        "sample_answer": "Học ngôn ngữ ký hiệu giúp phá vỡ rào cản giao tiếp với cộng đồng người Điếc. Nó tạo ra một xã hội toàn diện hơn và giúp chúng ta hiểu về văn hóa Điếc phong phú. Ngoài ra, nó còn phát triển kỹ năng giao tiếp trực quan và tăng cường sự đồng cảm."
    },
    {
        "id": "q5",
        "question": "Yếu tố nào KHÔNG phải là thông số hình thành dấu hiệu trong VSL?",
        "type": "multiple_choice",
        "options": [
            "Hình dạng bàn tay",
            "Chuyển động",
            "Giọng điệu",
            "Vị trí"
        ],
        "correct_answer": 2,
        "difficulty": "beginner",
        "explanation": "Giọng điệu không phải là thông số trong ngôn ngữ ký hiệu vì VSL là ngôn ngữ trực quan, không dựa vào âm thanh. Các thông số chính là hình dạng tay, chuyển động, vị trí, và biểu hiện khuôn mặt."
    }
]


class QuizGenerator:
    """
    Service for generating personalized quiz questions using LLM.

    This class uses ChatGPT to create customized quiz questions based on
    user profiles, with fallback to static questions on failure.
    """

    def __init__(self, llm: ChatOpenAI):
        """
        Initialize quiz generator.

        Args:
            llm: Configured ChatOpenAI instance
        """
        self._llm = llm

    def generate_quiz(
        self, user_profile: UserProfile, max_retries: int = 2
    ) -> List[QuizQuestion]:
        """
        Generate personalized quiz questions using structured output.

        Args:
            user_profile: Validated user profile
            max_retries: Maximum number of retry attempts

        Returns:
            List of 5 QuizQuestion objects (MC or SA)
        """
        logger.info(f"Generating quiz for user: {user_profile.name}")
        logger.debug(f"Profile: prior_experience={user_profile.prior_experience}, goal={user_profile.learning_goal}")

        for attempt in range(max_retries):
            try:
                # Generate prompt
                prompt = get_quiz_generator_prompt(user_profile.model_dump())

                # Configure LLM with structured output
                structured_llm = self._llm.with_structured_output(QuizQuestionsResponse)

                # Call LLM
                logger.info(f"Calling LLM for quiz generation (attempt {attempt + 1}/{max_retries})")
                response = structured_llm.invoke(prompt)

                # Extract questions from structured response
                questions = response.questions

                logger.info(f"Successfully generated {len(questions)} questions")
                return questions

            except ValidationError as e:
                logger.error(f"Question validation failed: {e}")
                if attempt < max_retries - 1:
                    continue
                else:
                    return self._get_fallback_quiz(user_profile)

            except Exception as e:
                logger.error(f"Unexpected error in quiz generation: {e}", exc_info=True)
                return self._get_fallback_quiz(user_profile)

        return self._get_fallback_quiz(user_profile)

    def _get_fallback_quiz(self, user_profile: UserProfile) -> List[QuizQuestion]:
        """
        Get static fallback quiz when LLM generation fails.

        Args:
            user_profile: User profile for adaptation

        Returns:
            List of static quiz questions adapted to user level
        """
        logger.info("Using static fallback quiz")

        # Convert static quiz to validated models
        questions = []
        for q_data in STATIC_FALLBACK_QUIZ:
            q_type = q_data.get("type")

            if q_type == "multiple_choice":
                question = MultipleChoiceQuestion(**q_data)
            else:
                question = ShortAnswerQuestion(**q_data)

            questions.append(question)

        return questions


def get_static_quiz_questions() -> List[dict]:
    """
    Get static quiz questions as dictionaries.

    Returns:
        List of quiz question dictionaries
    """
    return STATIC_FALLBACK_QUIZ
