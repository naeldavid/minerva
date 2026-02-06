import os
import logging
import html
from typing import Dict, Any, Optional

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

def process_ai_request(prompt: str, max_tokens: int = 500, image_bytes: Optional[bytes] = None) -> Dict[str, Any]:
    """
    Process a request to the AI API and return structured response.
    Calls HuggingFace Inference API directly with proper formatting for text-generation and vision-language models.
    
    Args:
        prompt: User's input prompt
        max_tokens: Maximum tokens for the response
        image_bytes: Optional image bytes for multimodal models
        
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
        import requests
        import json
        import base64

        headers = {
            'Authorization': f'Bearer {AI_API_KEY}'
        }
        
        api_url = f"https://api-inference.huggingface.co/models/{AI_MODEL}"
        
        # Build payload for text-generation or multimodal models
        if image_bytes and len(image_bytes) > 0:
            # Multimodal: encode image and include text
            img_base64 = base64.b64encode(image_bytes).decode('utf-8')
            # Try to infer image type; default to JPEG
            image_type = "jpeg"
            
            # Payload for vision-language models (image + question format)
            payload = {
                "inputs": {
                    "image": img_base64,
                    "question": prompt
                },
                "parameters": {
                    "max_new_tokens": max_tokens
                }
            }
            headers['Content-Type'] = 'application/json'
            
            logger.debug(f"Sending multimodal request to {AI_MODEL} with image ({len(image_bytes)} bytes) and prompt")
            response = requests.post(api_url, headers=headers, json=payload, timeout=120)
        else:
            # Text-only: use text-generation format
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            headers['Content-Type'] = 'application/json'
            
            logger.debug(f"Sending text-only request to {AI_MODEL}")
            response = requests.post(api_url, headers=headers, json=payload, timeout=120)
        
        # Log response status
        logger.debug(f"API response status: {response.status_code}")
        
        # Handle HTTP errors
        if response.status_code != 200:
            error_detail = ""
            try:
                error_data = response.json()
                if isinstance(error_data, dict):
                    error_detail = error_data.get('error', str(error_data))
                    if 'message' in error_data:
                        error_detail = error_data['message']
            except:
                error_detail = response.text[:200] if response.text else "Unknown error"
            
            logger.error(f"HF API error {response.status_code}: {error_detail}")
            
            # Provide helpful error message
            if "not a chat model" in error_detail.lower():
                raise ValueError(
                    f"Model {AI_MODEL} is a vision-language model. "
                    "Please upload an image with your message, or use a different model."
                )
            elif response.status_code == 401:
                raise ValueError("Authentication failed. Check your AI_API_KEY.")
            elif response.status_code == 404:
                raise ValueError(f"Model {AI_MODEL} not found or not accessible.")
            else:
                raise ValueError(f"API error: {error_detail}")
        
        # Parse response
        data = response.json()
        response_text = None
        
        # Handle different response formats
        if isinstance(data, list) and len(data) > 0:
            first = data[0]
            if isinstance(first, dict):
                # Try common keys: generated_text, answer, result
                if 'generated_text' in first:
                    response_text = first['generated_text']
                elif 'answer' in first:
                    response_text = first['answer']
                else:
                    response_text = str(first)
            else:
                response_text = str(first)
        elif isinstance(data, dict):
            if 'generated_text' in data:
                response_text = data['generated_text']
            elif 'answer' in data:
                response_text = data['answer']
            elif 'result' in data:
                response_text = str(data['result'])
            else:
                response_text = str(data)
        else:
            response_text = str(data)
        
        if not response_text:
            raise ValueError("Empty response from API")
        
        return format_response(response_text)
        
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise
    except Exception as e:
        logger.exception("Error processing AI request:")
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