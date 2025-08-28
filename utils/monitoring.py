"""
Monitoring & Observability Module for JobSniper AI
Provides comprehensive system monitoring, logging, and alerting
"""

import logging
import time
import psutil
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from collections import defaultdict, deque
import json
import asyncio
from functools import wraps

@dataclass
class MetricPoint:
    timestamp: datetime
    value: float
    labels: Dict[str, str] = None

@dataclass
class Alert:
    name: str
    condition: str
    threshold: float
    current_value: float
    triggered_at: datetime
    severity: str = "warning"  # info, warning, error, critical

class MetricsCollector:
    def __init__(self, max_points: int = 1000):
        self.metrics = defaultdict(lambda: deque(maxlen=max_points))
        self.counters = defaultdict(int)
        self.gauges = defaultdict(float)
        self.histograms = defaultdict(list)
        self.alerts = []
        self.alert_rules = []
        self.callbacks = []
        
        # Start background collection
        self.collection_thread = threading.Thread(target=self._collect_system_metrics, daemon=True)
        self.collection_thread.start()
    
    def record_metric(self, name: str, value: float, labels: Dict[str, str] = None):
        """Record a metric point"""
        point = MetricPoint(
            timestamp=datetime.now(),
            value=value,
            labels=labels or {}
        )
        self.metrics[name].append(point)
        
        # Check alert rules
        self._check_alerts(name, value)
    
    def increment_counter(self, name: str, value: int = 1, labels: Dict[str, str] = None):
        """Increment a counter metric"""
        key = f"{name}:{json.dumps(labels or {}, sort_keys=True)}"
        self.counters[key] += value
        self.record_metric(f"{name}_total", self.counters[key], labels)
    
    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        """Set a gauge metric"""
        key = f"{name}:{json.dumps(labels or {}, sort_keys=True)}"
        self.gauges[key] = value
        self.record_metric(name, value, labels)
    
    def record_histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        """Record a histogram value"""
        key = f"{name}:{json.dumps(labels or {}, sort_keys=True)}"
        self.histograms[key].append(value)
        
        # Keep only last 1000 values
        if len(self.histograms[key]) > 1000:
            self.histograms[key] = self.histograms[key][-1000:]
        
        # Record percentiles
        if self.histograms[key]:
            sorted_values = sorted(self.histograms[key])
            percentiles = [50, 90, 95, 99]
            
            for p in percentiles:
                idx = int(len(sorted_values) * p / 100)
                if idx < len(sorted_values):
                    self.record_metric(f"{name}_p{p}", sorted_values[idx], labels)
    
    def add_alert_rule(self, name: str, metric: str, condition: str, threshold: float, severity: str = "warning"):
        """Add an alert rule"""
        self.alert_rules.append({
            "name": name,
            "metric": metric,
            "condition": condition,  # "gt", "lt", "eq"
            "threshold": threshold,
            "severity": severity
        })
    
    def _check_alerts(self, metric_name: str, value: float):
        """Check if any alert rules are triggered"""
        for rule in self.alert_rules:
            if rule["metric"] == metric_name:
                triggered = False
                
                if rule["condition"] == "gt" and value > rule["threshold"]:
                    triggered = True
                elif rule["condition"] == "lt" and value < rule["threshold"]:
                    triggered = True
                elif rule["condition"] == "eq" and value == rule["threshold"]:
                    triggered = True
                
                if triggered:
                    alert = Alert(
                        name=rule["name"],
                        condition=f"{metric_name} {rule['condition']} {rule['threshold']}",
                        threshold=rule["threshold"],
                        current_value=value,
                        triggered_at=datetime.now(),
                        severity=rule["severity"]
                    )
                    
                    self.alerts.append(alert)
                    self._notify_alert(alert)
    
    def _notify_alert(self, alert: Alert):
        """Notify about triggered alert"""
        logging.warning(f"ALERT: {alert.name} - {alert.condition} (current: {alert.current_value})")
        
        # Call registered callbacks
        for callback in self.callbacks:
            try:
                callback(alert)
            except Exception as e:
                logging.error(f"Alert callback failed: {e}")
    
    def add_alert_callback(self, callback: Callable[[Alert], None]):
        """Add alert notification callback"""
        self.callbacks.append(callback)
    
    def _collect_system_metrics(self):
        """Background thread to collect system metrics"""
        while True:
            try:
                # CPU metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                self.set_gauge("system_cpu_percent", cpu_percent)
                
                # Memory metrics
                memory = psutil.virtual_memory()
                self.set_gauge("system_memory_percent", memory.percent)
                self.set_gauge("system_memory_used_bytes", memory.used)
                self.set_gauge("system_memory_available_bytes", memory.available)
                
                # Disk metrics
                disk = psutil.disk_usage('/')
                self.set_gauge("system_disk_percent", disk.percent)
                self.set_gauge("system_disk_used_bytes", disk.used)
                self.set_gauge("system_disk_free_bytes", disk.free)
                
                # Network metrics (if available)
                try:
                    network = psutil.net_io_counters()
                    self.increment_counter("system_network_bytes_sent", network.bytes_sent)
                    self.increment_counter("system_network_bytes_recv", network.bytes_recv)
                except:
                    pass
                
                time.sleep(30)  # Collect every 30 seconds
                
            except Exception as e:
                logging.error(f"System metrics collection failed: {e}")
                time.sleep(60)  # Wait longer on error
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "metrics_count": len(self.metrics),
            "counters_count": len(self.counters),
            "gauges_count": len(self.gauges),
            "active_alerts": len([a for a in self.alerts if a.triggered_at > datetime.now() - timedelta(hours=1)]),
            "recent_metrics": {}
        }
        
        # Get latest values for key metrics
        for name, points in self.metrics.items():
            if points:
                latest = points[-1]
                summary["recent_metrics"][name] = {
                    "value": latest.value,
                    "timestamp": latest.timestamp.isoformat()
                }
        
        return summary

