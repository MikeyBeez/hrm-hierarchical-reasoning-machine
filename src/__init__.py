"""
HRM Package Initialization
=========================

Hierarchical Reasoning Machine (HRM) - A multi-level AI reasoning system
with Model Context Protocol (MCP) integration for Claude.

Author: HRM Implementation Team
Date: August 2025
Platform: Claude App + MCP on Mac Mini
Status: Proof of Concept (40% Complete)
"""

__version__ = "0.4.0"  # 40% completion - proof of concept
__author__ = "HRM Implementation Team"
__description__ = "Hierarchical Reasoning Machine with MCP Integration"
__platform__ = "Claude App + MCP on Mac Mini"

from .hrm_core import (
    ComplexityAssessor,
    PatternSelector, 
    ConvergenceDetector,
    HRMSystem,
    HRMResult
)