#!/usr/bin/env python3
"""
Proxy Detector Installation Verification Script

This script verifies that all components are properly installed and configured.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version >= (3, 8):
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} (Requires 3.8+)")
        return False

def check_dependencies():
    print("\n🔍 Checking Python dependencies...")
    dependencies = [
        'aiohttp',
        'aiofiles',
        'yaml',
        'loguru',
        'pydantic',
    ]
    
    all_ok = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"   ✓ {dep}")
        except ImportError:
            print(f"   ✗ {dep} (Not installed)")
            all_ok = False
    
    return all_ok

def check_file_structure():
    print("\n🔍 Checking file structure...")
    required_files = [
        'main.py',
        'requirements.txt',
        'config/config.yaml',
        'config/mihomo-template.yaml',
        'core/__init__.py',
        'core/detector.py',
        'protocols/__init__.py',
        'protocols/http_handler.py',
        'protocols/mihomo_handler.py',
        'data_sources/__init__.py',
        'data_sources/base.py',
        'data_sources/file_source.py',
        'data_sources/url_source.py',
        'data_sources/api_source.py',
        'utils/__init__.py',
        'utils/config_loader.py',
        'utils/logger.py',
        '.gitignore',
        'Dockerfile',
        'docker-compose.yaml',
    ]
    
    all_ok = True
    for file in required_files:
        if Path(file).exists():
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} (Missing)")
            all_ok = False
    
    return all_ok

def check_mihomo():
    print("\n🔍 Checking Mihomo binary...")
    mihomo_paths = ['./mihomo', '/usr/local/bin/mihomo', '/usr/bin/mihomo']
    
    for path in mihomo_paths:
        if Path(path).exists():
            print(f"   ✓ Mihomo found at {path}")
            return True
    
    print("   ⚠ Mihomo binary not found (optional, but required for SS/SSR/VMess/VLESS/Trojan/Hysteria)")
    print("   Download from: https://github.com/MetaCubeX/mihomo/releases")
    return None

def check_syntax():
    print("\n🔍 Checking Python syntax...")
    try:
        import py_compile
        files = [
            'main.py',
            'core/detector.py',
            'protocols/http_handler.py',
            'protocols/mihomo_handler.py',
            'data_sources/file_source.py',
            'utils/config_loader.py',
            'utils/logger.py',
        ]
        
        all_ok = True
        for file in files:
            try:
                py_compile.compile(file, doraise=True)
                print(f"   ✓ {file}")
            except py_compile.PyCompileError as e:
                print(f"   ✗ {file} - {e}")
                all_ok = False
        
        return all_ok
    except Exception as e:
        print(f"   ✗ Syntax check failed: {e}")
        return False

def check_documentation():
    print("\n🔍 Checking documentation...")
    docs = [
        'README.md',
        'QUICKSTART.md',
        'ARCHITECTURE.md',
        'PROJECT_OVERVIEW.md',
        'TECHNICAL_SPECS.md',
        'IMPLEMENTATION_SUMMARY.md',
        'CHANGELOG.md',
    ]
    
    all_ok = True
    for doc in docs:
        if Path(doc).exists():
            print(f"   ✓ {doc}")
        else:
            print(f"   ✗ {doc} (Missing)")
            all_ok = False
    
    return all_ok

def main():
    print("=" * 60)
    print("Proxy Detector - Installation Verification")
    print("=" * 60)
    
    results = []
    
    results.append(("Python Version", check_python_version()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("File Structure", check_file_structure()))
    mihomo_result = check_mihomo()
    if mihomo_result is not None:
        results.append(("Mihomo Binary", mihomo_result))
    results.append(("Python Syntax", check_syntax()))
    results.append(("Documentation", check_documentation()))
    
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:20} {status}")
        if not result:
            all_passed = False
    
    if mihomo_result is None:
        print(f"{'Mihomo Binary':20} ⚠ OPTIONAL")
    
    print("=" * 60)
    
    if all_passed:
        print("\n✅ All checks passed! You can start using Proxy Detector.")
        print("\nQuick start:")
        print("  1. Edit proxies.txt with your proxy list")
        print("  2. Run: python main.py --once")
        print("  3. Check results in output/ directory")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        print("\nTo install dependencies:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == '__main__':
    sys.exit(main())
