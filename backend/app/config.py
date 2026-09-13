"""
Configuration & Deterministic Weights for ThinkForge Intelligence Engines.
Section 6, 24, and 25 of Project Specification.
"""

from pydantic import BaseModel, Field


class OpportunityScoringWeights(BaseModel):
    """Configurable weights for Opportunity Fit Scoring (Section 24)"""
    capital_fit: float = Field(default=0.20, description="Capital Fit Weight (20%)")
    skill_fit: float = Field(default=0.20, description="Skill Fit Weight (20%)")
    resource_fit: float = Field(default=0.15, description="Resource Fit Weight (15%)")
    local_opportunity: float = Field(default=0.20, description="Local Opportunity Signal Weight (20%)")
    market_access: float = Field(default=0.10, description="Market Accessibility Weight (10%)")
    margin_potential: float = Field(default=0.10, description="Margin Potential Weight (10%)")
    risk_suitability: float = Field(default=0.05, description="Risk Suitability Weight (5%)")


class PartnerSynergyWeights(BaseModel):
    """Configurable weights for Partner Synergy Scoring (Section 6 & 25)"""
    skill_complementarity: float = Field(default=0.30, description="Skill Complementarity Weight (30%)")
    capital_compatibility: float = Field(default=0.20, description="Capital Compatibility Weight (20%)")
    resource_complementarity: float = Field(default=0.15, description="Resource Complementarity Weight (15%)")
    shared_interest: float = Field(default=0.15, description="Shared Business Interest Weight (15%)")
    location_proximity: float = Field(default=0.10, description="Geographic Proximity Weight (10%)")
    experience_compatibility: float = Field(default=0.10, description="Experience Compatibility Weight (10%)")



"""ThinkForge Backend Configuration Module.

Reads configuration from environment variables or .env file with safe defaults.
"""

from functools import lru_cache
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Project Information
    PROJECT_NAME: str = "ThinkForge API"
    PROJECT_DESCRIPTION: str = "AI-Driven Rural Business Advisory & Financial Assistant"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Security & Authentication
    SECRET_KEY: str = "thinkforge-dev-insecure-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALLOW_DEV_OTP_BYPASS: bool = False

    # External APIs
    GEMINI_API_KEY: str = "redacted"
    FAST2SMS_API_KEY: str = ""

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/thinkforge"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800

    # Engine Intelligence Settings
    DEFAULT_SERVICE_RADIUS_KM: float = 10.0
    MAX_PARTNER_RADIUS_KM: float = 50.0
    DEFAULT_OPPORTUNITY_WEIGHTS: OpportunityScoringWeights = OpportunityScoringWeights()
    DEFAULT_SYNERGY_WEIGHTS: PartnerSynergyWeights = PartnerSynergyWeights()

    # CORS Whitelist
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


@lru_cache()
def get_settings() -> Settings:
    """Returns cached settings instance."""
    return Settings()


settings = get_settings()
