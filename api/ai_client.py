import os
import requests
import json
import logging
import html
from typing import Dict, Any

# Configure minimal logging
log_level = os.environ.get('LOG_LEVEL', 'WARNING')
logging.basicConfig(level=getattr(logging, log_level, logging.WARNING))
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
    # Validate configuration
    if not AI_API_URL:
        raise ValueError("AI_API_URL environment variable not set")
    
    # Validate and sanitize input
    if not prompt or not isinstance(prompt, str):
        raise ValueError("Invalid prompt")
    
    prompt = prompt.strip()
    if len(prompt) > 2000:
        raise ValueError("Prompt too long (max 2000 characters)")
    
    # Sanitize prompt to prevent injection
    prompt = html.escape(prompt)
    
    # Validate max_tokens
    if not isinstance(max_tokens, int) or max_tokens < 1 or max_tokens > 2000:
        max_tokens = 500
    
    # Prepare headers
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Add API key if provided
    if AI_API_KEY:
        headers['Authorization'] = f'Bearer {AI_API_KEY}'
    
    # Prepare the payload for Ollama API
    payload = {
        "model": AI_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        # Make request to AI API using reusable session with timeout
        response = session.post(
            AI_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Raise exception for bad status codes
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        
        # Parse Ollama response format
        if 'response' in data:
            response_text = data['response']
        elif 'choices' in data and len(data['choices']) > 0:
            if 'message' in data['choices'][0]:
                response_text = data['choices'][0]['message']['content']
            elif 'text' in data['choices'][0]:
                response_text = data['choices'][0]['text']
            else:
                response_text = str(data)
        else:
            response_text = str(data)
        
        # Format response for display
        return format_response(response_text)
        
    except requests.exceptions.Timeout:
        raise ValueError("AI service timeout - please try again")
    except requests.exceptions.RequestException:
        raise ValueError("Could not connect to AI service")
    except json.JSONDecodeError:
        raise ValueError("Invalid response from AI service")
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
    if not isinstance(text, str):
        text = str(text)
    
    # Sanitize output
    text = html.unescape(text)
    
    return {
        "content": text,
        "format": "text"
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