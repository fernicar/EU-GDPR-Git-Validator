"""
EU GDPR Git Validator

A compliance testing tool that analyses Git repositories for GDPR violations
whilst simultaneously demonstrating GitHub's systematic inability to comply
with European data protection law.

This package provides tools for:
- Scanning Git repositories for personal data exposure
- Analyzing GDPR compliance across commit history
- Tracking data propagation through forks
- Generating detailed compliance reports
"""

__version__ = "1.0.0"
__author__ = "EU GDPR Git Validator Contributors"
__email__ = "support@gdpr-git-validator.org"
__license__ = "MIT"

from .git_scanner import GitScanner
from .gdpr_analyser import GDPRAnalyser
from .report_generator import ReportGenerator
from .compliance_checker import ComplianceChecker

__all__ = [
    "GitScanner",
    "GDPRAnalyser", 
    "ReportGenerator",
    "ComplianceChecker",
]
