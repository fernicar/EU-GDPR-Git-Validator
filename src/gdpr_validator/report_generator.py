"""
Report Generator Module

Generates detailed GDPR compliance reports in multiple formats including
HTML, PDF, JSON, and Markdown with comprehensive analysis and recommendations.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from jinja2 import Template
import base64


class ReportGenerator:
    """
    Generates comprehensive GDPR compliance reports.
    
    Supports multiple output formats:
    - HTML: Interactive web report with charts and navigation
    - PDF: Professional document for sharing and archiving
    - JSON: Machine-readable format for integration
    - Markdown: Documentation-friendly format
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the report generator.
        
        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        
        # User-friendly explanations for violations
        self.violation_explanations = {
            'missing_lawful_basis': {
                'simple': "No legal permission to process contributor personal data",
                'technical': "Every Git commit contains personal information (names, emails, timestamps) but there's no legal basis for processing this data under GDPR Article 6",
                'fixable': True,
                'fix': "Add privacy notice explaining why you need contributor data",
                'priority': 'high'
            },
            'erasure_impossible': {
                'simple': "Cannot delete personal data due to Git's design",
                'technical': "Git's distributed architecture and immutable history make it technically impossible to completely erase personal data, violating GDPR Article 17",
                'fixable': False,
                'fix': "Impossible - this is a fundamental Git architecture problem",
                'priority': 'critical'
            },
            'fork_propagation': {
                'simple': "Personal data automatically copies to other repositories",
                'technical': "When repositories are forked, all personal data (commit history, contributor information) is automatically duplicated without consent",
                'fixable': False,
                'fix': "Impossible - Git's fork mechanism cannot be disabled",
                'priority': 'critical'
            },
            'cross_border_transfer': {
                'simple': "Personal data transferred internationally without consent",
                'technical': "Git repositories hosted on platforms like GitHub automatically transfer EU personal data to US servers without adequate safeguards",
                'fixable': True,
                'fix': "Document international transfers and implement adequate safeguards",
                'priority': 'high'
            },
            'no_privacy_notice': {
                'simple': "Contributors not informed about data processing",
                'technical': "GDPR Articles 13/14 require informing data subjects about processing, but Git repositories typically lack privacy notices",
                'fixable': True,
                'fix': "Add CONTRIBUTING.md with privacy notice and data processing information",
                'priority': 'medium'
            },
            'permanent_retention': {
                'simple': "Personal data stored permanently without justification",
                'technical': "Git's immutable history creates permanent retention of personal data without documented retention periods or justification",
                'fixable': True,
                'fix': "Document data retention policy and justification for permanent storage",
                'priority': 'medium'
            },
            'distributed_processing': {
                'simple': "Personal data processed by unlimited third parties",
                'technical': "Git's distributed nature means personal data is automatically processed by anyone who clones or forks the repository",
                'fixable': False,
                'fix': "Impossible - Git's distributed architecture cannot be changed",
                'priority': 'critical'
            }
        }
        
        # HTML template for reports
        self.html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GDPR Compliance Report - {{ repository_name }}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }
        .card.critical {
            border-left-color: #dc3545;
        }
        .card.warning {
            border-left-color: #ffc107;
        }
        .card.success {
            border-left-color: #28a745;
        }
        .card h3 {
            margin: 0 0 10px 0;
            color: #495057;
        }
        .card .value {
            font-size: 2em;
            font-weight: bold;
            color: #212529;
        }
        .section {
            background: white;
            margin-bottom: 30px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .section-header {
            background: #495057;
            color: white;
            padding: 15px 20px;
            font-weight: bold;
            font-size: 1.2em;
        }
        .section-content {
            padding: 20px;
        }
        .violation {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .violation.critical {
            background: #f8d7da;
            border-color: #f5c6cb;
        }
        .violation.high {
            background: #fff3cd;
            border-color: #ffeaa7;
        }
        .violation.medium {
            background: #d1ecf1;
            border-color: #bee5eb;
        }
        .violation-title {
            font-weight: bold;
            color: #721c24;
            margin-bottom: 5px;
        }
        .article-result {
            border: 1px solid #dee2e6;
            border-radius: 5px;
            margin-bottom: 15px;
            overflow: hidden;
        }
        .article-header {
            background: #f8f9fa;
            padding: 15px;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            justify-content: between;
            align-items: center;
        }
        .article-header.non-compliant {
            background: #f8d7da;
        }
        .article-header.compliant {
            background: #d4edda;
        }
        .article-content {
            padding: 15px;
        }
        .recommendation {
            background: #e7f3ff;
            border-left: 4px solid #0066cc;
            padding: 10px 15px;
            margin-bottom: 10px;
        }
        .data-list {
            background: #f8f9fa;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
        }
        .data-list ul {
            margin: 0;
            padding-left: 20px;
        }
        .severity-critical { color: #dc3545; font-weight: bold; }
        .severity-high { color: #fd7e14; font-weight: bold; }
        .severity-medium { color: #ffc107; font-weight: bold; }
        .severity-low { color: #20c997; }
        .status-compliant { color: #28a745; font-weight: bold; }
        .status-non-compliant { color: #dc3545; font-weight: bold; }
        .criteria-section {
            margin: 20px 0;
        }
        .impossible-criteria {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .fixable-criteria {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .repo-status {
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
            font-weight: bold;
        }
        .repo-status.empty {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
        }
        .repo-status.minimal {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
        }
        .repo-status.moderate {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .repo-status.populated {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .footer {
            text-align: center;
            padding: 20px;
            color: #6c757d;
            border-top: 1px solid #dee2e6;
            margin-top: 30px;
        }
        @media print {
            body { background: white; }
            .card, .section { box-shadow: none; border: 1px solid #ddd; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔒 GDPR Compliance Report</h1>
        <p>{{ repository_name }} • Generated {{ timestamp }}</p>
    </div>

    <div class="summary-cards">
        <div class="card {% if overall_compliant %}success{% else %}critical{% endif %}">
            <h3>Overall Compliance</h3>
            <div class="value">{% if overall_compliant %}✅ PASS{% else %}❌ FAIL{% endif %}</div>
        </div>
        <div class="card {% if total_violations > 10 %}critical{% elif total_violations > 5 %}warning{% else %}success{% endif %}">
            <h3>Total Violations</h3>
            <div class="value">{{ total_violations }}</div>
        </div>
        <div class="card {% if critical_violations > 0 %}critical{% else %}success{% endif %}">
            <h3>Critical Issues</h3>
            <div class="value">{{ critical_violations }}</div>
        </div>
        <div class="card">
            <h3>Severity Level</h3>
            <div class="value severity-{{ severity_level }}">{{ severity_level|upper }}</div>
        </div>
    </div>

    {% if repository_status %}
    <div class="repo-status {{ repository_status.status_code }}">
        <h3>📁 Repository Status: {{ repository_status.status }}</h3>
        <p>{{ repository_status.message }}</p>
        <p><em>{{ repository_status.severity_note }}</em></p>
    </div>
    {% endif %}

    <div class="criteria-section">
        <h2>📋 GDPR Compliance Criteria</h2>
        
        <div class="impossible-criteria">
            <h3>❌ ARCHITECTURAL IMPOSSIBILITIES</h3>
            <p class="critical">These violations CANNOT be fixed due to Git's fundamental design:</p>
            <ul>
                <li><strong>Article 17 - Right to Erasure:</strong> Git's distributed nature makes data deletion impossible</li>
                <li><strong>Fork Propagation:</strong> Data automatically copies to unlimited repositories globally</li>
                <li><strong>Permanent Hash References:</strong> Git creates immutable links to personal data</li>
                <li><strong>International Transfers:</strong> Forks automatically transfer data across borders</li>
                <li><strong>Distributed Processing:</strong> Personal data processed by unlimited third parties</li>
            </ul>
            <p class="critical">⚖️ These prove that Git architecture fundamentally violates GDPR</p>
        </div>
        
        <div class="fixable-criteria">
            <h3>✅ POTENTIALLY FIXABLE</h3>
            <p class="info">These violations can be addressed with documentation and agreements:</p>
            <ul>
                <li><strong>Privacy Notices:</strong> Add CONTRIBUTING.md with data processing information</li>
                <li><strong>Lawful Basis:</strong> Document legitimate interests for processing contributor data</li>
                <li><strong>Consent Mechanisms:</strong> Implement contributor agreements</li>
                <li><strong>Rights Information:</strong> Inform contributors about data protection rights</li>
                <li><strong>Retention Policies:</strong> Document data retention justification</li>
            </ul>
            <p class="warning">⚠️ Even with these fixes, fundamental architectural violations remain</p>
        </div>
    </div>

    <div class="section">
        <div class="section-header">📊 Repository Analysis</div>
        <div class="section-content">
            <p><strong>Repository:</strong> {{ repository_path }}</p>
            <p><strong>Scan Date:</strong> {{ scan_timestamp }}</p>
            <p><strong>Total Commits Analyzed:</strong> {{ total_commits }}</p>
            <p><strong>Total Branches:</strong> {{ total_branches }}</p>
            
            <div class="data-list">
                <h4>Personal Data Found:</h4>
                <ul>
                    <li><strong>Email Addresses:</strong> {{ personal_data.emails|length }}</li>
                    <li><strong>Author Names:</strong> {{ personal_data.authors|length }}</li>
                    <li><strong>Committer Names:</strong> {{ personal_data.committers|length }}</li>
                    <li><strong>Potential PII:</strong> {{ personal_data.potential_pii|length }} instances</li>
                </ul>
            </div>
        </div>
    </div>

    {% if violations %}
    <div class="section">
        <div class="section-header">⚠️ GDPR Violations Found</div>
        <div class="section-content">
            {% for violation in violations %}
            <div class="violation {{ violation.severity }}">
                <div class="violation-title">{{ violation.type|title }} (Article {{ violation.article }})</div>
                <div>{{ violation.description }}</div>
            </div>
            {% endfor %}
        </div>
    </div>
    {% endif %}

    <div class="section">
        <div class="section-header">📋 Article-by-Article Analysis</div>
        <div class="section-content">
            {% for article, result in article_results.items() %}
            <div class="article-result">
                <div class="article-header {% if result.compliant %}compliant{% else %}non-compliant{% endif %}">
                    <div>
                        <strong>Article {{ article }}: {{ result.title }}</strong>
                        <span class="status-{% if result.compliant %}compliant{% else %}non-compliant{% endif %}">
                            {% if result.compliant %}✅ COMPLIANT{% else %}❌ NON-COMPLIANT{% endif %}
                        </span>
                    </div>
                    <div class="severity-{{ result.severity }}">{{ result.severity|upper }}</div>
                </div>
                <div class="article-content">
                    {% if result.violations %}
                    <h4>Violations:</h4>
                    {% for violation in result.violations %}
                    <div class="violation {{ violation.severity }}">
                        <strong>{{ violation.type|title }}:</strong> {{ violation.description }}
                    </div>
                    {% endfor %}
                    {% endif %}
                    
                    {% if result.recommendations %}
                    <h4>Recommendations:</h4>
                    {% for rec in result.recommendations %}
                    <div class="recommendation">{{ rec }}</div>
                    {% endfor %}
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    {% if fork_results %}
    <div class="section">
        <div class="section-header">🌐 Fork Impact Analysis</div>
        <div class="section-content">
            <div class="data-list">
                <ul>
                    <li><strong>Total Forks:</strong> {{ fork_results.total_forks }}</li>
                    <li><strong>Countries Involved:</strong> {{ fork_results.countries|length }}</li>
                    <li><strong>Data Multiplication Factor:</strong> {{ fork_results.multiplication_factor }}x</li>
                    <li><strong>Erasure Possible:</strong> {% if fork_results.erasure_impossible %}❌ No{% else %}✅ Yes{% endif %}</li>
                </ul>
            </div>
            
            {% if fork_results.gdpr_implications %}
            <h4>GDPR Implications:</h4>
            {% for implication in fork_results.gdpr_implications %}
            <div class="violation medium">{{ implication }}</div>
            {% endfor %}
            {% endif %}
        </div>
    </div>
    {% endif %}

    {% if recommendations %}
    <div class="section">
        <div class="section-header">💡 Priority Recommendations</div>
        <div class="section-content">
            {% for rec in recommendations[:10] %}
            <div class="recommendation">{{ loop.index }}. {{ rec }}</div>
            {% endfor %}
        </div>
    </div>
    {% endif %}

    <div class="footer">
        <p>Generated by EU GDPR Git Validator v1.0.0</p>
        <p>This report is for educational and compliance purposes only. Consult legal professionals for specific advice.</p>
    </div>
</body>
</html>
        """
    
    def generate_report(
        self,
        scan_results: Dict[str, Any],
        compliance_results: Dict[str, Any],
        fork_results: Optional[Dict[str, Any]] = None,
        output_path: Path = Path("gdpr-compliance-report.html"),
        format: str = "html"
    ) -> None:
        """
        Generate a comprehensive GDPR compliance report.
        
        Args:
            scan_results: Results from GitScanner
            compliance_results: Results from GDPRAnalyser
            fork_results: Optional fork analysis results
            output_path: Path for the output file
            format: Output format (html, pdf, json, markdown)
        """
        if self.verbose:
            print(f"📄 Generating {format.upper()} report: {output_path}")
        
        # Prepare report data
        report_data = self._prepare_report_data(
            scan_results, compliance_results, fork_results
        )
        
        # Generate report based on format
        if format.lower() == "html":
            self._generate_html_report(report_data, output_path)
        elif format.lower() == "pdf":
            self._generate_pdf_report(report_data, output_path)
        elif format.lower() == "json":
            self._generate_json_report(report_data, output_path)
        elif format.lower() == "markdown":
            self._generate_markdown_report(report_data, output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        if self.verbose:
            print(f"✅ Report generated successfully: {output_path}")
    
    def get_user_friendly_explanation(self, violation_type: str) -> Dict[str, Any]:
        """Convert legal violations to plain English explanations."""
        return self.violation_explanations.get(violation_type, {
            'simple': 'Unknown violation type',
            'technical': 'No explanation available',
            'fixable': False,
            'fix': 'Contact support',
            'priority': 'unknown'
        })
    
    def generate_criteria_section(self) -> str:
        """Generate clear pass/fail criteria for HTML report."""
        return """
        <div class="criteria-section">
            <h2>📋 GDPR Compliance Criteria</h2>
            
            <div class="impossible-criteria">
                <h3>❌ ARCHITECTURAL IMPOSSIBILITIES</h3>
                <p class="critical">These violations CANNOT be fixed due to Git's fundamental design:</p>
                <ul>
                    <li><strong>Article 17 - Right to Erasure:</strong> Git's distributed nature makes data deletion impossible</li>
                    <li><strong>Fork Propagation:</strong> Data automatically copies to unlimited repositories globally</li>
                    <li><strong>Permanent Hash References:</strong> Git creates immutable links to personal data</li>
                    <li><strong>International Transfers:</strong> Forks automatically transfer data across borders</li>
                    <li><strong>Distributed Processing:</strong> Personal data processed by unlimited third parties</li>
                </ul>
                <p class="critical">⚖️ These prove that Git architecture fundamentally violates GDPR</p>
            </div>
            
            <div class="fixable-criteria">
                <h3>✅ POTENTIALLY FIXABLE</h3>
                <p class="info">These violations can be addressed with documentation and agreements:</p>
                <ul>
                    <li><strong>Privacy Notices:</strong> Add CONTRIBUTING.md with data processing information</li>
                    <li><strong>Lawful Basis:</strong> Document legitimate interests for processing contributor data</li>
                    <li><strong>Consent Mechanisms:</strong> Implement contributor agreements</li>
                    <li><strong>Rights Information:</strong> Inform contributors about data protection rights</li>
                    <li><strong>Retention Policies:</strong> Document data retention justification</li>
                </ul>
                <p class="warning">⚠️ Even with these fixes, fundamental architectural violations remain</p>
            </div>
        </div>
        """
    
    def _prepare_report_data(
        self,
        scan_results: Dict[str, Any],
        compliance_results: Dict[str, Any],
        fork_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Prepare and structure data for report generation."""
        
        # Extract repository name from path
        repo_path = scan_results.get('repository_path', 'Unknown Repository')
        repo_name = Path(repo_path).name if repo_path != 'Unknown Repository' else 'Unknown Repository'
        
        # Count violations by severity
        violations = compliance_results.get('violations', [])
        critical_violations = sum(1 for v in violations if v.get('severity') == 'critical')
        
        # Collect all recommendations
        recommendations = set()
        for article_result in compliance_results.get('article_results', {}).values():
            recommendations.update(article_result.get('recommendations', []))
        
        return {
            'repository_name': repo_name,
            'repository_path': repo_path,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
            'scan_timestamp': scan_results.get('scan_timestamp', ''),
            'overall_compliant': compliance_results.get('overall_compliance', False),
            'total_violations': len(violations),
            'critical_violations': critical_violations,
            'severity_level': compliance_results.get('severity_level', 'unknown'),
            'total_commits': scan_results.get('total_commits', 0),
            'total_branches': scan_results.get('total_branches', 0),
            'repository_status': scan_results.get('repository_status', {}),
            'personal_data': scan_results.get('personal_data', {}),
            'violations': violations,
            'article_results': compliance_results.get('article_results', {}),
            'fork_results': fork_results,
            'recommendations': list(recommendations),
            'scan_results': scan_results,
            'compliance_results': compliance_results
        }
    
    def _generate_html_report(self, report_data: Dict[str, Any], output_path: Path) -> None:
        """Generate HTML report."""
        template = Template(self.html_template)
        html_content = template.render(**report_data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _generate_pdf_report(self, report_data: Dict[str, Any], output_path: Path) -> None:
        """Generate PDF report using HTML to PDF conversion."""
        try:
            import weasyprint
            
            # First generate HTML
            html_template = Template(self.html_template)
            html_content = html_template.render(**report_data)
            
            # Convert to PDF
            html_doc = weasyprint.HTML(string=html_content)
            html_doc.write_pdf(str(output_path))
            
        except ImportError:
            # Fallback: generate HTML with PDF-friendly styling
            if self.verbose:
                print("⚠️  WeasyPrint not available, generating HTML report instead")
            
            html_path = output_path.with_suffix('.html')
            self._generate_html_report(report_data, html_path)
            
            if self.verbose:
                print(f"💡 To generate PDF, install WeasyPrint: pip install weasyprint")
    
    def _generate_json_report(self, report_data: Dict[str, Any], output_path: Path) -> None:
        """Generate JSON report."""
        # Create a clean JSON structure
        json_data = {
            'metadata': {
                'repository_name': report_data['repository_name'],
                'repository_path': report_data['repository_path'],
                'generated_at': report_data['timestamp'],
                'scan_timestamp': report_data['scan_timestamp'],
                'generator': 'EU GDPR Git Validator v1.0.0'
            },
            'summary': {
                'overall_compliant': report_data['overall_compliant'],
                'total_violations': report_data['total_violations'],
                'critical_violations': report_data['critical_violations'],
                'severity_level': report_data['severity_level']
            },
            'repository_analysis': {
                'total_commits': report_data['total_commits'],
                'total_branches': report_data['total_branches'],
                'personal_data_found': report_data['personal_data']
            },
            'violations': report_data['violations'],
            'article_results': report_data['article_results'],
            'fork_analysis': report_data['fork_results'],
            'recommendations': report_data['recommendations'],
            'raw_data': {
                'scan_results': report_data['scan_results'],
                'compliance_results': report_data['compliance_results']
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)
    
    def _generate_markdown_report(self, report_data: Dict[str, Any], output_path: Path) -> None:
        """Generate Markdown report."""
        md_content = []
        
        # Header
        md_content.extend([
            f"# 🔒 GDPR Compliance Report",
            f"",
            f"**Repository:** {report_data['repository_name']}  ",
            f"**Generated:** {report_data['timestamp']}  ",
            f"**Scan Date:** {report_data['scan_timestamp']}  ",
            f"",
            "---",
            ""
        ])
        
        # Summary
        status = "✅ COMPLIANT" if report_data['overall_compliant'] else "❌ NON-COMPLIANT"
        md_content.extend([
            "## 📊 Summary",
            "",
            f"- **Overall Status:** {status}",
            f"- **Total Violations:** {report_data['total_violations']}",
            f"- **Critical Issues:** {report_data['critical_violations']}",
            f"- **Severity Level:** {report_data['severity_level'].upper()}",
            f"- **Commits Analyzed:** {report_data['total_commits']}",
            f"- **Branches Analyzed:** {report_data['total_branches']}",
            ""
        ])
        
        # Personal Data Found
        personal_data = report_data['personal_data']
        md_content.extend([
            "## 👤 Personal Data Found",
            "",
            f"- **Email Addresses:** {len(personal_data.get('emails', []))}",
            f"- **Author Names:** {len(personal_data.get('authors', []))}",
            f"- **Committer Names:** {len(personal_data.get('committers', []))}",
            f"- **Potential PII:** {len(personal_data.get('potential_pii', []))} instances",
            ""
        ])
        
        # Violations
        if report_data['violations']:
            md_content.extend([
                "## ⚠️ GDPR Violations",
                ""
            ])
            
            for violation in report_data['violations']:
                severity_emoji = {
                    'critical': '🚨',
                    'high': '⚠️',
                    'medium': '⚡',
                    'low': 'ℹ️'
                }.get(violation.get('severity', 'medium'), 'ℹ️')
                
                md_content.extend([
                    f"### {severity_emoji} {violation.get('type', 'Unknown').title()}",
                    f"",
                    f"**Article:** {violation.get('article', 'Unknown')}  ",
                    f"**Severity:** {violation.get('severity', 'Unknown').title()}  ",
                    f"**Description:** {violation.get('description', 'No description available')}",
                    ""
                ])
        
        # Article Results
        md_content.extend([
            "## 📋 Article-by-Article Analysis",
            ""
        ])
        
        for article, result in report_data['article_results'].items():
            status = "✅ COMPLIANT" if result.get('compliant', False) else "❌ NON-COMPLIANT"
            md_content.extend([
                f"### Article {article}: {result.get('title', 'Unknown')}",
                f"",
                f"**Status:** {status}  ",
                f"**Severity:** {result.get('severity', 'Unknown').title()}",
                ""
            ])
            
            if result.get('violations'):
                md_content.append("**Violations:**")
                for violation in result['violations']:
                    md_content.append(f"- {violation.get('description', 'No description')}")
                md_content.append("")
            
            if result.get('recommendations'):
                md_content.append("**Recommendations:**")
                for rec in result['recommendations']:
                    md_content.append(f"- {rec}")
                md_content.append("")
        
        # Fork Analysis
        if report_data['fork_results']:
            fork_results = report_data['fork_results']
            md_content.extend([
                "## 🌐 Fork Impact Analysis",
                "",
                f"- **Total Forks:** {fork_results.get('total_forks', 0)}",
                f"- **Countries Involved:** {len(fork_results.get('countries', []))}",
                f"- **Data Multiplication Factor:** {fork_results.get('multiplication_factor', 1)}x",
                f"- **Erasure Possible:** {'❌ No' if fork_results.get('erasure_impossible', True) else '✅ Yes'}",
                ""
            ])
            
            if fork_results.get('gdpr_implications'):
                md_content.extend([
                    "**GDPR Implications:**",
                    ""
                ])
                for implication in fork_results['gdpr_implications']:
                    md_content.append(f"- {implication}")
                md_content.append("")
        
        # Recommendations
        if report_data['recommendations']:
            md_content.extend([
                "## 💡 Priority Recommendations",
                ""
            ])
            for i, rec in enumerate(report_data['recommendations'][:10], 1):
                md_content.append(f"{i}. {rec}")
            md_content.append("")
        
        # Footer
        md_content.extend([
            "---",
            "",
            "*Generated by EU GDPR Git Validator v1.0.0*",
            "",
            "*This report is for educational and compliance purposes only. Consult legal professionals for specific advice.*"
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))
    
    def generate_summary_report(
        self,
        scan_results: Dict[str, Any],
        compliance_results: Dict[str, Any]
    ) -> str:
        """Generate a brief text summary of the compliance status."""
        
        violations = compliance_results.get('violations', [])
        critical_count = sum(1 for v in violations if v.get('severity') == 'critical')
        
        summary_lines = [
            "🔍 GDPR Compliance Summary",
            "=" * 30,
            f"Repository: {scan_results.get('repository_path', 'Unknown')}",
            f"Overall Status: {'✅ COMPLIANT' if compliance_results.get('overall_compliance', False) else '❌ NON-COMPLIANT'}",
            f"Total Violations: {len(violations)}",
            f"Critical Issues: {critical_count}",
            f"Severity Level: {compliance_results.get('severity_level', 'unknown').upper()}",
            "",
            f"Personal Data Found:",
            f"├── Emails: {len(scan_results.get('personal_data', {}).get('emails', []))}",
            f"├── Authors: {len(scan_results.get('personal_data', {}).get('authors', []))}",
            f"└── Potential PII: {len(scan_results.get('personal_data', {}).get('potential_pii', []))} instances"
        ]
        
        return '\n'.join(summary_lines)
