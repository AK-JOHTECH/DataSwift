Dimensional Entry & Inspection System
This repository contains a custom desktop application used for dimensional data entry, inspection, and analysis of ceramic components at various stages of the manufacturing process — specifically during the Green (Drill) and Fired (FT) states. Built with Python and CustomTkinter, this system provides a modern GUI and integrates with an internal SQL Server database for part validation, dimensional tracking, and PDF report generation.

Features
Login & Access Control
IT-managed login system with role-based access (Drill-only, FT-only, Full Access, etc.).

New & Edit Entry Forms

Input fields for OD, Length, Thickness, Width, Warpage, and Inner Diameters (ID1–ID3).

Automatically adapts required fields based on part type.

Validates existing entries to prevent duplicates.

Multi-Frame Navigation

Each dimension group gets its own tab with dynamic labels and placeholders.

Smart navigation using Enter key for rapid data input.

Query & Reporting Tool

Search parts by Part Number, MO, or Revision.

View associated Drill and FT dimension switches.

Generate statistical reports with charts and auto-generated PDF documents.

Statistical Analysis

Range, average, standard deviation, and variance calculations.

Binomial defect testing for MRB and yield-loss flags.

Control charts and visual plots using matplotlib.

Automated PDF Export

Converts dimensional results into a styled Word document.

Auto-generates PDF summary reports via docx2pdf.


Directory Structure: 
.
├── access.py           # SQL Server read/write logic for Drill & FT dimensions
├── Access_Page.py      # Entry point for new/edit dimensional entries
├── CTKlib.py           # Custom UI framework with reusable windows and navigation
├── DataSwift.py        # Main executable entry script
├── Drill_Form.py       # Drill (green-state) data input GUI
├── Fired_Form.py       # Fired-state data input GUI
├── Login.py            # Login and signup system with access role filtering
├── Query.py            # Query interface and results window
├── Sucess.py           # Confirmation screen with report generation
├── word_temp.py        # Report formatting, statistical analysis, and PDF conversion


