import os
import logging
import requests
from typing import Dict, Any

# Configure minimal logging
log_level = os.environ.get('LOG_LEVEL', 'WARNING')
logging.basicConfig(level=getattr(logging, log_level, logging.WARNING))
logger = logging.getLogger(__name__)

# Get duino-coin configuration from environment
DUINO_COIN_USERNAME = os.environ.get('DUINO_COIN_USERNAME', '')

def get_miner_stats() -> Dict[str, Any]:
    """
    Get mining statistics from Duino-Coin Public API
    
    Requires DUINO_COIN_USERNAME environment variable to fetch stats.
    If not set, returns placeholder stats (miner still runs locally).
    
    Returns:
        Dictionary containing mining statistics
    """
    try:
        if not DUINO_COIN_USERNAME:
            # Gracefully degrade if username not set
            logger.debug("DUINO_COIN_USERNAME not set - returning placeholder stats")
            return {
                'hashrate': 0.0,
                'total_mined': 0.0,
                'uptime': 0,
                'estimated_daily_yield': 0.0
            }
        
        # Fetch from Duino-Coin API
        api_url = f"https://server.duinocoin.com/users/{DUINO_COIN_USERNAME}"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('success'):
            logger.error(f"API error: {data.get('message', 'Unknown error')}")
            return {
                'hashrate': 0.0,
                'total_mined': 0.0,
                'uptime': 0,
                'estimated_daily_yield': 0.0
            }
        
        result = data.get('result', {})
        balance = float(result.get('balance', {}).get('balance', 0))
        
        # Get miners data if available
        miners = result.get('miners', [])
        total_hashrate = 0.0
        if miners:
            for miner in miners:
                hashrate_str = miner.get('hashrate', '0')
                # Parse hashrate (e.g., "2.5 kH/s" -> 2500)
                try:
                    if 'kH/s' in hashrate_str:
                        total_hashrate += float(hashrate_str.replace('kH/s', '').strip()) * 1000
                    elif 'H/s' in hashrate_str:
                        total_hashrate += float(hashrate_str.replace('H/s', '').strip())
                except:
                    pass
        
        return {
            'hashrate': total_hashrate,
            'total_mined': balance,
            'uptime': 0,
            'estimated_daily_yield': 0.0
        }
        
    except requests.exceptions.ConnectionError as e:
        logger.debug(f"Could not connect to Duino-Coin API: {e}")
        return {
            'hashrate': 0.0,
            'total_mined': 0.0,
            'uptime': 0,
            'estimated_daily_yield': 0.0
        }
    except requests.exceptions.Timeout:
        logger.debug("Duino-Coin API timeout")
        return {
            'hashrate': 0.0,
            'total_mined': 0.0,
            'uptime': 0,
            'estimated_daily_yield': 0.0
        }
    except Exception as e:
        logger.debug(f"Error getting miner stats: {e}")
        return {
            'hashrate': 0.0,
            'total_mined': 0.0,
            'uptime': 0,
            'estimated_daily_yield': 0.0
        }

if __name__ == "__main__":
    # Test the function
    try:
        stats = get_miner_stats()
        print(stats)
    except Exception as e:
        print(f"Error: {e}")