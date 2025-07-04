"""
JobSniper AI - Base Agent Class
===============================

Foundation class for all AI agents in the JobSniper AI platform.
Provides common functionality including prompt engineering, model management,
performance monitoring, caching, and error handling.
"""

import time
import hashlib
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

from src.core.utils.logger import get_logger, log_execution_time
from src.core.config.settings import settings

class AgentStatus(str, Enum):
    """Agent status enumeration"""
    IDLE = "idle"
    PROCESSING = "processing"
    ERROR = "error"
    DISABLED = "disabled"

class ProcessingMode(str, Enum):
    """Processing mode enumeration"""
    SYNC = "synchronous"
    ASYNC = "asynchronous"
    STREAM = "streaming"

@dataclass
class AgentMetrics:
    """Agent performance metrics"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_processing_time: float = 0.0
    average_processing_time: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    last_request_time: Optional[datetime] = None
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100
    
    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate percentage"""
        total_cache_requests = self.cache_hits + self.cache_misses
        if total_cache_requests == 0:
            return 0.0
        return (self.cache_hits / total_cache_requests) * 100

@dataclass
class AgentConfig:
    """Agent configuration"""
    name: str
    version: str = "1.0.0"
    description: str = ""
    max_retries: int = 3
    timeout: float = 30.0
    enable_caching: bool = True
    cache_ttl: int = 3600  # 1 hour
    enable_monitoring: bool = True
    processing_mode: ProcessingMode = ProcessingMode.SYNC
    model_config: Dict[str, Any] = field(default_factory=dict)
    custom_settings: Dict[str, Any] = field(default_factory=dict)

