"""
HRM Phase 5 Production System: Real-World Integration
===================================================

This module provides the complete Phase 5 system that integrates
real MCP tools with the automated execution engine for production use.

Author: HRM Implementation Team
Date: August 2025  
Phase: 5 - Real-World Integration
Status: Production Integration Complete
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from .hrm_automation_engine import (
    AutomatedExecutionEngine, 
    HRMExecutionResult,
    ComplexityAnalyzer,
    PatternOrchestrator,
    ConvergenceAnalyzer,
    InsightGenerator
)
from .hrm_real_mcp import ProductionMCPIntegration

logger = logging.getLogger(__name__)


class Phase5ExecutionEngine(AutomatedExecutionEngine):
    """
    Phase 5 execution engine with real MCP tool integration
    
    This extends the Phase 4 automation engine with real MCP tool calls,
    providing production-ready hierarchical reasoning with actual tools.
    """
    
    def __init__(self, max_retries: int = 3, convergence_threshold: float = 0.75, use_real_tools: bool = True):
        # Initialize base components
        self.complexity_analyzer = ComplexityAnalyzer()
        self.pattern_orchestrator = PatternOrchestrator()
        self.convergence_analyzer = ConvergenceAnalyzer(convergence_threshold)
        self.insight_generator = InsightGenerator()
        
        # Phase 5: Real MCP integration
        self.mcp_integration = ProductionMCPIntegration(use_real_tools=use_real_tools)
        
        self.max_retries = max_retries
        self.execution_history = []
        
        logger.info(f"🚀 Phase 5 HRM Engine initialized with {'real' if use_real_tools else 'mock'} MCP tools")
    
    async def _execute_pattern_with_retries(self, pattern: List[str], query: str) -> List:
        """Execute pattern with real MCP tools and enhanced error handling"""
        results = []
        context = query
        
        for i, tool_name in enumerate(pattern):
            logger.info(f"📋 Step {i+1}/{len(pattern)}: Executing {tool_name}")
            
            # Execute with retries using real MCP integration
            for attempt in range(self.max_retries):
                try:
                    # Prepare tool-specific parameters
                    if tool_name == 'brain_recall':
                        params = {'query': context, 'limit': 10}
                    elif tool_name == 'web_search':
                        params = {'query': context}
                    elif tool_name == 'brain_remember':
                        synthesis_key = f"hrm_phase5_{len(self.execution_history)}_{i}_{tool_name}"
                        synthesis_content = {
                            'query': query,
                            'context': context[:500],  # Limit context size
                            'step': i + 1,
                            'tool': tool_name,
                            'timestamp': '2025-08-04T04:40:00Z'
                        }
                        params = {'key': synthesis_key, 'value': synthesis_content, 'memory_type': 'hrm_synthesis'}
                    elif tool_name == 'sequential_thinking':
                        params = {'thought': context, 'problem_type': 'analysis'}
                    elif tool_name == 'reasoning_tools':
                        params = {'problem': context, 'problem_type': 'systematic'}
                    else:
                        params = {'query': context}
                    
                    # Execute with real MCP integration
                    result = await self.mcp_integration.execute_tool(tool_name, **params)
                    result.retry_count = attempt
                    
                    if result.success:
                        results.append(result)
                        
                        # Enhanced context chaining for better reasoning
                        if result.data and isinstance(result.data, dict):
                            if 'final_answer' in result.data:
                                context = f"{context} | Analysis: {result.data['final_answer'][:150]}"
                            elif 'verification_result' in result.data:
                                context = f"{context} | Verification: {result.data['verification_result'][:150]}"
                            elif 'memories' in result.data and result.data['memories']:
                                top_memory = result.data['memories'][0]['content'][:150]
                                context = f"{context} | Memory: {top_memory}"
                            elif 'results' in result.data and result.data['results']:
                                top_result = result.data['results'][0]['snippet'][:150]
                                context = f"{context} | Search: {top_result}"
                            else:
                                context = f"{context} | Output: {str(result.data)[:150]}"
                        
                        logger.info(f"  ✅ {tool_name} completed (confidence: {result.confidence:.2f})")
                        break  # Success
                    else:
                        logger.warning(f"  ⚠️ Attempt {attempt + 1} failed: {result.error_message}")
                        if attempt == self.max_retries - 1:
                            results.append(result)  # Add failed result
                        else:
                            await asyncio.sleep(0.5 * (attempt + 1))  # Progressive retry delay
                            
                except Exception as e:
                    error_msg = f"Unexpected error in {tool_name}: {str(e)}"
                    logger.error(f"  ❌ {error_msg}")
                    
                    if attempt == self.max_retries - 1:
                        # Create error result
                        from .hrm_automation_engine import MCPExecutionResult, ExecutionPhase
                        error_result = MCPExecutionResult(
                            tool_name=tool_name,
                            success=False,
                            data=None,
                            confidence=0.0,
                            execution_time=0.0,
                            phase=ExecutionPhase.ORCHESTRATION,
                            error_message=error_msg,
                            retry_count=attempt
                        )
                        results.append(error_result)
        
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive Phase 5 engine status"""
        base_stats = super().get_status()
        integration_stats = self.mcp_integration.get_integration_status()
        
        return {
            **base_stats,
            'phase': '5 - Real-World Integration',
            'engine_status': '🚀 Phase 5 Production Ready - Real MCP Integration',
            'mcp_integration': integration_stats,
            'capabilities': [
                '✅ Real MCP tool integration',
                '✅ Production-ready automation',
                '✅ Enhanced error handling',
                '✅ Advanced context chaining',
                '✅ Comprehensive convergence analysis',
                '✅ Intelligent retry mechanisms'
            ]
        }


