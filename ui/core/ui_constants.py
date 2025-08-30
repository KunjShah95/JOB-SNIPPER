"""UI Constants Configuration for JobSniper AI

Centralized configuration for all UI-related constants to ensure consistency
and eliminate hardcoded values across the application.
"""

from typing import Dict, List, Any

class UIConstants:
    """Centralized UI constants for consistent design and maintainability"""

    # 🎨 Brand Identity
    BRAND = {
        'name': 'JobSniper AI',
        'short_name': 'JobSniper',
        'tagline': 'AI-Powered Job Search & Career Development',
        'version': '2.0.0',
        'copyright': '© 2025 JobSniper AI. All rights reserved.',
        'logo_url': 'https://img.icons8.com/ios-filled/100/2D6A4F/ai.png',
        'logo_width': 60,
    }

    # 📄 Page Configuration
    PAGES = {
        'home': {
            'title': 'Home',
            'icon': '🏠',
            'description': 'Welcome to JobSniper AI',
            'route': 'home'
        },
        'application_tracker': {
            'title': 'Application Tracker',
            'icon': '📋',
            'description': 'Track your job applications',
            'route': 'application_tracker'
        },
        'resume_builder': {
            'title': 'Resume Builder',
            'icon': '📝',
            'description': 'Build professional resumes',
            'route': 'resume_builder'
        },
        'resume_analysis': {
            'title': 'Resume Analysis',
            'icon': '🔍',
            'description': 'AI-powered resume analysis',
            'route': 'resume_analysis'
        },
        'resume_scoring': {
            'title': 'Resume Scoring',
            'icon': '📊',
            'description': 'Get detailed resume scores',
            'route': 'resume_scoring'
        },
        'job_finder': {
            'title': 'Job Finder',
            'icon': '🔎',
            'description': 'Find relevant job opportunities',
            'route': 'job_finder'
        },
        'job_matching': {
            'title': 'Job Matching',
            'icon': '🎯',
            'description': 'Match jobs to your profile',
            'route': 'job_matching'
        },
        'resume_qa_search': {
            'title': 'Resume Q&A Search',
            'icon': '💬',
            'description': 'Ask questions about your resume',
            'route': 'resume_qa_search'
        },
        'analytics_dashboard': {
            'title': 'Analytics Dashboard',
            'icon': '📈',
            'description': 'View analytics and insights',
            'route': 'analytics_dashboard'
        },
        'hr_dashboard': {
            'title': 'HR Dashboard',
            'icon': '👥',
            'description': 'HR management tools',
            'route': 'hr_dashboard'
        },
        'interview_prep': {
            'title': 'Interview Prep',
            'icon': '🎤',
            'description': 'Prepare for interviews',
            'route': 'interview_prep'
        },
        'skill_recommendations': {
            'title': 'Skill Recommendations',
            'icon': '📚',
            'description': 'Get skill recommendations',
            'route': 'skill_recommendations'
        },
        'settings': {
            'title': 'Settings',
            'icon': '⚙️',
            'description': 'Application settings',
            'route': 'settings'
        }
    }

    # 🧭 Navigation Configuration
    NAVIGATION = {
        'sidebar_pages': [
            'home',
            'application_tracker',
            'resume_builder',
            'resume_analysis',
            'resume_scoring',
            'job_finder',
            'job_matching',
            'resume_qa_search',
            'analytics_dashboard',
            'hr_dashboard',
            'interview_prep',
            'skill_recommendations',
            'settings'
        ],
        'top_nav_pages': [
            'home',
            'resume_analysis',
            'job_matching',
            'skill_recommendations',
            'hr_dashboard',
            'settings'
        ],
        'default_page': 'home'
    }

    # 🎨 Design System Constants
    DESIGN = {
        'colors': {
            'primary': '#2D6A4F',
            'secondary': '#4A90E2',
            'accent': '#F5A623',
            'success': '#10B981',
            'warning': '#F59E0B',
            'error': '#EF4444',
            'info': '#3B82F6',
            'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'glass_bg': 'rgba(255,255,255,0.4)',
            'glass_border': 'rgba(255,255,255,0.25)',
        },
        'typography': {
            'primary_font': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            'display_font': '"Poppins", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            'mono_font': '"JetBrains Mono", "Fira Code", Consolas, monospace',
            'brand_size': '1.6rem',
            'heading_size': '2rem',
            'body_size': '1rem',
        },
        'spacing': {
            'xs': '0.5rem',
            'sm': '0.75rem',
            'md': '1rem',
            'lg': '1.5rem',
            'xl': '2rem',
            'xxl': '3rem',
        },
        'effects': {
            'blur': '16px',
            'shadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            'glow': '0 0 20px rgba(99, 102, 241, 0.3)',
        }
    }

    # 📱 Layout Configuration
    LAYOUT = {
        'sidebar_width': '280px',
        'navbar_height': '64px',
        'content_max_width': '1400px',
        'container_padding': '2rem 1rem',
        'border_radius': '0.75rem',
    }

    # 🎯 Component Styles
    COMPONENTS = {
        'button_primary': {
            'background': 'linear-gradient(135deg, #2D6A4F, #4A90E2)',
            'color': 'white',
            'border_radius': '0.5rem',
            'padding': '0.75rem 1.5rem',
            'font_weight': '600',
        },
        'button_secondary': {
            'background': 'rgba(255,255,255,0.1)',
            'color': '#2D6A4F',
            'border': '1px solid rgba(255,255,255,0.25)',
            'border_radius': '0.5rem',
            'padding': '0.75rem 1.5rem',
        },
        'card': {
            'background': 'rgba(255,255,255,0.1)',
            'border': '1px solid rgba(255,255,255,0.2)',
            'border_radius': '1rem',
            'padding': '1.5rem',
            'backdrop_filter': 'blur(16px)',
        },
        'input': {
            'background': 'rgba(255,255,255,0.1)',
            'border': '1px solid rgba(255,255,255,0.25)',
            'border_radius': '0.5rem',
            'padding': '0.75rem',
            'color': '#374151',
        }
    }

    # 📊 Animation & Transition Settings
    ANIMATIONS = {
        'transition_duration': '0.3s',
        'transition_easing': 'ease-in-out',
        'hover_scale': '1.02',
        'loading_duration': '1s',
    }

    # 🔧 Feature Flags
    FEATURES = {
        'enable_dark_mode': True,
        'enable_animations': True,
        'enable_sound_effects': False,
        'enable_notifications': True,
        'enable_analytics': True,
    }

    # 🎨 Color Gradients (for backward compatibility with quantum components)
    COLORS = {
        'gradient_aurora': 'linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%)',
        'gradient_ocean': 'linear-gradient(135deg, #667eea 0%, #06b6d4 50%, #10b981 100%)',
        'gradient_sunset': 'linear-gradient(135deg, #f59e0b 0%, #f43f5e 50%, #6366f1 100%)',
    }

    @classmethod
    def get_page_info(cls, page_key: str) -> Dict[str, Any]:
        """Get page information by key"""
        return cls.PAGES.get(page_key, cls.PAGES['home'])

    @classmethod
    def get_sidebar_pages(cls) -> List[str]:
        """Get list of pages for sidebar navigation"""
        return [cls.PAGES[page]['title'] for page in cls.NAVIGATION['sidebar_pages']]

    @classmethod
    def get_top_nav_pages(cls) -> List[Dict[str, str]]:
        """Get list of pages for top navigation"""
        return [
            {
                'label': cls.PAGES[page]['title'],
                'icon': cls.PAGES[page]['icon']
            }
            for page in cls.NAVIGATION['top_nav_pages']
        ]

    @classmethod
    def get_default_page(cls) -> str:
        """Get default page title"""
        default_key = cls.NAVIGATION['default_page']
        return cls.PAGES[default_key]['title']

    @classmethod
    def get_page_route(cls, page_title: str) -> str:
        """Get page route from title"""
        for page_key, page_info in cls.PAGES.items():
            if page_info['title'] == page_title:
                return page_info['route']
        return 'home'
