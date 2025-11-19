"""
Backend functions for Streamlit frontend integration.

This module provides high-level functions that the frontend can call
to interact with the RAG system and other backend services.

Uses singleton pattern to ensure RAG components are initialized once
and reused throughout the application lifecycle.
"""

from typing import Any, Optional

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from backend.assessment import (
    LearningPlanGenerator,
    QuizGenerator,
    QuizScorer,
    UserProfile,
)
from backend.assessment.database import get_learning_plan_db
from backend.config import config
from backend.core.chromadb import ChromaVectorDB
from backend.core.rag import RAGSystem
from backend.core.video_service import get_video_service


class RAGServiceSingleton:
    """
    Singleton class for RAG service components.

    Ensures that embeddings, vector DB, LLM, and RAG system are initialized
    only once and reused throughout the application lifecycle.
    """

    _instance: Optional["RAGServiceSingleton"] = None
    _initialized: bool = False

    def __new__(cls) -> "RAGServiceSingleton":
        """Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize components only once."""
        # Skip if already initialized
        if RAGServiceSingleton._initialized:
            return

        # Initialize embeddings (reused for all operations)
        self.embeddings = OpenAIEmbeddings(
            model=config.openai_embedding_model,
            api_key=config.openai_api_key,
        )

        # Initialize vector database (persistent connection)
        self.vector_db = ChromaVectorDB(
            api_key=config.chroma_api_key,
            tenant=config.chroma_tenant,
            database=config.chroma_database,
            collection_name=config.chroma_collection_name,
            embedding_function=self.embeddings,
            distance_metric=config.chroma_distance_metric,
        )

        # Initialize LLM (reused for all generations)
        self.llm = ChatOpenAI(
            model=config.openai_model,
            temperature=0.1,
            api_key=config.openai_api_key,
        )

        # Create and build RAG system (chain built once)
        self.rag_system = RAGSystem(
            vector_db=self.vector_db,
            llm=self.llm,
        )
        self.rag_system.build_chain()

        # Mark as initialized
        RAGServiceSingleton._initialized = True

    @classmethod
    def get_instance(cls) -> "RAGServiceSingleton":
        """
        Get the singleton instance.

        Returns:
            RAGServiceSingleton: The singleton instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """
        Reset the singleton instance.

        Use this to force re-initialization, for example if config changes.
        """
        cls._instance = None
        cls._initialized = False


def query_rag_system(
    question: str,
    include_sources: bool = True,
    top_k: int = 3,
) -> dict[str, Any]:
    try:
        # Get singleton instance (initializes once, reuses thereafter)
        service = RAGServiceSingleton.get_instance()

        # Query the RAG system
        answer = service.rag_system.query(question)

        # Prepare response
        response: dict[str, Any] = {
            "success": True,
            "answer": answer,
            "sources": [],
        }

        # Get source documents if requested
        if include_sources:
            source_docs = service.rag_system.retrieve_only(question, top_k=top_k)

            # Enrich sources with video URLs
            video_service = get_video_service()
            for doc in source_docs:
                metadata = doc.get("metadata", {})
                video_id = metadata.get("video_id")

                if video_id:
                    # Add video URLs to metadata
                    metadata["video_url"] = video_service.get_video_url(video_id)
                    metadata["video_view_url"] = video_service.get_view_url(video_id)
                    metadata["video_download_url"] = video_service.get_download_url(video_id)
                    metadata["has_video"] = video_service.has_video(video_id)
                else:
                    metadata["has_video"] = False

            response["sources"] = source_docs

        return response

    except Exception as e:
        # Return error response
        return {
            "success": False,
            "answer": "",
            "sources": [],
            "error": str(e),
        }


def retrieve_similar_signs(
    query: str,
    top_k: int = 5,
) -> dict[str, Any]:
    """
    Retrieve similar sign language entries without LLM generation.

    This function is useful for quick lookups or when you just want
    to see similar entries without generating a full answer.

    Args:
        query: Search query (word or description)
        top_k: Number of results to return

    Returns:
        dict with keys:
            - success (bool): Whether the retrieval was successful
            - results (list): List of similar documents
            - error (str): Error message (if success=False)

    Example:
        >>> result = retrieve_similar_signs("xin ch�o", top_k=5)
        >>> for doc in result["results"]:
        >>>     print(doc["metadata"]["word"])
    """
    try:
        # Get singleton instance
        service = RAGServiceSingleton.get_instance()

        # Retrieve similar documents
        results = service.rag_system.retrieve_only(query, top_k=top_k)

        # Enrich results with video URLs
        video_service = get_video_service()
        for doc in results:
            metadata = doc.get("metadata", {})
            video_id = metadata.get("video_id")

            if video_id:
                metadata["video_url"] = video_service.get_video_url(video_id)
                metadata["video_view_url"] = video_service.get_view_url(video_id)
                metadata["video_download_url"] = video_service.get_download_url(video_id)
                metadata["has_video"] = video_service.has_video(video_id)
            else:
                metadata["has_video"] = False

        return {
            "success": True,
            "results": results,
        }

    except Exception as e:
        return {
            "success": False,
            "results": [],
            "error": str(e),
        }


def get_rag_stats() -> dict[str, Any]:
    """
    Get statistics about the RAG system.

    Returns:
        dict with keys:
            - initialized (bool): Whether RAG system is initialized
            - collection_name (str): ChromaDB collection name
            - document_count (int): Number of documents in the database
            - model (str): LLM model being used
            - embedding_model (str): Embedding model being used
    """
    try:
        service = RAGServiceSingleton.get_instance()

        return {
            "initialized": RAGServiceSingleton._initialized,
            "collection_name": service.vector_db.collection_name,
            "document_count": service.vector_db.count(),
            "model": config.openai_model,
            "embedding_model": config.openai_embedding_model,
        }

    except Exception as e:
        return {
            "initialized": False,
            "error": str(e),
        }


# ============================================================================
# Assessment Services (Quiz Generation and Learning Plan)
# ============================================================================


class AssessmentServiceSingleton:
    """
    Singleton class for assessment service components.

    Ensures that quiz generator, scorer, and learning plan generator
    are initialized only once and reused throughout the application lifecycle.
    """

    _instance: Optional["AssessmentServiceSingleton"] = None
    _initialized: bool = False

    def __new__(cls) -> "AssessmentServiceSingleton":
        """Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize assessment components only once."""
        # Skip if already initialized
        if AssessmentServiceSingleton._initialized:
            return

        # Initialize LLM (reused for all assessment services)
        self.llm = ChatOpenAI(
            model=config.openai_model,
            temperature=0.7,
            api_key=config.openai_api_key,
        )

        # Initialize assessment services
        self.quiz_generator = QuizGenerator(llm=self.llm)
        self.quiz_scorer = QuizScorer(llm=self.llm)
        self.learning_plan_generator = LearningPlanGenerator(llm=self.llm)

        # Mark as initialized
        AssessmentServiceSingleton._initialized = True

    @classmethod
    def get_instance(cls) -> "AssessmentServiceSingleton":
        """
        Get the singleton instance.

        Returns:
            AssessmentServiceSingleton: The singleton instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """
        Reset the singleton instance.

        Use this to force re-initialization, for example if config changes.
        """
        cls._instance = None
        cls._initialized = False


