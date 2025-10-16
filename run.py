#!/usr/bin/env python3
"""
Simple run script for the Vietnamese Finance News Aggregator
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'feedparser', 'requests', 'python-dateutil', 'gunicorn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall them with: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main run function"""
    print("Vietnamese Finance News Aggregator")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n🔧 Installing dependencies...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
            print("Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("Failed to install dependencies")
            sys.exit(1)
    
    # Check if .env file exists
    if not Path('.env').exists() and Path('env.example').exists():
        print("\nCreating .env file from template...")
        try:
            with open('env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print(".env file created. Edit it to add your OpenAI API key if needed.")
        except Exception as e:
            print(f"Could not create .env file: {e}")
    
    # Run the application
    print("\nStarting the application...")
    print("   Open your browser and go to: http://localhost:5001")
    print("   Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        from app import app
        app.run(host='0.0.0.0', port=5001, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\nError starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