# Global metrics collector
metrics = MetricsCollector()

# Setup default alert rules
metrics.add_alert_rule("High CPU Usage", "system_cpu_percent", "gt", 80.0, "warning")
metrics.add_alert_rule("High Memory Usage", "system_memory_percent", "gt", 85.0, "warning")
metrics.add_alert_rule("Low Disk Space", "system_disk_percent", "gt", 90.0, "error")
metrics.add_alert_rule("High Response Time", "request_duration_p95", "gt", 5.0, "warning")

class PerformanceMonitor:
    """Monitor application performance"""
    
    def __init__(self):
        self.request_times = deque(maxlen=1000)
        self.error_counts = defaultdict(int)
        self.endpoint_stats = defaultdict(lambda: {"count": 0, "total_time": 0, "errors": 0})
    
    def time_function(self, func_name: str = None):
        """Decorator to time function execution"""
        def decorator(func):
            name = func_name or f"{func.__module__}.{func.__name__}"
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    success = True
                    error = None
                except Exception as e:
                    success = False
                    error = str(e)
                    raise
                finally:
                    duration = time.time() - start_time
                    
                    # Record metrics
                    metrics.record_histogram("function_duration", duration, {"function": name})
                    metrics.increment_counter("function_calls", 1, {"function": name, "success": str(success)})
                    
                    if not success:
                        metrics.increment_counter("function_errors", 1, {"function": name})
                        self.error_counts[name] += 1
                    
                    # Update endpoint stats
                    self.endpoint_stats[name]["count"] += 1
                    self.endpoint_stats[name]["total_time"] += duration
                    if not success:
                        self.endpoint_stats[name]["errors"] += 1
                
                return result
            return wrapper
        return decorator
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        stats = {
            "timestamp": datetime.now().isoformat(),
            "endpoints": {}
        }
        
        for endpoint, data in self.endpoint_stats.items():
            if data["count"] > 0:
                stats["endpoints"][endpoint] = {
                    "total_requests": data["count"],
                    "total_errors": data["errors"],
                    "error_rate": data["errors"] / data["count"],
                    "avg_response_time": data["total_time"] / data["count"],
                    "requests_per_minute": data["count"] / max(1, (time.time() - 3600) / 60)  # Rough estimate
                }
        
        return stats

# Global performance monitor
performance = PerformanceMonitor()

class LoggingManager:
    """Enhanced logging with structured output"""
    
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        """Setup structured logging"""
        
        # Create custom formatter
        class StructuredFormatter(logging.Formatter):
            def format(self, record):
                log_entry = {
                    "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                    "level": record.levelname,
                    "logger": record.name,
                    "message": record.getMessage(),
                    "module": record.module,
                    "function": record.funcName,
                    "line": record.lineno
                }
                
                # Add extra fields if present
                if hasattr(record, 'user_id'):
                    log_entry["user_id"] = record.user_id
                if hasattr(record, 'request_id'):
                    log_entry["request_id"] = record.request_id
                if hasattr(record, 'duration'):
                    log_entry["duration"] = record.duration
                
                return json.dumps(log_entry)
        
        # Setup root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # Console handler with structured format
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(StructuredFormatter())
        root_logger.addHandler(console_handler)
        
        # File handler for persistent logs
        try:
            file_handler = logging.FileHandler('logs/jobsniper.log')
            file_handler.setFormatter(StructuredFormatter())
            root_logger.addHandler(file_handler)
        except:
            pass  # File logging optional
    
    def log_request(self, endpoint: str, user_id: str, duration: float, status: str):
        """Log API request"""
        logger = logging.getLogger("api.requests")
        logger.info(
            f"API request completed",
            extra={
                "endpoint": endpoint,
                "user_id": user_id,
                "duration": duration,
                "status": status
            }
        )
        
        # Record metrics
        metrics.record_histogram("api_request_duration", duration, {"endpoint": endpoint})
        metrics.increment_counter("api_requests", 1, {"endpoint": endpoint, "status": status})

