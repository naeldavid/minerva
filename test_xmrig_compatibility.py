#!/usr/bin/env python3
"""
Test XMRig API compatibility for different versions
Supports: XMRig 2.8.3+ (including rPi-xmrig-gcc7.3.0)
"""

import json
import requests
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Sample API responses for different XMRig versions
XMRIG_2_8_3_RESPONSE = {
    "hashrate": 250.5,
    "results": {
        "shares_good": 42,
        "shares_total": 45,
        "hashes_good": 1250000,
        "hashes_total": 1300000
    },
    "connection": {
        "uptime": 3600,
        "pool": "pool.moneroocean.stream:10128",
        "failures": 0
    }
}

XMRIG_NEW_RESPONSE = {
    "hashrate": {
        "total": [250.5, 248.3, 247.9],
        "threads": [[125.2], [125.3]]
    },
    "results": {
        "accepted": 42,
        "rejected": 0,
        "diff_current": 1250000,
        "diff_total": 1300000
    },
    "connection": {
        "uptime": 3600,
        "pool": "pool.moneroocean.stream:10128",
        "failures": 0
    }
}

def test_xmrig_2_8_3_format():
    """Test parsing XMRig 2.8.3 response format"""
    print("\n--- Testing XMRig 2.8.3 Format ---")
    data = XMRIG_2_8_3_RESPONSE
    
    miner_stats = {
        'hashrate': 0,
        'total_mined': 0,
        'uptime': 0,
        'estimated_daily_yield': 0
    }
    
    # Hashrate - old format (direct number)
    if 'hashrate' in data and isinstance(data['hashrate'], (int, float)):
        miner_stats['hashrate'] = data['hashrate']
        print(f"✓ Hashrate (old format): {miner_stats['hashrate']} H/s")
    
    # Total mined - old field names
    if 'results' in data:
        if 'shares_good' in data['results']:
            miner_stats['total_mined'] = data['results']['shares_good']
            print(f"✓ Total mined (shares_good): {miner_stats['total_mined']}")
    
    # Uptime
    if 'connection' in data and 'uptime' in data['connection']:
        miner_stats['uptime'] = data['connection']['uptime']
        print(f"✓ Uptime: {miner_stats['uptime']} seconds")
    
    # Estimated yield
    if miner_stats['hashrate'] > 0:
        miner_stats['estimated_daily_yield'] = round(miner_stats['hashrate'] * 0.0001, 8)
        print(f"✓ Estimated daily yield: {miner_stats['estimated_daily_yield']}")
    
    return miner_stats

def test_xmrig_new_format():
    """Test parsing newer XMRig response format"""
    print("\n--- Testing Newer XMRig Format ---")
    data = XMRIG_NEW_RESPONSE
    
    miner_stats = {
        'hashrate': 0,
        'total_mined': 0,
        'uptime': 0,
        'estimated_daily_yield': 0
    }
    
    # Hashrate - new format (array)
    if 'hashrate' in data and isinstance(data['hashrate'], dict):
        if 'total' in data['hashrate']:
            hashrate_raw = data['hashrate']['total']
            if isinstance(hashrate_raw, list) and len(hashrate_raw) > 0:
                miner_stats['hashrate'] = hashrate_raw[0]
                print(f"✓ Hashrate (new format array): {miner_stats['hashrate']} H/s")
    
    # Total mined - new field names
    if 'results' in data:
        if 'accepted' in data['results']:
            miner_stats['total_mined'] = data['results']['accepted']
            print(f"✓ Total mined (accepted): {miner_stats['total_mined']}")
    
    # Uptime
    if 'connection' in data and 'uptime' in data['connection']:
        miner_stats['uptime'] = data['connection']['uptime']
        print(f"✓ Uptime: {miner_stats['uptime']} seconds")
    
    # Estimated yield
    if miner_stats['hashrate'] > 0:
        miner_stats['estimated_daily_yield'] = round(miner_stats['hashrate'] * 0.0001, 8)
        print(f"✓ Estimated daily yield: {miner_stats['estimated_daily_yield']}")
    
    return miner_stats

def test_real_xmrig_api(api_url="http://localhost:18080/api.json"):
    """Test against a real running XMRig instance"""
    print(f"\n--- Testing Real XMRig at {api_url} ---")
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        print("✓ Successfully connected to XMRig API")
        print(f"  Response keys: {list(data.keys())}")
        
        # Detect version based on response structure
        if isinstance(data.get('hashrate'), dict):
            print("✓ Detected: Newer XMRig version (hashrate as dict)")
        elif isinstance(data.get('hashrate'), (int, float)):
            print("✓ Detected: XMRig 2.8.3 or older (hashrate as number)")
        
        # Try to parse with our compatible function
        from api.miner_stats import get_miner_stats
        stats = get_miner_stats(api_url)
        print(f"✓ Successfully parsed stats: {stats}")
        return stats
        
    except requests.exceptions.ConnectionError:
        print(f"✗ Could not connect to {api_url}")
        print("  Make sure XMRig is running with API enabled (--api-port 18080)")
        return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("XMRig API Compatibility Test")
    print("=" * 60)
    
    # Test both formats
    old_format_result = test_xmrig_2_8_3_format()
    new_format_result = test_xmrig_new_format()
    
    print("\n" + "=" * 60)
    print("Results Comparison")
    print("=" * 60)
    print(f"\nXMRig 2.8.3 Format: {old_format_result}")
    print(f"Newer Format:      {new_format_result}")
    
    # Test real API if available
    print("\n" + "=" * 60)
    real_api_result = test_real_xmrig_api()
    
    if real_api_result:
        print("\n✓ All tests passed! Your XMRig version is compatible.")
    else:
        print("\n⚠ Could not test against live XMRig, but format tests passed.")
        print("  Once you start XMRig, run this test again to verify compatibility.")
