import os
import requests
import json
import logging
from typing import Dict, Any

# Configure minimal logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Get API configuration from environment variables
AI_API_URL = os.environ.get('AI_API_URL', '')
AI_API_KEY = os.environ.get('AI_API_KEY', '')
AI_MODEL = os.environ.get('AI_MODEL', 'llama3')  # Default model

# Global session for connection reuse
session = requests.Session()
session.timeout = 30

# Rate limiting variables
last_request_time = 0
min_request_interval = 1.0  # Minimum seconds between requests

def process_ai_request(prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
    """
    Process a request to the AI API and return structured response
    
    Args:
        prompt: User's input prompt
        max_tokens: Maximum tokens for the response
        
    Returns:
        Dictionary containing the AI response formatted for display
    """
    global last_request_time
    
    # Validate configuration
    if not AI_API_URL:
        raise Exception("AI_API_URL environment variable not set")
    
    # Prepare headers
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Add API key if provided
    if AI_API_KEY:
        headers['Authorization'] = f'Bearer {AI_API_KEY}'
    
    # Prepare the payload
    payload = {
        "model": AI_MODEL,
        "prompt": prompt,
        "stream": False,
        "max_tokens": max_tokens
    }
    
    try:
        # Make request to AI API using reusable session
        response = session.post(
            AI_API_URL,
            headers=headers,
            json=payload
        )
        
        # Raise exception for bad status codes
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        
        # Extract response text
        # This depends on the API format - adjust as needed
        if 'choices' in data and len(data['choices']) > 0:
            if 'message' in data['choices'][0]:
                # Chat completion format
                response_text = data['choices'][0]['message']['content']
            elif 'text' in data['choices'][0]:
                # Completion format
                response_text = data['choices'][0]['text']
            else:
                response_text = str(data)
        else:
            response_text = str(data)
        
        # Format response for display
        return format_response(response_text)
        
    except requests.exceptions.Timeout:
        logger.error("AI API request timed out")
        raise Exception("AI service timeout - please try again")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to AI API: {e}")
        raise Exception(f"Could not connect to AI service: {str(e)}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON response from AI API: {e}")
        raise Exception("Invalid response from AI service")
    except Exception as e:
        logger.error(f"Error processing AI request: {e}")
        raise

def format_response(text: str) -> Dict[str, Any]:
    """
    Format AI response text into structured content for display
    
    Args:
        text: Raw AI response text
        
    Returns:
        Dictionary with structured content
    """
    # For now, we'll return the text as-is
    # In future, we could parse markdown or other formatting
    return {
        "content": text,
        "format": "text"  # Could be "markdown", "html", etc.
    }

# Example usage function
def example_usage():
    """Example of how to use the AI client"""
    # This would typically be called from app.py
    try:
        response = process_ai_request("Explain how Raspberry Pi works in simple terms")
        print(response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    example_usage()