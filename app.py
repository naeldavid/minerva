from flask import Flask, render_template, jsonify, request
import os
import logging
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), 'config', 'settings.env'))

# Configure minimal logging to reduce I/O
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Initialize Flask app with minimal configuration for Raspberry Pi Zero
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'raspberry-pi-secret-key')

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
            user_message = data.get('message', '')
            
            if not user_message:
                return jsonify({"error": "No message provided"}), 400
            
            # Process the AI request
            response = process_ai_request(user_message)
            return jsonify({"response": response})
        except Exception as e:
            logger.error(f"Error processing chat request: {e}")
            return jsonify({"error": "Failed to process chat request"}), 500
    else:
        return jsonify({"error": "AI client module not available"}), 500

if __name__ == '__main__':
    # Run with minimal configuration for Raspberry Pi Zero
    app.run(host='0.0.0.0', port=5000, debug=False)