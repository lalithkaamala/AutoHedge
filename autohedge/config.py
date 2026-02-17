import os
from pydantic import BaseModel, Field

class Settings(BaseModel):
    OPENAI_API_KEY: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    GROQ_API_KEY: str = Field(default_factory=lambda: os.getenv("GROQ_API_KEY", ""))
    
    # Model Configuration
    DIRECTOR_MODEL: str = os.getenv("DIRECTOR_MODEL", "groq/deepseek-r1-distill-llama-70b")
    QUANT_MODEL: str = os.getenv("QUANT_MODEL", "groq/deepseek-r1-distill-llama-70b")
    RISK_MODEL: str = os.getenv("RISK_MODEL", "groq/deepseek-r1-distill-llama-70b")
    EXECUTION_MODEL: str = os.getenv("EXECUTION_MODEL", "groq/deepseek-r1-distill-llama-70b")
    SENTIMENT_MODEL: str = os.getenv("SENTIMENT_MODEL", "gpt-4o-mini")
    
    # Agent Configuration
    MAX_LOOPS: int = int(os.getenv("MAX_LOOPS", "1"))
    CONTEXT_LENGTH: int = int(os.getenv("CONTEXT_LENGTH", "16000"))
    VERBOSE: bool = os.getenv("VERBOSE", "True").lower() == "true"
    
    # Output
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "outputs")

settings = Settings()
