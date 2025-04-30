import hashlib

from anthropic import Anthropic
from google import genai
from openai import OpenAI
import os
import logging
import json
from datetime import datetime

from utils.settings import settings
from utils.ollama_client import OllaMa

# Configure logging
log_directory = os.getenv("LOG_DIR", "logs")
os.makedirs(log_directory, exist_ok=True)
log_file = os.path.join(log_directory, f"llm_calls_{datetime.now().strftime('%Y%m%d')}.log")

# Set up logger
logger = logging.getLogger("llm_logger")
logger.setLevel(logging.INFO)
logger.propagate = False  # Prevent propagation to root logger
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Simple cache configuration
cache_file = "llm_cache.json"


def get_string_checksum(string):
    h = hashlib.md5(string.encode())
    return h.hexdigest()


def find_in_cache(skip_cache, prompt_hash):
    # Load cache from disk

    if not skip_cache and settings.IS_LLM_CACHE_ENABLED:
        cache = {}
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cache = json.load(f)
            except:
                logger.warning(f"Failed to load cache, starting with empty cache")

        # Return from cache if exists
        if prompt_hash in cache:
            logger.info(f"RESPONSE: {cache[prompt_hash]}")
            return cache[prompt_hash]

    return None


def store_to_cache(skip_cache, prompt_hash, response_text):
    if not skip_cache and settings.IS_LLM_CACHE_ENABLED and response_text is not None:
        # Load cache again to avoid overwrites
        cache = {}
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cache = json.load(f)
            except:
                pass

        # Add to cache and save
        cache[prompt_hash] = response_text
        try:
            with open(cache_file, 'w') as f:
                json.dump(cache, f)
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")


# By default, we Google Gemini 2.5 pro, as it shows great performance for code understanding
def call_llm(prompt: str, skip_cache: bool = False, retry: bool = False) -> str:
    logger.info(f"PROMPT: {prompt}")
    prompt_hash = get_string_checksum(prompt)

    if retry:
        print("  -- Last request failed. Try request to LLM without cache")

    if not retry:
        if cached := find_in_cache(skip_cache, prompt_hash):
            return cached

    # Call the LLM if not in cache or cache disabled
    response_text = ""
    print(f"  -- Prompt length: {len(prompt)}")

    if settings.AI_TYPE == "google":
        if settings.USE_OWN_GOOGLE_PROJECT:
            client = genai.Client(
               vertexai=True,
               project=settings.GEMINI_PROJECT_ID,
               location=settings.GEMINI_LOCATION
            )
        else:
            client = genai.Client(api_key=settings.GOOGLE_AI_STUDIO_KEY)

        response = client.models.generate_content(
            model=settings.GOOGLE_AI_MODEL,
            contents=[prompt]
        )
        response_text = response.text
    elif settings.AI_TYPE == "ollama":
        client = OllaMa(host=settings.OLLAMA_HOST)
        response = client.generate_content(prompt=prompt, model=settings.OLLAMA_MODEL)
        response_text = response.response
    elif settings.AI_TYPE == "anthrophic":
        client = Anthropic(api_key=settings.ANTHROPHIC_API_KEY)
        response = client.messages.create(
            model=settings.ANTHROPHIC_MODEL,
            max_tokens=settings.ANTHROPHIC_MAX_TOKENS,
            thinking={
                "type": "enabled" if settings.ANTHROPHIC_IS_THINKING_ENABLED else "disabled",
                "budget_tokens": settings.ANTHROPHIC_BUDGET_TOKENS
            },
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        response_text = response.content[1].text
    elif settings.AI_TYPE == "openai":
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=settings.OPENAI_API_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={
                "type": "text"
            },
            reasoning_effort="medium",
            store=False
        )
        response_text = response.choices[0].message.content

    # Avoid thinking block in result
    if "</think>" in response_text:
        _, content_response = response_text.split("</think>", 1)
    else:
        content_response = response_text

    store_to_cache(skip_cache, prompt_hash, content_response)

    # Log the response
    logger.info(f"RESPONSE: {content_response}")

    return content_response


if __name__ == "__main__":
    test_prompt = "Hello, how are you?"

    # First call - should hit the API
    print("Making call...")
    response1 = call_llm(test_prompt, use_cache=False)
    print(f"Response: {response1}")
