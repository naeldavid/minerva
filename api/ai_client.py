import os
import logging
import html
from typing import Dict, Any

# Configure minimal logging
log_level = os.environ.get('LOG_LEVEL', 'WARNING')
logging.basicConfig(level=getattr(logging, log_level, logging.WARNING))
logger = logging.getLogger(__name__)

# Get API configuration from environment variables
AI_API_KEY = os.environ.get('AI_API_KEY', '')
AI_MODEL = os.environ.get('AI_MODEL', 'nae1/eva')  # Default to your model

# Try to import InferenceClient for better model support
try:
    from huggingface_hub import InferenceClient
    HF_CLIENT_AVAILABLE = True
except ImportError:
    HF_CLIENT_AVAILABLE = False
    logger.warning("huggingface_hub not installed; falling back to requests")
    import requests
    session = requests.Session()
    session.timeout = 120

def process_ai_request(prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
    """
    Process a request to the AI API and return structured response.
    Uses HuggingFace InferenceClient for automatic model routing and format handling.
    
    Args:
        prompt: User's input prompt
        max_tokens: Maximum tokens for the response
        
    Returns:
        Dictionary containing the AI response formatted for display
    """
    # Validate configuration
    if not AI_API_KEY:
        raise ValueError("AI_API_KEY not set. Get one from https://huggingface.co/settings/tokens")
    
    if not AI_MODEL:
        raise ValueError("AI_MODEL environment variable not set")
    
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
    
    try:
        if HF_CLIENT_AVAILABLE:
            # Use InferenceClient - handles routing and format automatically
            client = InferenceClient(api_key=AI_API_KEY)
            
            try:
                # Try chat completion first (preferred for conversational models)
                response = client.chat_completion(
                    model=AI_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                
                if response and hasattr(response, 'choices') and len(response.choices) > 0:
                    response_text = response.choices[0].message.content
                else:
                    response_text = str(response)
                
            except Exception as chat_error:
                # Fall back to text generation if chat fails
                logger.debug(f"Chat completion failed, trying text generation: {chat_error}")
                response = client.text_generation(
                    model=AI_MODEL,
                    prompt=prompt,
                    max_new_tokens=max_tokens,
                    temperature=0.7,
                    do_sample=True
                )
                response_text = response if isinstance(response, str) else str(response)
        
        else:
            # Fallback: use requests with the old API format
            logger.warning("Using fallback requests method (install huggingface_hub for better support)")
            import requests
            import json
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {AI_API_KEY}'
            }
            
            # Try old API format
            api_url = f"https://api-inference.huggingface.co/models/{AI_MODEL}"
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                response_text = data[0].get('generated_text', str(data))
            elif isinstance(data, dict) and 'generated_text' in data:
                response_text = data['generated_text']
            else:
                response_text = str(data)
        
        return format_response(response_text)
        
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise
    except Exception as e:
        logger.error(f"Error processing AI request: {e}")
        raise ValueError(f"AI service error: {str(e)}")

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