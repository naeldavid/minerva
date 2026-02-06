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
    Uses HuggingFace InferenceClient with fallback for vision-language models.
    
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
        if HF_CLIENT_AVAILABLE:
            # Use InferenceClient for Inference Providers support
            client = InferenceClient(api_key=AI_API_KEY)
            response_text = None
            
            # If image provided, try vision-language tasks first
            if image_bytes and len(image_bytes) > 0:
                logger.debug(f"Attempting multimodal request with image ({len(image_bytes)} bytes) to {AI_MODEL}")
                
                # Try image_to_text (good for caption/description models)
                try:
                    logger.debug("Trying image_to_text...")
                    result = client.image_to_text(image=image_bytes, model=AI_MODEL)
                    response_text = result if isinstance(result, str) else str(result)
                    logger.debug("image_to_text succeeded")
                except Exception as e:
                    logger.debug(f"image_to_text failed: {e}")
                
                # If image_to_text failed, try visual_question_answering
                if not response_text:
                    try:
                        logger.debug(f"Trying visual_question_answering with question: {prompt[:50]}...")
                        result = client.visual_question_answering(image=image_bytes, question=prompt, model=AI_MODEL)
                        if isinstance(result, dict):
                            response_text = result.get('answer') or str(result)
                        elif isinstance(result, list) and len(result) > 0:
                            first = result[0]
                            response_text = first.get('answer', str(first)) if isinstance(first, dict) else str(first)
                        else:
                            response_text = str(result)
                        logger.debug("visual_question_answering succeeded")
                    except Exception as e:
                        logger.debug(f"visual_question_answering failed: {e}")
                
                # If all vision tasks failed, log and try text-only fallback
                if not response_text:
                    logger.debug("All multimodal methods failed. Falling back to text-only inference.")
            
            # Text-only inference (or fallback from failed multimodal)
            if not response_text:
                try:
                    logger.debug(f"Attempting text_generation on {AI_MODEL}")
                    result = client.text_generation(
                        prompt=prompt,
                        model=AI_MODEL,
                        max_new_tokens=max_tokens,
                        temperature=0.7,
                        do_sample=True
                    )
                    response_text = result if isinstance(result, str) else str(result)
                    logger.debug("text_generation succeeded")
                except Exception as tg_err:
                    logger.debug(f"text_generation failed: {tg_err}")
                    # Last resort: try chat_completion
                    try:
                        logger.debug(f"Attempting chat_completion on {AI_MODEL}")
                        result = client.chat_completion(
                            messages=[{"role": "user", "content": prompt}],
                            model=AI_MODEL,
                            max_tokens=max_tokens,
                            temperature=0.7
                        )
                        if result and hasattr(result, 'choices') and len(result.choices) > 0:
                            response_text = result.choices[0].message.content
                        else:
                            response_text = str(result)
                        logger.debug("chat_completion succeeded")
                    except Exception as cc_err:
                        logger.debug(f"chat_completion also failed: {cc_err}")
                        # If all methods fail, provide guidance
                        error_msg = str(tg_err) or str(cc_err)
                        if "not a chat model" in error_msg.lower():
                            raise ValueError(
                                f"Model '{AI_MODEL}' is a vision-language model and is not available on free Inference Providers. "
                                "To use this model, deploy it to a HuggingFace Inference Endpoint: "
                                "https://huggingface.co/docs/hub/en/inference-endpoints"
                            )
                        else:
                            raise ValueError(f"Model inference failed: {error_msg}")
            
            if not response_text:
                raise ValueError("No response from model")
            
            return format_response(response_text)
        
        else:
            raise ValueError("HuggingFace SDK not installed. Install with: pip install huggingface_hub")
        
    except ValueError as ve:
        logger.error(f"API Error: {ve}")
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