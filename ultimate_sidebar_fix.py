#!/usr/bin/env python3
"""
ULTIMATE Sidebar Visibility Fix for Streamlit Apps

This is the most comprehensive fix that targets ALL possible Streamlit sidebar selectors
and uses multiple strategies to ensure text visibility.

Usage:
    from ultimate_sidebar_fix import fix_sidebar_now
    fix_sidebar_now()
"""

import streamlit as st

def fix_sidebar_now():
    """Apply the most comprehensive sidebar visibility fix"""
    
    st.markdown("""
    <style>
    /* ULTIMATE SIDEBAR FIX - TARGETS ALL POSSIBLE SELECTORS */
    
    /* Method 1: Target all known sidebar container classes */
    .css-1d391kg, .css-1lcbmhc, .css-17eq0hr, .css-1y4p8pa, .css-16txtl3,
    .st-emotion-cache-16txtl3, .st-emotion-cache-1y4p8pa, .st-emotion-cache-1lcbmhc,
    .st-emotion-cache-1d391kg, .st-emotion-cache-17eq0hr,
    section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div,
    .stSidebar, .sidebar, [data-testid="stSidebar"],
    .css-1aumxhk, .css-1cypcdb, .css-1outpf7, .css-1v0mbdj {
        background: linear-gradient(180deg, #1a365d 0%, #2d3748 50%, #1a202c 100%) !important;
        color: white !important;
    }
    
    /* Method 2: Force ALL text in sidebar to be white */
    .css-1d391kg *, .css-1lcbmhc *, .css-17eq0hr *, .css-1y4p8pa *, .css-16txtl3 *,
    .st-emotion-cache-16txtl3 *, .st-emotion-cache-1y4p8pa *, .st-emotion-cache-1lcbmhc *,
    .st-emotion-cache-1d391kg *, .st-emotion-cache-17eq0hr *,
    section[data-testid="stSidebar"] *, section[data-testid="stSidebar"] > div *,
    .stSidebar *, .sidebar *, [data-testid="stSidebar"] *,
    .css-1aumxhk *, .css-1cypcdb *, .css-1outpf7 *, .css-1v0mbdj * {
        color: white !important;
    }
    
    /* Method 3: Target specific elements with !important */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] h5,
    section[data-testid="stSidebar"] h6,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stText,
    section[data-testid="stSidebar"] .element-container {
        color: white !important;
        background-color: transparent !important;
    }
    
    /* Method 4: Target form elements specifically */
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stCheckbox label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stTextInput label,
    section[data-testid="stSidebar"] .stTextArea label,
    section[data-testid="stSidebar"] .stNumberInput label,
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stDateInput label,
    section[data-testid="stSidebar"] .stTimeInput label {
        color: white !important;
    }
    
    /* Method 5: Target radio button text specifically */
    section[data-testid="stSidebar"] .stRadio > div > div > div > label > div {
        color: white !important;
    }
    
    /* Method 6: Target checkbox text specifically */
    section[data-testid="stSidebar"] .stCheckbox > div > div > div > label > div {
        color: white !important;
    }
    
    /* Method 7: Override any inherited styles */
    section[data-testid="stSidebar"] .stMarkdown > div,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: white !important;
    }
    
    /* Method 8: Status messages with better visibility */
    section[data-testid="stSidebar"] .stSuccess {
        background-color: rgba(72, 187, 120, 0.2) !important;
        border: 2px solid #48bb78 !important;
        color: #c6f6d5 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    
    section[data-testid="stSidebar"] .stWarning {
        background-color: rgba(237, 137, 54, 0.2) !important;
        border: 2px solid #ed8936 !important;
        color: #fbd38d !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    
    section[data-testid="stSidebar"] .stError {
        background-color: rgba(245, 101, 101, 0.2) !important;
        border: 2px solid #f56565 !important;
        color: #fed7d7 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    
    section[data-testid="stSidebar"] .stInfo {
        background-color: rgba(66, 153, 225, 0.2) !important;
        border: 2px solid #4299e1 !important;
        color: #bee3f8 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    
    /* Method 9: Dividers */
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.3) !important;
        border-width: 1px !important;
        margin: 16px 0 !important;
    }
    
    /* Method 10: Buttons in sidebar */
    section[data-testid="stSidebar"] .stButton > button {
        background-color: #4299e1 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #3182ce !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(66, 153, 225, 0.4) !important;
    }
    
    /* Method 11: Force text color on all possible text elements */
    section[data-testid="stSidebar"] .css-1cpxqw2,
    section[data-testid="stSidebar"] .css-16huue1,
    section[data-testid="stSidebar"] .css-1inwz65,
    section[data-testid="stSidebar"] .css-1v0mbdj,
    section[data-testid="stSidebar"] .css-1outpf7 {
        color: white !important;
    }
    
    /* Method 12: Target any remaining text elements */
    section[data-testid="stSidebar"] [class*="css-"] {
        color: white !important;
    }
    
    /* Method 13: Ensure sidebar container has proper styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a365d 0%, #2d3748 50%, #1a202c 100%) !important;
        border-right: 2px solid #4a5568 !important;
    }
    
    /* Method 14: Add some padding and styling */
    section[data-testid="stSidebar"] > div {
        padding: 16px !important;
    }
    
    /* Method 15: Override any theme-specific styles */
    .stApp section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Method 16: Nuclear option - force white text everywhere in sidebar */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Method 17: Add a subtle glow effect for better readability */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Method 18: Ensure form inputs are visible */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] textarea {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
        border-radius: 6px !important;
    }
    
    /* Method 19: Fix any remaining visibility issues */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stText,
    section[data-testid="stSidebar"] .element-container,
    section[data-testid="stSidebar"] .row-widget {
        color: white !important;
    }
    
    /* Method 20: Final override for stubborn elements */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

def apply_emergency_sidebar_fix():
    """Emergency fix using JavaScript to force white text"""
    
    st.markdown("""
    <script>
    // JavaScript fallback to force white text
    function fixSidebarText() {
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (sidebar) {
            // Force background
            sidebar.style.background = 'linear-gradient(180deg, #1a365d 0%, #2d3748 50%, #1a202c 100%)';
            sidebar.style.borderRight = '2px solid #4a5568';
            
            // Force all text to white
            const allElements = sidebar.querySelectorAll('*');
            allElements.forEach(element => {
                element.style.color = 'white';
                element.style.setProperty('color', 'white', 'important');
            });
        }
    }
    
    // Run immediately and on DOM changes
    fixSidebarText();
    setTimeout(fixSidebarText, 100);
    setTimeout(fixSidebarText, 500);
    setTimeout(fixSidebarText, 1000);
    
    // Observer for dynamic content
    const observer = new MutationObserver(fixSidebarText);
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)

