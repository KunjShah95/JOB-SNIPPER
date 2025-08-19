"""Application Tracker Page for JobSniper AI

Track job applications, interviews, and follow-ups with detailed status management.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
import plotly.express as px

def render():
    """Main application tracker page"""

    st.title("📊 Application Tracker")
    st.markdown("Track your job applications, interviews, and follow-ups")
    
    if "job_applications" not in st.session_state:
        st.session_state.job_applications = []
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Applications", "📈 Analytics", "📅 Calendar", "⚙️ Manage"])
    
    with tab1:
        _render_applications_tab()
    
    with tab2:
        _render_analytics_tab()
    
    with tab3:
        _render_calendar_tab()
    
    with tab4:
        _render_manage_tab()

def _render_applications_tab():
    """Render applications tracking tab"""
    applications = st.session_state.job_applications

    if not applications:
        # Empty state
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #666;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📋</div>
            <h3>No Applications Yet</h3>
            <p>Start tracking your job applications by adding your first application below.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("➕ Add Your First Application", use_container_width=True, type="primary"):
            _show_add_application_form()
        return

    # Display metrics using Streamlit columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📄 Total Applications", len(applications))
    with col2:
        pending_count = len([app for app in applications if app['status'] in ['Applied', 'Under Review']])
        st.metric("⏳ Pending", pending_count)
    with col3:
        interview_count = len([app for app in applications if 'Interview' in app['status']])
        st.metric("🎤 Interviews", interview_count)
    with col4:
        offer_count = len([app for app in applications if app['status'] == 'Offer Received'])
        st.metric("🏆 Offers", offer_count)

    with st.form("filters"):
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All"] + list(set([app['status'] for app in applications])))
        with col2:
            company_filter = st.selectbox("Filter by Company", ["All"] + list(set([app['company'] for app in applications])))
        with col3:
            search_term = st.text_input("Search", placeholder="Job title, company...")
        st.form_submit_button("Apply Filters")

    filtered_apps = applications
    if status_filter != "All":
        filtered_apps = [app for app in filtered_apps if app['status'] == status_filter]
    if company_filter != "All":
        filtered_apps = [app for app in filtered_apps if app['company'] == company_filter]
    if search_term:
        filtered_apps = [
            app for app in filtered_apps
            if search_term.lower() in app['job_title'].lower() or
               search_term.lower() in app['company'].lower()
        ]

    if filtered_apps:
        for i, app in enumerate(filtered_apps):
            _render_application_card(app, i)
    else:
        st.info("No applications found matching your filters.")

    if st.button("➕ Add New Application", use_container_width=True):
        _show_add_application_form()

def _render_application_card(app: Dict[str, Any], index: int = 0):
    """Render individual application card"""

    # Status color mapping
    status_colors = {
        'Applied': '🔵',
        'Under Review': '🟡',
        'Phone Screen': '🟣',
        'Technical Interview': '🟣',
        'Final Interview': '🟣',
        'Offer Received': '🟢',
        'Rejected': '🔴',
        'Withdrawn': '⚫'
    }
    status_icon = status_colors.get(app['status'], '⚫')

    # Create a container for the application card
    with st.container():
        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader(f"{app['job_title']}")
            st.write(f"**{app['company']}**")
            st.caption(f"📅 Applied: {app['applied_date']}")

        with col2:
            st.write(f"{status_icon} {app['status']}")

        st.divider()

    with st.expander(f"Details - {app['job_title']}"):
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Location:** {app.get('location', 'N/A')}")
            st.write(f"**Salary Range:** {app.get('salary_range', 'N/A')}")
            st.write(f"**Source:** {app.get('source', 'N/A')}")

        with col2:
            st.write(f"**Notes:** {app.get('notes', 'No notes')}")

        if 'timeline' in app and app['timeline']:
            st.write("**Timeline:**")
            for event in app['timeline']:
                st.write(f"• {event['date']}: {event['event']}")



# Other tab functions
def _render_analytics_tab():
    """Render analytics tab"""
    applications = st.session_state.job_applications

    if not applications:
        st.info("📊 Add some applications first to see analytics!")
        return

    st.subheader("📊 Application Analytics")

    # Status distribution
    status_counts = {}
    for app in applications:
        status = app['status']
        status_counts[status] = status_counts.get(status, 0) + 1

    if status_counts:
        import plotly.express as px
        import pandas as pd

        df = pd.DataFrame(list(status_counts.items()), columns=['Status', 'Count'])
        fig = px.pie(df, values='Count', names='Status', title='Application Status Distribution')
        st.plotly_chart(fig, use_container_width=True)

    # Application timeline
    st.subheader("📅 Application Timeline")
    timeline_data = []
    for app in applications:
        timeline_data.append({
            'Date': app['applied_date'],
            'Company': app['company'],
            'Job Title': app['job_title'],
            'Status': app['status']
        })

    if timeline_data:
        df = pd.DataFrame(timeline_data)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        st.dataframe(df, use_container_width=True)

def _render_calendar_tab():
    """Render calendar tab"""
    st.subheader("📅 Interview Calendar")

    applications = st.session_state.job_applications
    upcoming_interviews = [
        app for app in applications
        if 'Interview' in app['status']
    ]

    if upcoming_interviews:
        st.write("**Upcoming Interviews:**")
        for app in upcoming_interviews:
            st.write(f"🎤 **{app['job_title']}** at **{app['company']}** - {app['status']}")
    else:
        st.info("No upcoming interviews scheduled.")

def _render_manage_tab():
    """Render manage tab"""
    st.subheader("⚙️ Manage Applications")

    applications = st.session_state.job_applications

    if not applications:
        st.info("No applications to manage yet.")
        return

    st.write("**All Applications:**")

    for i, app in enumerate(applications):
        with st.expander(f"{app['job_title']} at {app['company']}"):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(f"**Status:** {app['status']}")
                st.write(f"**Applied:** {app['applied_date']}")
                st.write(f"**Location:** {app.get('location', 'N/A')}")

            with col2:
                if st.button(f"Delete", key=f"delete_{i}"):
                    st.session_state.job_applications.pop(i)
                    st.success("Application deleted!")
                    st.rerun()

def _show_add_application_form():
    """Show add application form"""
    st.subheader("➕ Add New Job Application")

    with st.form("add_application"):
        col1, col2 = st.columns(2)

        with col1:
            job_title = st.text_input("Job Title *", placeholder="e.g., Software Engineer")
            company = st.text_input("Company *", placeholder="e.g., Google")
            location = st.text_input("Location", placeholder="e.g., San Francisco, CA")
            salary_range = st.text_input("Salary Range", placeholder="e.g., $80k - $120k")

        with col2:
            status = st.selectbox("Status", [
                "Applied", "Under Review", "Phone Screen", "Technical Interview",
                "Final Interview", "Offer Received", "Rejected", "Withdrawn"
            ])
            source = st.selectbox("Source", [
                "LinkedIn", "Company Website", "Indeed", "Glassdoor",
                "Recruiter", "Referral", "Job Fair", "Other"
            ])
            applied_date = st.date_input("Applied Date", value=datetime.now().date())

        notes = st.text_area("Notes", placeholder="Any additional notes about this application...")

        submitted = st.form_submit_button("Add Application", use_container_width=True)

        if submitted and job_title and company:
            new_app = {
                'id': f"app_{len(st.session_state.job_applications) + 1}",
                'job_title': job_title,
                'company': company,
                'applied_date': applied_date.strftime('%Y-%m-%d'),
                'status': status,
                'location': location,
                'salary_range': salary_range,
                'source': source,
                'notes': notes,
                'timeline': [
                    {'date': applied_date.strftime('%Y-%m-%d'), 'event': 'Application submitted'}
                ]
            }

            st.session_state.job_applications.append(new_app)
            st.success(f"✅ Added application for {job_title} at {company}!")
            st.rerun()
        elif submitted:
            st.error("Please fill in the required fields (Job Title and Company)")