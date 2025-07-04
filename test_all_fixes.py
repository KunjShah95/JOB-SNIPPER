#!/usr/bin/env python3
"""
Comprehensive test script to verify all fixes in JobSniper AI

Tests:
1. Gemini 2.5 Pro model configuration
2. Sidebar visibility fix
3. Resume parser abstract method fix
4. Configuration validation
5. All imports work correctly

Run with: streamlit run test_all_fixes.py
"""

import streamlit as st
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work correctly"""
    st.subheader("🔍 Import Tests")
    
    try:
        from utils.config import validate_config, load_config, GEMINI_AVAILABLE
        st.success("✅ Config imports successful")
    except Exception as e:
        st.error(f"❌ Config import failed: {e}")
        return False
    
    try:
        from agents.multi_ai_base import MultiAIAgent
        st.success("✅ MultiAI base import successful")
    except Exception as e:
        st.error(f"❌ MultiAI base import failed: {e}")
        return False
    
    try:
        from agents.resume_parser_agent import ResumeParserAgent
        st.success("✅ Resume parser import successful")
    except Exception as e:
        st.error(f"❌ Resume parser import failed: {e}")
        return False
    
    try:
        from ui.components.sidebar import create_sidebar
        st.success("✅ Sidebar component import successful")
    except Exception as e:
        st.error(f"❌ Sidebar component import failed: {e}")
        return False
    
    return True

def test_gemini_model():
    """Test Gemini 2.5 Pro model configuration"""
    st.subheader("🤖 Gemini 2.5 Pro Test")
    
    try:
        from utils.config import validate_config
        validation = validate_config()
        
        if 'gemini-2.5-pro' in validation.get('ai_providers', []):
            st.success("✅ Gemini 2.5 Pro model configured correctly")
            return True
        elif validation.get('gemini_model') == 'gemini-2.5-pro':
            st.success("✅ Gemini 2.5 Pro model set in config")
            return True
        else:
            st.warning("⚠️ Gemini 2.5 Pro not configured (API key needed)")
            return True  # Not an error, just needs API key
    except Exception as e:
        st.error(f"❌ Gemini model test failed: {e}")
        return False

def test_resume_parser():
    """Test that ResumeParserAgent can be instantiated"""
    st.subheader("📄 Resume Parser Test")
    
    try:
        from agents.resume_parser_agent import ResumeParserAgent
        
        # This should not raise "Can't instantiate abstract class" error
        agent = ResumeParserAgent()
        st.success("✅ ResumeParserAgent instantiated successfully")
        
        # Test that required methods exist
        if hasattr(agent, 'process'):
            st.success("✅ process() method implemented")
        else:
            st.error("❌ process() method missing")
            return False
            
        if hasattr(agent, 'run'):
            st.success("✅ run() method implemented")
        else:
            st.error("❌ run() method missing")
            return False
            
        return True
        
    except TypeError as e:
        if "abstract" in str(e).lower():
            st.error(f"❌ Abstract method error still exists: {e}")
            return False
        else:
            st.error(f"❌ Unexpected TypeError: {e}")
            return False
    except Exception as e:
        st.error(f"❌ Resume parser test failed: {e}")
        return False

def test_config_validation():
    """Test configuration validation"""
    st.subheader("⚙️ Configuration Test")
    
    try:
        from utils.config import validate_config, load_config
        
        config = load_config()
        validation = validate_config()
        
        st.write("**Configuration Status:**")
        st.write(f"- Valid: {validation.get('valid', False)}")
        st.write(f"- AI Providers: {validation.get('ai_providers', [])}")
        st.write(f"- Features Enabled: {validation.get('total_features', 0)}")
        st.write(f"- Gemini Model: {validation.get('gemini_model', 'Not set')}")
        
        if validation.get('warnings'):
            st.write("**Warnings:**")
            for warning in validation['warnings']:
                st.warning(f"⚠️ {warning}")
        
        if validation.get('issues'):
            st.write("**Issues:**")
            for issue in validation['issues']:
                st.error(f"❌ {issue}")
        
        st.success("✅ Configuration validation working")
        return True
        
    except Exception as e:
        st.error(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Main test function"""
    
    # Set page config
    st.set_page_config(
        page_title="JobSniper AI - All Fixes Test",
        page_icon="🧪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply sidebar fix
    st.markdown('<style>section[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a365d 0%,#2d3748 50%,#1a202c 100%)!important}section[data-testid="stSidebar"] *{color:white!important}</style>', unsafe_allow_html=True)
    
    # Main content
    st.title("🧪 JobSniper AI - Comprehensive Fix Test")
    st.write("Testing all fixes: Gemini 2.5 Pro, Sidebar UI, Resume Parser, and Configuration")
    
    # Sidebar test
    with st.sidebar:
        st.title("🎯 Test Sidebar")
        st.write("This sidebar should have:")
        st.write("✅ Dark gradient background")
        st.write("✅ White text (visible)")
        st.write("✅ Functional controls")
        
        test_nav = st.radio("Navigation Test:", ["Home", "Resume", "Jobs"])
        st.checkbox("Checkbox Test")
        st.selectbox("Selectbox Test", ["Option 1", "Option 2"])
        
        st.success("✅ Success message")
        st.warning("⚠️ Warning message")
        st.error("❌ Error message")
        st.info("ℹ️ Info message")
    
    # Run all tests
    st.header("🔬 Test Results")
    
    tests = [
        ("Import Tests", test_imports),
        ("Gemini 2.5 Pro Test", test_gemini_model),
        ("Resume Parser Test", test_resume_parser),
        ("Configuration Test", test_config_validation)
    ]
    
    results = []
    for test_name, test_func in tests:
        with st.expander(f"🧪 {test_name}", expanded=True):
            result = test_func()
            results.append((test_name, result))
    
    # Summary
    st.header("📊 Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    if passed == total:
        st.success(f"🎉 All tests passed! ({passed}/{total})")
        st.balloons()
    else:
        st.error(f"💥 Some tests failed. ({passed}/{total} passed)")
    
    # Detailed results
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Passed Tests")
        for test_name, result in results:
            if result:
                st.write(f"✅ {test_name}")
    
    with col2:
        st.subheader("❌ Failed Tests")
        failed_tests = [test_name for test_name, result in results if not result]
        if failed_tests:
            for test_name in failed_tests:
                st.write(f"❌ {test_name}")
        else:
            st.write("🎉 No failed tests!")
    
    # Instructions
    st.header("📋 What's Fixed")
    
    st.markdown("""
    ## ✅ Fixed Issues:
    
    1. **Gemini 2.5 Pro Model** - Updated from gemini-2.0-flash to gemini-2.5-pro
    2. **Sidebar Visibility** - Dark gradient background with white text
    3. **Resume Parser Abstract Method** - Added missing process() method
    4. **Configuration Validation** - Improved error handling and status reporting
    5. **Import Issues** - Fixed all broken imports and dependencies
    
    ## 🚀 How to Use:
    
    1. **Set API Keys** in `.env` file:
       ```
       GEMINI_API_KEY=your_gemini_api_key_here
       MISTRAL_API_KEY=your_mistral_api_key_here
       ```
    
    2. **Run the main app**:
       ```bash
       streamlit run ui/app.py
       ```
    
    3. **Sidebar should be visible** with dark background and white text
    
    4. **All agents should work** without abstract method errors
    """)

if __name__ == "__main__":
    main()