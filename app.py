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
secret_key = os.environ.get('SECRET_KEY')
if not secret_key or secret_key == 'your-secret-key-here':
    logger.warning("SECRET_KEY not set or using default. Generating random key.")
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
            return jsonify({"error": "Failed to get system stats"}), 500
    else:
        return jsonify({"error": "System stats module not available"}), 500

@app.route('/api/miner-stats')
def miner_stats():
    """API endpoint for mining statistics"""
    if miner_stats_available:
        try:
            stats = get_miner_stats()
            return jsonify(stats)
        except Exception as e:
            logger.error(f"Error getting miner stats: {e}")
            return jsonify({"error": "Failed to get miner stats"}), 500
    else:
        return jsonify({"error": "Miner stats module not available"}), 500

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

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for AI chat"""
    if ai_client_available:
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
        except ValueError:
            return jsonify({"error": "Invalid JSON"}), 400
        except Exception as e:
            logger.error(f"Error processing chat request: {e}")
            return jsonify({"error": "Failed to process chat request"}), 500
    else:
        return jsonify({"error": "AI client module not available"}), 500

if __name__ == '__main__':
    # Run with minimal configuration for Raspberry Pi Zero
    # Only bind to localhost for security - use reverse proxy for external access
    app.run(host='127.0.0.1', port=5000, debug=False)