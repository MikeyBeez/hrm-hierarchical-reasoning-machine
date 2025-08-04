"""
HRM Advanced Convergence: Phase 5 Enhancement
============================================

This module provides advanced convergence detection and optimization
algorithms for the Phase 5 HRM system, enabling sophisticated reasoning
pattern adaptation and performance optimization.

Author: HRM Implementation Team
Date: August 2025
Phase: 5 - Advanced Features
Status: Production Enhancement
"""

import math
import statistics
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ConvergenceStrategy(Enum):
    """Convergence detection strategies"""
    CONFIDENCE_THRESHOLD = "confidence_threshold"
    DIMINISHING_RETURNS = "diminishing_returns"
    CONSENSUS_VALIDATION = "consensus_validation"
    ADAPTIVE_LEARNING = "adaptive_learning"


@dataclass
class ConvergenceMetrics:
    """Advanced convergence metrics"""
    confidence_trend: List[float]
    execution_efficiency: float
    pattern_stability: float
    information_gain: float
    convergence_score: float
    strategy_used: ConvergenceStrategy
    recommendation: str


class AdvancedConvergenceAnalyzer:
    """
    Advanced convergence analysis with multiple strategies
    
    This analyzer uses sophisticated algorithms to determine when
    hierarchical reasoning has achieved sufficient convergence,
    enabling dynamic optimization of reasoning patterns.
    """
    
    def __init__(self, base_threshold: float = 0.75):
        self.base_threshold = base_threshold
        self.convergence_history = []
        self.pattern_performance = {}
        
    def analyze_convergence(self, mcp_results: List, iteration: int = 1, 
                          complexity: str = "medium", pattern: List[str] = None) -> Dict[str, Any]:
        """
        Advanced convergence analysis using multiple strategies
        
        Args:
            mcp_results: List of MCP execution results
            iteration: Current iteration number
            complexity: Query complexity level
            pattern: Execution pattern used
            
        Returns:
            Advanced convergence analysis with recommendations
        """
        if not mcp_results:
            return self._create_convergence_result(False, "No results to analyze", ConvergenceStrategy.CONFIDENCE_THRESHOLD)
        
        # Extract confidence values and success rates
        confidences = [r.confidence for r in mcp_results if hasattr(r, 'confidence') and r.success]
        success_rate = sum(1 for r in mcp_results if hasattr(r, 'success') and r.success) / len(mcp_results)
        
        if not confidences:
            return self._create_convergence_result(False, "No successful results with confidence", ConvergenceStrategy.CONFIDENCE_THRESHOLD)
        
        # Strategy 1: Confidence Threshold Analysis
        confidence_analysis = self._analyze_confidence_threshold(confidences, success_rate, complexity)
        
        # Strategy 2: Diminishing Returns Analysis
        returns_analysis = self._analyze_diminishing_returns(confidences, mcp_results)
        
        # Strategy 3: Consensus Validation
        consensus_analysis = self._analyze_consensus_validation(mcp_results, pattern)
        
        # Strategy 4: Adaptive Learning Analysis (if we have history)
        adaptive_analysis = self._analyze_adaptive_learning(confidences, pattern, complexity)
        
        # Combine strategies for final convergence decision
        final_convergence = self._combine_convergence_strategies(
            confidence_analysis, returns_analysis, consensus_analysis, adaptive_analysis
        )
        
        # Store for learning
        self._update_convergence_history(final_convergence, pattern, complexity, confidences)
        
        return final_convergence
    
    def _analyze_confidence_threshold(self, confidences: List[float], success_rate: float, complexity: str) -> Dict[str, Any]:
        """Strategy 1: Dynamic confidence threshold based on complexity"""
        # Adjust threshold based on complexity
        complexity_thresholds = {
            'simple': 0.65,
            'medium': 0.75,
            'complex': 0.80,
            'expert': 0.85
        }
        
        threshold = complexity_thresholds.get(complexity, self.base_threshold)
        avg_confidence = statistics.mean(confidences)
        
        # Enhanced analysis considering distribution
        confidence_std = statistics.stdev(confidences) if len(confidences) > 1 else 0
        confidence_stability = 1.0 - min(confidence_std / avg_confidence, 1.0) if avg_confidence > 0 else 0
        
        converged = (avg_confidence >= threshold and 
                    success_rate >= 0.8 and 
                    confidence_stability >= 0.7)
        
        return {
            'converged': converged,
            'strategy': ConvergenceStrategy.CONFIDENCE_THRESHOLD,
            'score': avg_confidence * success_rate * confidence_stability,
            'metrics': {
                'avg_confidence': avg_confidence,
                'threshold': threshold,
                'success_rate': success_rate,
                'stability': confidence_stability
            },
            'reason': f"Confidence: {avg_confidence:.2f} vs {threshold:.2f}, Success: {success_rate:.1%}, Stability: {confidence_stability:.2f}"
        }
    
    def _analyze_diminishing_returns(self, confidences: List[float], mcp_results: List) -> Dict[str, Any]:
        """Strategy 2: Detect when additional processing yields diminishing returns"""
        if len(confidences) < 3:
            return {
                'converged': False,
                'strategy': ConvergenceStrategy.DIMINISHING_RETURNS,
                'score': 0.0,
                'reason': "Insufficient data for diminishing returns analysis"
            }
        
        # Calculate information gain between consecutive steps
        gains = []
        for i in range(1, len(confidences)):
            gain = confidences[i] - confidences[i-1]
            gains.append(max(0, gain))  # Only positive gains
        
        # Check if recent gains are diminishing
        if len(gains) >= 2:
            recent_trend = gains[-2:]
            diminishing = all(g <= 0.05 for g in recent_trend)  # Very small gains
            avg_gain = statistics.mean(gains)
            
            converged = diminishing and avg_gain < 0.1
            
            return {
                'converged': converged,
                'strategy': ConvergenceStrategy.DIMINISHING_RETURNS,
                'score': 1.0 - avg_gain if converged else avg_gain,
                'metrics': {
                    'information_gains': gains,
                    'average_gain': avg_gain,
                    'recent_trend': recent_trend
                },
                'reason': f"Information gain trend: {recent_trend}, avg: {avg_gain:.3f}"
            }
        
        return {
            'converged': False,
            'strategy': ConvergenceStrategy.DIMINISHING_RETURNS,
            'score': 0.5,
            'reason': "Insufficient trend data"
        }
    
    def _analyze_consensus_validation(self, mcp_results: List, pattern: List[str]) -> Dict[str, Any]:
        """Strategy 3: Cross-validate results for consensus"""
        if not pattern or len(mcp_results) < 2:
            return {
                'converged': False,
                'strategy': ConvergenceStrategy.CONSENSUS_VALIDATION,
                'score': 0.0,
                'reason': "Insufficient results for consensus validation"
            }
        
        # Group results by tool type for cross-validation
        tool_results = {}
        for i, result in enumerate(mcp_results):
            tool_name = result.tool_name if hasattr(result, 'tool_name') else pattern[i] if i < len(pattern) else 'unknown'
            if tool_name not in tool_results:
                tool_results[tool_name] = []
            tool_results[tool_name].append(result)
        
        # Calculate consensus based on result agreement
        consensus_scores = []
        for tool_name, results in tool_results.items():
            if len(results) >= 1:
                confidences = [r.confidence for r in results if hasattr(r, 'confidence') and r.success]
                if confidences:
                    tool_consensus = statistics.mean(confidences)
                    consensus_scores.append(tool_consensus)
        
        if consensus_scores:
            overall_consensus = statistics.mean(consensus_scores)
            consensus_stability = 1.0 - (statistics.stdev(consensus_scores) / overall_consensus) if len(consensus_scores) > 1 and overall_consensus > 0 else 1.0
            
            converged = overall_consensus >= 0.75 and consensus_stability >= 0.8
            
            return {
                'converged': converged,
                'strategy': ConvergenceStrategy.CONSENSUS_VALIDATION,
                'score': overall_consensus * consensus_stability,
                'metrics': {
                    'tool_consensus': dict(zip(tool_results.keys(), consensus_scores)),
                    'overall_consensus': overall_consensus,
                    'stability': consensus_stability
                },
                'reason': f"Consensus: {overall_consensus:.2f}, Stability: {consensus_stability:.2f}"
            }
        
        return {
            'converged': False,
            'strategy': ConvergenceStrategy.CONSENSUS_VALIDATION,
            'score': 0.0,
            'reason': "No valid consensus data"
        }
    
    def _analyze_adaptive_learning(self, confidences: List[float], pattern: List[str], complexity: str) -> Dict[str, Any]:
        """Strategy 4: Learn from historical pattern performance"""
        if not pattern:
            return {
                'converged': False,
                'strategy': ConvergenceStrategy.ADAPTIVE_LEARNING,
                'score': 0.0,
                'reason': "No pattern specified for learning"
            }
        
        pattern_key = f"{complexity}:{'-'.join(pattern)}"
        
        # Initialize pattern tracking
        if pattern_key not in self.pattern_performance:
            self.pattern_performance[pattern_key] = {
                'executions': 0,
                'avg_confidence': 0.0,
                'success_rate': 0.0,
                'confidence_history': []
            }
        
        # Current performance
        current_confidence = statistics.mean(confidences)
        
        # Historical performance
        historical_data = self.pattern_performance[pattern_key]
        
        if historical_data['executions'] > 0:
            # Compare with historical performance
            performance_delta = current_confidence - historical_data['avg_confidence']
            
            # Adaptive threshold based on historical performance
            adaptive_threshold = min(0.9, historical_data['avg_confidence'] + 0.1)
            
            converged = current_confidence >= adaptive_threshold
            
            return {
                'converged': converged,
                'strategy': ConvergenceStrategy.ADAPTIVE_LEARNING,
                'score': current_confidence / adaptive_threshold,
                'metrics': {
                    'current_confidence': current_confidence,
                    'historical_avg': historical_data['avg_confidence'],
                    'performance_delta': performance_delta,
                    'adaptive_threshold': adaptive_threshold,
                    'executions': historical_data['executions']
                },
                'reason': f"Adaptive threshold: {adaptive_threshold:.2f}, Performance delta: {performance_delta:+.3f}"
            }
        
        return {
            'converged': current_confidence >= self.base_threshold,
            'strategy': ConvergenceStrategy.ADAPTIVE_LEARNING,
            'score': current_confidence,
            'reason': "First execution for this pattern - using base threshold"
        }
    
    def _combine_convergence_strategies(self, confidence_analysis: Dict, returns_analysis: Dict, 
                                      consensus_analysis: Dict, adaptive_analysis: Dict) -> Dict[str, Any]:
        """Combine multiple convergence strategies for final decision"""
        
        strategies = [confidence_analysis, returns_analysis, consensus_analysis, adaptive_analysis]
        valid_strategies = [s for s in strategies if s.get('score', 0) > 0]
        
        if not valid_strategies:
            return self._create_convergence_result(False, "No valid convergence strategies", ConvergenceStrategy.CONFIDENCE_THRESHOLD)
        
        # Weighted combination of strategies
        weights = {
            ConvergenceStrategy.CONFIDENCE_THRESHOLD: 0.4,
            ConvergenceStrategy.DIMINISHING_RETURNS: 0.2,
            ConvergenceStrategy.CONSENSUS_VALIDATION: 0.25,
            ConvergenceStrategy.ADAPTIVE_LEARNING: 0.15
        }
        
        weighted_scores = []
        convergence_votes = 0
        strategy_details = {}
        
        for strategy in valid_strategies:
            strategy_type = strategy['strategy']
            weight = weights.get(strategy_type, 0.1)
            score = strategy.get('score', 0)
            
            weighted_scores.append(score * weight)
            if strategy.get('converged', False):
                convergence_votes += weight
            
            strategy_details[strategy_type.value] = strategy
        
        # Final convergence decision
        combined_score = sum(weighted_scores)
        converged = convergence_votes >= 0.5  # Majority vote by weight
        
        # Select primary strategy (highest score)
        primary_strategy = max(valid_strategies, key=lambda x: x.get('score', 0))
        
        return {
            'converged': converged,
            'combined_score': combined_score,
            'convergence_votes': convergence_votes,
            'primary_strategy': primary_strategy['strategy'].value,
            'strategy_details': strategy_details,
            'confidence': combined_score,
            'reason': f"Combined analysis: {convergence_votes:.1f}/1.0 vote weight, primary: {primary_strategy['strategy'].value}",
            'recommendation': self._generate_convergence_recommendation(converged, combined_score, strategy_details)
        }
    
    def _generate_convergence_recommendation(self, converged: bool, score: float, strategies: Dict) -> str:
        """Generate actionable convergence recommendation"""
        if converged:
            if score >= 0.9:
                return "Excellent convergence achieved - consider reducing future pattern complexity for efficiency"
            elif score >= 0.8:
                return "Good convergence achieved - pattern is well-optimized"
            else:
                return "Convergence achieved but with room for improvement - consider pattern refinement"
        else:
            if score >= 0.6:
                return "Near convergence - one additional iteration may achieve convergence"
            elif score >= 0.4:
                return "Moderate progress - continue with current pattern or consider tool adjustment"
            else:
                return "Low convergence - consider alternative reasoning pattern or tool selection"
    
    def _create_convergence_result(self, converged: bool, reason: str, strategy: ConvergenceStrategy) -> Dict[str, Any]:
        """Create standardized convergence result"""
        return {
            'converged': converged,
            'confidence': 0.0,
            'reason': reason,
            'strategy': strategy.value,
            'recommendation': "System needs attention - review input data and tool configuration"
        }
    
    def _update_convergence_history(self, convergence_result: Dict, pattern: List[str], 
                                   complexity: str, confidences: List[float]):
        """Update convergence history for adaptive learning"""
        if not pattern:
            return
        
        pattern_key = f"{complexity}:{'-'.join(pattern)}"
        
        # Update pattern performance tracking
        if pattern_key not in self.pattern_performance:
            self.pattern_performance[pattern_key] = {
                'executions': 0,
                'avg_confidence': 0.0,
                'success_rate': 0.0,
                'confidence_history': []
            }
        
        perf_data = self.pattern_performance[pattern_key]
        current_avg = statistics.mean(confidences)
        
        # Update running averages
        perf_data['executions'] += 1
        perf_data['confidence_history'].append(current_avg)
        perf_data['avg_confidence'] = statistics.mean(perf_data['confidence_history'])
        
        # Keep history manageable
        if len(perf_data['confidence_history']) > 50:
            perf_data['confidence_history'] = perf_data['confidence_history'][-50:]
        
        # Store convergence history
        self.convergence_history.append({
            'pattern': pattern,
            'complexity': complexity,
            'convergence_result': convergence_result,
            'timestamp': '2025-08-04T04:45:00Z'
        })
        
        # Keep convergence history manageable
        if len(self.convergence_history) > 100:
            self.convergence_history = self.convergence_history[-100:]

        """Get insights from convergence learning"""
        if not self.pattern_performance:
            return {'insights': [], 'recommendations': []}
        
        insights = []
        recommendations = []
        
        # Analyze pattern performance
        best_patterns = sorted(
            self.pattern_performance.items(),
            key=lambda x: x[1]['avg_confidence'],
            reverse=True
        )[:3]
        
        for pattern_key, perf in best_patterns:
            complexity, pattern_str = pattern_key.split(':', 1)
            insights.append(
                f"High-performing pattern for {complexity}: {pattern_str} "
                f"(avg confidence: {perf['avg_confidence']:.2f}, {perf['executions']} executions)"
            )
        
        # Performance recommendations
        if len(self.pattern_performance) >= 3:
            recommendations.append("Sufficient pattern data collected for optimization")
            recommendations.append("Consider A/B testing alternative patterns for underperforming queries")
        
        return {
            'total_patterns_learned': len(self.pattern_performance),
            'total_executions': sum(p['executions'] for p in self.pattern_performance.values()),
            'best_patterns': [p[0] for p in best_patterns],
            'insights': insights,
            'recommendations': recommendations
        }


