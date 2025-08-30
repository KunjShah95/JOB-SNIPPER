# Simple alias for global style injection
def apply_global_styles():
    QuantumDesignSystem.inject_global_styles()
"""
🎨 JobSniper AI - Revolutionary Design System
===============================================

Ultra-modern design system with glassmorphism, neumorphism, and cutting-edge UI patterns.
Built for 2025+ with advanced CSS, animations, and responsive design.
"""

import streamlit as st
from typing import Dict, List, Optional, Union
import json
from .ui_constants import UIConstants


class QuantumDesignSystem:
    """Quantum Design System for JobSniper AI

    Revolutionary design system with glassmorphism, neumorphism, and quantum aesthetics.
    Now uses centralized UI constants for consistency and maintainability.
    """

    # 🎨 Color Palette (Now using UI Constants)
    COLORS = {
        # Quantum Theme
        'quantum_blue': UIConstants.DESIGN['colors']['primary'],
        'quantum_purple': UIConstants.DESIGN['colors']['secondary'],
        'quantum_cyan': '#06B6D4',
        'quantum_emerald': UIConstants.DESIGN['colors']['success'],
        'quantum_amber': UIConstants.DESIGN['colors']['warning'],
        'quantum_rose': UIConstants.DESIGN['colors']['error'],
        
        # Glass Effects
        'glass_white': 'rgba(255, 255, 255, 0.15)',
        'glass_dark': 'rgba(0, 0, 0, 0.1)',
        'glass_blue': 'rgba(74, 144, 226, 0.1)',
        'glass_purple': 'rgba(118, 75, 162, 0.1)',
        
        # Gradients
        'gradient_aurora': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'gradient_ocean': 'linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%)',
        'gradient_sunset': 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
        
        # Semantic Colors
        'success': UIConstants.DESIGN['colors']['success'],
        'warning': UIConstants.DESIGN['colors']['warning'],
        'error': UIConstants.DESIGN['colors']['error'],
        'info': UIConstants.DESIGN['colors']['info'],
        
        # Neutral Palette
        'white': '#FFFFFF',
        'gray_50': '#F9FAFB',
        'gray_100': '#F3F4F6',
        'gray_200': '#E5E7EB',
        'gray_300': '#D1D5DB',
        'gray_400': '#9CA3AF',
        'gray_500': '#6B7280',
        'gray_600': '#4B5563',
        'gray_700': '#374151',
        'gray_800': '#1F2937',
        'gray_900': '#111827',
        'black': '#000000',
    }
    
    # 🔤 Typography System (Now using UI Constants)
    TYPOGRAPHY = {
        'font_primary': UIConstants.DESIGN['typography']['primary_font'],
        'font_display': UIConstants.DESIGN['typography']['display_font'],
        'font_mono': UIConstants.DESIGN['typography']['mono_font'],
        
        'text_xs': '0.75rem',    # 12px
        'text_sm': '0.875rem',   # 14px
        'text_base': '1rem',     # 16px
        'text_lg': '1.125rem',   # 18px
        'text_xl': '1.25rem',    # 20px
        'text_2xl': '1.5rem',    # 24px
        'text_3xl': '1.875rem',  # 30px
        'text_4xl': '2.25rem',   # 36px
        'text_5xl': '3rem',      # 48px
        'text_6xl': '3.75rem',   # 60px
    }
    
    # 📏 Spacing System
    SPACING = {
        'px': '1px',
        '0': '0',
        '1': '0.25rem',   # 4px
        '2': '0.5rem',    # 8px
        '3': '0.75rem',   # 12px
        '4': '1rem',      # 16px
        '5': '1.25rem',   # 20px
        '6': '1.5rem',    # 24px
        '8': '2rem',      # 32px
        '10': '2.5rem',   # 40px
        '12': '3rem',     # 48px
        '16': '4rem',     # 64px
        '20': '5rem',     # 80px
        '24': '6rem',     # 96px
        '32': '8rem',     # 128px
    }
    
    # 🔄 Border Radius
    RADIUS = {
        'none': '0',
        'sm': '0.125rem',   # 2px
        'base': '0.25rem',  # 4px
        'md': '0.375rem',   # 6px
        'lg': '0.5rem',     # 8px
        'xl': '0.75rem',    # 12px
        '2xl': '1rem',      # 16px
        '3xl': '1.5rem',    # 24px
        'full': '9999px',
    }
    
    # 🌟 Shadows & Effects
    SHADOWS = {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'base': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
        'glow': '0 0 20px rgba(99, 102, 241, 0.3)',
        'glow_lg': '0 0 40px rgba(99, 102, 241, 0.4)',
    }

    @classmethod
    def inject_global_styles(cls):
        """Inject revolutionary CSS styles"""
        
        st.markdown(f"""
        <style>
        /* 🌐 Import Modern Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=Poppins:wght@100;200;300;400;500;600;700;800;900&family=JetBrains+Mono:wght@100;200;300;400;500;600;700;800&display=swap');
        
        /* 🎯 CSS Variables */
        :root {{
            --quantum-blue: {cls.COLORS['quantum_blue']};
            --quantum-purple: {cls.COLORS['quantum_purple']};
            --quantum-cyan: {cls.COLORS['quantum_cyan']};
            --quantum-emerald: {cls.COLORS['quantum_emerald']};
            --quantum-amber: {cls.COLORS['quantum_amber']};
            --quantum-rose: {cls.COLORS['quantum_rose']};
            
            --glass-white: {cls.COLORS['glass_white']};
            --glass-dark: {cls.COLORS['glass_dark']};
            --glass-blue: {cls.COLORS['glass_blue']};
            --glass-purple: {cls.COLORS['glass_purple']};
            
            --gradient-aurora: {cls.COLORS['gradient_aurora']};
            --gradient-ocean: {cls.COLORS['gradient_ocean']};
            --gradient-sunset: {cls.COLORS['gradient_sunset']};
            
            --shadow-glow: {cls.SHADOWS['glow']};
            --shadow-glow-lg: {cls.SHADOWS['glow_lg']};
        }}
        
        /* 🌍 Global Reset & Base */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html {{
            scroll-behavior: smooth;
            font-size: 16px;
        }}
        
        body {{
            font-family: {cls.TYPOGRAPHY['font_primary']};
            background: {UIConstants.DESIGN['colors']['background']};
            background-attachment: fixed;
            color: {cls.COLORS['gray_800']};
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        /* 🎨 Streamlit App Container */
        .stApp {{
            background: transparent;
            font-family: {cls.TYPOGRAPHY['font_primary']};
        }}
        
        /* 🚫 Hide Streamlit Branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        .stDeployButton {{visibility: hidden;}}
        
        /* 🎯 Main Content Container */
        .main .block-container {{
            padding: {cls.SPACING['6']} {cls.SPACING['4']};
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        /* 🌟 Glassmorphism Card */
        .quantum-glass {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: {cls.RADIUS['2xl']};
            box-shadow: {cls.SHADOWS['xl']};
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .quantum-glass:hover {{
            transform: translateY(-4px);
            box-shadow: {cls.SHADOWS['2xl']};
            border-color: rgba(255, 255, 255, 0.3);
        }}
        
        /* 🎨 Neumorphism Card */
        .quantum-neuro {{
            background: linear-gradient(145deg, #f0f0f0, #cacaca);
            border-radius: {cls.RADIUS['2xl']};
            box-shadow: 
                20px 20px 60px #bebebe,
                -20px -20px 60px #ffffff;
            transition: all 0.3s ease;
        }}
        
        .quantum-neuro:hover {{
            box-shadow: 
                inset 20px 20px 60px #bebebe,
                inset -20px -20px 60px #ffffff;
        }}
        
        /* 🌈 Gradient Cards */
        .quantum-gradient {{
            background: var(--gradient-aurora);
            border-radius: {cls.RADIUS['2xl']};
            padding: {cls.SPACING['6']};
            color: white;
            box-shadow: var(--shadow-glow-lg);
            transition: all 0.3s ease;
        }}
        
        .quantum-gradient:hover {{
            transform: scale(1.02);
            box-shadow: 0 0 60px rgba(99, 102, 241, 0.5);
        }}
        
        /* 📱 Responsive Grid */
        .quantum-grid {{
            display: grid;
            gap: {cls.SPACING['6']};
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }}
        
        .quantum-grid-2 {{
            display: grid;
            gap: {cls.SPACING['6']};
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        }}
        
        .quantum-grid-3 {{
            display: grid;
            gap: {cls.SPACING['6']};
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }}
        
        /* 🎯 Typography */
        .quantum-title {{
            font-family: {cls.TYPOGRAPHY['font_display']};
            font-size: {cls.TYPOGRAPHY['text_5xl']};
            font-weight: 800;
            background: var(--gradient-aurora);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: {cls.SPACING['6']};
            text-align: center;
        }}
        
        .quantum-subtitle {{
            font-family: {cls.TYPOGRAPHY['font_display']};
            font-size: {cls.TYPOGRAPHY['text_2xl']};
            font-weight: 600;
            color: {cls.COLORS['gray_700']};
            text-align: center;
            margin-bottom: {cls.SPACING['8']};
        }}
        
        .quantum-heading {{
            font-family: {cls.TYPOGRAPHY['font_display']};
            font-size: {cls.TYPOGRAPHY['text_3xl']};
            font-weight: 700;
            color: {cls.COLORS['gray_800']};
            margin-bottom: {cls.SPACING['4']};
        }}
        
        /* 🔘 Modern Buttons */
        .quantum-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: {cls.SPACING['3']} {cls.SPACING['6']};
            font-family: {cls.TYPOGRAPHY['font_primary']};
            font-weight: 600;
            font-size: {cls.TYPOGRAPHY['text_base']};
            border: none;
            border-radius: {cls.RADIUS['xl']};
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-decoration: none;
            position: relative;
            overflow: hidden;
        }}
        
        .quantum-btn-primary {{
            background: var(--gradient-ocean);
            color: white;
            box-shadow: var(--shadow-glow);
        }}
        
        .quantum-btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-glow-lg);
        }}
        
        .quantum-btn-secondary {{
            background: var(--glass-white);
            backdrop-filter: blur(10px);
            color: {cls.COLORS['gray_800']};
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        .quantum-btn-secondary:hover {{
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }}
        
        /* 📊 Metrics Cards */
        .quantum-metric {{
            background: var(--glass-white);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: {cls.RADIUS['2xl']};
            padding: {cls.SPACING['6']};
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .quantum-metric:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-glow);
        }}
        
        .quantum-metric-value {{
            font-size: {cls.TYPOGRAPHY['text_4xl']};
            font-weight: 800;
            background: var(--gradient-ocean);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: {cls.SPACING['2']};
        }}
        
        .quantum-metric-label {{
            font-size: {cls.TYPOGRAPHY['text_sm']};
            font-weight: 600;
            color: {cls.COLORS['gray_600']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        /* 🎨 Status Indicators */
        .quantum-status {{
            display: inline-flex;
            align-items: center;
            padding: {cls.SPACING['2']} {cls.SPACING['4']};
            border-radius: {cls.RADIUS['full']};
            font-size: {cls.TYPOGRAPHY['text_sm']};
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .quantum-status-success {{
            background: rgba(16, 185, 129, 0.1);
            color: {cls.COLORS['success']};
            border: 1px solid rgba(16, 185, 129, 0.2);
        }}
        
        .quantum-status-warning {{
            background: rgba(245, 158, 11, 0.1);
            color: {cls.COLORS['warning']};
            border: 1px solid rgba(245, 158, 11, 0.2);
        }}
        
        .quantum-status-error {{
            background: rgba(239, 68, 68, 0.1);
            color: {cls.COLORS['error']};
            border: 1px solid rgba(239, 68, 68, 0.2);
        }}
        
        .quantum-status-info {{
            background: rgba(59, 130, 246, 0.1);
            color: {cls.COLORS['info']};
            border: 1px solid rgba(59, 130, 246, 0.2);
        }}
        
        /* 🌊 Animated Background */
        .quantum-bg-animated {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }}
        
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        /* 💫 Loading Animations */
        .quantum-loading {{
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 3px solid rgba(99, 102, 241, 0.3);
            border-radius: 50%;
            border-top-color: var(--quantum-purple);
            animation: spin 1s ease-in-out infinite;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        .quantum-pulse {{
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        
        /* 📱 Responsive Design */
        @media (max-width: 768px) {{
            .main .block-container {{
                padding: {cls.SPACING['4']} {cls.SPACING['2']};
            }}
            
            .quantum-title {{
                font-size: {cls.TYPOGRAPHY['text_4xl']};
            }}
            
            .quantum-subtitle {{
                font-size: {cls.TYPOGRAPHY['text_xl']};
            }}
            
            .quantum-grid,
            .quantum-grid-2,
            .quantum-grid-3 {{
                grid-template-columns: 1fr;
                gap: {cls.SPACING['4']};
            }}
        }}
        
        /* 🎯 Streamlit Component Overrides */
        .stButton > button {{
            background: var(--gradient-ocean) !important;
            color: white !important;
            border: none !important;
            border-radius: {cls.RADIUS['xl']} !important;
            padding: {cls.SPACING['3']} {cls.SPACING['6']} !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: var(--shadow-glow) !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-glow-lg) !important;
        }}
        
        .stSelectbox > div > div {{
            background: var(--glass-white) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: {cls.RADIUS['xl']} !important;
        }}
        
        .stTextInput > div > div > input {{
            background: var(--glass-white) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: {cls.RADIUS['xl']} !important;
            color: {cls.COLORS['gray_800']} !important;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: var(--quantum-purple) !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        }}
        
        /* 📊 Sidebar Styling */
        .css-1d391kg {{
            background: var(--glass-white) !important;
            backdrop-filter: blur(20px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
        }}
        
        /* 🎨 File Uploader */
        .stFileUploader {{
            background: var(--glass-white) !important;
            backdrop-filter: blur(20px) !important;
            border: 2px dashed rgba(255, 255, 255, 0.3) !important;
            border-radius: {cls.RADIUS['2xl']} !important;
            transition: all 0.3s ease !important;
        }}
        
        .stFileUploader:hover {{
            border-color: var(--quantum-purple) !important;
            background: rgba(255, 255, 255, 0.15) !important;
        }}
        
        /* 📈 Progress Bars */
        .stProgress > div > div > div > div {{
            background: var(--gradient-ocean) !important;
            border-radius: {cls.RADIUS['full']} !important;
        }}
        
        /* 🎯 Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: {cls.SPACING['4']} !important;
            background: var(--glass-white) !important;
            backdrop-filter: blur(20px) !important;
            border-radius: {cls.RADIUS['2xl']} !important;
            padding: {cls.SPACING['2']} !important;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: transparent !important;
            border-radius: {cls.RADIUS['xl']} !important;
            padding: {cls.SPACING['3']} {cls.SPACING['6']} !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: var(--gradient-ocean) !important;
            color: white !important;
            box-shadow: var(--shadow-glow) !important;
        }}
        
        /* 🌟 Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: {cls.RADIUS['full']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--gradient-ocean);
            border-radius: {cls.RADIUS['full']};
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--gradient-sunset);
        }}
        </style>
        """, unsafe_allow_html=True)

    @classmethod
    def create_hero_section(cls, title: str, subtitle: str, icon: str = "🎯") -> None:
        """Create an epic hero section"""
        st.markdown(f"""
        <div class="quantum-bg-animated"></div>
        <div style="text-align: center; padding: {cls.SPACING['16']} 0; position: relative; z-index: 1;">
            <div style="font-size: 5rem; margin-bottom: {cls.SPACING['6']}; animation: pulse 2s infinite;">{icon}</div>
            <h1 class="quantum-title">{title}</h1>
            <p class="quantum-subtitle">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)

    @classmethod
    def create_glass_card(cls, content: str, title: str = "", padding: str = None) -> None:
        """Create a glassmorphism card"""
        padding = padding or cls.SPACING['6']
        title_html = f'<h3 class="quantum-heading">{title}</h3>' if title else ''
        
        st.markdown(f"""
        <div class="quantum-glass" style="padding: {padding}; margin-bottom: {cls.SPACING['6']};">
            {title_html}
            {content}
        </div>
        """, unsafe_allow_html=True)

    @classmethod
    def create_metric_card(cls, value: str, label: str, icon: str = "📊") -> None:
        """Create a modern metric card"""
        st.markdown(f"""
        <div class="quantum-metric">
            <div style="font-size: 2rem; margin-bottom: {cls.SPACING['2']};">{icon}</div>
            <div class="quantum-metric-value">{value}</div>
            <div class="quantum-metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    @classmethod
    def create_status_badge(cls, text: str, status: str = "info") -> str:
        """Create a status badge"""
        return f'<span class="quantum-status quantum-status-{status}">{text}</span>'

    @classmethod
    def create_gradient_card(cls, content: str, title: str = "") -> None:
        """Create a gradient card"""
        title_html = f'<h3 style="margin: 0 0 {cls.SPACING["4"]} 0; color: white;">{title}</h3>' if title else ''
        
        st.markdown(f"""
        <div class="quantum-gradient">
            {title_html}
            {content}
        </div>
        """, unsafe_allow_html=True)

    @classmethod
    def create_loading_spinner(cls, text: str = "Loading...") -> None:
        """Create a modern loading spinner"""
        st.markdown(f"""
        <div style="text-align: center; padding: {cls.SPACING['8']};">
            <div class="quantum-loading"></div>
            <p style="margin-top: {cls.SPACING['4']}; color: {cls.COLORS['gray_600']}; font-weight: 500;">{text}</p>
        </div>
        """, unsafe_allow_html=True)


# Convenience functions
def apply_quantum_design():
    """Apply the quantum design system"""
    QuantumDesignSystem.inject_global_styles()

def create_hero(title: str, subtitle: str, icon: str = "🎯"):
    """Create hero section"""
    QuantumDesignSystem.create_hero_section(title, subtitle, icon)

def glass_card(content: str, title: str = ""):
    """Create glass card"""
    QuantumDesignSystem.create_glass_card(content, title)

def metric_card(value: str, label: str, icon: str = "📊"):
    """Create metric card"""
    QuantumDesignSystem.create_metric_card(value, label, icon)

def status_badge(text: str, status: str = "info") -> str:
    """Create status badge"""
    return QuantumDesignSystem.create_status_badge(text, status)

def gradient_card(content: str, title: str = ""):
    """Create gradient card"""
    QuantumDesignSystem.create_gradient_card(content, title)

def loading_spinner(text: str = "Loading..."):
    """Create loading spinner"""
    QuantumDesignSystem.create_loading_spinner(text)