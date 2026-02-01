#!/usr/bin/env python3
"""
Test cpuminer-ulti API compatibility and mining statistics
Minerva miner API compatibility tester
"""

import json
import requests
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Sample API response from cpuminer-ulti
CPUMINER_ULTI_RESPONSE = {
    "hashrate": 2500.5,
    "shares_valid": 42,
    "shares_rejected": 2,
    "uptime": 3600,
    "pool": "pool.moneroocean.stream:10128",
    "accepted": 42,
    "rejected": 2,
    "elapsed": 3600,
    "threads": 1,
    "version": "cpuminer-ulti"
}

def test_cpuminer_ulti_format():
    """Test parsing cpuminer-ulti API response format"""
    print("\n--- Testing cpuminer-ulti API Format ---")
    data = CPUMINER_ULTI_RESPONSE
    
    miner_stats = {
        'hashrate': 0,
        'total_mined': 0,
        'uptime': 0,
        'estimated_daily_yield': 0
    }
    
    # Hashrate
    if 'hashrate' in data:
        miner_stats['hashrate'] = float(data['hashrate'])
        print(f"✓ Hashrate: {miner_stats['hashrate']} H/s")
    
    # Total valid shares
    if 'shares_valid' in data:
        miner_stats['total_mined'] = int(data['shares_valid'])
        print(f"✓ Valid shares: {miner_stats['total_mined']}")
    elif 'accepted' in data:
        miner_stats['total_mined'] = int(data['accepted'])
        print(f"✓ Accepted shares: {miner_stats['total_mined']}")
    
    # Uptime
    if 'uptime' in data:
        miner_stats['uptime'] = int(data['uptime'])
        print(f"✓ Uptime: {miner_stats['uptime']} seconds")
    elif 'elapsed' in data:
        miner_stats['uptime'] = int(data['elapsed'])
        print(f"✓ Elapsed: {miner_stats['uptime']} seconds")
    
    # Additional info
    if 'threads' in data:
        print(f"✓ CPU threads: {data['threads']}")
    if 'version' in data:
        print(f"✓ Miner: {data['version']}")
    if 'pool' in data:
        print(f"✓ Pool: {data['pool']}")
    
    # Estimated yield (simplified)
    if miner_stats['hashrate'] > 0:
        miner_stats['estimated_daily_yield'] = round(miner_stats['hashrate'] * 0.0001, 8)
        print(f"✓ Estimated daily yield: {miner_stats['estimated_daily_yield']}")
    
    return miner_stats

def test_real_cpuminer_ulti_api(api_url="http://localhost:4048/api/get_stats"):
    """Test against a real running cpuminer-ulti instance"""
    print(f"\n--- Testing cpuminer-ulti at {api_url} ---")
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        print("✓ Successfully connected to cpuminer-ulti API")
        print(f"  Response keys: {list(data.keys())}")
        
        # Try to parse with our compatible function
        from api.miner_stats import get_miner_stats
        stats = get_miner_stats(api_url)
        print(f"✓ Successfully parsed stats:")
        print(f"  - Hashrate: {stats['hashrate']} H/s")
        print(f"  - Shares accepted: {stats['total_mined']}")
        print(f"  - Uptime: {stats['uptime']} seconds")
        print(f"  - Est. daily yield: {stats['estimated_daily_yield']}")
        return stats
        
    except requests.exceptions.ConnectionError:
        print(f"✗ Could not connect to {api_url}")
        print("  Make sure cpuminer-ulti is running with API enabled:")
        print("    cpuminer-ulti --api-bind=127.0.0.1:4048")
        return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("Cpuminer-ulti API Compatibility Test")
    print("=" * 60)
    
    # Test format parsing
    format_result = test_cpuminer_ulti_format()
    
    print("\n" + "=" * 60)
    print("Format Test Results")
    print("=" * 60)
    print(f"\nParsed stats: {format_result}")
    
    # Test real API if available
    print("\n" + "=" * 60)
    real_api_result = test_real_cpuminer_ulti_api()
    
    if real_api_result:
        print("\n✓ All tests passed! Cpuminer-ulti is ready for Minerva.")
    else:
        print("\n⚠ Could not test against live cpuminer-ulti.")
        print("  Format tests passed. Once you start cpuminer-ulti with API,")
        print("  run this test again to verify full compatibility.")
