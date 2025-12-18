## Load Combination Generator (Tkinter)

A desktop GUI application built with Python (Tkinter) to generate STAAD.Pro–style load cases and load combinations efficiently.
This tool helps structural engineers define load cases, subcases, coefficients, and automatically generate all valid load combinations with proper numbering.

**✨ Features**

📊 Spreadsheet-like interface for defining load cases and combinations

🧮 Automatic generation of load cases and load combinations

🔢 Supports multiple subcases per load case (combinatorial expansion)

🏷️ Load type selection (Dead, Live, Wind, Seismic, etc.)

⌨️ Keyboard navigation using arrow keys

📋 One-click copy of generated STAAD.Pro commands to clipboard

📈 Displays total number of load cases and combinations

🧹 Clear/reset all inputs instantly
  
  
**🖥️ Application Overview**
**Inputs**

Case Names – Base names for load cases (e.g., DL, LL, WL)

Load Types – Select from predefined load types

Combination Coefficients – Factors applied to each load case

Subcases – Number of subcases per load case

Start Load Number – Starting LOAD number

Start Combination Number – Starting LOAD COMB number

**Output**

STAAD.Pro–compatible LOAD definitions

Automatically expanded LOAD COMB definitions

Output window with copy-to-clipboard functionality

**📦 Sample Output**
Load Cases  
LOAD 1 LOADTYPE Dead TITLE DL1  
LOAD 2 LOADTYPE Dead TITLE DL2  
LOAD 3 LOADTYPE Live TITLE LL1  

Load Combinations  
LOAD COMB 101 COMB - + 1.0 DL1 + 1.5 LL1  
1 1.0 3 1.5  

  
**🚀 Installation & Usage**  
Requirements  

Python 3.8 or higher

No external dependencies (uses standard library only)

Run the Application
python load_combination_generator.py

  
**⌨️ Keyboard Navigation**

Arrow Keys – Move between table cells

Down Arrow – Jump from input fields to Generate button

Left / Right – Navigate between action buttons

Designed for fast, keyboard-driven data entry.
  

**📁 Project Structure**
load-combination-generator/  
│  
├── load_combination_generator.py  
├── README.md  

**📜 License**  

© Gaurav Bhardwaj. All rights reserved.  

This software is released under a custom personal license.
No part of this project may be copied, modified, distributed, or used commercially without explicit permission from the author.

**👷 Author**  
Gaurav Bhardwaj
