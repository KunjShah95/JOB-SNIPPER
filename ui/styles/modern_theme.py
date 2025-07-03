"""Modern UI Theme for JobSniper AI

Provides a comprehensive, modern design system with consistent
styling, responsive layouts, and professional appearance.
"""

import streamlit as st
from typing import Dict, Any, Optional


class ModernTheme:
    """Modern design system for JobSniper AI"""
    
    # Color Palette
    COLORS = {
        # Primary Colors
        'primary': '#2E86AB',
        'primary_light': '#A23B72',
        'primary_dark': '#F18F01',
        'secondary': '#C73E1D',
        
        # Neutral Colors
        'background': '#FFFFFF',
        'surface': '#F8F9FA',
        'surface_dark': '#E9ECEF',
        'text_primary': '#212529',
        'text_secondary': '#6C757D',
        'text_muted': '#ADB5BD',
        
        # Status Colors
        'success': '#28A745',
        'warning': '#FFC107',
        'error': '#DC3545',
        'info': '#17A2B8',
        
        # Gradient Colors
        'gradient_primary': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'gradient_success': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'gradient_warning': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'gradient_info': 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    }
    
    # Typography
    FONTS = {
        'primary': '"Inter", "Segoe UI", "Roboto", sans-serif',
        'secondary': '"Poppins", "Helvetica Neue", sans-serif',
        'mono': '"JetBrains Mono", "Fira Code", monospace'
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
        'sm': '4px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
        'full': '50%'
    }
    
    # Shadows
    SHADOWS = {
        'sm': '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)',
        'md': '0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23)',
        'lg': '0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23)',
        'xl': '0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22)'
    }

    @classmethod
    def apply_global_styles(cls):
        """Apply global CSS styles to the Streamlit app"""
        
        st.markdown(f"""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .stApp {{
            font-family: {cls.FONTS['primary']};
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text_primary']};
        }}
        
        /* Hide Streamlit Branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
        /* ULTIMATE SIDEBAR VISIBILITY FIX */
        /* Target ALL possible sidebar container classes */
        .css-1d391kg, .css-1lcbmhc, .css-17eq0hr, .css-1y4p8pa, .css-16txtl3,
        .st-emotion-cache-16txtl3, .st-emotion-cache-1y4p8pa, .st-emotion-cache-1lcbmhc,
        .st-emotion-cache-1d391kg, .st-emotion-cache-17eq0hr,
        section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div,
        .stSidebar, .sidebar, [data-testid="stSidebar"],
        .css-1aumxhk, .css-1cypcdb, .css-1outpf7, .css-1v0mbdj {
            background: linear-gradient(180deg, #1a365d 0%, #2d3748 50%, #1a202c 100%) !important;
            border-right: 2px solid #4a5568 !important;
            color: white !important;
        }
        
        /* Force ALL text in sidebar to be white - NUCLEAR OPTION */
        section[data-testid="stSidebar"] * {
            color: white !important;
        }
        
        /* Target specific text elements */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stMarkdown {
            color: white !important;
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Form elements in sidebar */
        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] .stCheckbox label,
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stTextInput label {
            color: white !important;
            font-weight: 500 !important;
        }
        
        /* Status messages in sidebar */
        section[data-testid="stSidebar"] .stSuccess {
            background-color: rgba(72, 187, 120, 0.2) !important;
            border: 2px solid #48bb78 !important;
            color: #c6f6d5 !important;
            border-radius: 8px !important;
        }
        
        section[data-testid="stSidebar"] .stWarning {
            background-color: rgba(237, 137, 54, 0.2) !important;
            border: 2px solid #ed8936 !important;
            color: #fbd38d !important;
            border-radius: 8px !important;
        }
        
        section[data-testid="stSidebar"] .stError {
            background-color: rgba(245, 101, 101, 0.2) !important;
            border: 2px solid #f56565 !important;
            color: #fed7d7 !important;
            border-radius: 8px !important;
        }
        
        section[data-testid="stSidebar"] .stInfo {
            background-color: rgba(66, 153, 225, 0.2) !important;
            border: 2px solid #4299e1 !important;
            color: #bee3f8 !important;
            border-radius: 8px !important;
        }
        /* Main Content Area */
        .main .block-container {
            padding-top: {cls.SPACING['lg']};
            padding-bottom: {cls.SPACING['lg']};
            max-width: 1200px;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            font-family: {cls.FONTS['secondary']};
            font-weight: 600;
            color: {cls.COLORS['text_primary']};
            margin-bottom: {cls.SPACING['md']};
        }
        
        h1 {
            font-size: 2.5rem;
            line-height: 1.2;
        }
        
        h2 {
            font-size: 2rem;
            line-height: 1.3;
        }
        
        h3 {
            font-size: 1.5rem;
            line-height: 1.4;
        }
        
        /* Buttons */
        .stButton > button {
            background: {cls.COLORS['primary']};
            color: white;
            border: none;
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['sm']} {cls.SPACING['lg']};
            font-weight: 500;
            font-family: {cls.FONTS['primary']};
            transition: all 0.3s ease;
            box-shadow: {cls.SHADOWS['sm']};
        }
        
        .stButton > button:hover {
            background: {cls.COLORS['primary_dark']};
            box-shadow: {cls.SHADOWS['md']};
            transform: translateY(-2px);
        }
        /* Expander */
        .streamlit-expanderHeader {{
            background: {cls.COLORS['surface']};
            border-radius: {cls.RADIUS['md']};
            border: 1px solid {cls.COLORS['surface_dark']};
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: {cls.SPACING['md']};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: {cls.COLORS['surface']};
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['sm']} {cls.SPACING['lg']};
            border: 1px solid {cls.COLORS['surface_dark']};
        }}
        
        .stTabs [aria-selected="true"] {{
            background: {cls.COLORS['primary']};
            color: white;
        }}
        
        /* Alerts */
        .stAlert {{
            border-radius: {cls.RADIUS['md']};
            border: none;
            box-shadow: {cls.SHADOWS['sm']};
        }}
        
        /* Custom Classes */
        .modern-card {{
            background: white;
            padding: {cls.SPACING['xl']};
            border-radius: {cls.RADIUS['lg']};
            box-shadow: {cls.SHADOWS['md']};
            margin-bottom: {cls.SPACING['lg']};
            border: 1px solid {cls.COLORS['surface_dark']};
            transition: all 0.3s ease;
        }}
        
        .modern-card:hover {{
            box-shadow: {cls.SHADOWS['lg']};
            transform: translateY(-4px);
        }}
        
        .gradient-header {{
            background: {cls.COLORS['gradient_primary']};
            color: white;
            padding: {cls.SPACING['xl']};
            border-radius: {cls.RADIUS['lg']};
            text-align: center;
            margin-bottom: {cls.SPACING['xl']};
            box-shadow: {cls.SHADOWS['md']};
        }}
        
        .status-badge {{
            display: inline-block;
            padding: {cls.SPACING['xs']} {cls.SPACING['sm']};
            border-radius: {cls.RADIUS['full']};
            font-size: 0.875rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .status-success {{
            background: {cls.COLORS['success']};
            color: white;
        }}
        
        .status-warning {{
            background: {cls.COLORS['warning']};
            color: white;
        }}
        
        .status-error {{
            background: {cls.COLORS['error']};
            color: white;
        }}
        
        .status-info {{
            background: {cls.COLORS['info']};
            color: white;
        }}
        
        /* Loading Animation */
        .loading-spinner {{
            border: 4px solid {cls.COLORS['surface_dark']};
            border-top: 4px solid {cls.COLORS['primary']};
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .main .block-container {{
                padding-left: {cls.SPACING['md']};
                padding-right: {cls.SPACING['md']};
            }}
            
            h1 {{
                font-size: 2rem;
            }}
            
            h2 {{
                font-size: 1.5rem;
            }}
            
            .modern-card {{
                padding: {cls.SPACING['lg']};
            }}
        }}
        </style>
        """, unsafe_allow_html=True)

    @classmethod
    def create_header(cls, title: str, subtitle: str = "", icon: str = "🎯") -> None:
        """Create a modern gradient header"""
        st.markdown(f"""
        <div class="gradient-header">
            <h1>{icon} {title}</h1>
            {f'<p style="font-size: 1.2rem; margin: 0; opacity: 0.9;">{subtitle}</p>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)

    @classmethod
    def create_card(cls, content: str, title: str = "", hover: bool = True) -> None:
        """Create a modern card component"""
        hover_class = "modern-card" if hover else "modern-card" 
        st.markdown(f"""
        <div class="{hover_class}">
            {f'<h3 style="margin-top: 0;">{title}</h3>' if title else ''}
            {content}
        </div>
        """, unsafe_allow_html=True)

    @classmethod
    def create_status_badge(cls, text: str, status: str = "info") -> str:
        """Create a status badge"""
        return f'<span class="status-badge status-{status}">{text}</span>'

    @classmethod
    def create_metric_card(cls, title: str, value: str, delta: str = "", 
                          delta_color: str = "success") -> None:
        """Create a metric card"""
        delta_html = f'<p style="color: {cls.COLORS[delta_color]}; margin: 0; font-size: 0.9rem;">{delta}</p>' if delta else ''
        
        st.markdown(f"""
        <div class="metric-container">
            <h4 style="margin: 0 0 {cls.SPACING['sm']} 0; color: {cls.COLORS['text_secondary']};">{title}</h4>
            <h2 style="margin: 0; color: {cls.COLORS['primary']};">{value}</h2>
            {delta_html}
        </div>
        """, unsafe_allow_html=True)

    @classmethod
    def create_loading_spinner(cls, text: str = "Loading...") -> None:
        """Create a loading spinner"""
        st.markdown(f"""
        <div style="text-align: center; padding: {cls.SPACING['xl']};">
            <div class="loading-spinner"></div>
            <p style="margin-top: {cls.SPACING['md']}; color: {cls.COLORS['text_secondary']};">{text}</p>
        </div>
        """, unsafe_allow_html=True)

    @classmethod
    def create_feature_grid(cls, features: list) -> None:
        """Create a responsive feature grid"""
        cols = st.columns(len(features))
        for i, feature in enumerate(features):
            with cols[i]:
                cls.create_card(
                    content=f"""
                    <div style="text-align: center;">
                        <div style="font-size: 3rem; margin-bottom: {cls.SPACING['md']};">{feature['icon']}</div>
                        <h4>{feature['title']}</h4>
                        <p style="color: {cls.COLORS['text_secondary']};">{feature['description']}</p>
                    </div>
                    """,
                    hover=True
                )

    @classmethod
    def create_progress_card(cls, title: str, progress: float, 
                           color: str = "primary") -> None:
        """Create a progress card"""
        st.markdown(f"""
        <div class="modern-card">
            <h4 style="margin-top: 0;">{title}</h4>
            <div style="background: {cls.COLORS['surface']}; border-radius: {cls.RADIUS['full']}; height: 8px; margin: {cls.SPACING['md']} 0;">
                <div style="background: {cls.COLORS[color]}; height: 100%; width: {progress}%; border-radius: {cls.RADIUS['full']}; transition: width 0.3s ease;"></div>
            </div>
            <p style="margin: 0; text-align: right; color: {cls.COLORS['text_secondary']};">{progress:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)


# Convenience functions for easy use
def apply_modern_theme():
    """Apply the modern theme to the current page"""
    ModernTheme.apply_global_styles()

def create_header(title: str, subtitle: str = "", icon: str = "🎯"):
    """Create a modern header"""
    ModernTheme.create_header(title, subtitle, icon)

def create_card(content: str, title: str = ""):
    """Create a modern card"""
    ModernTheme.create_card(content, title)

def create_metric_card(title: str, value: str, delta: str = ""):
    """Create a metric card"""
    ModernTheme.create_metric_card(title, value, delta)

def create_loading_spinner(text: str = "Loading..."):
    """Create a loading spinner"""
    ModernTheme.create_loading_spinner(text)

def create_feature_grid(features: list):
    """Create a feature grid"""
    ModernTheme.create_feature_grid(features)