# Integration test
async def test_advanced_convergence():
    """Test advanced convergence analysis"""
    print("🧪 Testing Advanced Convergence Analysis")
    print("=" * 45)
    
    # Mock MCP results for testing
    @dataclass
    class MockResult:
        tool_name: str
        success: bool
        confidence: float
    
    test_cases = [
        {
            'name': 'High Confidence Convergence',
            'results': [
                MockResult('brain_recall', True, 0.92),
                MockResult('web_search', True, 0.88),
                MockResult('brain_remember', True, 0.90)
            ],
            'pattern': ['brain_recall', 'web_search', 'brain_remember'],
            'complexity': 'medium'
        },
        {
            'name': 'Diminishing Returns',
            'results': [
                MockResult('brain_recall', True, 0.70),
                MockResult('sequential_thinking', True, 0.75),
                MockResult('web_search', True, 0.77),
                MockResult('reasoning_tools', True, 0.78),
                MockResult('brain_remember', True, 0.78)
            ],
            'pattern': ['brain_recall', 'sequential_thinking', 'web_search', 'reasoning_tools', 'brain_remember'],
            'complexity': 'complex'
        }
    ]
    
    analyzer = AdvancedConvergenceAnalyzer()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🎯 Test {i}: {test_case['name']}")
        print("-" * 40)
        
        analysis = analyzer.analyze_convergence(
            test_case['results'],
            1,
            test_case['complexity'],
            test_case['pattern']
        )
        
        print(f"Convergence: {'✅' if analysis['converged'] else '❌'} "
              f"(score: {analysis.get('combined_score', 0):.2f})")
        print(f"Primary Strategy: {analysis.get('primary_strategy', 'N/A')}")
        print(f"Recommendation: {analysis.get('recommendation', 'N/A')}")
    
    print(f"\n✅ Advanced convergence analysis testing complete!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_advanced_convergence())
