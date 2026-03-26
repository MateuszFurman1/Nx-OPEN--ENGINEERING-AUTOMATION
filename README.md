NX Open Engineering Automation (Python)
This repository contains a collection of Python scripts developed using the NX Open API to automate repetitive tasks, manage metadata, and streamline engineering workflows within Siemens NX.

Key Features & Scripts:
-> Part List & BOM Management
- Part list- BOM: Scripts for automated extraction of assembly structures and attributes. Designed to bridge the gap between CAD models and ERP/Excel reporting.

- Resize Kolumn: Utility to automatically adjust UI/Table columns within NX drafting or reporting tools for better data visibility.

-> Geometry & Visual Automation
- Feature_color: Automatically assigns colors to specific features based on their type or attributes. Great for identifying manufacturing-ready surfaces (e.g., holes, milled faces).

- Body_random_color: A tool to quickly distinguish multiple bodies in a complex assembly by assigning unique random colors.

- Base_trimetric_view: One-click automation to set the display to a standardized trimetric view, ensuring consistency in technical documentation.

-> Work in Progress
-Macros- In work: Ongoing development of complex macros aimed at further reducing manual modeling time.

* Tech Stack
Language: Python

API: NX Open API, UF (User Function)

Environment: Siemens NX

* How to use
Open Siemens NX.

Go to Menu -> Tools -> Journal -> Play.

Select the desired .py file from this repository.
Alternatively, some scripts can be attached to custom icons in the NX Ribbon.
