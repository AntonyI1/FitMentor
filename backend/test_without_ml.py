"""
Test script to verify backend structure without ML dependencies
Useful for development and quick testing
"""

import sys
import os

# Test basic imports
print("Testing FitMentor Backend Structure")
print("=" * 50)

try:
    print("\n1. Testing data collector...")
    from models.data_collector import DataCollector
    collector = DataCollector()
    print(f"   ✓ DataCollector works")
    print(f"   ✓ Data directory: {collector.data_dir}")
except Exception as e:
    print(f"   ✗ Error: {e}")

try:
    print("\n2. Testing Flask app structure...")
    # Check if app.py exists and is readable
    app_path = os.path.join(os.path.dirname(__file__), 'app.py')
    if os.path.exists(app_path):
        print(f"   ✓ app.py exists")
        with open(app_path, 'r') as f:
            content = f.read()
            if 'Flask' in content:
                print(f"   ✓ Flask app defined")
            if '@app.route' in content:
                routes = content.count('@app.route')
                print(f"   ✓ {routes} API routes defined")
except Exception as e:
    print(f"   ✗ Error: {e}")

try:
    print("\n3. Testing model files exist...")
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    if os.path.exists(models_dir):
        files = os.listdir(models_dir)
        print(f"   ✓ Models directory exists")
        print(f"   Files: {', '.join([f for f in files if f.endswith('.py')])}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 50)
print("\nTo run the full app, install dependencies:")
print("  pip install flask flask-cors numpy tensorflow torch")
print("\nOr use the setup script:")
print("  ./setup.sh")
