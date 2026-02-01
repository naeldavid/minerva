import requests
import logging
from typing import Dict, Any

# Configure minimal logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Default cpuminer-ulti API endpoint
MINER_API_URL = "http://localhost:4048/api/get_stats"

# Global session for connection reuse
session = requests.Session()
session.timeout = 5

def get_miner_stats(api_url: str = MINER_API_URL) -> Dict[str, Any]:
    """
    Get mining statistics from cpuminer-ulti API
    
    Args:
        api_url: URL to the cpuminer-ulti API endpoint (default: http://localhost:4048/api/get_stats)
        
    Returns:
        Dictionary containing mining statistics
    """
    try:
        # Make request to cpuminer-ulti API using reusable session
        response = session.get(api_url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant statistics
        miner_stats = {
            'hashrate': 0,
            'total_mined': 0,
            'uptime': 0,
            'estimated_daily_yield': 0
        }
        
        # cpuminer-ulti API response handling
        # The API typically returns: hashrate (H/s), shares_valid, shares_rejected, uptime (seconds)
        if 'hashrate' in data:
            miner_stats['hashrate'] = float(data['hashrate'])
        
        # Total valid shares accepted
        if 'shares_valid' in data:
            miner_stats['total_mined'] = int(data['shares_valid'])
        elif 'accepted' in data:
            miner_stats['total_mined'] = int(data['accepted'])
        
        # Uptime in seconds
        if 'uptime' in data:
            miner_stats['uptime'] = int(data['uptime'])
        elif 'elapsed' in data:
            miner_stats['uptime'] = int(data['elapsed'])
        
        # Estimated daily yield (simplified calculation)
        if miner_stats['hashrate'] > 0:
            # Rough estimate - would need actual network data for accuracy
            miner_stats['estimated_daily_yield'] = round(miner_stats['hashrate'] * 0.0001, 8)
        
        return miner_stats
        
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Could not connect to miner API at {api_url}")
        raise Exception(f"Could not connect to miner. Is cpuminer-ulti running with API enabled on {api_url}?")
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout connecting to miner API: {e}")
        raise Exception("Miner API request timed out")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to miner API: {e}")
        raise Exception(f"Could not connect to miner API at {api_url}")
    except Exception as e:
        logger.error(f"Error getting miner stats: {e}")
        raise

if __name__ == "__main__":
    # Test the function
    try:
        stats = get_miner_stats()
        print(stats)
    except Exception as e:
        print(f"Error: {e}")