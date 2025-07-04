#!/usr/bin/env python3
"""
Quick syntax test to verify the fix
"""

def test_imports():
    """Test that all imports work without syntax errors"""
    try:
        print("Testing imports...")
        
        # Test the problematic import chain
        from agents.resume_parser_agent import ResumeParserAgent
        print("✅ ResumeParserAgent import successful")
        
        from agents.controller_agent import ControllerAgent
        print("✅ ControllerAgent import successful")
        
        from agents import ControllerAgent as CA
        print("✅ Package-level import successful")
        
        # Test instantiation
        agent = ResumeParserAgent()
        print("✅ ResumeParserAgent instantiation successful")
        
        controller = ControllerAgent()
        print("✅ ControllerAgent instantiation successful")
        
        print("\n🎉 All syntax errors fixed!")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")
        return False
    except Exception as e:
        print(f"⚠️ Other Error: {e}")
        return False

if __name__ == "__main__":
    test_imports()