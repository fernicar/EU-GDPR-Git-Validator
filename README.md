# 🔒 EU GDPR Git Validator (TINS Edition)

**Are your Git repositories GDPR compliant?**

This tool analyzes your Git history for potential European data protection violations. This TINS Edition refactors the original command-line tool into a modern GUI application using PySide6, following the principles of TINS (There Is No Source).

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GDPR Compliant](https://img.shields.io/badge/GDPR-Compliant%20Tool-green.svg)](https://gdpr.eu/)

## 🚀 GUI Architecture

This version of the EU GDPR Git Validator features a new GUI built with PySide6. The architecture is designed to be modular and extensible, with a clear separation between the business logic and the user interface.

### Key Architectural Features:

*   **PySide6-based GUI**: The entire user interface is built using PySide6, the official Python bindings for the Qt framework.
*   **Model-View-Controller (MVC) Pattern**: The application follows the MVC pattern to separate the data model, the user interface, and the control logic.
*   **`model.py`**: This file encapsulates the core business logic of the application, including the Git scanner, GDPR analyzer, and compliance checker.
*   **`main.py`**: This file contains the view and controller logic for the PySide6-based GUI.
*   **Signals and Slots**: The GUI communicates with the business logic using Qt's signals and slots mechanism, ensuring a decoupled and event-driven architecture.
*   **Jinja2 Templates for Reports**: The application uses Jinja2 templates to generate interactive and user-friendly HTML reports.

### GUI Components:

*   **Main Window**: A central window that provides access to all the application's features.
*   **Repository Selection**: A user-friendly interface for selecting the Git repository to be analyzed.
*   **Scan Configuration**: Options for customizing the scan, such as selecting specific GDPR articles to check.
*   **Interactive Report View**: A web view widget for displaying the HTML compliance report.

## 📋 What This Tool Does

- **🔍 Git History Scanner**: Analyzes commit logs for personal identifiable information
- **🌐 Fork Tracking**: Documents how personal data propagates across repository forks
- **🔐 Hash Analysis**: Examains git hashes for permanent data retention issues
- **📊 Branch Inspection**: Checks branch metadata for personal data exposure
- **✅ GDPR Compliance Checker**: Validates against specific GDPR articles
- **📄 Report Generator**: Creates detailed compliance documentation in various formats (HTML, PDF, JSON, Markdown)

## 🎯 Why You Need This

Every Git repository potentially contains:
- Author names and email addresses in commit history
- Timestamps creating detailed activity patterns
- Personal data that propagates across forks indefinitely
- Cross-border data transfers without explicit consent
- Permanent data retention violating erasure rights

**⭐ Star this repo** to stay updated  
**🍴 Fork to contribute** improvements  
**📥 Clone to test** your repositories  

*Every interaction helps us improve GDPR compliance tooling for the community!*

## 🔧 Installation

```bash
git clone https://github.com/DragonDiffusionbyBoyo/EU-GDPR-Git-Validator.git
cd EU-GDPR-Git-Validator
pip install -r requirements.txt
python TINS_Edition/main.py
```

## Usage

1.  Launch the application by running `python TINS_Edition/main.py`.
2.  Click the "Select Repository" button to choose the Git repository you want to analyze.
3.  Configure the scan options as needed.
4.  Click the "Start Scan" button to begin the analysis.
5.  Once the scan is complete, the compliance report will be displayed in the report view.
6.  You can save the report in various formats using the "Save Report" button.

## 🤝 Contributing

We welcome contributions! This project helps the entire development community understand and address GDPR compliance challenges in version control systems.

1.  Fork the repository
2.  Create a feature branch
3.  Make your changes
4.  Add tests for new functionality
5.  Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal Notice

This tool is designed for educational and compliance purposes. It identifies potential GDPR compliance issues but does not constitute legal advice. Consult with qualified legal professionals for specific compliance requirements.
