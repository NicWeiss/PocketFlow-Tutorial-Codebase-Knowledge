from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        case_sensitive = True


    AI_TYPE: str = "google"

    # IF you want to use Google AI set AI_TYPE as "google" and fill studio key and model name
    GOOGLE_AI_STUDIO_KEY: str = ""
    GOOGLE_AI_MODEL: str = "gemini-2.5-flash-preview-04-17"

    # IF you want to use your Google project - set also use_own_google_project to True and fill id and location
    GEMINI_PROJECT_ID: str = ""
    GEMINI_LOCATION: str = ""

    # IF you want to use OllaMa AI set AI_TYPE as "ollama" and fill host and model name
    OLLAMA_HOST: str = ""
    OLLAMA_MODEL: str = ""
    OLLAMA_NUM_CTX: int = 20000

    # IF you want to use Anthrophic AI set AI_TYPE as "anthrophic" and fill api key and model name
    ANTHROPHIC_API_KEY: str = ""
    ANTHROPHIC_MODEL: str = "claude-3-7-sonnet-20250219"
    ANTHROPHIC_MAX_TOKENS: int = 21000
    ANTHROPHIC_IS_THINKING_ENABLED: bool = True
    ANTHROPHIC_BUDGET_TOKENS: int = 20000

    # IF you want to use OpenAI set AI_TYPE as "openai" and fill api key and model name
    OPENAI_API_KEY: str = ""
    OPENAI_API_MODEL: str = "o1"

    IS_LLM_CACHE_ENABLED: bool = True

    # Settings for Nodes
    ABSTRACTIONS_COUNT: int = 10

    # Settings for LLM queries
    PREVIOUS_CHAPTERS_CONTEXT_ENABLED: bool = True
    PREVIOUS_CHAPTERS_CONTEXT_LENGTH: int = 10

settings = Settings()