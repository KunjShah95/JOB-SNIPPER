# Simple function to inject the modern theme CSS
import streamlit as st
def set_modern_theme():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

"""
Modern UI Theme for JobSniper AI
Provides a comprehensive, modern design system with consistent styling and professional appearance.
"""

PRIMARY_COLOR = "#2D6A4F"  # Deep green
SECONDARY_COLOR = "#40916C"  # Lighter green
ACCENT_COLOR = "#FFD166"  # Gold
BACKGROUND_COLOR = "#F8F9FA"  # Light gray
TEXT_COLOR = "#22223B"  # Dark blue-gray
SIDEBAR_BG = "#FFFFFF"
SIDEBAR_TEXT = "#22223B"
ERROR_COLOR = "#EF476F"
SUCCESS_COLOR = "#06D6A0"

FONT = "'Inter', 'Segoe UI', 'Arial', sans-serif"

CUSTOM_CSS = f"""
<style>
body, .stApp {{
    background-color: {BACKGROUND_COLOR} !important;
    color: {TEXT_COLOR} !important;
    font-family: {FONT} !important;
}}

.stSidebar {{
    background-color: {SIDEBAR_BG} !important;
    color: {SIDEBAR_TEXT} !important;
}}

.stButton>button {{
    background-color: {PRIMARY_COLOR} !important;
    color: white !important;
    border-radius: 6px;
    border: none;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
    transition: background 0.2s;
}}
.stButton>button:hover {{
    background-color: {SECONDARY_COLOR} !important;
}}

.stTabs [data-baseweb="tab"] {{
    font-weight: 600;
    color: {PRIMARY_COLOR};
}}

.stAlert {{
    border-radius: 6px;
}}

h1, h2, h3, h4, h5, h6 {{
    color: {PRIMARY_COLOR};
    font-family: {FONT};
    font-weight: 700;
}}

.stTextInput>div>input {{
    border-radius: 6px;
    border: 1px solid #ccc;
    padding: 0.5rem;
}}

.main .block-container {{
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}}
</style>
"""


import streamlit as st


