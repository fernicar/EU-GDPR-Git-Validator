"""
Command Line Interface for EU GDPR Git Validator

Provides the main entry point and CLI commands for the GDPR compliance tool.
"""

import click
import sys
from pathlib import Path
from typing import Optional, List

from .git_scanner import GitScanner
from .gdpr_analyser import GDPRAnalyser
from .report_generator import ReportGenerator
from .compliance_checker import ComplianceChecker


@click.group()
@click.version_option(version="1.0.0", prog_name="gdpr-validator")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """
    EU GDPR Git Validator - Analyze Git repositories for GDPR compliance.
    
    This tool scans Git repositories for potential European data protection
    violations and generates detailed compliance reports.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


@cli.command()
@click.argument("repository_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output", "-o", 
    type=click.Path(path_type=Path),
    help="Output file for the compliance report"
)
@click.option(
    "--format", "report_format",
    type=click.Choice(["html", "pdf", "json", "markdown"], case_sensitive=False),
    default="html",
    help="Report output format (default: html)"
)
@click.option(
    "--articles",
    help="Comma-separated list of GDPR articles to check (e.g., '6,17,20')"
)
@click.option(
    "--include-forks", 
    is_flag=True,
    help="Include fork analysis (requires internet connection)"
)
@click.pass_context
def scan(
    ctx: click.Context,
    repository_path: Path,
    output: Optional[Path],
    report_format: str,
    articles: Optional[str],
    include_forks: bool
) -> None:
    """
    Scan a Git repository for GDPR compliance violations.
    
    REPOSITORY_PATH: Path to the Git repository to analyze
    """
    verbose = ctx.obj.get("verbose", False)
    
    if verbose:
        click.echo(f"🔍 Starting GDPR compliance scan of: {repository_path}")
    
    try:
        # Initialize scanner
        scanner = GitScanner(repository_path, verbose=verbose)
        
        # Scan repository
        click.echo("📊 Scanning Git history...")
        scan_results = scanner.scan_repository()
        
        # Analyze GDPR compliance
        click.echo("⚖️  Analyzing GDPR compliance...")
        analyser = GDPRAnalyser(verbose=verbose)
        
        # Parse articles if provided
        article_list = None
        if articles:
            try:
                article_list = [int(a.strip()) for a in articles.split(",")]
            except ValueError:
                click.echo("❌ Error: Invalid article numbers. Use comma-separated integers.", err=True)
                sys.exit(1)
        
        compliance_results = analyser.analyze_compliance(scan_results, articles=article_list)
        
        # Fork analysis if requested
        fork_results = None
        if include_forks:
            click.echo("🌐 Analyzing fork propagation...")
            fork_results = analyser.analyze_fork_impact(repository_path)
        
        # Generate report
        click.echo(f"📄 Generating {report_format.upper()} report...")
        generator = ReportGenerator(verbose=verbose)
        
        if output is None:
            output = Path(f"gdpr-compliance-report.{report_format}")
        
        generator.generate_report(
            scan_results=scan_results,
            compliance_results=compliance_results,
            fork_results=fork_results,
            output_path=output,
            format=report_format
        )
        
        # Display summary
        _display_summary(scan_results, compliance_results, fork_results)
        
        click.echo(f"✅ Report saved to: {output}")
        
    except Exception as e:
        click.echo(f"❌ Error during scan: {str(e)}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument("repository_url")
@click.option(
    "--depth", 
    type=int, 
    default=2,
    help="Maximum depth for fork analysis (default: 2)"
)
@click.option(
    "--output", "-o",
    type=click.Path(path_type=Path),
    help="Output file for fork analysis results"
)
@click.pass_context
def analyze_forks(
    ctx: click.Context,
    repository_url: str,
    depth: int,
    output: Optional[Path]
) -> None:
    """
    Analyze fork propagation for a GitHub repository.
    
    REPOSITORY_URL: GitHub repository URL to analyze
    """
    verbose = ctx.obj.get("verbose", False)
    
    if verbose:
        click.echo(f"🌐 Analyzing fork propagation for: {repository_url}")
    
    try:
        analyser = GDPRAnalyser(verbose=verbose)
        fork_results = analyser.analyze_fork_impact(repository_url, max_depth=depth)
        
        # Display results
        click.echo("\n📈 Fork Analysis Results:")
        click.echo(f"├── Total forks found: {fork_results.get('total_forks', 0)}")
        click.echo(f"├── Geographic distribution: {len(fork_results.get('countries', []))} countries")
        click.echo(f"├── Data multiplication factor: {fork_results.get('multiplication_factor', 1)}x")
        click.echo(f"└── Erasure impossibility: {fork_results.get('erasure_impossible', True)}")
        
        if output:
            import json
            with open(output, 'w') as f:
                json.dump(fork_results, f, indent=2)
            click.echo(f"✅ Fork analysis saved to: {output}")
            
    except Exception as e:
        click.echo(f"❌ Error during fork analysis: {str(e)}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument("repository_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--article", 
    type=int,
    help="Specific GDPR article to check (6, 13, 14, 17, 20)"
)
@click.pass_context
def check_compliance(
    ctx: click.Context,
    repository_path: Path,
    article: Optional[int]
) -> None:
    """
    Quick compliance check for specific GDPR articles.
    
    REPOSITORY_PATH: Path to the Git repository to check
    """
    verbose = ctx.obj.get("verbose", False)
    
    try:
        checker = ComplianceChecker(verbose=verbose)
        scanner = GitScanner(repository_path, verbose=verbose)
        
        scan_results = scanner.scan_repository()
        
        if article:
            result = checker.check_article_compliance(scan_results, article)
            _display_article_result(article, result)
        else:
            # Check all articles
            for art in [6, 13, 14, 17, 20]:
                result = checker.check_article_compliance(scan_results, art)
                _display_article_result(art, result)
                
    except Exception as e:
        click.echo(f"❌ Error during compliance check: {str(e)}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def _display_summary(scan_results: dict, compliance_results: dict, fork_results: Optional[dict]) -> None:
    """Display a summary of the scan results."""
    click.echo("\n🔍 GDPR Compliance Scan Results")
    click.echo("=" * 50)
    
    # Personal data exposure
    personal_data = scan_results.get("personal_data", {})
    click.echo(f"📧 Email addresses found: {len(personal_data.get('emails', []))}")
    click.echo(f"👤 Author names found: {len(personal_data.get('authors', []))}")
    click.echo(f"📅 Commits analyzed: {scan_results.get('total_commits', 0)}")
    
    # Compliance violations
    violations = compliance_results.get("violations", [])
    if violations:
        click.echo(f"\n⚠️  VIOLATIONS FOUND: {len(violations)}")
        for violation in violations[:3]:  # Show first 3
            click.echo(f"├── {violation.get('type', 'Unknown')}: {violation.get('description', '')}")
        if len(violations) > 3:
            click.echo(f"└── ... and {len(violations) - 3} more violations")
    else:
        click.echo("\n✅ No major violations detected")
    
    # Fork impact
    if fork_results:
        click.echo(f"\n🌐 Fork Impact:")
        click.echo(f"├── Data exists in {fork_results.get('total_forks', 0)} additional repositories")
        click.echo(f"└── Erasure impossibility factor: {fork_results.get('erasure_impossible', True)}")


def _display_article_result(article: int, result: dict) -> None:
    """Display compliance result for a specific GDPR article."""
    status = "✅ COMPLIANT" if result.get("compliant", False) else "❌ NON-COMPLIANT"
    click.echo(f"Article {article}: {status}")
    
    if result.get("issues"):
        for issue in result["issues"]:
            click.echo(f"  └── {issue}")


def main() -> None:
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
