#!/usr/bin/env python3
"""
Test file for JobSniper AI application
Run this to verify the application works correctly
"""

import sys
import os
import pytest
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import streamlit as st
        import pandas as pd
        import numpy as np
        print("✅ All core dependencies imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_structure():
    """Test that the main app file exists and has required components"""
    app_file = project_root / "app.py"
    
    if not app_file.exists():
        print("❌ app.py file not found")
        return False
    
    with open(app_file, 'r') as f:
        content = f.read()
    
    required_components = [
        "class JobSniperAI",
        "def render_dashboard",
        "def render_resume_analysis",
        "def render_job_matching",
        "def main()"
    ]
    
    for component in required_components:
        if component not in content:
            print(f"❌ Missing component: {component}")
            return False
    
    print("✅ App structure validation passed")
    return True

def test_requirements():
    """Test that requirements.txt exists and has core dependencies"""
    req_file = project_root / "requirements.txt"
    
    if not req_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    with open(req_file, 'r') as f:
        content = f.read()
    
    required_deps = ["streamlit", "pandas", "numpy"]
    
    for dep in required_deps:
        if dep not in content:
            print(f"❌ Missing dependency: {dep}")
            return False
    
    print("✅ Requirements validation passed")
    return True

def test_demo_functionality():
    """Test core demo functionality"""
    try:
        # Import the main app class
        from app import JobSniperAI
        
        # Create an instance
        app = JobSniperAI()
        
        # Test resume parsing
        test_text = "Python developer with 5 years experience in machine learning and data science"
        result = app.parse_resume_text(test_text)
        
        assert 'skills' in result
        assert 'total_score' in result
        assert len(result['skills']) > 0
        
        # Test job matching
        job_matches = app.generate_job_matches(result)
        assert len(job_matches) > 0
        assert 'match_score' in job_matches[0]
        
        print("✅ Demo functionality test passed")
        return True
        
    except Exception as e:
        print(f"❌ Demo functionality test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and return overall result"""
    print("🧪 Running JobSniper AI Tests...\n")
    
    tests = [
        ("Import Test", test_imports),
        ("App Structure Test", test_app_structure),
        ("Requirements Test", test_requirements),
        ("Demo Functionality Test", test_demo_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        result = test_func()
        results.append(result)
        print()
    
    passed = sum(results)
    total = len(results)
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\n🚀 To start the application, run:")
        print("   streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)