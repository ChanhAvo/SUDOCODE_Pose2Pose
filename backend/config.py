"""
Configuration management using Pydantic Settings.

This module provides a centralized configuration class that loads settings
from environment variables with type validation and default values.
"""

from enum import Enum
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Application environment types."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Config(BaseSettings):
    """
    Application configuration loaded from environment variables.

    All settings can be overridden via environment variables.
    For example: OPENAI_API_KEY=xxx python app.py
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application Settings
    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Application environment"
    )

    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )

    # Streamlit Settings
    streamlit_server_port: int = Field(
        default=8501,
        description="Streamlit server port",
        ge=1024,
        le=65535
    )

    # OpenAI Settings
    openai_api_key: str = Field(
        ...,
        description="OpenAI API key (required)",
        min_length=1
    )

    openai_model: str = Field(
        default="gpt-5-mini",
        description="OpenAI model to use for chat completion"
    )

    openai_embedding_model: str = Field(
        default="text-embedding-3-large",
        description="OpenAI model to use for embeddings"
    )

    # ChromaDB Cloud Settings
    chroma_api_key: str = Field(
        ...,
        description="ChromaDB Cloud API key (required)",
        min_length=1
    )

    chroma_tenant: str = Field(
        ...,
        description="ChromaDB Cloud tenant ID (required)",
        min_length=1
    )

    chroma_database: str = Field(
        default="pose2pose_vectordb",
        description="ChromaDB Cloud database name"
    )

    chroma_collection_name: str = Field(
        default="pose2pose_collection",
        description="ChromaDB collection name"
    )

    chroma_distance_metric: str = Field(
        default="cosine",
        description="Distance metric for similarity search (l2, cosine, ip)"
    )

    # Google Drive Video Settings
    google_drive_folder_id: Optional[str] = Field(
        default="1kGAzGKgO9Sc53D5bNoWQYjhQHiucG3sZ",
        description="Google Drive folder ID for VSL videos"
    )

    video_mapping_path: str = Field(
        default="data/video_mapping.json",
        description="Path to video ID to Google Drive file ID mapping"
    )

    # Assessment Settings
    assessment_temperature: float = Field(
        default=0.7,
        description="Temperature for assessment LLM generation",
        ge=0.0,
        le=2.0
    )

    assessment_max_tokens: int = Field(
        default=4000,
        description="Maximum tokens for assessment LLM responses",
        ge=1000
    )

    user_plans_directory: str = Field(
        default="data/user_plans",
        description="Directory to store generated user learning plans"
    )

    # Logging Settings
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )

    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format"
    )

    # LangChain Settings
    langchain_tracing_v2: bool = Field(
        default=False,
        description="Enable LangChain tracing"
    )

    langchain_api_key: Optional[str] = Field(
        default=None,
        description="LangChain API key for tracing"
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is a valid Python logging level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v_upper

    @field_validator("chroma_distance_metric")
    @classmethod
    def validate_distance_metric(cls, v: str) -> str:
        """Validate distance metric is valid."""
        valid_metrics = ["l2", "cosine", "ip"]
        v_lower = v.lower()
        if v_lower not in valid_metrics:
            raise ValueError(f"Distance metric must be one of {valid_metrics}")
        return v_lower

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == Environment.PRODUCTION

    @property
    def openai_config(self) -> dict:
        """Get OpenAI configuration as a dictionary."""
        return {
            "api_key": self.openai_api_key,
            "model": self.openai_model,
        }

    @property
    def chroma_config(self) -> dict:
        """Get ChromaDB Cloud configuration as a dictionary."""
        return {
            "api_key": self.chroma_api_key,
            "tenant": self.chroma_tenant,
            "database": self.chroma_database,
            "collection_name": self.chroma_collection_name,
            "distance_metric": self.chroma_distance_metric,
        }


# Global config instance
# This can be imported and used throughout the application
config = Config()


# Convenience function to get config
def get_config() -> Config:
    """
    Get the global configuration instance.

    Returns:
        Config: The global configuration object
    """
    return config
