"""UI Components Package for JobSniper AI

Modular UI components to break down the monolithic app.py file
and improve maintainability and reusability.
"""

from .sidebar import create_sidebar, get_navigation_choice
from .charts import create_skill_chart, create_match_chart, create_metrics_dashboard
from .forms import resume_upload_form, email_config_form, api_key_form
from .display import show_analysis_results, show_job_recommendations, show_error_message

__all__ = [
    'create_sidebar',
    'get_navigation_choice', 
    'create_skill_chart',
    'create_match_chart',
    'create_metrics_dashboard',
    'resume_upload_form',
    'email_config_form',
    'api_key_form',
    'show_analysis_results',
    'show_job_recommendations',
    'show_error_message'
]