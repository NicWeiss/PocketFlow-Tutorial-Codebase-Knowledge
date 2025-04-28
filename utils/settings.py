from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        case_sensitive = True

    # ! IMPORTANT !
    # Use only one WITH_..._AI flag enabled
    # Because if enabled many, used will be only first

    # IF you want to use Google AI set with_google_ai as True and fill studio key and model name
    WITH_GOOGLE_AI: bool = False
    GOOGLE_AI_STUDIO_KEY: str = ""
    GOOGLE_AI_MODEL: str = ""

    # IF you want to use your Google project - set also use_own_google_project to True and fill id and location
    USE_OWN_GOOGLE_PROJECT: bool =  False
    GEMINI_PROJECT_ID: str = ""
    GEMINI_LOCATION: str = ""

    # IF you want to use OllaMa AI set with_ollama_ai as True and fill host and model name
    WITH_OLLAMA_AI: bool = True
    OLLAMA_HOST: str = None
    OLLAMA_MODEL: str = None
    OLLAMA_MAX_PROMPT: int = 100000

    IS_LLM_CACHE_ENABLED: bool = True

settings = Settings()