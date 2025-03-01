from openai import OpenAI
import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
# Configure logging with timestamp and user context
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - User: %(user)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Add user info to logger
logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(logger, {'user': 'VOID-001'})


class APIConfig:
    """API Configuration and Key Management"""
    PRIMARY_API_KEY = os.getenv("OPENAI_API_KEY")
    CURRENT_UTC_TIME = "2025-01-19 11:08:51"
    CURRENT_USER = "VOID-001"


# Initialize OpenAI client
client = OpenAI(api_key=APIConfig.PRIMARY_API_KEY)


def prepare_system_prompt() -> str:
    return """You are an experienced automotive diagnostic expert analyzing vehicle maintenance data.
    Your role is to:
    1. Interpret maintenance metrics and diagnostic trouble codes (DTCs)
    2. Identify potential issues and maintenance needs
    3. Provide clear, actionable recommendations
    4. Explain technical findings in user-friendly language
    5. Prioritize safety-critical issues in your response

    Please provide concise, practical advice based on the data provided also answer the users query."""


def analyze_with_gpt(
        context: str,
        user_id: str = APIConfig.CURRENT_USER,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 500
) -> str:
    try:
        messages = [
            {"role": "system", "content": prepare_system_prompt()},
            {"role": "user", "content": context}
        ]

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        analysis = response.choices[0].message.content
        logger.info(f"Successfully generated GPT analysis for user {user_id}")
        return analysis

    except Exception as e:
        logger.error(f"Error in GPT analysis for user {user_id}: {str(e)}")
        return f"Failed to process your query. Error: {str(e)}"


def safe_analyze_with_retries(
        context: str,
        user_id: str = APIConfig.CURRENT_USER,
        max_retries: int = 3
) -> Dict[str, Any]:
    for attempt in range(max_retries):
        try:
            analysis = analyze_with_gpt(context, user_id)
            timestamp = APIConfig.CURRENT_UTC_TIME

            return {
                "success": True,
                "analysis": analysis,
                "attempt": attempt + 1,
                "timestamp": timestamp,
                "user_id": user_id
            }
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed for user {user_id}: {str(e)}")
            if attempt == max_retries - 1:
                return {
                    "success": False,
                    "error": str(e),
                    "attempt": attempt + 1,
                    "timestamp": APIConfig.CURRENT_UTC_TIME,
                    "user_id": user_id,
                    "analysis": "Analysis failed after multiple attempts"
                }