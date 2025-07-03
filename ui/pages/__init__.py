"""UI Pages Package for JobSniper AI

Modular page components to replace the monolithic app.py structure.
Each page handles a specific feature with clean separation of concerns.
"""

from .home import render_home_page
from .resume_analysis import render_resume_analysis_page
from .job_matching import render_job_matching_page
from .skill_recommendations import render_skill_recommendations_page
from .hr_dashboard import render_hr_dashboard_page
from .settings import render_settings_page

__all__ = [
    'render_home_page',
    'render_resume_analysis_page', 
    'render_job_matching_page',
    'render_skill_recommendations_page',
    'render_hr_dashboard_page',
    'render_settings_page'
]