def generate_dynamic_quiz(user_profile: dict) -> dict[str, Any]:
    """
    Generate personalized quiz questions based on user profile.

    This is the main function that the frontend should call to generate
    a customized quiz. It uses LLM to create questions tailored to the
    user's experience level, goals, and motivation.

    Args:
        user_profile: Dictionary with keys:
            - name (str): User's name
            - email (str, optional): User's email
            - age_group (str): Age group
            - prior_experience (str): Prior VSL experience
            - learning_goal (str): Primary learning goal
            - time_commitment (str): Available time per week
            - motivation (str): User's motivation for learning

    Returns:
        dict with keys:
            - success (bool): Whether generation was successful
            - questions (list): List of quiz question dicts
            - source (str): "dynamic" or "static_fallback"
            - error (str, optional): Error message if failed

    Example:
        >>> profile = {"name": "John", "age_group": "25-34", ...}
        >>> result = generate_dynamic_quiz(profile)
        >>> if result["success"]:
        >>>     for q in result["questions"]:
        >>>         print(q["question"])
    """
    try:
        # Validate and convert user profile
        profile = UserProfile(**user_profile)

        # Get singleton instance
        service = AssessmentServiceSingleton.get_instance()

        # Generate quiz
        questions = service.quiz_generator.generate_quiz(profile)

        # Convert to dicts for JSON serialization
        questions_dict = [q.model_dump() for q in questions]

        return {
            "success": True,
            "questions": questions_dict,
            "source": "dynamic",
        }

    except Exception as e:
        # Return fallback quiz on any error
        from backend.assessment.quiz_generator import get_static_quiz_questions

        return {
            "success": True,  # Still successful, just using fallback
            "questions": get_static_quiz_questions(),
            "source": "static_fallback",
            "error": str(e),
        }


