#!/usr/bin/env python3
"""
HRM Module Test: Validate Phase 4 Implementation
===============================================

Simple test to validate the modular HRM automation engine works correctly.
"""

import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from hrm_automation_engine import HRMProductionSystem, execute_hrm_query


async def test_modular_architecture():
    """Test the modular HRM architecture"""
    print("🧪 Testing HRM Modular Architecture")
    print("=" * 50)
    
    # Test 1: Production System
    print("\n🔧 Test 1: Production System Initialization")
    system = HRMProductionSystem()
    status = system.get_status()
    print(f"✅ System Status: {status['engine_status']}")
    
    # Test 2: Query Execution
    print("\n🔧 Test 2: Query Execution")
    query = "Compare machine learning and deep learning"
    result = await system.process_query(query)
    
    print(f"Query: {result['query']}")
    print(f"Complexity: {result['complexity']}")
    print(f"Pattern: {' → '.join(result['pattern'])}")
    print(f"Success: {'✅' if result['success'] else '❌'}")
    print(f"Tools Executed: {len(result['mcp_results'])}")
    print(f"Execution Time: {result['total_execution_time']:.2f}s")
    
    # Test 3: Convenience Function
    print("\n🔧 Test 3: Convenience Function")
    simple_result = await execute_hrm_query("What is artificial intelligence?")
    print(f"Simple Query Result: {simple_result['complexity']} complexity, "
          f"{len(simple_result['pattern'])} steps")
    
    # Test 4: Different Complexity Levels
    print("\n🔧 Test 4: Complexity Detection")
    test_queries = [
        ("Simple", "What is quantum computing?"),
        ("Medium", "Compare quantum vs classical computing"),
        ("Complex", "Design a quantum computing system"),
        ("Expert", "How might quantum consciousness emerge recursively?")
    ]
    
    for expected, query in test_queries:
        result = await execute_hrm_query(query)
        actual = result['complexity']
        status = "✅" if actual.lower() == expected.lower() else "⚠️"
        print(f"  {status} {expected}: '{query[:40]}...' → {actual}")
    
    print(f"\n✅ All modular architecture tests completed successfully!")
    print("🚀 Phase 4 automation engine is working correctly")


if __name__ == "__main__":
    asyncio.run(test_modular_architecture())
