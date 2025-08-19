# Simple function to inject the quantum theme CSS
def set_quantum_theme():
    QuantumTheme.apply_global_styles()
"""Quantum UI Theme for JobSniper AI

Provides a futuristic, quantum-inspired design system with
glassmorphism, vibrant gradients, and a clean, professional look.
"""

import streamlit as st

class QuantumTheme:
    """Futuristic design system for JobSniper AI"""

    # Color Palette - Inspired by quantum phenomena
    COLORS = {
        'primary': '#00F2FE',  # Bright Cyan
        'secondary': '#A8EDEA', # Light Cyan
        'accent': '#FED6E3', # Pink
        'background': '#111827',  # Dark Blue
        'surface': 'rgba(31, 41, 55, 0.6)',  # Semi-transparent dark
        'surface_dark': 'rgba(17, 24, 39, 0.8)',
        'text_primary': '#FFFFFF',
        'text_secondary': '#9CA3AF',
        'text_muted': '#6B7280',
        'success': '#34D399',
        'warning': '#FBBF24',
        'error': '#F87171',
        'info': '#60A5FA',
        'gradient_primary': 'linear-gradient(135deg, #00F2FE 0%, #A8EDEA 100%)',
        'gradient_accent': 'linear-gradient(135deg, #FED6E3 0%, #A8EDEA 100%)',
    }

    # Typography
    FONTS = {
        'primary': '"Roboto", "Segoe UI", sans-serif',
        'secondary': '"Montserrat", "Helvetica Neue", sans-serif',
        'mono': '"Fira Code", monospace'
    }

    # Spacing
    SPACING = {
        'xs': '0.25rem',
        'sm': '0.5rem',
        'md': '1rem',
        'lg': '1.5rem',
        'xl': '2rem',
        'xxl': '3rem'
    }

    # Border Radius
    RADIUS = {
        'sm': '8px',
        'md': '12px',
        'lg': '16px',
        'xl': '24px',
        'full': '50%'
    }

    # Shadows
    SHADOWS = {
        'sm': '0 2px 4px rgba(0,0,0,0.1)',
        'md': '0 4px 8px rgba(0,0,0,0.15)',
        'lg': '0 10px 20px rgba(0,0,0,0.2)',
        'xl': '0 15px 30px rgba(0,0,0,0.25)'
    }

    @classmethod
    def apply_global_styles(cls):
        """Apply global CSS styles with a futuristic feel"""
        st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Roboto:wght@400;500;700&display=swap');
        
        .stApp {{
            font-family: {cls.FONTS['primary']};
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text_primary']};
        }}

        #MainMenu, footer, header {{
            visibility: hidden;
        }}

        .main .block-container {{
            padding-top: {cls.SPACING['xl']};
            padding-bottom: {cls.SPACING['xl']};
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: {cls.FONTS['secondary']};
            font-weight: 700;
            color: {cls.COLORS['primary']};
        }}

        .stButton > button {{
            background: {cls.COLORS['gradient_primary']};
            color: {cls.COLORS['background']};
            border: none;
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['sm']} {cls.SPACING['lg']};
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: {cls.SHADOWS['md']};
        }}

        .stButton > button:hover {{
            transform: translateY(-3px);
            box-shadow: {cls.SHADOWS['lg']};
        }}

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {{
            background-color: {cls.COLORS['surface']};
            color: {cls.COLORS['text_primary']};
            border: 1px solid {cls.COLORS['surface_dark']};
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['sm']} {cls.SPACING['md']};
            transition: all 0.3s ease;
        }}

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {{
            border-color: {cls.COLORS['primary']};
            box-shadow: 0 0 0 3px {cls.COLORS['primary']}33;
        }}

        .glass-card {{
            background: {cls.COLORS['surface']};
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: {cls.RADIUS['lg']};
            padding: {cls.SPACING['xl']};
            border: 1px solid {cls.COLORS['surface_dark']};
            box-shadow: {cls.SHADOWS['lg']};
            transition: all 0.3s ease;
        }}

        .glass-card:hover {{
            transform: scale(1.02);
            box-shadow: {cls.SHADOWS['xl']};
        }}
        </style>
        """, unsafe_allow_html=True)

    @classmethod
    def create_glass_card(cls, content: str, title: str = ""):
        """Create a glassmorphism card"""
        st.markdown(f"""
        <div class="glass-card">
            {f'<h3>{title}</h3>' if title else ''}
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)
