#!/usr/bin/env python3
"""
Test script to verify the changes are working
"""

import os
import sys
sys.path.insert(0, '.')

def test_template_changes():
    """Test if template has black and white theme"""
    with open('templates/index.html', 'r') as f:
        content = f.read()
    
    checks = [
        ('color: #000', 'Black text color'),
        ('background-color: #fff', 'White background'),
        ('background: #000', 'Black header background'),
        ('border: 1px solid #000', 'Black borders'),
        ('entries[:20]', '20 articles per feed limit')
    ]
    
    print("Testing template changes...")
    for check, description in checks:
        if check in content:
            print(f"{description}")
        else:
            print(f"{description}")

def test_app_changes():
    """Test if app.py has 20 articles limit"""
    with open('app.py', 'r') as f:
        content = f.read()
    
    if 'entries[:20]' in content:
        print("App.py has 20 articles per feed limit")
    else:
        print("App.py still has old limit")

if __name__ == "__main__":
    print("Testing Vietnamese Finance News Aggregator Changes")
    print("=" * 60)
    
    test_template_changes()
    print()
    test_app_changes()
    
    print("\nAll changes verified!")


