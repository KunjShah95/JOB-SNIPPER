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

# Define nav items shown in the top bar
NAV_ITEMS: List[Dict[str, str]] = [
    {"label": "Home", "icon": "🏠"},
    {"label": "Resume Analysis", "icon": "🔍"},
    {"label": "Job Matching", "icon": "🎯"},
    {"label": "Skill Recommendations", "icon": "📚"},
    {"label": "HR Dashboard", "icon": "👥"},
    {"label": "Settings", "icon": "⚙️"},
]


def _inject_navbar_styles():
    """Inject CSS for a fixed, animated top navbar (glassmorphism + subtle 3D)."""
    st.markdown(
        """
        <style>
        /* Container offset so content doesn't hide under fixed navbar */
        .jobsniper-content-offset { margin-top: 76px; }

        /* Top Navbar */
        .jobsniper-navbar {
            position: fixed;
            top: 0; left: 0; right: 0;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 1rem;
            background: rgba(255,255,255,0.12);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(255,255,255,0.25);
            z-index: 1000;
        }

        .jobsniper-brand {
            display: flex; align-items: center; gap: 0.5rem;
            font-weight: 700; font-size: 1.1rem; color: #0f172a;
            text-decoration: none;
        }

        .jobsniper-nav {
            display: flex; gap: 0.25rem;
            perspective: 600px; /* subtle 3D hover */
        }

        .jobsniper-nav a {
            display: inline-flex; align-items: center; gap: 0.5rem;
            padding: 0.5rem 0.9rem; border-radius: 9999px;
            text-decoration: none; color: #1f2937; font-weight: 600;
            transition: transform .2s ease, box-shadow .3s ease, background .3s ease;
            background: rgba(255,255,255,0.5);
            border: 1px solid rgba(255,255,255,0.35);
            box-shadow: 0 10px 20px -10px rgba(0,0,0,0.25);
            transform-style: preserve-3d;
        }

        .jobsniper-nav a:hover {
            transform: translateY(-3px) rotateX(6deg);
            box-shadow: 0 20px 40px -15px rgba(99,102,241,0.35);
            background: rgba(255,255,255,0.65);
        }

        .jobsniper-nav a.active {
            background: linear-gradient(135deg, #667eea, #06b6d4);
            color: white; border-color: transparent;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.25);
        }

        /* Mobile: allow horizontal scroll */
        @media (max-width: 900px) {
            .jobsniper-nav { overflow-x: auto; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_top_nav(active_page: str = "Home") -> None:
    """Render the top navbar. Uses query params for routing.

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
        </div>
        <div class="jobsniper-content-offset"></div>
        """,
        unsafe_allow_html=True,
    )

    # Highlight active link via JS (class toggle) to avoid brittle string concat above
    st.markdown(
        f"""
        <script>
        const params = new URLSearchParams(window.location.search);
        const current = params.get('page') || '{active_page}';
        document.querySelectorAll('.jobsniper-nav a').forEach(a => {{
            const url = new URL(a.href);
            const label = new URLSearchParams(url.search).get('page');
            if (label === current) {{ a.classList.add('active'); }} else {{ a.classList.remove('active'); }}
        }});
        </script>
        """,
        unsafe_allow_html=True,
    )