def score_quiz(questions: list[dict], answers: dict[str, Any]) -> dict[str, Any]:
    """
    Score quiz answers and determine proficiency level.

    This function uses LLM to evaluate answers, particularly for
    subjective short answer questions, and provides detailed feedback.

    Args:
        questions: List of quiz question dictionaries
        answers: Dictionary mapping question_id to user answer

    Returns:
        dict with keys:
            - success (bool): Whether scoring was successful
            - result (dict): QuizResult as dictionary with:
                - question_scores (dict): Score for each question
                - total_score (float): Total points earned
                - percentage (float): Overall percentage
                - level (str): Proficiency level (Beginner/Intermediate/Advanced)
                - overall_feedback (str): Summary feedback
                - strengths (list): List of strengths
                - areas_for_improvement (list): Areas to improve
            - error (str, optional): Error message if failed

    Example:
        >>> result = score_quiz(questions, {"q1": 0, "q2": "My answer..."})
        >>> print(result["result"]["level"])
        >>> print(result["result"]["percentage"])
    """
    try:
        # Get singleton instance
        service = AssessmentServiceSingleton.get_instance()

        # Convert question dicts to QuizQuestion objects
        from backend.assessment.schemas import (
            MultipleChoiceQuestion,
            ShortAnswerQuestion,
        )

        quiz_questions = []
        for q_data in questions:
            if q_data["type"] == "multiple_choice":
                quiz_questions.append(MultipleChoiceQuestion(**q_data))
            else:
                quiz_questions.append(ShortAnswerQuestion(**q_data))

        # Score quiz
        quiz_result = service.quiz_scorer.score_quiz(quiz_questions, answers)

        return {
            "success": True,
            "result": quiz_result.model_dump(),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def generate_learning_plan(
    user_profile: dict, quiz_result: dict
) -> dict[str, Any]:
    """
    Generate personalized learning plan based on profile and quiz results.

    This function creates a comprehensive learning path with modules and
    lessons tailored to the user's assessed level, goals, and time commitment.

    Args:
        user_profile: User profile dictionary
        quiz_result: Quiz scoring result dictionary

    Returns:
        dict with keys:
            - success (bool): Whether generation was successful
            - plan (dict): LearningPlan as dictionary
            - file_path (str, optional): Path where plan was saved
            - error (str, optional): Error message if failed

    Example:
        >>> plan_result = generate_learning_plan(profile, quiz_result)
        >>> if plan_result["success"]:
        >>>     modules = plan_result["plan"]["modules"]
        >>>     print(f"Generated {len(modules)} modules")
    """
    try:
        # Validate inputs
        profile = UserProfile(**user_profile)

        from backend.assessment.schemas import QuizResult as QuizResultModel

        result = QuizResultModel(**quiz_result)

        # Get singleton instance
        service = AssessmentServiceSingleton.get_instance()

        # Generate learning plan
        learning_plan = service.learning_plan_generator.generate_plan(profile, result)

        # Save to file
        file_path = service.learning_plan_generator.save_plan(learning_plan)

        return {
            "success": True,
            "plan": learning_plan.model_dump(),
            "file_path": file_path,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# ============================================================================
# Learning Plan Database CRUD Functions
# ============================================================================


def get_user_plan(user_id: str) -> Optional[dict]:
    """
    Get a user's learning plan from the JSON database.

    Args:
        user_id: User identifier

    Returns:
        Plan dictionary if found, None otherwise

    Example:
        >>> plan = get_user_plan("john_doe_12345")
        >>> if plan:
        >>>     print(f"User has {len(plan['modules'])} modules")
    """
    db = get_learning_plan_db()
    return db.get_plan_dict(user_id)


def save_user_plan(plan: dict) -> bool:
    """
    Save or update a user's learning plan to the JSON database.

    Args:
        plan: Learning plan dictionary (matching LearningPlan schema)

    Returns:
        True if successful, False otherwise

    Example:
        >>> success = save_user_plan(learning_plan_dict)
        >>> if success:
        >>>     print("Plan saved successfully!")
    """
    try:
        from backend.assessment.schemas import LearningPlan

        # Validate plan
        learning_plan = LearningPlan(**plan)

        # Save to database
        db = get_learning_plan_db()
        return db.update_plan(learning_plan)

    except Exception as e:
        return False


def delete_user_plan(user_id: str) -> bool:
    """
    Delete a user's learning plan from the JSON database.

    Args:
        user_id: User identifier

    Returns:
        True if successful, False otherwise

    Example:
        >>> deleted = delete_user_plan("john_doe_12345")
    """
    db = get_learning_plan_db()
    return db.delete_plan(user_id)


def list_all_user_ids() -> list[str]:
    """
    List all user IDs with saved learning plans.

    Returns:
        List of user IDs

    Example:
        >>> user_ids = list_all_user_ids()
        >>> print(f"Found {len(user_ids)} users with plans")
    """
    db = get_learning_plan_db()
    return db.list_all_plans()


def user_has_plan(user_id: str) -> bool:
    """
    Check if a user has a saved learning plan.

    Args:
        user_id: User identifier

    Returns:
        True if plan exists, False otherwise

    Example:
        >>> if user_has_plan("john_doe_12345"):
        >>>     plan = get_user_plan("john_doe_12345")
    """
    db = get_learning_plan_db()
    return db.plan_exists(user_id)
