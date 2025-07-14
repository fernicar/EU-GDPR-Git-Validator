import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLineEdit, QProgressBar, QTabWidget,
    QMessageBox, QLabel
)
from PySide6.QtWidgets import QTextBrowser, QStyleFactory
from PySide6.QtCore import QUrl, Slot, QThread, Signal, Qt
from pathlib import Path
import tempfile

from model import Model


class Worker(QThread):
    scan_complete = Signal(str)
    scan_error = Signal(str)

    def __init__(self, model, articles, include_forks):
        super().__init__()
        self.model = model
        self.articles = articles
        self.include_forks = include_forks

    def run(self):
        try:
            self.model.run_scan(self.articles, self.include_forks)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w") as f:
                report_path = Path(f.name)
            self.model.generate_report(report_path, "html")
            self.scan_complete.emit(str(report_path))
        except Exception as e:
            self.scan_error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EU GDPR Git Validator")
        self.model = Model()

        self.app = QApplication.instance()
        self.app.setStyle(QStyleFactory.create('Fusion'))
        self.app.styleHints().setColorScheme(Qt.ColorScheme.Dark)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.scan_view = QWidget()
        self.report_view = QTextBrowser()
        self.analysis_view = QWidget()

        self.tabs.addTab(self.scan_view, "Scan")
        self.tabs.addTab(self.report_view, "Report")
        self.tabs.addTab(self.analysis_view, "Analysis")

        self.init_scan_view()
        self.init_analysis_view()

    def init_scan_view(self):
        layout = QVBoxLayout()

        # Repository selection
        repo_layout = QHBoxLayout()
        self.repo_path_edit = QLineEdit()
        self.repo_path_edit.setPlaceholderText("Select a Git repository")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_for_repo)
        repo_layout.addWidget(self.repo_path_edit)
        repo_layout.addWidget(browse_button)
        layout.addLayout(repo_layout)

        # Scan options
        options_layout = QVBoxLayout()
        self.include_forks_checkbox = QLabel("Include Forks (Not implemented yet)")
        self.articles_edit = QLineEdit()
        self.articles_edit.setPlaceholderText("Articles (e.g., 6,17,20)")
        options_layout.addWidget(self.include_forks_checkbox)
        options_layout.addWidget(self.articles_edit)
        layout.addLayout(options_layout)

        # Scan button and progress bar
        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.start_scan)
        self.progress_bar = QProgressBar()
        layout.addWidget(self.scan_button)
        layout.addWidget(self.progress_bar)

        # Save report button
        self.save_report_button = QPushButton("Save Report")
        self.save_report_button.clicked.connect(self.save_report)
        layout.addWidget(self.save_report_button)

        self.scan_view.setLayout(layout)

    @Slot()
    def browse_for_repo(self):
        repo_path = QFileDialog.getExistingDirectory(self, "Select Repository")
        if repo_path:
            self.repo_path_edit.setText(repo_path)
            self.model.set_repository_path(Path(repo_path))

    @Slot()
    def start_scan(self):
        if not self.repo_path_edit.text():
            QMessageBox.warning(self, "Warning", "Please select a repository first.")
            return

        self.scan_button.setEnabled(False)
        self.progress_bar.setRange(0, 0)

        articles_text = self.articles_edit.text()
        articles = [int(a.strip()) for a in articles_text.split(",")] if articles_text else None
        include_forks = False  # Not implemented yet

        self.worker = Worker(self.model, articles, include_forks)
        self.worker.scan_complete.connect(self.scan_complete)
        self.worker.scan_error.connect(self.scan_error)
        self.worker.start()

    @Slot(str)
    def scan_complete(self, report_path):
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        self.scan_button.setEnabled(True)
        with open(report_path, "r", encoding="utf-8") as f:
            self.report_view.setHtml(f.read())
        self.tabs.setCurrentWidget(self.report_view)
        self.update_analysis_view()

    @Slot(str)
    def scan_error(self, error_message):
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.scan_button.setEnabled(True)
        QMessageBox.critical(self, "Error", f"An error occurred during the scan:\n{error_message}")

    @Slot()
    def save_report(self):
        if not self.model.get_scan_results():
            QMessageBox.warning(self, "Warning", "Please run a scan first.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report",
            "",
            "PDF Files (*.pdf);;HTML Files (*.html);;JSON Files (*.json);;Markdown Files (*.md)",
        )

        if file_path:
            file_path = Path(file_path)
            selected_filter = _
            if "PDF" in selected_filter:
                format = "pdf"
            elif "HTML" in selected_filter:
                format = "html"
            elif "JSON" in selected_filter:
                format = "json"
            elif "Markdown" in selected_filter:
                format = "markdown"
            else:
                format = "html"  # Default to HTML
            self.model.generate_report(file_path, format)
            QMessageBox.information(self, "Success", f"Report saved to {file_path}")

    def init_analysis_view(self):
        layout = QVBoxLayout()
        self.analysis_view.setLayout(layout)

    def update_analysis_view(self):
        layout = self.analysis_view.layout()
        # Clear previous widgets
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not self.model.get_scan_results():
            return

        # Example analysis: personal data distribution
        personal_data = self.model.get_scan_results().get("personal_data", {})
        emails = len(personal_data.get("emails", []))
        authors = len(personal_data.get("authors", []))
        committers = len(personal_data.get("committers", []))

        # This is a placeholder for where you would use matplotlib/seaborn
        # to generate and display charts. For now, we'll just show a summary.
        summary = f"Emails: {emails}\nAuthors: {authors}\nCommitters: {committers}"
        label = QLabel(summary)
        layout.addWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
