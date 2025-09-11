"""Configuration models using pydantic for secure validation."""

from __future__ import annotations

import warnings
from typing import Optional

from pydantic import BaseSettings, Field, HttpUrl, validator


class ApiConfig(BaseSettings):
    """Configuration for API client with secure defaults."""

    api_base_url: HttpUrl = Field(
        default="https://api.example.com", description="Base URL for API endpoints"
    )
    api_timeout: float = Field(
        default=10.0, ge=1.0, le=60.0, description="Request timeout in seconds"
    )
    api_max_retries: int = Field(
        default=3, ge=0, le=10, description="Maximum number of retry attempts"
    )
    tls_verify: bool = Field(
        default=True,
        description="Verify TLS certificates (should always be True in production)",
    )
    api_key: Optional[str] = Field(
        default=None, description="API key for authentication"
    )

    @validator("api_key")
    def validate_api_key(cls, v: Optional[str]) -> Optional[str]:
        """Validate API key format if provided."""
        if v is not None and len(v) < 10:
            raise ValueError("API key must be at least 10 characters long")
        return v

    class Config:
        """Pydantic config to read from environment variables."""

        env_prefix = "SECUREKIT_"
        case_sensitive = True


class AppConfig(BaseSettings):
    """Main application configuration."""

    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Log level")
    secret_key: str = Field(
        default="development-key-not-for-production-use",
        description="Secret key for cryptographic operations",
    )

    # API configuration
    api: ApiConfig = Field(default_factory=ApiConfig)

    @validator("log_level")
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v

    @validator("secret_key")
    def validate_secret_key(cls, v: str) -> str:
        """Validate secret key strength."""
        if not v or v == "development-key-not-for-production-use":
            # Only warn if we're not already using the development key
            if not v:
                warnings.warn(
                    "No secret key provided. Set SECUREKIT_SECRET_KEY environment variable.",
                    UserWarning,
                    stacklevel=3,
                )
            return "development-key-not-for-production-use"

        if len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters long")

        return v

    class Config:
        """Pydantic config to read from environment variables."""

        env_prefix = "SECUREKIT_"
        case_sensitive = True
        env_nested_delimiter = "__"


def get_config() -> AppConfig:
    """Get application configuration from environment variables."""
    return AppConfig()
