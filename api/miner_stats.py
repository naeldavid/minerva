import requests
import logging
from typing import Dict, Any

# Configure minimal logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Default XMRig API endpoint
XMRIG_API_URL = "http://localhost:18080/api.json"

# Global session for connection reuse
session = requests.Session()
session.timeout = 5

# Default XMRig API endpoint
XMRIG_API_URL = "http://localhost:18080/api.json"

def get_miner_stats(api_url: str = XMRIG_API_URL) -> Dict[str, Any]:
    """
    Get mining statistics from XMRig API
    Compatible with XMRig 2.8.3+ (including rPi-xmrig-gcc7.3.0)
    
    Args:
        api_url: URL to the XMRig API endpoint
        
    Returns:
        Dictionary containing mining statistics
    """
    try:
        # Make request to XMRig API using reusable session
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
        
        # XMRig 2.8.3 and newer API response handling
        # Hashrate (current 1-minute average) - supports both old and new formats
        hashrate_value = 0
        
        # New format: hashrate.total array
        if 'hashrate' in data and isinstance(data['hashrate'], dict):
            if 'total' in data['hashrate']:
                hashrate_raw = data['hashrate']['total']
                if isinstance(hashrate_raw, list) and len(hashrate_raw) > 0:
                    hashrate_value = hashrate_raw[0]  # 1-minute average
                elif isinstance(hashrate_raw, (int, float)):
                    hashrate_value = hashrate_raw
        
        # Old format (XMRig 2.8.3): hashrate as direct number
        elif 'hashrate' in data and isinstance(data['hashrate'], (int, float)):
            hashrate_value = data['hashrate']
        
        miner_stats['hashrate'] = hashrate_value
        
        # Total shares / hashes accepted
        # XMRig 2.8.3: results.shares_good or results.hashes_good
        # Newer: results.accepted or results.diff_current
        if 'results' in data:
            if 'shares_good' in data['results']:
                miner_stats['total_mined'] = data['results']['shares_good']
            elif 'hashes_good' in data['results']:
                miner_stats['total_mined'] = data['results']['hashes_good']
            elif 'accepted' in data['results']:
                miner_stats['total_mined'] = data['results']['accepted']
            elif 'diff_current' in data['results']:
                miner_stats['total_mined'] = data['results']['diff_current']
        
        # Uptime - handle both formats
        # XMRig 2.8.3: connection.uptime or uptime at root level
        uptime_value = 0
        if 'connection' in data and 'uptime' in data['connection']:
            uptime_value = data['connection']['uptime']
        elif 'uptime' in data:
            uptime_value = data['uptime']
        
        miner_stats['uptime'] = uptime_value
        
        # Estimated daily yield (simplified calculation)
        if miner_stats['hashrate'] > 0:
            # Rough estimate - would need actual network data for accuracy
            miner_stats['estimated_daily_yield'] = round(miner_stats['hashrate'] * 0.0001, 8)
        
        return miner_stats
        
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Could not connect to miner API at {api_url}")
        raise Exception(f"Could not connect to miner. Is XMRig running on {api_url}?")
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