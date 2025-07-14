# Operational Instructions for GUI Refactor Project: EU_GDPR_Git_Validator_TINS_Edition

## Branch Policy
- Always commit to the branch named `new_GUI` after each milestone (see milestones in GUI_progress.md).

## Repository Structure
- The root folder contains the main source code in `src/gdpr_validator/`:
  - `cli.py`: CLI entry points and orchestration logic
  - `report_generator.py`: Report generation in multiple formats
  - `git_scanner.py`: Repository scanning and PII detection
  - `gdpr_analyser.py`: GDPR compliance analysis
  - `compliance_checker.py`: Article compliance checks
- The TINS_Edition folder contains supporting files for GUI design, TINS methodology, and modernization:
  - `best_gui.py`, `GUI_progress.md`, `PySide6modern.md`, `scuffedepoch-sysp.md`, `scuffedepoch-tins.md`

## Behavioral Rules
1. Do NOT rely solely on documentation, verify all logic and functionality via the actual Python source files in `src/gdpr_validator/`.
2. Treat the source code modules as the source of truth for application logic and GUI mapping.
3. Use files in TINS_Edition as reference for GUI modernization and TINS principles.

## Development Tasks

1. Understand what TINS is by reading `scuffedepoch-tins.md` files.
2. Analyze all source code modules in `src/gdpr_validator/` (`cli.py`, `report_generator.py`, `git_scanner.py`, `gdpr_analyser.py`, `compliance_checker.py`) for functionality and UI-related logic.
3. Plan the GUI replacement using PySide6 idioms, mapping CLI and report logic to GUI widgets. Document this plan as a checkbox list in `GUI_progress.md`.
4. Commit to `new_GUI` branch: "Planned PySide6 GUI architecture and widget mapping."
5. Create the TINS `TINS_Edition/README.md` summarizing project relationships, design, and implementation details based on the source code.
6. Commit to `new_GUI` branch: "Drafted TINS_Edition/README.md with project relationships and design rationale."
7. Study PySide6 idioms in `PySide6modern.md` and layout samples in `best_gui.py`. Refactor the TINS `TINS_Edition/README.md` to describe how the GUI will be reconstructed using PySide6 version 6.9.1 architecture (signals, slots, widget hierarchies).
8. Commit to `new_GUI` branch: "Updated root README.md with PySide6 architecture and integration details."
9. Implement `model.py` to encapsulate the data model and business logic derived from earlier analysis.
10. Implement `main.py` to handle PySide6 view/controller logic using appropriate design patterns (e.g., MVC or MVVM), connecting widgets to model logic.
11. Create `requirements.txt` in the root folder, including `PySide6==6.9.1` and any other necessary dependencies. (Use only the modern PySide6 6.9.1.)
12. Commit to `new_GUI` branch: "Implemented core data model, view/controller logic."
13. Add a test block to the `__main__` section of `model.py` to validate functionality and detect architectural flaws.
14. Update the root `README.md` with standard GitHub install/run instructions, ensuring that usage aligns with TINS principles.
11. Test `model.py` and resolve any bugs uncovered during execution.
12. Perform a final integration review of GUI elements, verifying layout accuracy, event propagation, and modular consistency.
13. Commit to `new_GUI` branch: "Final integration review of GUI elements and architecture."

**Note:** Only update and mark progress in `TINS_Edition/GUI_progress.md` after completing a milestone (not every sub-step). The checkbox list should be maintained exclusively in `TINS_Edition/GUI_progress.md`.

## Task Checklist to update and mark progress:
`TINS_Edition/GUI_progress.md`
