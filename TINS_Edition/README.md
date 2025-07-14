# EU_GDPR_Git_Validator_TINS_Edition

This document provides an overview of the TINS Edition of the EU GDPR Git Validator, a project that refactors the original command-line tool into a modern GUI application using PySide6.

## Project Relationships

This project is a refactoring of the original EU GDPR Git Validator. The core logic for scanning Git repositories and analyzing them for GDPR compliance is preserved, but the user interface is completely replaced with a new GUI built with PySide6.

## TINS Motivation

The TINS (There Is No Source) methodology is a paradigm shift in software distribution. Instead of distributing source code, TINS applications are distributed as a set of instructions that an AI can use to generate the code on demand. This has several advantages, including smaller distribution sizes, automatic improvements as AI technology advances, and enhanced security.

This project is not a full Tins application, but it is a step in that direction. By separating the business logic from the UI and by providing a detailed plan for the UI, we are making it easier for an AI to understand and generate the code.

## Design Decisions

The main design decision was to use PySide6 for the GUI. PySide6 is a modern and powerful library for creating user interfaces in Python. It is also the official Python binding for the Qt framework, which is a mature and well-documented C++ library.

Another important design decision was to separate the business logic from the UI. This was done by creating a `model.py` file that encapsulates all the backend operations. The UI, which is implemented in `main.py`, communicates with the model using signals and slots. This makes the code more modular, easier to test, and easier to understand.

## Implementation Details

The application is divided into two main parts:

*   **`model.py`**: This file contains the business logic of the application. It encapsulates the functionality of the original `git_scanner.py`, `gdpr_analyser.py`, and `compliance_checker.py` modules.
*   **`main.py`**: This file contains the UI of the application. It is implemented using PySide6 and communicates with the model using signals and slots.

The application also has a `GUI_progress.md` file that documents the plan for the GUI replacement. This file serves as a roadmap for the project and helps to ensure that all the requirements are met.