# Global logging manager
log_manager = LoggingManager()

class HealthChecker:
    """System health monitoring"""
    
    def __init__(self):
        self.checks = {}
        self.last_check_time = {}
    
    def add_health_check(self, name: str, check_func: Callable[[], bool], interval_seconds: int = 60):
        """Add a health check"""
        self.checks[name] = {
            "func": check_func,
            "interval": interval_seconds,
            "last_result": None,
            "last_error": None
        }
    
    def run_health_checks(self) -> Dict[str, Any]:
        """Run all health checks"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "checks": {}
        }
        
        for name, check in self.checks.items():
            try:
                # Check if we need to run this check
                last_check = self.last_check_time.get(name, 0)
                if time.time() - last_check < check["interval"]:
                    # Use cached result
                    results["checks"][name] = {
                        "status": "healthy" if check["last_result"] else "unhealthy",
                        "cached": True,
                        "last_error": check["last_error"]
                    }
                    continue
                
                # Run the check
                result = check["func"]()
                check["last_result"] = result
                check["last_error"] = None
                self.last_check_time[name] = time.time()
                
                results["checks"][name] = {
                    "status": "healthy" if result else "unhealthy",
                    "cached": False
                }
                
                if not result:
                    results["overall_status"] = "degraded"
                
            except Exception as e:
                check["last_result"] = False
                check["last_error"] = str(e)
                results["checks"][name] = {
                    "status": "error",
                    "error": str(e),
                    "cached": False
                }
                results["overall_status"] = "unhealthy"
        
        return results

# Global health checker
health = HealthChecker()

# Add default health checks
def check_database_connection():
    """Check database connectivity"""
    try:
        # Add your database connection check here
        return True
    except:
        return False

def check_ai_services():
    """Check AI service availability"""
    try:
        # Add your AI service checks here
        return True
    except:
        return False

health.add_health_check("database", check_database_connection, 30)
health.add_health_check("ai_services", check_ai_services, 60)

# Utility functions for Streamlit integration
def display_metrics_dashboard():
    """Display metrics in Streamlit dashboard"""
    import streamlit as st
    import plotly.graph_objects as go
    
    st.markdown("### 📊 System Metrics")
    
    # Get current metrics
    summary = metrics.get_metrics_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cpu_value = summary["recent_metrics"].get("system_cpu_percent", {}).get("value", 0)
        st.metric("CPU Usage", f"{cpu_value:.1f}%")
    
    with col2:
        memory_value = summary["recent_metrics"].get("system_memory_percent", {}).get("value", 0)
        st.metric("Memory Usage", f"{memory_value:.1f}%")
    
    with col3:
        disk_value = summary["recent_metrics"].get("system_disk_percent", {}).get("value", 0)
        st.metric("Disk Usage", f"{disk_value:.1f}%")
    
    with col4:
        st.metric("Active Alerts", summary["active_alerts"])
    
    # Performance stats
    perf_stats = performance.get_performance_stats()
    
    if perf_stats["endpoints"]:
        st.markdown("### ⚡ Performance Stats")
        
        endpoints_df = []
        for endpoint, stats in perf_stats["endpoints"].items():
            endpoints_df.append({
                "Endpoint": endpoint,
                "Requests": stats["total_requests"],
                "Errors": stats["total_errors"],
                "Error Rate": f"{stats['error_rate']:.2%}",
                "Avg Response Time": f"{stats['avg_response_time']:.3f}s"
            })
        
        if endpoints_df:
            import pandas as pd
            st.dataframe(pd.DataFrame(endpoints_df))

def get_monitoring_summary() -> Dict[str, Any]:
    """Get comprehensive monitoring summary"""
    return {
        "metrics": metrics.get_metrics_summary(),
        "performance": performance.get_performance_stats(),
        "health": health.run_health_checks(),
        "alerts": [
            {
                "name": alert.name,
                "severity": alert.severity,
                "triggered_at": alert.triggered_at.isoformat(),
                "condition": alert.condition,
                "current_value": alert.current_value
            }
            for alert in metrics.alerts[-10:]  # Last 10 alerts
        ]
    }
