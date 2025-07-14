# GUI Replacement Plan

This document outlines the plan for replacing the command-line interface (CLI) with a graphical user interface (GUI) using PySide6.

## I. Foundational Components

- [x] **Project Initialization**: Set up a new project structure with `main.py` as the entry point and `model.py` for business logic.
- [x] **Dependency Management**: Create a `requirements.txt` file listing all necessary dependencies, including `PySide6`.
- [x] **README Update**: Draft a `TINS_Edition/README.md` to explain the project's architecture, TINS motivation, and design choices.

## II. Core Application Window

- [x] **Main Window**: Create the main application window with a title, menu bar, and status bar.
- [x] **Menu Bar**:
    - [x] **File Menu**:
        - [x] "Select Repository" action to open a file dialog for choosing a Git repository.
        - [x] "Exit" action to close the application.
- [x] **Central Widget**:
    - [x] A tabbed interface to switch between different views (e.g., "Scan", "Report").

## III. Scan Configuration View

- [x] **Repository Selection**:
    - [x] A line edit to display the selected repository path.
    - [x] A "Browse" button to open the file dialog.
- [x] **Scan Options**:
    - [x] Checkboxes for scan options (e.g., "Include Forks").
    - [x] A text input for specifying GDPR articles to check.
- [x] **Scan Button**:
    - [x] A "Start Scan" button to trigger the scanning process.
- [x] **Progress Bar**:
    - [x] A progress bar to show the progress of the scan.

## IV. Report View

- [x] **Report Display**:
    - [x] A web view widget to display the HTML report.
- [x] **Report Actions**:
    - [x] "Save Report" button to save the report in different formats (HTML, PDF, JSON, Markdown).

## V. Business Logic and Data Model

- [x] **`model.py`**:
    - [x] Encapsulate the logic from `git_scanner.py`, `gdpr_analyser.py`, and `compliance_checker.py` into a `Model` class.
    - [x] The `Model` class will handle all the backend operations and data processing.
    - [x] Implement methods to:
        - [x] Set the repository path.
        - [x] Run the scan.
        - [x] Get the scan results.
        - [x] Generate the report.
- [x] **Signals and Slots**:
    - [x] Use signals and slots to communicate between the GUI and the `Model`.
    - [x] For example, the `Model` will emit a signal when the scan is complete, and the GUI will have a slot to receive this signal and update the report view.

## VI. Finalization

- [x] **Testing**:
    - [x] Add a `__main__` block to `model.py` to test its functionality.
    - [x] Perform a final integration review of all GUI elements.
- [x] **README Update**:
    - [x] Update the root `README.md` with instructions on how to install and run the new GUI application.

## VII. Advanced Features (Full Installation)

- [ ] **PDF Report Generation**:
    - [ ] Add a "Save as PDF" option to the "Save Report" dialog.
    - [ ] Implement the logic to generate PDF reports using `weasyprint`.
- [x] **Data Analysis Features**:
    - [x] Add a new "Analysis" tab to the GUI.
    - [x] Implement charts and visualizations using `matplotlib` and `seaborn`.
    - [x] Display data analysis results in the "Analysis" tab.
- [x] **Fork Analysis**:
    - [x] Add a new button to the GUI to trigger the fork analysis.
    - [x] Add a new method to the `Model` class to handle the fork analysis.
    - [x] Add a new view to the GUI to display the fork analysis results.
