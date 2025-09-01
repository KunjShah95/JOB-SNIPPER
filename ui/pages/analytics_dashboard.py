"""
Analytics Dashboard - Real-time insights and metrics
Advanced analytics for resume processing and system performance
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import Dict, Any, List

from ui.templates.page_template import render_standard_page
from ui.components.quantum_components import quantum_card, quantum_metrics_grid
from ui.core.ui_constants import UIConstants

def render():
    """Render the analytics dashboard"""
    
    # Configure tabs
    tabs_config = [
        {"key": "overview", "label": "📈 Overview"},
        {"key": "resume_insights", "label": "🎯 Resume Insights"},
        {"key": "performance", "label": "⚡ Performance"},
        {"key": "search_analytics", "label": "🔍 Search Analytics"}
    ]
    
    tab_renders = {
        "overview": render_overview_analytics,
        "resume_insights": render_resume_insights,
        "performance": render_performance_metrics,
        "search_analytics": render_search_analytics
    }
    
    # Use standard page template
    render_standard_page(
        title="Analytics Dashboard",
        subtitle="Real-time insights into resume processing and system performance",
        icon="📊",
        tabs_config=tabs_config,
        tab_renders=tab_renders,
        gradient="aurora"
    )

def render_overview_analytics():
    """Render overview analytics"""
    
    # Key metrics using quantum components
    metrics = [
        {
            "icon": "📄",
            "value": "1,247",
            "label": "Total Resumes Processed",
            "trend": "23 today",
            "color": "blue"
        },
        {
            "icon": "📊",
            "value": "78.5",
            "label": "Average Score",
            "trend": "2.3 vs last week",
            "color": "green"
        },
        {
            "icon": "💬",
            "value": "342",
            "label": "QA Queries",
            "trend": "15 today",
            "color": "purple"
        },
        {
            "icon": "⚡",
            "value": "99.8%",
            "label": "System Uptime",
            "trend": "0.1% vs last month",
            "color": "orange"
        }
    ]
    
    quantum_metrics_grid(metrics, columns=4)
    
    # Processing trends in quantum card
    quantum_card(
        title="📈 Daily Processing Trends",
        content="",
        card_type="glass"
    )
    
    # Generate sample data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    processing_data = pd.DataFrame({
        'Date': dates,
        'Resumes Processed': [20 + i*2 + (i%7)*5 for i in range(len(dates))],
        'Average Score': [75 + (i%10)*2 + (i%3) for i in range(len(dates))],
        'QA Queries': [10 + i + (i%5)*3 for i in range(len(dates))]
    })
    
    # Multi-line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=processing_data['Date'],
        y=processing_data['Resumes Processed'],
        mode='lines+markers',
        name='Resumes Processed',
        line=dict(color=UIConstants.DESIGN['colors']['primary'])
    ))
    
    fig.add_trace(go.Scatter(
        x=processing_data['Date'],
        y=processing_data['QA Queries'],
        mode='lines+markers',
        name='QA Queries',
        yaxis='y2',
        line=dict(color=UIConstants.DESIGN['colors']['secondary'])
    ))
    
    fig.update_layout(
        title='Daily Processing Volume',
        xaxis_title='Date',
        yaxis_title='Resumes Processed',
        yaxis2=dict(
            title='QA Queries',
            overlaying='y',
            side='right'
        ),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Score distribution
    col1, col2 = st.columns(2)
    
    with col1:
        # Score distribution histogram
        scores = [65, 72, 78, 85, 91, 68, 74, 82, 88, 76, 79, 83, 87, 71, 77]
        fig_hist = px.histogram(
            x=scores,
            nbins=10,
            title="Resume Score Distribution",
            labels={'x': 'Score', 'y': 'Count'}
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Top skills pie chart
        skills_data = {
            'Python': 45,
            'JavaScript': 38,
            'SQL': 42,
            'React': 28,
            'AWS': 25,
            'Machine Learning': 22
        }
        
        fig_pie = px.pie(
            values=list(skills_data.values()),
            names=list(skills_data.keys()),
            title="Most Common Skills"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

def render_resume_insights():
    """Render detailed resume insights"""
    
    st.markdown("### 🎯 Resume Analysis Insights")
    
    # Score breakdown analysis
    st.markdown("#### Score Breakdown Analysis")
    
    categories = ['Technical Skills', 'Experience', 'Education', 'Format', 'Keywords']
    avg_scores = [18.5, 19.2, 16.8, 12.3, 11.7]
    max_scores = [25, 25, 20, 15, 15]
    
    fig_breakdown = go.Figure()
    
    fig_breakdown.add_trace(go.Bar(
        name='Average Score',
        x=categories,
        y=avg_scores,
        marker_color='steelblue'
    ))
    
    fig_breakdown.add_trace(go.Bar(
        name='Maximum Possible',
        x=categories,
        y=max_scores,
        marker_color='lightgray',
        opacity=0.5
    ))
    
    fig_breakdown.update_layout(
        title='Average Scores by Category',
        barmode='overlay',
        height=400
    )
    
    st.plotly_chart(fig_breakdown, use_container_width=True)
    
    # Industry analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Industry Distribution")
        industry_data = {
            'Technology': 45,
            'Healthcare': 18,
            'Finance': 15,
            'Marketing': 12,
            'Education': 8,
            'Other': 12
        }
        
        fig_industry = px.bar(
            x=list(industry_data.keys()),
            y=list(industry_data.values()),
            title="Resumes by Industry"
        )
        st.plotly_chart(fig_industry, use_container_width=True)
    
    with col2:
        st.markdown("#### Experience Level Distribution")
        exp_data = {
            'Entry (0-2 years)': 28,
            'Mid (3-5 years)': 42,
            'Senior (6-10 years)': 23,
            'Executive (10+ years)': 7
        }
        
        fig_exp = px.pie(
            values=list(exp_data.values()),
            names=list(exp_data.keys()),
            title="Experience Levels"
        )
        st.plotly_chart(fig_exp, use_container_width=True)
    
    # Improvement recommendations analysis
    st.markdown("#### Common Improvement Areas")
    
    improvements = {
        'Add quantified achievements': 67,
        'Include more technical skills': 54,
        'Improve formatting': 43,
        'Add relevant keywords': 38,
        'Expand project descriptions': 32,
        'Include certifications': 28
    }
    
    fig_improvements = px.bar(
        x=list(improvements.values()),
        y=list(improvements.keys()),
        orientation='h',
        title="Most Common Improvement Suggestions"
    )
    fig_improvements.update_layout(height=400)
    st.plotly_chart(fig_improvements, use_container_width=True)

def render_performance_metrics():
    """Render system performance metrics"""
    
    st.markdown("### ⚡ System Performance")
    
    # Real-time metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Response Time", "1.2s", delta="-0.3s vs last hour")
    
    with col2:
        st.metric("Success Rate", "99.2%", delta="0.1% vs yesterday")
    
    with col3:
        st.metric("Active Users", "47", delta="5 vs last hour")
    
    # Performance over time
    st.markdown("#### Performance Trends")
    
    # Generate performance data
    hours = list(range(24))
    response_times = [1.1 + 0.3 * (h % 6) + 0.1 * (h % 3) for h in hours]
    success_rates = [99.5 - 0.5 * (h % 8) + 0.2 * (h % 4) for h in hours]
    
    fig_perf = go.Figure()
    
    fig_perf.add_trace(go.Scatter(
        x=hours,
        y=response_times,
        mode='lines+markers',
        name='Response Time (s)',
        line=dict(color='red')
    ))
    
    fig_perf.add_trace(go.Scatter(
        x=hours,
        y=[rt/10 for rt in success_rates],  # Scale for visibility
        mode='lines+markers',
        name='Success Rate (%/10)',
        yaxis='y2',
        line=dict(color='green')
    ))
    
    fig_perf.update_layout(
        title='24-Hour Performance Metrics',
        xaxis_title='Hour of Day',
        yaxis_title='Response Time (seconds)',
        yaxis2=dict(
            title='Success Rate (%/10)',
            overlaying='y',
            side='right'
        ),
        height=400
    )
    
    st.plotly_chart(fig_perf, use_container_width=True)
    
    # Agent performance
    st.markdown("#### Agent Performance")
    
    agent_data = pd.DataFrame({
        'Agent': ['Parser', 'Scorer', 'QA', 'Matcher', 'Feedback'],
        'Avg Response Time (s)': [0.8, 1.5, 2.1, 1.2, 0.9],
        'Success Rate (%)': [99.8, 98.5, 97.2, 99.1, 99.5],
        'Requests/Hour': [45, 23, 18, 38, 42]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_agent_time = px.bar(
            agent_data,
            x='Agent',
            y='Avg Response Time (s)',
            title='Agent Response Times'
        )
        st.plotly_chart(fig_agent_time, use_container_width=True)
    
    with col2:
        fig_agent_requests = px.bar(
            agent_data,
            x='Agent',
            y='Requests/Hour',
            title='Agent Request Volume'
        )
        st.plotly_chart(fig_agent_requests, use_container_width=True)
    
    # System resources
    st.markdown("#### System Resources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CPU usage gauge
        fig_cpu = go.Figure(go.Indicator(
            mode="gauge+number",
            value=67,
            title={'text': "CPU Usage (%)"},
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': "darkblue"},
                   'steps': [{'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "red"}]}
        ))
        fig_cpu.update_layout(height=300)
        st.plotly_chart(fig_cpu, use_container_width=True)
    
    with col2:
        # Memory usage gauge
        fig_mem = go.Figure(go.Indicator(
            mode="gauge+number",
            value=45,
            title={'text': "Memory Usage (%)"},
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': "darkgreen"},
                   'steps': [{'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "red"}]}
        ))
        fig_mem.update_layout(height=300)
        st.plotly_chart(fig_mem, use_container_width=True)
    
    with col3:
        # Disk usage gauge
        fig_disk = go.Figure(go.Indicator(
            mode="gauge+number",
            value=23,
            title={'text': "Disk Usage (%)"},
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': "darkorange"},
                   'steps': [{'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "red"}]}
        ))
        fig_disk.update_layout(height=300)
        st.plotly_chart(fig_disk, use_container_width=True)

def render_search_analytics():
    """Render search and QA analytics"""
    
    st.markdown("### 🔍 Search & QA Analytics")
    
    # Search metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Queries", "1,847", delta="42 today")
    
    with col2:
        st.metric("Avg Confidence", "0.82", delta="0.05 vs last week")
    
    with col3:
        st.metric("Vector DB Size", "15.2k chunks", delta="234 new")
    
    with col4:
        st.metric("Search Accuracy", "94.3%", delta="1.2% improvement")
    
    # Query patterns
    st.markdown("#### Popular Query Patterns")
    
    query_patterns = {
        'Skills-based queries': 45,
        'Experience level queries': 32,
        'Industry-specific queries': 28,
        'Education queries': 18,
        'Location-based queries': 12,
        'Certification queries': 8
    }
    
    fig_patterns = px.bar(
        x=list(query_patterns.keys()),
        y=list(query_patterns.values()),
        title="Query Types Distribution"
    )
    fig_patterns.update_xaxes(tickangle=45)
    st.plotly_chart(fig_patterns, use_container_width=True)
    
    # Search performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Search Response Times")
        
        response_times = [0.5, 0.8, 1.2, 0.9, 1.5, 0.7, 1.1, 0.6, 1.3, 0.8]
        fig_response = px.histogram(
            x=response_times,
            nbins=8,
            title="Search Response Time Distribution"
        )
        st.plotly_chart(fig_response, use_container_width=True)
    
    with col2:
        st.markdown("#### Confidence Score Distribution")
        
        confidence_scores = [0.9, 0.85, 0.78, 0.92, 0.67, 0.88, 0.75, 0.91, 0.82, 0.79]
        fig_confidence = px.histogram(
            x=confidence_scores,
            nbins=8,
            title="Query Confidence Scores"
        )
        st.plotly_chart(fig_confidence, use_container_width=True)
    
    # Recent queries table
    st.markdown("#### Recent Queries")
    
    recent_queries = pd.DataFrame({
        'Timestamp': [
            '2024-01-15 14:30:22',
            '2024-01-15 14:28:15',
            '2024-01-15 14:25:08',
            '2024-01-15 14:22:45',
            '2024-01-15 14:20:12'
        ],
        'Query': [
            'Which candidates have Python and AWS experience?',
            'Find senior developers with React skills',
            'Show me data scientists with PhD',
            'Who has machine learning experience?',
            'Find candidates with 5+ years experience'
        ],
        'Results': [3, 5, 2, 4, 8],
        'Confidence': [0.92, 0.87, 0.95, 0.83, 0.78],
        'Response Time (s)': [1.2, 0.8, 1.5, 1.1, 0.9]
    })
    
    st.dataframe(recent_queries, use_container_width=True)
    
    # Export functionality
    if st.button("📥 Export Analytics Data"):
        # Create downloadable CSV
        analytics_data = pd.DataFrame({
            'Metric': ['Total Resumes', 'Average Score', 'QA Queries', 'System Uptime'],
            'Value': [1247, 78.5, 342, 99.8],
            'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * 4
        })
        
        csv = analytics_data.to_csv(index=False)
        st.download_button(
            label="Download Analytics CSV",
            data=csv,
            file_name=f"jobsniper_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
