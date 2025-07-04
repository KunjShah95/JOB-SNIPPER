#!/usr/bin/env python3
"""
Test script to verify abstract method fix is working

This tests that ResumeParserAgent can be instantiated and used without
the "Can't instantiate abstract class" error.
"""

import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_resume_parser_instantiation():
    """Test that ResumeParserAgent can be instantiated"""
    print("🧪 Testing ResumeParserAgent instantiation...")
    
    try:
        from agents.resume_parser_agent import ResumeParserAgent
        
        # This should NOT raise "Can't instantiate abstract class" error
        agent = ResumeParserAgent()
        print("✅ ResumeParserAgent instantiated successfully!")
        
        # Test that the process method exists and is callable
        if hasattr(agent, 'process') and callable(getattr(agent, 'process')):
            print("✅ process() method is implemented and callable")
        else:
            print("❌ process() method is missing or not callable")
            return False
        
        # Test that the run method exists
        if hasattr(agent, 'run') and callable(getattr(agent, 'run')):
            print("✅ run() method is implemented and callable")
        else:
            print("❌ run() method is missing or not callable")
            return False
        
        return True
        
    except TypeError as e:
        if "abstract" in str(e).lower():
            print(f"❌ Abstract method error still exists: {e}")
            return False
        else:
            print(f"❌ Unexpected TypeError: {e}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_resume_parser_process_method():
    """Test that the process method works correctly"""
    print("\n🧪 Testing ResumeParserAgent.process() method...")
    
    try:
        from agents.resume_parser_agent import ResumeParserAgent
        
        agent = ResumeParserAgent()
        
        # Test with sample data
        test_data = {
            'data': 'John Doe\nSoftware Engineer\njohn.doe@email.com\n(555) 123-4567\nPython, JavaScript, React'
        }
        
        # This should work without errors
        result = agent.process(test_data)
        print("✅ process() method executed successfully!")
        
        # Check if result is a dictionary
        if isinstance(result, dict):
            print("✅ process() method returns a dictionary")
        else:
            print(f"⚠️ process() method returns {type(result)}, expected dict")
        
        # Check for expected fields
        expected_fields = ['personal_info', 'skills', 'experience', 'education']
        for field in expected_fields:
            if field in result:
                print(f"✅ Found expected field: {field}")
            else:
                print(f"⚠️ Missing expected field: {field}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing process() method: {e}")
        return False

def test_controller_agent():
    """Test that ControllerAgent can be instantiated and uses ResumeParserAgent"""
    print("\n🧪 Testing ControllerAgent with ResumeParserAgent...")
    
    try:
        from agents.controller_agent import ControllerAgent
        
        # This should work without errors
        controller = ControllerAgent()
        print("✅ ControllerAgent instantiated successfully!")
        
        # Check if it has a parser attribute
        if hasattr(controller, 'parser'):
            print("✅ ControllerAgent has parser attribute")
            
            # Check if parser is a ResumeParserAgent
            from agents.resume_parser_agent import ResumeParserAgent
            if isinstance(controller.parser, ResumeParserAgent):
                print("✅ ControllerAgent.parser is a ResumeParserAgent instance")
            else:
                print(f"⚠️ ControllerAgent.parser is {type(controller.parser)}")
        else:
            print("❌ ControllerAgent missing parser attribute")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing ControllerAgent: {e}")
        return False

def test_all_agent_imports():
    """Test that all agent imports work"""
    print("\n🧪 Testing all agent imports...")
    
    agents_to_test = [
        'ResumeParserAgent',
        'ControllerAgent',
        'JobMatcherAgent',
        'FeedbackAgent',
        'ResumeTailorAgent',
        'TitleGeneratorAgent',
        'JDGeneratorAgent'
    ]
    
    success_count = 0
    
    for agent_name in agents_to_test:
        try:
            module_name = f"agents.{agent_name.lower().replace('agent', '_agent')}"
            module = __import__(module_name, fromlist=[agent_name])
            agent_class = getattr(module, agent_name)
            
            # Try to instantiate
            agent = agent_class()
            print(f"✅ {agent_name} imported and instantiated successfully")
            success_count += 1
            
        except Exception as e:
            print(f"❌ {agent_name} failed: {e}")
    
    print(f"\n📊 Import Results: {success_count}/{len(agents_to_test)} agents working")
    return success_count == len(agents_to_test)

def main():
    """Run all tests"""
    print("🔬 JobSniper AI - Abstract Method Fix Test")
    print("=" * 50)
    
    tests = [
        ("ResumeParserAgent Instantiation", test_resume_parser_instantiation),
        ("ResumeParserAgent Process Method", test_resume_parser_process_method),
        ("ControllerAgent Integration", test_controller_agent),
        ("All Agent Imports", test_all_agent_imports)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Abstract method error is FIXED!")
        print("\n✅ You can now:")
        print("   • Instantiate ResumeParserAgent without errors")
        print("   • Use the process() method")
        print("   • Run the full application")
    else:
        print(f"\n💥 {total - passed} tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)