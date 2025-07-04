"""Base Agent Class for JobSniper AI

Provides common functionality and interface for all AI agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging
import time
from datetime import datetime
import json


class Agent(ABC):
    """Abstract base class for all JobSniper AI agents"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.created_at = datetime.now()
        self.logger = self._setup_logger()
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0.0
        }
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logger for the agent"""
        logger = logging.getLogger(f"JobSniper.{self.name}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {self.name} - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
        
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing method - must be implemented by subclasses"""
        pass
        
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data - can be overridden by subclasses"""
        if not isinstance(input_data, dict):
            self.logger.error(f"Invalid input type: {type(input_data)}")
            return False
        return True
        
    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """Handle errors consistently across all agents"""
        error_msg = f"Error in {self.name}: {str(error)}"
        if context:
            error_msg += f" (Context: {context})"
            
        self.logger.error(error_msg)
        self.metrics['failed_requests'] += 1
        
        return {
            'success': False,
            'error': str(error),
            'agent': self.name,
            'timestamp': datetime.now().isoformat(),
            'context': context
        }
        
    def log_request(self, input_data: Dict[str, Any], output_data: Dict[str, Any], 
                   response_time: float) -> None:
        """Log request details for monitoring and debugging"""
        self.metrics['total_requests'] += 1
        if output_data.get('success', True):
            self.metrics['successful_requests'] += 1
        
        # Update average response time
        total_time = self.metrics['average_response_time'] * (self.metrics['total_requests'] - 1)
        self.metrics['average_response_time'] = (total_time + response_time) / self.metrics['total_requests']
        
        self.logger.info(f"Request processed in {response_time:.2f}s")
        
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent with error handling and logging"""
        start_time = time.time()
        
        try:
            # Validate input
            if not self.validate_input(input_data):
                return self.handle_error(
                    ValueError("Invalid input data"), 
                    "Input validation"
                )
            
            # Process the request
            result = self.process(input_data)
            
            # Ensure result has success flag
            if 'success' not in result:
                result['success'] = True
                
            # Add metadata
            result.update({
                'agent': self.name,
                'version': self.version,
                'timestamp': datetime.now().isoformat(),
                'processing_time': time.time() - start_time
            })
            
            # Log the request
            self.log_request(input_data, result, time.time() - start_time)
            
            return result
            
        except Exception as e:
            return self.handle_error(e, "Processing")
            
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        success_rate = 0.0
        if self.metrics['total_requests'] > 0:
            success_rate = (self.metrics['successful_requests'] / 
                          self.metrics['total_requests']) * 100
                          
        return {
            'agent_name': self.name,
            'version': self.version,
            'created_at': self.created_at.isoformat(),
            'total_requests': self.metrics['total_requests'],
            'successful_requests': self.metrics['successful_requests'],
            'failed_requests': self.metrics['failed_requests'],
            'success_rate': round(success_rate, 2),
            'average_response_time': round(self.metrics['average_response_time'], 3)
        }
        
    def reset_metrics(self) -> None:
        """Reset agent metrics"""
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0.0
        }
        self.logger.info("Metrics reset")
        
    def __str__(self) -> str:
        return f"{self.name} v{self.version}"
        
    def __repr__(self) -> str:
        return f"Agent(name='{self.name}', version='{self.version}')"