
import re
import os
from dotenv import load_dotenv
from google import genai
from django_chatbot.app_log import logger
# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def format_ai_response(response_text: str) -> str:
    """
    Format the AI response for better display.

    Args:
        response_text: Raw response text from AI

    Returns:
        Formatted and cleaned response text
    """
    # Remove the prefix if it exists
    formatted = response_text.replace(" Gemini Response:", "").strip()

    # Clean up excessive newlines
    formatted = re.sub(r'\n{3,}', '\n\n', formatted)

    # Ensure proper spacing after numbered/bulleted lists
    formatted = re.sub(r'(\d+\.\s.*?)(\n)([^\d\n])', r'\1\n\n\3', formatted)
    formatted = re.sub(r'(\*\s.*?)(\n)([^\*\n])', r'\1\n\n\3', formatted)

    return formatted.strip()


def ask_geminiai(message: str) -> str:
    """
    Get response from Gemini AI and format it properly.

    Args:
        message: User's message to send to AI

    Returns:
        Formatted AI response or error message
    """
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=message,
        )

        raw_answer = response.text.strip()
        formatted_answer = format_ai_response(raw_answer)

        return formatted_answer

    except Exception as e:
        error_msg = f"I apologize, but I encountered an error while processing your request: {str(e)}. Please try again."
        logger.error(f"Gemini API error: {str(e)}")
        return error_msg

