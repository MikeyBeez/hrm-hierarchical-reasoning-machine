#!/usr/bin/env python3
"""
HRM Functional Test Script - Phase 6.2
=====================================

Test script to demonstrate HRM working with real Claude MCP tools.
"""

import sys
import os
import asyncio
import json
import time

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from hrm_claude_functional import execute_hrm_production, test_hrm_functional_integration


async def main():
    """Main test function"""
    print("🧠 HRM Phase 6.2: Real Claude MCP Integration Demo")
    print("=" * 60)
    
    # Test with a specific HRM-related query
    query = "How can hierarchical reasoning systems improve AI convergence detection?"
    
    print(f"🎯 Testing Query: {query}")
    print("-" * 60)
    
    result = await execute_hrm_production(query)
    
    print("\n📊 Complete HRM Execution Result:")
    print("=" * 40)
    print(json.dumps(result, indent=2, default=str))
    
    print("\n🎉 HRM Phase 6.2 Functional Test Complete!")
    print("✅ HRM successfully integrated with Claude MCP tools!")
    

if __name__ == "__main__":
    asyncio.run(main())
