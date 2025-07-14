import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.gdpr_validator.git_scanner import GitScanner
from src.gdpr_validator.gdpr_analyser import GDPRAnalyser
from src.gdpr_validator.report_generator import ReportGenerator
from src.gdpr_validator.compliance_checker import ComplianceChecker


class Model:
    def __init__(self):
        self._repository_path = None
        self._scanner = None
        self._analyser = GDPRAnalyser()
        self._report_generator = ReportGenerator()
        self._compliance_checker = ComplianceChecker()
        self._scan_results = None
        self._compliance_results = None
        self._fork_results = None

    def set_repository_path(self, path):
        self._repository_path = path
        self._scanner = GitScanner(self._repository_path)

    def run_scan(self, articles=None, include_forks=False):
        if self._scanner:
            self._scan_results = self._scanner.scan_repository()
            self._compliance_results = self._analyser.analyze_compliance(self._scan_results, articles)
            if include_forks:
                # Assuming the repository URL can be derived from the path or is configured elsewhere
                # For now, let's use a placeholder
                repo_url = "https://github.com/example/repo"
                self._fork_results = self._analyser.analyze_fork_impact(repo_url)

    def get_scan_results(self):
        return self._scan_results

    def get_compliance_results(self):
        return self._compliance_results

    def get_fork_results(self):
        return self._fork_results

    def generate_report(self, output_path, format):
        if self._scan_results and self._compliance_results:
            self._report_generator.generate_report(
                self._scan_results,
                self._compliance_results,
                self._fork_results,
                output_path,
                format
            )

    def analyze_forks(self, repo_url):
        self._fork_results = self._analyser.analyze_fork_impact(repo_url)

if __name__ == '__main__':
    # Create a dummy repository for testing
    import subprocess
    from pathlib import Path
    import tempfile
    import os
    import shutil

    # Create a temporary directory
    temp_dir = Path(tempfile.gettempdir()) / "gdpr_validator_test"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()

    # Initialize a git repository
    subprocess.run(["git", "init"], cwd=temp_dir)

    # Create a dummy file
    (temp_dir / "test.txt").write_text("This is a test file.")

    # Commit the file
    subprocess.run(["git", "add", "."], cwd=temp_dir)
    subprocess.run(["git", "commit", "-m", "Initial commit", "--author", "Test User <test@example.com>"], cwd=temp_dir)

    # Create a model instance
    model = Model()
    model.set_repository_path(temp_dir)
    model.run_scan()

    # Generate a report
    report_path = temp_dir / "report.html"
    model.generate_report(report_path, "html")

    print(f"Test report generated at: {report_path}")

    # Clean up the dummy repository
    shutil.rmtree(temp_dir)