class BaseAgent(ABC):
    """
    Base class for all AI agents in JobSniper AI.
    
    Provides common functionality including:
    - Prompt engineering and management
    - Model interaction and management
    - Performance monitoring and metrics
    - Caching and optimization
    - Error handling and retry logic
    - Logging and debugging
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = get_logger(f"agent.{config.name}")
        self.status = AgentStatus.IDLE
        self.metrics = AgentMetrics()
        self.cache = {} if config.enable_caching else None
        self.created_at = datetime.now()
        
        # Initialize components
        self._initialize_components()
        
        self.logger.info(f"Agent {config.name} v{config.version} initialized")
    
    def _initialize_components(self):
        """Initialize agent components"""
        try:
            # Import components here to avoid circular imports
            from .prompt_engine import PromptEngine
            from .model_manager import ModelManager
            
            self.prompt_engine = PromptEngine(self.config.name)
            self.model_manager = ModelManager(self.config.model_config)
            
        except ImportError as e:
            self.logger.warning(f"Some components not available: {e}")
            self.prompt_engine = None
            self.model_manager = None
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process input data and return results.
        
        Args:
            input_data: Input data to process
            context: Optional context information
            
        Returns:
            Dictionary containing processing results
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Get list of agent capabilities.
        
        Returns:
            List of capability strings
        """
        pass
    
    def execute(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute agent processing with monitoring and error handling.
        
        Args:
            input_data: Input data to process
            context: Optional context information
            
        Returns:
            Dictionary containing execution results
        """
        execution_id = self._generate_execution_id()
        start_time = time.time()
        
        self.logger.info(f"Starting execution {execution_id}")
        self.status = AgentStatus.PROCESSING
        self.metrics.total_requests += 1
        self.metrics.last_request_time = datetime.now()
        
        try:
            # Check cache if enabled
            if self.cache is not None:
                cache_key = self._generate_cache_key(input_data, context)
                cached_result = self._get_from_cache(cache_key)
                
                if cached_result is not None:
                    self.metrics.cache_hits += 1
                    self.logger.info(f"Cache hit for execution {execution_id}")
                    return self._add_metadata(cached_result, execution_id, time.time() - start_time, cached=True)
                else:
                    self.metrics.cache_misses += 1
            
            # Execute processing with retry logic
            result = self._execute_with_retry(input_data, context)
            
            # Cache result if enabled
            if self.cache is not None and cache_key:
                self._store_in_cache(cache_key, result)
            
            # Update metrics
            processing_time = time.time() - start_time
            self.metrics.successful_requests += 1
            self.metrics.total_processing_time += processing_time
            self.metrics.average_processing_time = (
                self.metrics.total_processing_time / self.metrics.successful_requests
            )
            
            self.status = AgentStatus.IDLE
            self.logger.info(f"Execution {execution_id} completed successfully in {processing_time:.2f}s")
            
            return self._add_metadata(result, execution_id, processing_time)
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.metrics.failed_requests += 1
            self.status = AgentStatus.ERROR
            
            self.logger.error(f"Execution {execution_id} failed: {e}")
            
            # Return error result
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
                "metadata": {
                    "execution_id": execution_id,
                    "processing_time": processing_time,
                    "agent_name": self.config.name,
                    "agent_version": self.config.version,
                    "timestamp": datetime.now().isoformat(),
                    "cached": False
                }
            }
    
    def _execute_with_retry(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute processing with retry logic"""
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                if attempt > 0:
                    self.logger.info(f"Retry attempt {attempt}/{self.config.max_retries}")
                    time.sleep(min(2 ** attempt, 10))  # Exponential backoff, max 10s
                
                return self.process(input_data, context)
                
            except Exception as e:
                last_exception = e
                self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt == self.config.max_retries:
                    break
        
        raise last_exception
    
    def _generate_execution_id(self) -> str:
        """Generate unique execution ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"{self.config.name}_{timestamp}"
    
    def _generate_cache_key(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]]) -> str:
        """Generate cache key for input data"""
        cache_data = {
            "input": input_data,
            "context": context or {},
            "agent": self.config.name,
            "version": self.config.version
        }
        
        cache_string = json.dumps(cache_data, sort_keys=True, default=str)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get result from cache"""
        if not self.cache or cache_key not in self.cache:
            return None
        
        cached_item = self.cache[cache_key]
        
        # Check if cache item has expired
        if datetime.now() > cached_item["expires_at"]:
            del self.cache[cache_key]
            return None
        
        return cached_item["data"]
    
    def _store_in_cache(self, cache_key: str, data: Dict[str, Any]):
        """Store result in cache"""
        if not self.cache:
            return
        
        expires_at = datetime.now() + timedelta(seconds=self.config.cache_ttl)
        
        self.cache[cache_key] = {
            "data": data,
            "created_at": datetime.now(),
            "expires_at": expires_at
        }
        
        # Clean up expired cache entries periodically
        if len(self.cache) % 100 == 0:  # Every 100 entries
            self._cleanup_cache()
    
    def _cleanup_cache(self):
        """Clean up expired cache entries"""
        if not self.cache:
            return
        
        now = datetime.now()
        expired_keys = [
            key for key, item in self.cache.items()
            if now > item["expires_at"]
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            self.logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")
    
    def _add_metadata(self, result: Dict[str, Any], execution_id: str, 
                     processing_time: float, cached: bool = False) -> Dict[str, Any]:
        """Add metadata to result"""
        if not isinstance(result, dict):
            result = {"data": result}
        
        result["metadata"] = {
            "execution_id": execution_id,
            "processing_time": processing_time,
            "agent_name": self.config.name,
            "agent_version": self.config.version,
            "timestamp": datetime.now().isoformat(),
            "cached": cached,
            "success": True
        }
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status and metrics"""
        return {
            "name": self.config.name,
            "version": self.config.version,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "uptime": (datetime.now() - self.created_at).total_seconds(),
            "metrics": {
                "total_requests": self.metrics.total_requests,
                "successful_requests": self.metrics.successful_requests,
                "failed_requests": self.metrics.failed_requests,
                "success_rate": self.metrics.success_rate,
                "average_processing_time": self.metrics.average_processing_time,
                "cache_hit_rate": self.metrics.cache_hit_rate,
                "last_request_time": (
                    self.metrics.last_request_time.isoformat() 
                    if self.metrics.last_request_time else None
                )
            },
            "capabilities": self.get_capabilities(),
            "config": {
                "max_retries": self.config.max_retries,
                "timeout": self.config.timeout,
                "enable_caching": self.config.enable_caching,
                "cache_ttl": self.config.cache_ttl,
                "processing_mode": self.config.processing_mode.value
            }
        }
    
    def reset_metrics(self):
        """Reset agent metrics"""
        self.metrics = AgentMetrics()
        self.logger.info("Agent metrics reset")
    
    def clear_cache(self):
        """Clear agent cache"""
        if self.cache:
            self.cache.clear()
            self.logger.info("Agent cache cleared")
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check"""
        health_status = {
            "healthy": True,
            "issues": [],
            "checks": {}
        }
        
        # Check agent status
        if self.status == AgentStatus.ERROR:
            health_status["healthy"] = False
            health_status["issues"].append("Agent in error state")
        
        health_status["checks"]["status"] = self.status.value
        
        # Check success rate
        if self.metrics.total_requests > 10 and self.metrics.success_rate < 80:
            health_status["healthy"] = False
            health_status["issues"].append(f"Low success rate: {self.metrics.success_rate:.1f}%")
        
        health_status["checks"]["success_rate"] = self.metrics.success_rate
        
        # Check average processing time
        if self.metrics.average_processing_time > self.config.timeout * 0.8:
            health_status["healthy"] = False
            health_status["issues"].append("High processing time")
        
        health_status["checks"]["avg_processing_time"] = self.metrics.average_processing_time
        
        # Check component availability
        health_status["checks"]["prompt_engine"] = self.prompt_engine is not None
        health_status["checks"]["model_manager"] = self.model_manager is not None
        
        if not self.prompt_engine or not self.model_manager:
            health_status["issues"].append("Some components not available")
        
        return health_status
    
    def __str__(self) -> str:
        return f"{self.config.name} v{self.config.version} ({self.status.value})"
    
    def __repr__(self) -> str:
        return f"BaseAgent(name='{self.config.name}', version='{self.config.version}', status='{self.status.value}')"