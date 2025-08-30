"""
🌟 Quantum UI Components Library
================================

Advanced, reusable UI components with cutting-edge design patterns.
Built for JobSniper AI with glassmorphism, animations, and modern aesthetics.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Union, Any
import json
from ..core.ui_constants import UIConstants


class QuantumComponents:
    """Advanced UI components library"""
    
    @staticmethod
    def quantum_header(title: str, subtitle: str = "", icon: str = "🎯", 
                      gradient: str = "aurora") -> None:
        """Create a quantum header with animated background"""
        
        gradients = {
            "aurora": UIConstants.COLORS['gradient_aurora'],
            "ocean": UIConstants.COLORS['gradient_ocean'],
            "sunset": UIConstants.COLORS['gradient_sunset'],
            "cosmic": f"linear-gradient(135deg, {UIConstants.DESIGN['colors']['primary']} 0%, {UIConstants.DESIGN['colors']['secondary']} 50%, {UIConstants.DESIGN['colors']['info']} 100%)"
        }
        
        st.markdown(f"""
        <div style="
            background: {gradients.get(gradient, gradients['aurora'])};
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            padding: 4rem 2rem;
            border-radius: 24px;
            text-align: center;
            margin-bottom: 3rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
            "></div>
            <div style="position: relative; z-index: 1;">
                <div style="font-size: 5rem; margin-bottom: 1rem; animation: pulse 2s infinite;">{icon}</div>
                <h1 style="
                    font-family: 'Poppins', sans-serif;
                    font-size: 3.5rem;
                    font-weight: 800;
                    color: white;
                    margin: 0 0 1rem 0;
                    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
                ">{title}</h1>
                {f'<p style="font-size: 1.25rem; color: rgba(255, 255, 255, 0.9); margin: 0; font-weight: 500;">{subtitle}</p>' if subtitle else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def quantum_card(content: str, title: str = "", card_type: str = "glass", 
                    hover_effect: bool = True, padding: str = "2rem") -> None:
        """Create advanced quantum cards"""
        
        card_styles = {
            "glass": """
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            """,
            "neuro": """
                background: linear-gradient(145deg, #f0f0f0, #cacaca);
                box-shadow: 20px 20px 60px #bebebe, -20px -20px 60px #ffffff;
            """,
            "gradient": """
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                box-shadow: 0 0 40px rgba(99, 102, 241, 0.4);
            """,
            "solid": """
                background: white;
                border: 1px solid #E5E7EB;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            """
        }
        
        hover_transform = "transform: translateY(-8px) scale(1.02);" if hover_effect else ""
        title_html = f'<h3 style="margin: 0 0 1.5rem 0; font-weight: 700; font-size: 1.5rem;">{title}</h3>' if title else ''
        
        st.markdown(f"""
        <div style="
            {card_styles.get(card_type, card_styles['glass'])}
            border-radius: 20px;
            padding: {padding};
            margin-bottom: 2rem;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        " onmouseover="this.style.cssText += '{hover_transform}'"
           onmouseout="this.style.transform = 'translateY(0) scale(1)';">
            {title_html}
            {content}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def quantum_metrics_grid(metrics: List[Dict[str, str]], columns: int = 4) -> None:
        """Create a responsive metrics grid"""
        
        st.markdown(f"""
        <div style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        ">
        """, unsafe_allow_html=True)
        
        for metric in metrics:
            icon = metric.get('icon', '📊')
            value = metric.get('value', '0')
            label = metric.get('label', 'Metric')
            trend = metric.get('trend', '')
            color = metric.get('color', 'blue')
            
            color_map = {
                'blue': '#3B82F6',
                'green': '#10B981', 
                'purple': '#8B5CF6',
                'orange': '#F59E0B',
                'red': '#EF4444',
                'cyan': '#06B6D4'
            }
            
            trend_html = f'<div style="color: {color_map.get(color, "#3B82F6")}; font-size: 0.875rem; font-weight: 600; margin-top: 0.5rem;">{trend}</div>' if trend else ''
            
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 2rem;
                text-align: center;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            " onmouseover="this.style.transform = 'translateY(-4px)'; this.style.boxShadow = '0 0 30px rgba(99, 102, 241, 0.3)';"
               onmouseout="this.style.transform = 'translateY(0)'; this.style.boxShadow = 'none';">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">{icon}</div>
                <div style="
                    font-size: 2.5rem;
                    font-weight: 800;
                    background: linear-gradient(135deg, {color_map.get(color, "#3B82F6")} 0%, {color_map.get(color, "#3B82F6")}80 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin-bottom: 0.5rem;
                ">{value}</div>
                <div style="
                    font-size: 0.875rem;
                    font-weight: 600;
                    color: #6B7280;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                ">{label}</div>
                {trend_html}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    @staticmethod
    def quantum_progress_ring(value: float, max_value: float = 100, 
                             label: str = "", size: int = 120, 
                             color: str = "#3B82F6") -> None:
        """Create an animated progress ring"""
        
        percentage = (value / max_value) * 100
        circumference = 2 * 3.14159 * 45  # radius = 45
        stroke_dasharray = circumference
        stroke_dashoffset = circumference - (percentage / 100) * circumference
        
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <div style="position: relative; display: inline-block;">
                <svg width="{size}" height="{size}" style="transform: rotate(-90deg);">
                    <circle
                        cx="{size//2}"
                        cy="{size//2}"
                        r="45"
                        stroke="#E5E7EB"
                        stroke-width="8"
                        fill="transparent"
                    />
                    <circle
                        cx="{size//2}"
                        cy="{size//2}"
                        r="45"
                        stroke="{color}"
                        stroke-width="8"
                        fill="transparent"
                        stroke-dasharray="{stroke_dasharray}"
                        stroke-dashoffset="{stroke_dashoffset}"
                        stroke-linecap="round"
                        style="transition: stroke-dashoffset 2s ease-in-out;"
                    />
                </svg>
                <div style="
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    font-size: 1.5rem;
                    font-weight: 800;
                    color: {color};
                ">{percentage:.1f}%</div>
            </div>
            {f'<div style="margin-top: 1rem; font-weight: 600; color: #374151;">{label}</div>' if label else ''}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def quantum_feature_showcase(features: List[Dict[str, str]], 
                                layout: str = "grid") -> None:
        """Create a feature showcase section"""
        
        if layout == "grid":
            st.markdown("""
            <div style="
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                margin: 3rem 0;
            ">
            """, unsafe_allow_html=True)
            
            for feature in features:
                icon = feature.get('icon', '⭐')
                title = feature.get('title', 'Feature')
                description = feature.get('description', 'Description')
                action = feature.get('action', '')
                
                action_html = f'<div style="margin-top: 1.5rem;"><a href="#" class="quantum-btn quantum-btn-primary">{action}</a></div>' if action else ''
                
                st.markdown(f"""
                <div style="
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(20px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 20px;
                    padding: 2rem;
                    text-align: center;
                    transition: all 0.3s ease;
                    height: 100%;
                " onmouseover="this.style.transform = 'translateY(-8px)'; this.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.1)';"
                   onmouseout="this.style.transform = 'translateY(0)'; this.style.boxShadow = 'none';">
                    <div style="font-size: 3rem; margin-bottom: 1.5rem;">{icon}</div>
                    <h3 style="margin: 0 0 1rem 0; font-weight: 700; color: #1F2937;">{title}</h3>
                    <p style="color: #6B7280; line-height: 1.6; margin: 0;">{description}</p>
                    {action_html}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    @staticmethod
    def quantum_status_indicator(status: str, label: str = "", 
                               size: str = "md") -> str:
        """Create quantum status indicators"""
        
        status_config = {
            "online": {"color": "#10B981", "bg": "rgba(16, 185, 129, 0.1)", "icon": "🟢"},
            "offline": {"color": "#EF4444", "bg": "rgba(239, 68, 68, 0.1)", "icon": "🔴"},
            "warning": {"color": "#F59E0B", "bg": "rgba(245, 158, 11, 0.1)", "icon": "🟡"},
            "processing": {"color": "#3B82F6", "bg": "rgba(59, 130, 246, 0.1)", "icon": "🔵"},
            "success": {"color": "#10B981", "bg": "rgba(16, 185, 129, 0.1)", "icon": "✅"},
            "error": {"color": "#EF4444", "bg": "rgba(239, 68, 68, 0.1)", "icon": "❌"}
        }
        
        sizes = {
            "sm": {"padding": "0.25rem 0.75rem", "font": "0.75rem"},
            "md": {"padding": "0.5rem 1rem", "font": "0.875rem"},
            "lg": {"padding": "0.75rem 1.5rem", "font": "1rem"}
        }
        
        config = status_config.get(status.lower(), status_config["offline"])
        size_config = sizes.get(size, sizes["md"])
        
        return f"""
        <span style="
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: {size_config['padding']};
            background: {config['bg']};
            color: {config['color']};
            border: 1px solid {config['color']}40;
            border-radius: 50px;
            font-size: {size_config['font']};
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        ">
            <span>{config['icon']}</span>
            <span>{label or status}</span>
        </span>
        """
    
    @staticmethod
    def quantum_timeline(events: List[Dict[str, str]]) -> None:
        """Create a quantum timeline component"""
        
        st.markdown("""
        <div style="position: relative; margin: 3rem 0;">
            <div style="
                position: absolute;
                left: 2rem;
                top: 0;
                bottom: 0;
                width: 2px;
                background: linear-gradient(to bottom, #3B82F6, #8B5CF6, #EC4899);
            "></div>
        """, unsafe_allow_html=True)
        
        for i, event in enumerate(events):
            title = event.get('title', 'Event')
            description = event.get('description', '')
            time = event.get('time', '')
            icon = event.get('icon', '📅')
            
            st.markdown(f"""
            <div style="
                position: relative;
                margin-left: 4rem;
                margin-bottom: 2rem;
                padding: 1.5rem;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
            ">
                <div style="
                    position: absolute;
                    left: -3rem;
                    top: 1.5rem;
                    width: 2rem;
                    height: 2rem;
                    background: linear-gradient(135deg, #3B82F6, #8B5CF6);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 0.875rem;
                ">{icon}</div>
                
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                    <h4 style="margin: 0; font-weight: 700; color: #1F2937;">{title}</h4>
                    {f'<span style="color: #6B7280; font-size: 0.875rem; font-weight: 500;">{time}</span>' if time else ''}
                </div>
                
                {f'<p style="margin: 0; color: #6B7280; line-height: 1.6;">{description}</p>' if description else ''}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    @staticmethod
    def quantum_chart_container(chart_content: str, title: str = "", 
                              height: str = "400px") -> None:
        """Create a quantum container for charts"""
        
        title_html = f'<h3 style="margin: 0 0 1.5rem 0; font-weight: 700; text-align: center;">{title}</h3>' if title else ''
        
        st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            height: {height};
        ">
            {title_html}
            <div style="height: calc(100% - 3rem);">
                {chart_content}
            </div>
        </div>
        """, unsafe_allow_html=True)


# Convenience functions for easy use
def quantum_header(title: str, subtitle: str = "", icon: str = "🎯", gradient: str = "aurora"):
    """Create quantum header"""
    QuantumComponents.quantum_header(title, subtitle, icon, gradient)

def quantum_card(content: str, title: str = "", card_type: str = "glass", hover_effect: bool = True):
    """Create quantum card"""
    QuantumComponents.quantum_card(content, title, card_type, hover_effect)

def quantum_metrics_grid(metrics: List[Dict[str, str]], columns: int = 4):
    """Create quantum metrics grid"""
    QuantumComponents.quantum_metrics_grid(metrics, columns)

def quantum_metrics(metrics: List[Dict[str, str]], columns: int = 4):
    """Create quantum metrics grid (alias for backward compatibility)"""
    QuantumComponents.quantum_metrics_grid(metrics, columns)

def quantum_progress(value: float, max_value: float = 100, label: str = "", color: str = "#3B82F6"):
    """Create quantum progress ring"""
    QuantumComponents.quantum_progress_ring(value, max_value, label, color=color)

def quantum_features(features: List[Dict[str, str]], layout: str = "grid"):
    """Create quantum feature showcase"""
    QuantumComponents.quantum_feature_showcase(features, layout)

def quantum_status(status: str, label: str = "", size: str = "md") -> str:
    """Create quantum status indicator"""
    return QuantumComponents.quantum_status_indicator(status, label, size)

def quantum_timeline(events: List[Dict[str, str]]):
    """Create quantum timeline"""
    QuantumComponents.quantum_timeline(events)