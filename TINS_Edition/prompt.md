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

1. Read `scuffedepoch-tins.md` to extract guiding principles, intended functionality, and narrative design of TINS.
   - Commit to `new_GUI` branch: "Extracted TINS guiding principles and narrative design."
2. Analyze all source code modules in `src/gdpr_validator/` (`cli.py`, `report_generator.py`, `git_scanner.py`, `gdpr_analyser.py`, `compliance_checker.py`) for functionality and UI-related logic.
   - Commit to `new_GUI` branch: "Completed analysis of core modules and identified UI logic for refactor."
3. Plan the GUI replacement using PySide6 idioms, mapping CLI and report logic to GUI widgets. Document this plan as a checkbox list in `GUI_progress.md`.
   - Commit to `new_GUI` branch: "Planned PySide6 GUI architecture and widget mapping."
4. Create `TINS_Edition/README.md` summarizing project relationships, TINS motivation, design decisions, and implementation details based on the source code.
   - Commit to `new_GUI` branch: "Drafted TINS_Edition/README.md with project relationships and design rationale."
5. Study PySide6 idioms in `PySide6modern.md` and layout samples in `best_gui.py`. Refactor the main README.md to describe how the GUI will be reconstructed using PySide6 architecture (signals, slots, widget hierarchies).
   - Commit to `new_GUI` branch: "Updated root README.md with PySide6 architecture and integration details."
6. Implement `TINS_Edition/model.py` to encapsulate the data model and business logic derived from earlier analysis.
   - Commit to `new_GUI` branch: "Implemented core data model and business logic in model.py."
7. Implement `TINS_Edition/main.py` to handle PySide6 view/controller logic using appropriate design patterns (e.g., MVC or MVVM), connecting widgets to model logic.
   - Commit to `new_GUI` branch: "Implemented PySide6 view/controller logic in main.py."
8. Create `requirements.txt` in the root folder, including `PySide6==6.9.1` and any other necessary dependencies. (Use only the modern PySide6 6.9.1.)
   - Commit to `new_GUI` branch: "Added requirements.txt with PySide6==6.9.1 and dependencies."
9. Add a test block to the `__main__` section of `model.py` to validate functionality and detect architectural flaws.
10. Update the root `README.md` with standard GitHub install/run instructions, ensuring that usage aligns with TINS principles.
11. Test `model.py` and resolve any bugs uncovered during execution.
12. Perform a final integration review of GUI elements, verifying layout accuracy, event propagation, and modular consistency.
   - Commit to `new_GUI` branch: "Final integration review of GUI elements and architecture."
13. After each milestone, update `TINS_Edition/GUI_progress.md` and commit progress to `new_GUI` branch.

**Note:** Only update and mark progress in `TINS_Edition/GUI_progress.md` after completing a milestone (not every sub-step). The checkbox list should be maintained exclusively in `TINS_Edition/GUI_progress.md`.

## Task Checklist to update and mark progress:
`TINS_Edition/GUI_progress.md`
