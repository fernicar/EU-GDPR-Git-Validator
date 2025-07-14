import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLineEdit, QProgressBar, QTabWidget,
    QMessageBox, QLabel
)
from PySide6.QtWidgets import QTextBrowser
from PySide6.QtCore import QUrl, Slot, QThread, Signal
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

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.scan_view = QWidget()
        self.report_view = QTextBrowser()

        self.tabs.addTab(self.scan_view, "Scan")
        self.tabs.addTab(self.report_view, "Report")

        self.init_scan_view()

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
        with open(report_path, "r") as f:
            self.report_view.setHtml(f.read())
        self.tabs.setCurrentWidget(self.report_view)

    @Slot(str)
    def scan_error(self, error_message):
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.scan_button.setEnabled(True)
        QMessageBox.critical(self, "Error", f"An error occurred during the scan:\n{error_message}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