def fix_sidebar_nuclear_option():
    """Nuclear option - most aggressive fix possible"""
    
    # Apply CSS fix
    fix_sidebar_now()
    
    # Apply JavaScript fix
    apply_emergency_sidebar_fix()
    
    # Add inline styles to any sidebar content
    st.markdown("""
    <style>
    /* NUCLEAR OPTION - OVERRIDE EVERYTHING */
    * {
        --sidebar-bg: linear-gradient(180deg, #1a365d 0%, #2d3748 50%, #1a202c 100%);
        --sidebar-text: white;
    }
    
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] *,
    .css-1d391kg,
    .css-1d391kg *,
    .stSidebar,
    .stSidebar * {
        background: var(--sidebar-bg) !important;
        color: var(--sidebar-text) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Example usage with test
if __name__ == "__main__":
    st.set_page_config(
        page_title="ULTIMATE Sidebar Fix",
        page_icon="🚨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply the nuclear option
    fix_sidebar_nuclear_option()
    
    st.title("🚨 ULTIMATE Sidebar Visibility Fix")
    st.write("This is the most aggressive fix possible. If this doesn't work, nothing will!")
    
    with st.sidebar:
        st.title("🎯 Test Sidebar")
        st.markdown("### This text MUST be visible!")
        
        st.write("If you can read this clearly, the fix is working!")
        
        choice = st.radio(
            "Navigation Test:",
            ["🏠 Home", "📄 Resume", "🎯 Jobs", "⚙️ Settings"]
        )
        
        st.checkbox("Checkbox test")
        st.selectbox("Selectbox test", ["Option 1", "Option 2"])
        
        st.success("✅ Success message test")
        st.warning("⚠️ Warning message test")
        st.error("❌ Error message test")
        st.info("ℹ️ Info message test")
        
        if st.button("🔧 Test Button"):
            st.balloons()
    
    st.write(f"Selected: {choice}")
    
    st.markdown("""
    ## 🚨 Emergency Fix Applied!
    
    This fix uses **20 different methods** to ensure sidebar text visibility:
    
    1. ✅ Multiple CSS selector targeting
    2. ✅ JavaScript fallback
    3. ✅ Nuclear option overrides
    4. ✅ Dynamic content observation
    5. ✅ Inline style forcing
    
    **If the sidebar text is still not visible, please check:**
    - Browser cache (try Ctrl+F5)
    - Browser developer tools for CSS conflicts
    - Streamlit version compatibility
    """)