class HRMPhase5System:
    """
    Complete Phase 5 HRM system with real-world integration
    
    This is the production system that external applications should use
    for real-world hierarchical reasoning with actual MCP tools.
    """
    
    def __init__(self, use_real_tools: bool = True, **config):
        self.engine = Phase5ExecutionEngine(use_real_tools=use_real_tools, **config)
        self.use_real_tools = use_real_tools
        
        logger.info(f"🏭 HRM Phase 5 System Ready - {'Real' if use_real_tools else 'Mock'} MCP Integration")
    
    async def process_query(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Process query through Phase 5 HRM system with real MCP tools
        
        Args:
            query: Input query
            **kwargs: Additional options
            
        Returns:
            Comprehensive results with real MCP data
        """
        result = await self.engine.execute(query, **kwargs)
        
        return {
            'query': result.query,
            'complexity': result.complexity,
            'pattern': result.pattern,
            'mcp_results': [
                {
                    'tool_name': r.tool_name,
                    'success': r.success,
                    'confidence': r.confidence,
                    'execution_time': r.execution_time,
                    'phase': r.phase.value,
                    'error_message': r.error_message,
                    'retry_count': r.retry_count,
                    'data_preview': self._format_data_preview(r.data)
                }
                for r in result.mcp_results
            ],
            'convergence': result.convergence_data,
            'total_execution_time': result.total_execution_time,
            'success': result.success,
            'insights': result.insights,
            'next_actions': result.next_actions,
            'phase': '5 - Real-World Integration',
            'mcp_integration_status': self.engine.mcp_integration.get_integration_status()
        }
    
    def _format_data_preview(self, data: Any) -> Optional[str]:
        """Format MCP tool data for preview"""
        if not data:
            return None
        
        if isinstance(data, dict):
            # Extract most relevant information
            if 'final_answer' in data:
                return f"Analysis: {data['final_answer'][:200]}..."
            elif 'verification_result' in data:
                return f"Verification: {data['verification_result'][:200]}..."
            elif 'memories' in data and data['memories']:
                return f"Memories: {len(data['memories'])} found, top relevance: {data['memories'][0].get('relevance', 'N/A')}"
            elif 'results' in data and data['results']:
                return f"Search: {len(data['results'])} results, top: {data['results'][0].get('title', 'N/A')[:100]}..."
            else:
                return str(data)[:200] + "..." if len(str(data)) > 200 else str(data)
        else:
            return str(data)[:200] + "..." if len(str(data)) > 200 else str(data)
    
    def get_status(self) -> Dict[str, Any]:
        """Get Phase 5 system status"""
        return self.engine.get_status()


# Convenience functions for Phase 5
async def execute_hrm_phase5(query: str, use_real_tools: bool = True, **config) -> Dict[str, Any]:
    """
    Execute HRM query with Phase 5 real MCP integration
    
    Args:
        query: Input query
        use_real_tools: Whether to use real MCP tools (default: True)
        **config: Additional configuration
        
    Returns:
        Phase 5 HRM execution results
    """
    system = HRMPhase5System(use_real_tools=use_real_tools, **config)
    return await system.process_query(query)


async def compare_phase4_vs_phase5(query: str) -> Dict[str, Any]:
    """
    Compare Phase 4 (mock tools) vs Phase 5 (real tools) execution
    
    Args:
        query: Test query
        
    Returns:
        Comparison results
    """
    print(f"🔬 Comparing Phase 4 vs Phase 5 for: {query}")
    print("=" * 60)
    
    # Phase 4 execution (mock tools)
    print("\n📋 Phase 4 (Mock Tools):")
    phase4_result = await execute_hrm_phase5(query, use_real_tools=False)
    
    print(f"  Complexity: {phase4_result['complexity']}")
    print(f"  Pattern: {' → '.join(phase4_result['pattern'])}")
    print(f"  Success: {'✅' if phase4_result['success'] else '❌'}")
    print(f"  Time: {phase4_result['total_execution_time']:.2f}s")
    
    # Phase 5 execution (real tools)
    print("\n🚀 Phase 5 (Real MCP Tools):")
    phase5_result = await execute_hrm_phase5(query, use_real_tools=True)
    
    print(f"  Complexity: {phase5_result['complexity']}")
    print(f"  Pattern: {' → '.join(phase5_result['pattern'])}")
    print(f"  Success: {'✅' if phase5_result['success'] else '❌'}")
    print(f"  Time: {phase5_result['total_execution_time']:.2f}s")
    
    # Comparison analysis
    print(f"\n📊 Comparison Analysis:")
    print(f"  Complexity Detection: {'✅ Same' if phase4_result['complexity'] == phase5_result['complexity'] else '⚠️ Different'}")
    print(f"  Success Rate: Phase 4: {phase4_result['success']}, Phase 5: {phase5_result['success']}")
    print(f"  Performance: Phase 4: {phase4_result['total_execution_time']:.2f}s, Phase 5: {phase5_result['total_execution_time']:.2f}s")
    
    return {
        'phase4_result': phase4_result,
        'phase5_result': phase5_result,
        'comparison': {
            'complexity_match': phase4_result['complexity'] == phase5_result['complexity'],
            'both_successful': phase4_result['success'] and phase5_result['success'],
            'performance_difference': phase5_result['total_execution_time'] - phase4_result['total_execution_time']
        }
    }


# Example usage
async def main():
    """Demonstrate Phase 5 HRM system"""
    print("🚀 HRM Phase 5: Real-World Integration Demo")
    print("=" * 60)
    
    # Test queries
    test_queries = [
        "What is the future of artificial intelligence?",
        "Compare quantum computing advantages and limitations",
        "Design a framework for AI consciousness emergence"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🎯 Test {i}: {query}")
        print("-" * 50)
        
        result = await execute_hrm_phase5(query)
        
        print(f"Complexity: {result['complexity']}")
        print(f"Pattern: {' → '.join(result['pattern'])}")
        print(f"Success: {'✅' if result['success'] else '❌'}")
        print(f"MCP Integration: {result['mcp_integration_status']['integration_type']}")
        print(f"Tools Success Rate: {result['mcp_integration_status']['tool_stats']['success_rate']:.1%}")
        
        print(f"\nKey Insights:")
        for insight in result['insights'][:2]:
            print(f"  • {insight}")
    
    # System status
    system = HRMPhase5System()
    status = system.get_status()
    print(f"\n📊 Phase 5 System Status:")
    print(f"  Engine: {status['engine_status']}")
    print(f"  Phase: {status['phase']}")
    print(f"  Capabilities: {len(status['capabilities'])} production features")


if __name__ == "__main__":
    asyncio.run(main())
