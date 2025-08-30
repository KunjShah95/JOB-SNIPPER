# Wrapper for compatibility with app.py
def navbar(active_page: str = "Home"):
    render_top_nav(active_page)
"""Top Navigation Bar Component for JobSniper AI

Animated, glassmorphic navbar with page routing via query params.
Works with Streamlit by using anchor links (?page=...) so clicks
cause a lightweight reload and we can route in ui/app.py.
"""

import streamlit as st
from typing import List, Dict
from ..core.ui_constants import UIConstants

# Define nav items shown in the top bar using UI constants
NAV_ITEMS: List[Dict[str, str]] = UIConstants.get_top_nav_pages()


def _inject_navbar_styles():
    """Inject CSS for a fixed, animated top navbar with mobile popup menu."""
    st.markdown(
        f"""
        <style>
        /* Container offset so content doesn't hide under fixed navbar */
        .jobsniper-content-offset {{ margin-top: {UIConstants.LAYOUT['navbar_height']}; }}

        /* Top Navbar */
        .jobsniper-navbar {{
            position: fixed;
            top: 0; left: 0; right: 0;
            height: {UIConstants.LAYOUT['navbar_height']};
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 1rem;
            background: {UIConstants.DESIGN['colors']['glass_bg']};
            backdrop-filter: blur({UIConstants.DESIGN['effects']['blur']});
            -webkit-backdrop-filter: blur({UIConstants.DESIGN['effects']['blur']});
            border-bottom: 1px solid {UIConstants.DESIGN['colors']['glass_border']};
            z-index: 1000;
        }}

        .jobsniper-brand {{
            display: flex; align-items: center; gap: 0.5rem;
            font-weight: 700; font-size: 1.1rem; color: #0f172a;
            text-decoration: none;
        }}

        /* Desktop Navigation */
        .jobsniper-nav {{
            display: flex; gap: 0.25rem;
            perspective: 600px; /* subtle 3D hover */
        }}

        .jobsniper-nav a {{
            display: inline-flex; align-items: center; gap: 0.5rem;
            padding: 0.5rem 0.9rem; border-radius: 9999px;
            text-decoration: none; color: #1f2937; font-weight: 600;
            transition: transform .2s ease, box-shadow .3s ease, background .3s ease;
            background: rgba(255,255,255,0.5);
            border: 1px solid rgba(255,255,255,0.35);
            box-shadow: 0 10px 20px -10px rgba(0,0,0,0.25);
            transform-style: preserve-3d;
        }}

        .jobsniper-nav a:hover {{
            transform: translateY(-3px) rotateX(6deg);
            box-shadow: {UIConstants.DESIGN['effects']['glow']};
            background: rgba(255,255,255,0.65);
        }}

        .jobsniper-nav a.active {{
            background: linear-gradient(135deg, {UIConstants.DESIGN['colors']['primary']}, {UIConstants.DESIGN['colors']['secondary']});
            color: white; border-color: transparent;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.25);
        }}

        /* Mobile Menu Button */
        .mobile-menu-btn {{
            display: none;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #1f2937;
            padding: 0.5rem;
            border-radius: 0.5rem;
            transition: background-color 0.3s ease;
        }}

        .mobile-menu-btn:hover {{
            background: rgba(255,255,255,0.2);
        }}

        /* Mobile Navigation Popup */
        .mobile-nav-popup {{
            display: none;
            position: fixed;
            top: {UIConstants.LAYOUT['navbar_height']};
            left: 0;
            right: 0;
            background: {UIConstants.DESIGN['colors']['glass_bg']};
            backdrop-filter: blur({UIConstants.DESIGN['effects']['blur']});
            -webkit-backdrop-filter: blur({UIConstants.DESIGN['effects']['blur']});
            border-bottom: 1px solid {UIConstants.DESIGN['colors']['glass_border']};
            z-index: 999;
            animation: slideDown 0.3s ease-out;
        }}

        .mobile-nav-popup.show {{
            display: block;
        }}

        .mobile-nav-popup .jobsniper-nav {{
            flex-direction: column;
            gap: 0;
            padding: 1rem 0;
        }}

        .mobile-nav-popup .jobsniper-nav a {{
            justify-content: center;
            margin: 0.25rem 1rem;
            border-radius: 0.75rem;
        }}

        @keyframes slideDown {{
            from {{
                opacity: 0;
                transform: translateY(-10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        /* Mobile: hide desktop nav, show mobile menu */
        @media (max-width: 900px) {{
            .jobsniper-nav {{ display: none; }}
            .mobile-menu-btn {{ display: block; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_top_nav(active_page: str = "Home") -> None:
    """Render the top navbar with mobile popup menu.

    Args:
        active_page: current page label matching NAV_ITEMS labels
    """
    _inject_navbar_styles()

    # Build links with ?page=...
    links_html = "".join(
        [
            f'<a href="?page={item["label"].replace(" ", "%20")}" '
            f'class="{"jobsniper-link jobsniper active" if item["label"] == active_page else ""}">' # placeholder class
            f'{item["icon"]} <span>{item["label"]}</span></a>'
            for item in NAV_ITEMS
        ]
    )

    st.markdown(
        f"""
        <div class="jobsniper-navbar">
            <a class="jobsniper-brand" href="?page=Home">🎯 JobSniper AI</a>
            <nav class="jobsniper-nav">
                {links_html}
            </nav>
            <button class="mobile-menu-btn" onclick="toggleMobileMenu()">☰</button>
        </div>

        <!-- Mobile Navigation Popup -->
        <div class="mobile-nav-popup" id="mobile-nav-popup">
            <nav class="jobsniper-nav">
                {links_html}
            </nav>
        </div>

        <div class="jobsniper-content-offset"></div>
        """,
        unsafe_allow_html=True,
    )

    # JavaScript for mobile menu toggle and active link highlighting
    st.markdown(
        f"""
        <script>
        function toggleMobileMenu() {{
            const popup = document.getElementById('mobile-nav-popup');
            popup.classList.toggle('show');
        }}

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {{
            const popup = document.getElementById('mobile-nav-popup');
            const menuBtn = event.target.closest('.mobile-menu-btn');
            if (!menuBtn && !popup.contains(event.target)) {{
                popup.classList.remove('show');
            }}
        }});

        // Highlight active link
        const params = new URLSearchParams(window.location.search);
        const current = params.get('page') || '{active_page}';
        document.querySelectorAll('.jobsniper-nav a').forEach(a => {{
            const url = new URL(a.href);
            const label = new URLSearchParams(url.search).get('page');
            if (label === current) {{
                a.classList.add('active');
            }} else {{
                a.classList.remove('active');
            }}
        }});

        // Close mobile menu on navigation
        document.querySelectorAll('.mobile-nav-popup .jobsniper-nav a').forEach(a => {{
            a.addEventListener('click', function() {{
                document.getElementById('mobile-nav-popup').classList.remove('show');
            }});
        }});
        </script>
        """,
        unsafe_allow_html=True,
    )

