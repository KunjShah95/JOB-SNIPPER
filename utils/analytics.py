"""
Analytics tracking and performance monitoring
"""
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import pandas as pd

logger = logging.getLogger(__name__)

@dataclass
class AnalyticsEvent:
    """Analytics event data structure"""
    event_type: str
    timestamp: datetime
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class AnalyticsTracker:
    """Advanced analytics tracking system"""
    
    def __init__(self, storage_path: str = "data/analytics.json"):
        self.storage_path = storage_path
        self.events: List[AnalyticsEvent] = []
        self._ensure_storage_dir()
        self._load_events()
    
    def _ensure_storage_dir(self):
        """Ensure analytics storage directory exists"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
    
    def _load_events(self):
        """Load existing analytics events"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.events = [
                        AnalyticsEvent(
                            event_type=event['event_type'],
                            timestamp=datetime.fromisoformat(event['timestamp']),
                            user_id=event.get('user_id'),
                            session_id=event.get('session_id'),
                            data=event.get('data')
                        )
                        for event in data
                    ]
                logger.info(f"Loaded {len(self.events)} analytics events")
        except Exception as e:
            logger.error(f"Error loading analytics: {e}")
            self.events = []
    
    def _save_events(self):
        """Save analytics events to storage"""
        try:
            data = []
            for event in self.events:
                event_dict = asdict(event)
                event_dict['timestamp'] = event.timestamp.isoformat()
                data.append(event_dict)
            
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving analytics: {e}")
    
    def track_event(self, event_type: str, data: Optional[Dict[str, Any]] = None,
                   user_id: Optional[str] = None, session_id: Optional[str] = None):
        """Track a custom analytics event"""
        try:
            event = AnalyticsEvent(
                event_type=event_type,
                timestamp=datetime.now(),
                user_id=user_id,
                session_id=session_id,
                data=data or {}
            )
            
            self.events.append(event)
            self._save_events()
            
            logger.info(f"Tracked event: {event_type}")
            
        except Exception as e:
            logger.error(f"Error tracking event: {e}")
    
    def track_analysis(self, filename: str, score: float, 
                      user_id: Optional[str] = None, session_id: Optional[str] = None):
        """Track resume analysis event"""
        self.track_event(
            event_type="resume_analysis",
            data={
                "filename": filename,
                "score": score,
                "file_extension": filename.split('.')[-1] if '.' in filename else 'unknown'
            },
            user_id=user_id,
            session_id=session_id
        )
    
    def track_job_match(self, match_score: float, job_title: Optional[str] = None,
                       user_id: Optional[str] = None, session_id: Optional[str] = None):
        """Track job matching event"""
        self.track_event(
            event_type="job_match",
            data={
                "match_score": match_score,
                "job_title": job_title
            },
            user_id=user_id,
            session_id=session_id
        )
    
    def track_skill_recommendation(self, recommended_skills: List[str],
                                 user_id: Optional[str] = None, session_id: Optional[str] = None):
        """Track skill recommendation event"""
        self.track_event(
            event_type="skill_recommendation",
            data={
                "recommended_skills": recommended_skills,
                "skill_count": len(recommended_skills)
            },
            user_id=user_id,
            session_id=session_id
        )
    
    def get_analytics_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get analytics summary for the last N days"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_events = [e for e in self.events if e.timestamp >= cutoff_date]
            
            if not recent_events:
                return {
                    "total_events": 0,
                    "event_types": {},
                    "daily_activity": {},
                    "average_scores": {}
                }
            
            # Event type breakdown
            event_types = {}
            for event in recent_events:
                event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
            
            # Daily activity
            daily_activity = {}
            for event in recent_events:
                date_key = event.timestamp.strftime('%Y-%m-%d')
                daily_activity[date_key] = daily_activity.get(date_key, 0) + 1
            
            # Average scores for analyses
            analysis_events = [e for e in recent_events if e.event_type == "resume_analysis"]
            avg_score = 0
            if analysis_events:
                scores = [e.data.get('score', 0) for e in analysis_events if e.data]
                avg_score = sum(scores) / len(scores) if scores else 0
            
            return {
                "total_events": len(recent_events),
                "event_types": event_types,
                "daily_activity": daily_activity,
                "average_score": avg_score,
                "analysis_count": len(analysis_events),
                "period_days": days
            }
            
        except Exception as e:
            logger.error(f"Error generating analytics summary: {e}")
            return {"error": str(e)}
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        try:
            analysis_events = [e for e in self.events if e.event_type == "resume_analysis"]
            
            if not analysis_events:
                return {"message": "No analysis data available"}
            
            # Extract scores
            scores = []
            file_types = {}
            
            for event in analysis_events:
                if event.data:
                    score = event.data.get('score', 0)
                    scores.append(score)
                    
                    file_ext = event.data.get('file_extension', 'unknown')
                    file_types[file_ext] = file_types.get(file_ext, 0) + 1
            
            if not scores:
                return {"message": "No score data available"}
            
            # Calculate metrics
            metrics = {
                "total_analyses": len(scores),
                "average_score": sum(scores) / len(scores),
                "min_score": min(scores),
                "max_score": max(scores),
                "score_distribution": {
                    "excellent": len([s for s in scores if s >= 0.8]),
                    "good": len([s for s in scores if 0.6 <= s < 0.8]),
                    "fair": len([s for s in scores if 0.4 <= s < 0.6]),
                    "poor": len([s for s in scores if s < 0.4])
                },
                "file_types": file_types
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return {"error": str(e)}
    
    def export_analytics(self, format: str = "json") -> Optional[str]:
        """Export analytics data"""
        try:
            if format.lower() == "json":
                return json.dumps([asdict(event) for event in self.events], 
                                default=str, indent=2)
            
            elif format.lower() == "csv":
                # Convert to DataFrame for CSV export
                data = []
                for event in self.events:
                    row = {
                        "event_type": event.event_type,
                        "timestamp": event.timestamp.isoformat(),
                        "user_id": event.user_id,
                        "session_id": event.session_id
                    }
                    
                    # Flatten data dictionary
                    if event.data:
                        for key, value in event.data.items():
                            row[f"data_{key}"] = value
                    
                    data.append(row)
                
                df = pd.DataFrame(data)
                return df.to_csv(index=False)
            
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            logger.error(f"Error exporting analytics: {e}")
            return None
    
    def cleanup_old_events(self, days: int = 90):
        """Clean up events older than specified days"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            original_count = len(self.events)
            
            self.events = [e for e in self.events if e.timestamp >= cutoff_date]
            
            cleaned_count = original_count - len(self.events)
            if cleaned_count > 0:
                self._save_events()
                logger.info(f"Cleaned up {cleaned_count} old analytics events")
            
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error cleaning up analytics: {e}")
            return 0