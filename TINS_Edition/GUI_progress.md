
## Source-Driven GUI Refactor Plan with Commit Checkpoints

- [ ] Understand TINS requirements from `TINS_Edition/scuffedepoch-tins.md`.
  - **Checkpoint:** Commit findings and extracted principles to `new_GUI` branch.

- [ ] Analyze all source code in `src/gdpr_validator/` (`cli.py`, `report_generator.py`, `git_scanner.py`, `gdpr_analyser.py`, `compliance_checker.py`) for functionality and UI logic.
  - **Checkpoint:** Commit analysis notes and identified UI logic to `new_GUI` branch.

- [ ] Design PySide6 GUI structure based on TINS principles and source code modules:
    - Map CLI entry points to GUI actions.
    - Plan widgets for report generation, repository scanning, compliance analysis, and result display.
  - **Checkpoint:** Commit initial GUI design and widget mapping to `new_GUI` branch.

- [ ] Create `TINS_Edition/README.md` summarizing TINS motivation, design decisions, and implementation details.
  - **Checkpoint:** Commit README draft to `new_GUI` branch.

- [ ] Integrate PySide6 idioms and layout strategies:
    - Review `PySide6modern.md` and `best_gui.py` for best practices.
    - Document signal-slot mappings, widget hierarchies, and GUI design logic.
  - **Checkpoint:** Commit updated GUI architecture documentation to `new_GUI` branch.

- [ ] Implement Model component (`model.py`) to encapsulate business logic from all major modules.
  - **Checkpoint:** Commit initial model implementation to `new_GUI` branch.

- [ ] Implement View/Controller component (`main.py`) using PySide6, connecting widgets to model logic.
  - **Checkpoint:** Commit initial view/controller implementation to `new_GUI` branch.

- [ ] Create root `requirements.txt` with `PySide6==6.9.1` and other dependencies.
  - **Checkpoint:** Commit requirements file to `new_GUI` branch.

- [ ] Add a `__main__` test block to `model.py` for validating functionality.
  - **Checkpoint:** Commit test block and results to `new_GUI` branch.

- [ ] Update main `README.md` with installation and usage instructions aligned with TINS principles.
  - **Checkpoint:** Commit updated README to `new_GUI` branch.

- [ ] Test `model.py` and fix any bugs.
  - **Checkpoint:** Commit bug fixes and test results to `new_GUI` branch.

- [ ] Test `main.py` (GUI interaction) and fix any bugs.
  - **Checkpoint:** Commit GUI test results and fixes to `new_GUI` branch.

- [ ] Final review of GUI layout, event propagation, and modular consistency.
  - **Checkpoint:** Commit final integration review to `new_GUI` branch.
