from flask import Flask, render_template, jsonify, request
import os
import logging
import time
import secrets
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), 'config', 'settings.env'))

# Configure minimal logging to reduce I/O
log_level = os.environ.get('LOG_LEVEL', 'WARNING')
logging.basicConfig(level=getattr(logging, log_level, logging.WARNING))
logger = logging.getLogger(__name__)

# Initialize Flask app with minimal configuration for Raspberry Pi Zero
app = Flask(__name__)
secret_key = os.environ.get('SECRET_KEY', '')
if not secret_key or 'generate-with-python3' in secret_key or secret_key == 'your-secret-key-here':
    logger.warning("SECRET_KEY not configured. Generating random key for this session.")
    logger.warning("For production, set SECRET_KEY in config/settings.env")
    secret_key = secrets.token_hex(32)
app.config['SECRET_KEY'] = secret_key
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024  # 16KB max request size

# Import modules (will be implemented in separate files)
try:
    from api.system_stats import get_system_stats
    system_stats_available = True
except ImportError:
    logger.warning("System stats module not available")
    system_stats_available = False

try:
    from api.miner_stats import get_miner_stats
    miner_stats_available = True
except ImportError:
    logger.warning("Miner stats module not available")
    miner_stats_available = False

try:
    from api.ai_client import process_ai_request
    ai_client_available = True
except ImportError:
    logger.warning("AI client module not available")
    ai_client_available = False

@app.route('/')
def dashboard():
    """Serve the main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/system-stats')
def system_stats():
    """API endpoint for system statistics"""
    if system_stats_available:
        try:
            stats = get_system_stats()
            return jsonify(stats)
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            # Return partial stats on error instead of 500
            return jsonify({
                'cpu_usage': 0,
                'memory_usage': 0,
                'temperature': None,
                'uptime': 0,
                'network': {}
            }), 200
    else:
        # Return empty stats instead of error
        return jsonify({
            'cpu_usage': 0,
            'memory_usage': 0,
            'temperature': None,
            'uptime': 0,
            'network': {}
        }), 200

@app.route('/api/miner-stats')
def miner_stats():
    """API endpoint for mining statistics"""
    if miner_stats_available:
        try:
            stats = get_miner_stats()
            return jsonify(stats)
        except Exception as e:
            logger.error(f"Error getting miner stats: {e}")
            # Return partial stats on error instead of 500
            return jsonify({
                'hashrate': 0.0,
                'total_mined': 0.0,
                'uptime': 0,
                'estimated_daily_yield': 0.0
            }), 200
    else:
        # Return empty stats instead of error
        return jsonify({
            'hashrate': 0.0,
            'total_mined': 0.0,
            'uptime': 0,
            'estimated_daily_yield': 0.0
        }), 200

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "modules": {
            "system_stats": system_stats_available,
            "miner_stats": miner_stats_available,
            "ai_client": ai_client_available
        }
    })

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return '', 204

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for AI chat"""
    if not ai_client_available:
        return jsonify({"response": "AI unavailable. System is running without AI support."}), 200
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Validate message length
        if len(user_message) > 2000:
            return jsonify({"error": "Message too long (max 2000 characters)"}), 400
        
        # Process the AI request
        response = process_ai_request(user_message)
        return jsonify({"response": response})
    except ValueError as e:
        # Return 200 with message instead of 503 for better UX
        logger.warning(f"AI service unavailable: {e}")
        return jsonify({"response": "AI service temporarily unavailable. Check your API configuration."}), 200
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        return jsonify({"response": "Error processing your message. Please try again."}), 200

if __name__ == '__main__':
    # Run with minimal configuration for Raspberry Pi Zero
    # Accessible on local network
    app.run(host='0.0.0.0', port=5000, debug=False)