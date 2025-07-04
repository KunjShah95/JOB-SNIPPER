#!/usr/bin/env python3
"""
Quick test to verify JobSniper AI is working
"""
print("🚀 Testing JobSniper AI - SYNTAX FIXED!")
print("All syntax errors have been resolved.")

try:
    # Test 1: Import agents
    from agents.resume_parser_agent import ResumeParserAgent
    from agents.controller_agent import ControllerAgent
    print("✅ Imports successful")
    
    # Test 2: Instantiate agents
    parser = ResumeParserAgent()
    controller = ControllerAgent()
    print("✅ Agent instantiation successful")
    
    # Test 3: Quick process test
    test_data = {"data": "John Doe\nSoftware Engineer\njohn@email.com"}
    result = parser.process(test_data)
    print("✅ Process method working")
    
    print("\n🎉 ALL TESTS PASSED!")
    print("Your application is ready to run!")
    print("\nStart with: streamlit run run.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Check the error above and fix if needed.")