class ModernTheme:
    """Modern UI Theme class with comprehensive styling system"""

    # Color palette
    COLORS = {
        'primary': PRIMARY_COLOR,
        'secondary': SECONDARY_COLOR,
        'accent': ACCENT_COLOR,
        'background': BACKGROUND_COLOR,
        'text': TEXT_COLOR,
        'text_secondary': '#6C757D',
        'surface': '#FFFFFF',
        'surface_dark': '#E9ECEF',
        'error': ERROR_COLOR,
        'success': SUCCESS_COLOR,
        'warning': '#F77F00',
        'info': '#0077B6',
        'gradient_primary': f'linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%)',
    }

    # Spacing system
    SPACING = {
        'xs': '0.25rem',
        'sm': '0.5rem',
        'md': '1rem',
        'lg': '1.5rem',
        'xl': '2rem',
        'xxl': '3rem',
    }

    # Border radius
    RADIUS = {
        'sm': '4px',
        'md': '6px',
        'lg': '8px',
        'xl': '12px',
        'full': '50px',
    }

    # Shadows
    SHADOWS = {
        'sm': '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)',
        'md': '0 3px 6px rgba(0,0,0,0.15), 0 2px 4px rgba(0,0,0,0.12)',
        'lg': '0 10px 20px rgba(0,0,0,0.15), 0 3px 6px rgba(0,0,0,0.10)',
        'xl': '0 15px 25px rgba(0,0,0,0.15), 0 5px 10px rgba(0,0,0,0.05)',
    }

    @classmethod
    def apply_global_styles(cls) -> None:
        """Apply comprehensive global styles"""
        st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        .main .block-container {{
            padding-top: {cls.SPACING['lg']};
            padding-bottom: {cls.SPACING['lg']};
            max-width: 1200px;
        }}

        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: {cls.COLORS['surface_dark']};
            border-radius: {cls.RADIUS['sm']};
        }}

        ::-webkit-scrollbar-thumb {{
            background: {cls.COLORS['primary']};
            border-radius: {cls.RADIUS['sm']};
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: {cls.COLORS['secondary']};
        }}

        /* Enhanced button styles */
        .stButton > button {{
            background: {cls.COLORS['gradient_primary']};
            color: white;
            border: none;
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['sm']} {cls.SPACING['lg']};
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            transition: all 0.3s ease;
            box-shadow: {cls.SHADOWS['sm']};
        }}

        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: {cls.SHADOWS['md']};
        }}

        /* Enhanced selectbox */
        .stSelectbox > div > div {{
            border-radius: {cls.RADIUS['md']};
            border: 1px solid {cls.COLORS['surface_dark']};
            box-shadow: {cls.SHADOWS['sm']};
        }}

        /* Enhanced text input */
        .stTextInput > div > div > input {{
            border-radius: {cls.RADIUS['md']};
            border: 1px solid {cls.COLORS['surface_dark']};
            padding: {cls.SPACING['sm']};
            font-family: 'Inter', sans-serif;
        }}

        /* Enhanced text area */
        .stTextArea > div > div > textarea {{
            border-radius: {cls.RADIUS['md']};
            border: 1px solid {cls.COLORS['surface_dark']};
            font-family: 'Inter', sans-serif;
        }}

        /* Enhanced metrics */
        .metric-container {{
            background: {cls.COLORS['surface']};
            padding: {cls.SPACING['lg']};
            border-radius: {cls.RADIUS['lg']};
            box-shadow: {cls.SHADOWS['sm']};
            border-left: 4px solid {cls.COLORS['primary']};
        }}

        /* Enhanced sidebar */
        .css-1d391kg {{
            background: {cls.COLORS['surface']};
            border-right: 1px solid {cls.COLORS['surface_dark']};
        }}

        /* Enhanced tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: {cls.SPACING['sm']};
        }}

        .stTabs [data-baseweb="tab"] {{
            background: {cls.COLORS['surface']};
            border-radius: {cls.RADIUS['md']} {cls.RADIUS['md']} 0 0;
            padding: {cls.SPACING['sm']} {cls.SPACING['lg']};
            font-weight: 600;
            border: 1px solid {cls.COLORS['surface_dark']};
            border-bottom: none;
        }}

        .stTabs [aria-selected="true"] {{
            background: {cls.COLORS['primary']};
            color: white !important;
        }}
        </style>
        """, unsafe_allow_html=True)

    @classmethod
    def create_card(cls, content: str, title: str = None, color: str = 'surface') -> str:
        """Create a styled card component"""
        title_html = f"<h3 style='margin-top: 0; color: {cls.COLORS['primary']};'>{title}</h3>" if title else ""

        return f"""
        <div style='
            background: {cls.COLORS[color]};
            padding: {cls.SPACING['lg']};
            border-radius: {cls.RADIUS['lg']};
            box-shadow: {cls.SHADOWS['sm']};
            margin: {cls.SPACING['md']} 0;
            border-left: 4px solid {cls.COLORS['primary']};
        '>
            {title_html}
            {content}
        </div>
        """

    @classmethod
    def create_metric_card(cls, title: str, value: str, delta: str = None, delta_color: str = 'success') -> str:
        """Create a styled metric card"""
        delta_html = ""
        if delta:
            delta_html = f"""
            <div style='
                color: {cls.COLORS[delta_color]};
                font-size: 0.9rem;
                font-weight: 500;
                margin-top: {cls.SPACING['xs']};
            '>
                {delta}
            </div>
            """

        return f"""
        <div style='
            background: {cls.COLORS['surface']};
            padding: {cls.SPACING['lg']};
            border-radius: {cls.RADIUS['lg']};
            box-shadow: {cls.SHADOWS['sm']};
            text-align: center;
            border-top: 4px solid {cls.COLORS['primary']};
        '>
            <div style='
                font-size: 0.9rem;
                color: {cls.COLORS['text_secondary']};
                margin-bottom: {cls.SPACING['xs']};
                font-weight: 500;
            '>
                {title}
            </div>
            <div style='
                font-size: 2rem;
                font-weight: 700;
                color: {cls.COLORS['primary']};
                line-height: 1;
            '>
                {value}
            </div>
            {delta_html}
        </div>
        """

    @classmethod
    def create_alert(cls, message: str, alert_type: str = 'info') -> str:
        """Create a styled alert component"""
        icons = {
            'info': '💡',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }

        return f"""
        <div style='
            background: {cls.COLORS['surface']};
            border-left: 4px solid {cls.COLORS[alert_type]};
            padding: {cls.SPACING['lg']};
            border-radius: {cls.RADIUS['md']};
            margin: {cls.SPACING['md']} 0;
            box-shadow: {cls.SHADOWS['sm']};
        '>
            <div style='
                display: flex;
                align-items: center;
                gap: {cls.SPACING['sm']};
                color: {cls.COLORS['text']};
            '>
                <span style='font-size: 1.2rem;'>{icons.get(alert_type, '💡')}</span>
                <span>{message}</span>
            </div>
        </div>
        """

    @classmethod
    def create_progress_bar(cls, progress: float, label: str = None) -> str:
        """Create a styled progress bar"""
        label_html = f"<div style='margin-bottom: {cls.SPACING['xs']}; font-weight: 500;'>{label}</div>" if label else ""

        return f"""
        <div style='margin: {cls.SPACING['md']} 0;'>
            {label_html}
            <div style='
                background: {cls.COLORS['surface_dark']};
                border-radius: {cls.RADIUS['full']};
                height: 8px;
                overflow: hidden;
            '>
                <div style='
                    background: {cls.COLORS['gradient_primary']};
                    height: 100%;
                    width: {progress}%;
                    border-radius: {cls.RADIUS['full']};
                    transition: width 0.3s ease;
                '></div>
            </div>
            <div style='
                text-align: right;
                font-size: 0.8rem;
                color: {cls.COLORS['text_secondary']};
                margin-top: {cls.SPACING['xs']};
            '>
                {progress:.1f}%
            </div>
        </div>
        """

    @classmethod
    def create_badge(cls, text: str, color: str = 'primary') -> str:
        """Create a styled badge component"""
        return f"""
        <span style='
            background: {cls.COLORS[color]};
            color: white;
            padding: {cls.SPACING['xs']} {cls.SPACING['sm']};
            border-radius: {cls.RADIUS['full']};
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        '>
            {text}
        </span>
        """

    @classmethod
    def create_divider(cls, text: str = None) -> str:
        """Create a styled divider with optional text"""
        if text:
            return f"""
            <div style='
                display: flex;
                align-items: center;
                margin: {cls.SPACING['xl']} 0;
                color: {cls.COLORS['text_secondary']};
            '>
                <div style='
                    flex: 1;
                    height: 1px;
                    background: {cls.COLORS['surface_dark']};
                '></div>
                <div style='
                    padding: 0 {cls.SPACING['lg']};
                    font-weight: 500;
                '>
                    {text}
                </div>
                <div style='
                    flex: 1;
                    height: 1px;
                    background: {cls.COLORS['surface_dark']};
                '></div>
            </div>
            """
        else:
            return f"""
            <div style='
                height: 1px;
                background: {cls.COLORS['surface_dark']};
                margin: {cls.SPACING['xl']} 0;
            '></div>
            """

    @classmethod
    def apply_enhanced_styles(cls) -> None:
        """Apply enhanced styles with animations and advanced components"""
        st.markdown(f"""
        <style>
        .metric-container {{
            background: white;
            padding: {cls.SPACING['lg']};
            border-radius: {cls.RADIUS['lg']};
            box-shadow: {cls.SHADOWS['sm']};
            border-left: 4px solid {cls.COLORS['primary']};
            margin-bottom: {cls.SPACING['md']};
            animation: fadeInUp 0.7s cubic-bezier(.4,0,.2,1);
        }}
        .modern-card {{
            background: white;
            padding: {cls.SPACING['xl']};
            border-radius: {cls.RADIUS['lg']};
            box-shadow: {cls.SHADOWS['md']};
            margin-bottom: {cls.SPACING['lg']};
            border: 1px solid {cls.COLORS['surface_dark']};
            transition: box-shadow 0.4s, transform 0.3s, border-color 0.3s, background 0.4s;
            animation: fadeInUp 0.7s cubic-bezier(.4,0,.2,1);
        }}
        .modern-card:hover {{
            box-shadow: {cls.SHADOWS['xl']};
            border-color: {cls.COLORS['primary']};
            background: linear-gradient(120deg, #f8fafc 0%, #e9ecef 100%);
            transform: translateY(-6px) scale(1.02);
        }}
        .gradient-header {{
            background: {cls.COLORS['gradient_primary']};
            color: white;
            padding: {cls.SPACING['xl']};
            border-radius: {cls.RADIUS['lg']};
            text-align: center;
            margin-bottom: {cls.SPACING['xl']};
            box-shadow: {cls.SHADOWS['md']};
            animation: fadeInDown 0.7s cubic-bezier(.4,0,.2,1);
        }}
        @keyframes fadeInUp {{
            0% {{opacity: 0; transform: translateY(40px);}}
            100% {{opacity: 1; transform: translateY(0);}}
        }}
        @keyframes fadeInDown {{
            0% {{opacity: 0; transform: translateY(-40px);}}
            100% {{opacity: 1; transform: translateY(0);}}
        }}
        .status-badge {{
            display: inline-block;
            padding: {cls.SPACING['xs']} {cls.SPACING['sm']};
            border-radius: {cls.RADIUS['full']};
            font-size: 0.875rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: background 0.3s;
        }}
        .status-success {{background: {cls.COLORS['success']}; color: white;}}
        .status-warning {{background: {cls.COLORS['warning']}; color: white;}}
        .status-error {{background: {cls.COLORS['error']}; color: white;}}
        .status-info {{background: {cls.COLORS['info']}; color: white;}}
        .loading-spinner {{
            border: 4px solid {cls.COLORS['surface_dark']};
            border-top: 4px solid {cls.COLORS['primary']};
            border-radius: 50%;
            width: 40px; height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        @media (max-width: 768px) {{
            .main .block-container {{padding-left: {cls.SPACING['md']}; padding-right: {cls.SPACING['md']};}}
            h1 {{font-size: 2rem;}}
            h2 {{font-size: 1.5rem;}}
            .modern-card {{padding: {cls.SPACING['lg']};}}
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