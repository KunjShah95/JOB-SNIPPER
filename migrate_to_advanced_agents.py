#!/usr/bin/env python3
"""
Migration Script for Advanced Agents
====================================

This script helps migrate from legacy agents to the new advanced agent architecture.
It provides utilities for:
- Updating imports and method calls
- Converting data formats
- Testing compatibility
- Performance comparison
"""

import os
import sys
import json
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentMigrationTool:
    """Tool for migrating from legacy to advanced agents"""
    
    def __init__(self):
        self.migration_log = []
        self.performance_comparison = {}
        
    def migrate_controller_usage(self, legacy_code_path: str, output_path: str):
        """Migrate controller agent usage"""
        logger.info("Migrating controller agent usage...")
        
        # Read legacy code
        with open(legacy_code_path, 'r') as f:
            legacy_code = f.read()
        
        # Apply transformations
        migrated_code = self._transform_controller_code(legacy_code)
        
        # Write migrated code
        with open(output_path, 'w') as f:
            f.write(migrated_code)
        
        logger.info(f"Controller migration completed: {output_path}")
        
    def _transform_controller_code(self, code: str) -> str:
        """Transform legacy controller code to advanced version"""
        transformations = [
            # Update imports
            ('from agents.controller_agent import ControllerAgent', 
             'from agents.advanced_controller_agent import AdvancedControllerAgent'),
            
            # Update class instantiation
            ('ControllerAgent()', 'AdvancedControllerAgent()'),
            
            # Update method calls
            ('.run(', '.process('),
            
            # Update result access patterns
            ('result["parsed_data"]', 'result["comprehensive_analysis"]["resume_insights"]["parsed_data"]'),
            ('result["matched"]', 'result["comprehensive_analysis"]["job_compatibility"]'),
            ('result["skills"]', 'result["comprehensive_analysis"]["skill_development"]'),
        ]
        
        migrated_code = code
        for old, new in transformations:
            migrated_code = migrated_code.replace(old, new)
        
        return migrated_code
    
    def convert_legacy_input_format(self, legacy_input: Dict[str, Any]) -> Dict[str, Any]:
        """Convert legacy input format to advanced agent format"""
        logger.info("Converting input format...")
        
        # Legacy format typically uses message protocol
        if 'data' in legacy_input and 'sender' in legacy_input:
            # Convert from message protocol to direct input
            converted = {
                'resume_text': legacy_input.get('data', ''),
                'metadata': {
                    'source': 'legacy_migration',
                    'original_sender': legacy_input.get('sender'),
                    'migration_timestamp': datetime.now().isoformat()
                }
            }
        else:
            # Direct data format
            converted = legacy_input.copy()
            converted['metadata'] = {
                'source': 'legacy_migration',
                'migration_timestamp': datetime.now().isoformat()
            }
        
        return converted
    
    def compare_agent_performance(self, test_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare performance between legacy and advanced agents"""
        logger.info("Starting performance comparison...")
        
        results = {
            'test_count': len(test_data),
            'legacy_performance': {},
            'advanced_performance': {},
            'improvements': {}
        }
        
        # Test legacy agents (if available)
        try:
            legacy_results = self._test_legacy_agents(test_data)
            results['legacy_performance'] = legacy_results
        except Exception as e:
            logger.warning(f"Legacy agent testing failed: {e}")
            results['legacy_performance'] = {'error': str(e)}
        
        # Test advanced agents
        try:
            advanced_results = self._test_advanced_agents(test_data)
            results['advanced_performance'] = advanced_results
        except Exception as e:
            logger.error(f"Advanced agent testing failed: {e}")
            results['advanced_performance'] = {'error': str(e)}
        
        # Calculate improvements
        if 'error' not in results['legacy_performance'] and 'error' not in results['advanced_performance']:
            results['improvements'] = self._calculate_improvements(
                results['legacy_performance'], 
                results['advanced_performance']
            )
        
        return results
    
    def _test_legacy_agents(self, test_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test legacy agents performance"""
        try:
            from agents.controller_agent import ControllerAgent
            from agents.message_protocol import AgentMessage
            
            controller = ControllerAgent()
            
            total_time = 0
            success_count = 0
            error_count = 0
            
            for data in test_data:
                try:
                    start_time = time.time()
                    
                    # Convert to legacy format
                    message = AgentMessage("test", "ControllerAgent", data.get('resume_text', ''))
                    result = controller.run(message.to_json())
                    
                    end_time = time.time()
                    total_time += (end_time - start_time)
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    logger.warning(f"Legacy test failed: {e}")
            
            return {
                'total_tests': len(test_data),
                'successful_tests': success_count,
                'failed_tests': error_count,
                'average_response_time': total_time / max(success_count, 1),
                'success_rate': (success_count / len(test_data)) * 100
            }
            
        except ImportError:
            return {'error': 'Legacy agents not available'}
    
    def _test_advanced_agents(self, test_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test advanced agents performance"""
        try:
            from agents.advanced_controller_agent import AdvancedControllerAgent
            
            controller = AdvancedControllerAgent()
            
            total_time = 0
            success_count = 0
            error_count = 0
            quality_scores = []
            
            for data in test_data:
                try:
                    start_time = time.time()
                    
                    # Convert input format
                    converted_data = self.convert_legacy_input_format(data)
                    result = controller.process(converted_data)
                    
                    end_time = time.time()
                    total_time += (end_time - start_time)
                    success_count += 1
                    
                    # Extract quality score if available
                    if 'quality_assurance' in result:
                        quality_scores.append(result['quality_assurance'].get('quality_score', 0))
                    
                except Exception as e:
                    error_count += 1
                    logger.warning(f"Advanced test failed: {e}")
            
            return {
                'total_tests': len(test_data),
                'successful_tests': success_count,
                'failed_tests': error_count,
                'average_response_time': total_time / max(success_count, 1),
                'success_rate': (success_count / len(test_data)) * 100,
                'average_quality_score': sum(quality_scores) / max(len(quality_scores), 1) if quality_scores else 0
            }
            
        except ImportError as e:
            return {'error': f'Advanced agents not available: {e}'}
    
    def _calculate_improvements(self, legacy_perf: Dict[str, Any], advanced_perf: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance improvements"""
        improvements = {}
        
        # Response time improvement
        if 'average_response_time' in both_perfs := [legacy_perf, advanced_perf]:
            legacy_time = legacy_perf['average_response_time']
            advanced_time = advanced_perf['average_response_time']
            time_improvement = ((legacy_time - advanced_time) / legacy_time) * 100
            improvements['response_time_improvement'] = f"{time_improvement:.1f}%"
        
        # Success rate improvement
        if 'success_rate' in legacy_perf and 'success_rate' in advanced_perf:
            legacy_rate = legacy_perf['success_rate']
            advanced_rate = advanced_perf['success_rate']
            rate_improvement = advanced_rate - legacy_rate
            improvements['success_rate_improvement'] = f"{rate_improvement:.1f}%"
        
        # Quality score (new feature)
        if 'average_quality_score' in advanced_perf:
            improvements['quality_score'] = f"{advanced_perf['average_quality_score']:.1f}/100"
        
        return improvements
    
    def generate_migration_report(self, output_path: str):
        """Generate comprehensive migration report"""
        logger.info("Generating migration report...")
        
        report = {
            'migration_summary': {
                'timestamp': datetime.now().isoformat(),
                'tool_version': '2.0',
                'migration_steps_completed': len(self.migration_log)
            },
            'migration_log': self.migration_log,
            'performance_comparison': self.performance_comparison,
            'recommendations': self._generate_recommendations(),
            'next_steps': self._generate_next_steps()
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Migration report generated: {output_path}")
    
    def _generate_recommendations(self) -> List[str]:
        """Generate migration recommendations"""
        return [
            "Update all agent imports to use advanced versions",
            "Modify input data format to match new structure",
            "Update result access patterns for new response format",
            "Configure advanced features like caching and validation",
            "Set up performance monitoring for production deployment",
            "Test thoroughly with your specific use cases",
            "Consider gradual rollout with fallback to legacy system"
        ]
    
    def _generate_next_steps(self) -> List[str]:
        """Generate next steps for migration"""
        return [
            "Review and test migrated code thoroughly",
            "Update documentation and API references",
            "Train team on new agent capabilities",
            "Monitor performance in staging environment",
            "Plan production deployment strategy",
            "Set up monitoring and alerting for new system",
            "Prepare rollback plan if needed"
        ]

def main():
    """Main migration workflow"""
    print("🚀 JOB-SNIPPER Advanced Agents Migration Tool")
    print("=" * 50)
    
    migration_tool = AgentMigrationTool()
    
    # Example test data
    test_data = [
        {
            'resume_text': 'John Doe, Software Engineer with 5 years experience in Python and React...',
            'job_requirements': {
                'title': 'Senior Software Engineer',
                'required_skills': ['Python', 'React', 'AWS'],
                'experience_years': 5
            }
        },
        {
            'resume_text': 'Jane Smith, Data Scientist with expertise in machine learning and analytics...',
            'job_requirements': {
                'title': 'Data Scientist',
                'required_skills': ['Python', 'Machine Learning', 'SQL'],
                'experience_years': 3
            }
        }
    ]
    
    # Run performance comparison
    print("📊 Running performance comparison...")
    performance_results = migration_tool.compare_agent_performance(test_data)
    migration_tool.performance_comparison = performance_results
    
    # Display results
    print("\n📈 Performance Comparison Results:")
    print(f"Test Count: {performance_results['test_count']}")
    
    if 'error' not in performance_results['advanced_performance']:
        advanced_perf = performance_results['advanced_performance']
        print(f"Advanced Agents Success Rate: {advanced_perf['success_rate']:.1f}%")
        print(f"Advanced Agents Avg Response Time: {advanced_perf['average_response_time']:.2f}s")
        if 'average_quality_score' in advanced_perf:
            print(f"Advanced Agents Quality Score: {advanced_perf['average_quality_score']:.1f}/100")
    
    if 'improvements' in performance_results:
        improvements = performance_results['improvements']
        print("\n🎯 Improvements:")
        for metric, improvement in improvements.items():
            print(f"  {metric}: {improvement}")
    
    # Generate migration report
    print("\n📋 Generating migration report...")
    migration_tool.generate_migration_report('migration_report.json')
    
    print("\n✅ Migration analysis completed!")
    print("📄 Check 'migration_report.json' for detailed results")
    print("\n🔧 Next Steps:")
    print("1. Review the migration report")
    print("2. Update your code using the transformation patterns")
    print("3. Test thoroughly with your specific data")
    print("4. Deploy gradually with monitoring")

if __name__ == "__main__":
    main()