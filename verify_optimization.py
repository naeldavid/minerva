#!/usr/bin/env python3

"""
Verification script for Raspberry Pi Zero optimizations
"""

import sys
import os

def check_file_sizes():
    """Check that files are reasonably sized for Pi Zero"""
    print("Checking file sizes...")
    
    # Get sizes of key files
    key_files = [
        'app.py',
        'api/system_stats.py',
        'api/miner_stats.py',
        'api/ai_client.py',
        'static/app.js',
        'static/style.css',
        'templates/dashboard.html'
    ]
    
    total_size = 0
    for file in key_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            total_size += size
            print(f"  {file}: {size} bytes")
        else:
            # Check in subdirectories
            found = False
            for root, dirs, files in os.walk('.'):
                if file in files:
                    filepath = os.path.join(root, file)
                    size = os.path.getsize(filepath)
                    total_size += size
                    print(f"  {filepath}: {size} bytes")
                    found = True
                    break
            if not found:
                print(f"  {file}: NOT FOUND")
    
    print(f"Total size of key files: {total_size} bytes ({total_size/1024:.1f} KB)")
    
    if total_size < 100000:  # Less than 100KB
        print("✓ File sizes are appropriate for Pi Zero")
        return True
    else:
        print("⚠ File sizes may be too large for Pi Zero")
        return False

def check_dependencies():
    """Check that dependencies are minimal"""
    print("\nChecking dependencies...")
    
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            deps = f.readlines()
        
        print(f"Found {len(deps)} dependencies:")
        for dep in deps:
            print(f"  - {dep.strip()}")
        
        if len(deps) <= 5:
            print("✓ Minimal dependencies")
            return True
        else:
            print("⚠ Too many dependencies")
            return False
    else:
        print("⚠ requirements.txt not found")
        return False

def check_imports():
    """Check for heavy imports"""
    print("\nChecking for heavy imports...")
    
    heavy_modules = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'tensorflow', 
        'torch', 'sklearn', 'opencv', 'pygame', 'kivy'
    ]
    
    found_heavy = []
    
    # Check Python files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                        for module in heavy_modules:
                            if f'import {module}' in content or f'from {module}' in content:
                                found_heavy.append(f"{filepath}: {module}")
                except:
                    pass  # Skip binary or unreadable files
    
    if found_heavy:
        print("⚠ Heavy modules found:")
        for item in found_heavy:
            print(f"  {item}")
        return False
    else:
        print("✓ No heavy imports found")
        return True

def check_logging():
    """Check logging configuration"""
    print("\nChecking logging configuration...")
    
    logging_checks = [
        ('WARNING', 'api/system_stats.py'),
        ('WARNING', 'api/miner_stats.py'),
        ('WARNING', 'api/ai_client.py'),
        ('WARNING', 'app.py')
    ]
    
    all_good = True
    for level, file in logging_checks:
        if os.path.exists(file):
            with open(file, 'r') as f:
                content = f.read()
                if f'setLevel(logging.{level})' in content or f'level=logging.{level}' in content:
                    print(f"  {file}: {level} logging ✓")
                else:
                    print(f"  {file}: Not using {level} logging ⚠")
                    all_good = False
    
    return all_good

def check_websockets():
    """Check that WebSockets are not used"""
    print("\nChecking for WebSockets...")
    
    websocket_terms = ['socketio', 'websocket', 'SocketIO', 'WebSocket']
    
    found_websocket = False
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.py', '.js', '.html')):
                filepath = os.path.join(root, file)
                # Skip this verification script itself
                if 'verify_optimization' in filepath:
                    continue
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                        for term in websocket_terms:
                            if term in content:
                                print(f"  {filepath}: Contains {term} ⚠")
                                found_websocket = True
                except:
                    pass  # Skip binary files
    
    if not found_websocket:
        print("✓ No WebSocket references found")
        return True
    else:
        print("⚠ WebSocket references found")
        return False

def main():
    """Main verification function"""
    print("=== Raspberry Pi Zero Optimization Verification ===\n")
    
    checks = [
        ("File Sizes", check_file_sizes),
        ("Dependencies", check_dependencies),
        ("Heavy Imports", check_imports),
        ("Logging", check_logging),
        ("WebSockets", check_websockets)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"--- {name} ---")
        result = check_func()
        results.append((name, result))
        print()
    
    # Summary
    print("=== SUMMARY ===")
    passed = 0
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status:4} {name}")
        if result:
            passed += 1
    
    print(f"\n{passed}/{len(checks)} checks passed")
    
    if passed == len(checks):
        print("\n🎉 All optimizations verified! Ready for Raspberry Pi Zero!")
        return True
    else:
        print("\n⚠ Some optimizations need attention")
        return False

if __name__ == "__main__":
    main()