# Developer Guide

This guide provides in-depth documentation for developers who want to understand, modify, or extend the SpectrumTek Commissions Converter.

---

## Table of Contents

1. [Project Architecture Overview](#project-architecture-overview)
2. [File Reference](#file-reference)
3. [Common Modification Scenarios](#common-modification-scenarios)
4. [Development Workflow](#development-workflow)
5. [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## Project Architecture Overview

### High-Level Description

The SpectrumTek Commissions Converter is a Python application that parses SAP Commissions XML export files and converts them into structured Excel workbooks. The application originated from a VBA-based Excel workbook and has been ported to Python for cross-platform compatibility and easier maintenance.

### Core Concepts

The application handles several types of SAP Commissions data:
- **Plans** - Compensation plan definitions with component assignments
- **Components** - Groupings of rules that make up plan logic
- **Credit Rules** - Rules that allocate transaction credits
- **Measurements** - Primary/secondary measurement calculations
- **Incentives** - Commission and bulk commission calculations
- **Deposits** - Payment deposit rules
- **Lookup Tables** - Multi-dimensional lookup data
- **Rate Tables** - Rate tier definitions
- **Quota Tables** - Quota assignments by position
- **Fixed Values** - Constant values used in calculations
- **Variables** - Variable definitions
- **Formulas** - Formula expressions

### Data Flow

```
┌─────────────────┐     ┌─────────────────────┐     ┌───────────────────┐
│  XML Input      │────▶│  Parser             │────▶│  Writer           │
│  (SAP Export)   │     │  (parser.py)        │     │  (writer.py)      │
└─────────────────┘     └─────────────────────┘     └───────────────────┘
                                  │                           │
                                  │                           │
                        ┌─────────▼─────────┐       ┌─────────▼─────────┐
                        │ ExpressionParser  │       │  Excel Workbook   │
                        │ (function_parser) │       │  (.xlsx output)   │
                        └───────────────────┘       └───────────────────┘
```

**Step-by-step flow:**

1. **Input**: User provides an SAP Commissions XML export file (either via GUI or CLI)
2. **Parsing**: `SAPCommissionsXMLParser` reads and parses the XML structure
   - Uses Python's built-in `xml.etree.ElementTree` for XML parsing
   - Delegates expression parsing to `ExpressionParser` for formula/function nodes
   - Collects warnings/errors via `ParseLogger`
3. **Data Transformation**: Parsed data is organized into dictionaries keyed by sheet name
4. **Output Writing**: `write_xlsx_output()` creates an Excel workbook with:
   - Multiple sheets (one per data type)
   - Frozen header rows and auto-filters
   - Column headers mapped from internal keys to display names

### Application Entry Points

| Entry Point | Description |
|-------------|-------------|
| `gui_app.py` | Tkinter-based GUI application (what the .exe runs) |
| `parse_commissions_xml.py` | CLI entry point for command-line usage |
| `sap_commissions_xml/cli.py` | Actual CLI implementation with argument parsing |

---

## File Reference

### source/gui_app.py

**Purpose:** Provides the graphical user interface for end-users. This is the main entry point for the compiled executable.

**Key Classes:**
- `SpectrumTekConverterApp` - Main application class that manages:
  - Window setup and styling (SpectrumTek brand colors)
  - File selection dialogs (XML input, output folder)
  - Conversion process (runs in background thread)
  - Progress display and result presentation

**Key Methods:**
| Method | Description |
|--------|-------------|
| `_setup_window()` | Configures window size, title, positioning |
| `_setup_styles()` | Defines ttk styles for buttons, labels, progress bars |
| `_create_widgets()` | Builds the UI layout |
| `_select_xml_file()` | Opens file dialog to select XML input |
| `_start_conversion()` | Initiates conversion in background thread |
| `_run_conversion()` | Actual conversion logic (parsing + writing) |
| `_conversion_complete()` | Handles completion, displays results |

**When to modify:**
- Changing UI layout, colors, or branding
- Adding new user-facing options (e.g., format selection)
- Modifying conversion status/progress display
- Adding new output location options

---

### source/parse_commissions_xml.py

**Purpose:** Simple CLI entry point script. This is a thin wrapper that calls the `main()` function from `sap_commissions_xml.cli`.

**Contents:**
```python
from sap_commissions_xml.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
```

**When to modify:**
- Generally never - modifications should go to `cli.py` instead
- Only modify if you need to add initialization before CLI starts

---

### source/sap_commissions_xml/__init__.py

**Purpose:** Package initialization file. Exports the public API of the `sap_commissions_xml` package.

**Exports:**
- `ParseLogger` - For collecting warnings/errors during parsing
- `SAPCommissionsXMLParser` - Main parser class
- `write_csv_outputs` - CSV output writer
- `write_xlsx_output` - Excel output writer

**When to modify:**
- Adding new public classes/functions to the package
- Changing what's available when users `import sap_commissions_xml`

---

### source/sap_commissions_xml/cli.py

**Purpose:** Command-line interface implementation with argument parsing and main execution flow.

**Key Functions:**
| Function | Description |
|----------|-------------|
| `build_arg_parser()` | Creates `argparse.ArgumentParser` with supported arguments |
| `main()` | Main CLI entry point - parses args, runs conversion, outputs results |

**Supported CLI Arguments:**
- `input` - Path to SAP Commissions XML file (required)
- `-o, --output` - Output path (default: `parsed_plan.xlsx`)
- `--format` - Output format: `xlsx`, `csv`, or `auto` (default: `auto`)

**When to modify:**
- Adding new CLI arguments/options
- Changing default output filename or format
- Adding new output formats
- Modifying console output/reporting

---

### source/sap_commissions_xml/function_parser.py

**Purpose:** Parses function/expression nodes from XML into human-readable string format. This replicates the `mdFunctions.Parse_Function` logic from the original VBA project.

**Key Class:**
- `ExpressionParser` - Recursively parses expression tree nodes

**Supported Node Types:**
| Node Type | Handling |
|-----------|----------|
| `FUNCTION` | Converts to `FunctionName(arg1, arg2, ...)` format |
| `OPERATOR` | Converts to infix notation (e.g., `a + b`, `x AND y`) |
| `STRING_LITERAL` | Wraps in quotes, converts `NULL` to `-` |
| `VALUE` | Extracts attribute value |
| `*_REF` tags | Extracts `NAME` attribute |
| Literal tags | Extracts node text |

**Operator Mapping (`_OPERATOR_MAP`):**
Maps XML operator IDs to display symbols (e.g., `ADDITION_OPERATOR` → ` + `)

**When to modify:**
- Adding support for new function types
- Adding new operators
- Changing expression output format
- Fixing parsing edge cases

---

### source/sap_commissions_xml/logger.py

**Purpose:** Collects warnings and errors during parsing, formatted to match the VBA LOG sheet output.

**Key Classes:**
- `LogEntry` - Dataclass representing a single log entry
- `ParseLogger` - Main logger class

**LogEntry Fields:**
| Field | Description |
|-------|-------------|
| `timestamp` | ISO format timestamp |
| `module` | Source module name |
| `procedure` | Function/method name |
| `error_number` | Error type or "WARNING" |
| `description` | Error/warning message |
| `context` | Additional context info |

**ParseLogger Methods:**
| Method | Description |
|--------|-------------|
| `warning()` | Log a warning |
| `error()` | Log an exception/error |
| `as_rows()` | Convert to list of dicts for output |
| `count_warnings()` | Count warning entries |
| `count_errors()` | Count error entries |

**When to modify:**
- Adding new log fields
- Changing log format
- Adding log levels
- Integrating with external logging systems

---

### source/sap_commissions_xml/parser.py

**Purpose:** Core XML parsing logic. This is the heart of the application - it reads SAP Commissions XML and extracts structured data.

**Key Classes:**
- `SAPCommissionsXMLParser` - Main parser class
- `ParseResult` - Dataclass containing parsed rows and logger

**Supported Data Sets (matched in `_parse_node`):**
| XML Node | Method | Output Sheet |
|----------|--------|--------------|
| `PLAN_SET` | `_parse_plans()` | PLANS |
| `PLANCOMPONENT_SET` | `_parse_components()` | COMPONENTS |
| `RULE_SET` | `_parse_rule_set()` → type-specific methods | CREDITRULES, MEASUREMENTS, INCENTIVES, DEPOSITS |
| `MD_LOOKUP_TABLE_SET` | `_parse_lookup_tables()` | LOOKUP_TABLES |
| `RATETABLE_SET` | `_parse_rate_tables()` | RATE_TABLES |
| `QUOTA_SET` | `_parse_quota_tables()` | QUOTA_TABLES |
| `FIXED_VALUE_SET` | `_parse_fixed_values()` | FIXED_VALUES |
| `VARIABLE_SET` | `_parse_variables()` | VARIABLES |
| `FORMULA_SET` | `_parse_formulas()` | FORMULAS |

**Rule Types Handled:**
| Rule TYPE Attribute | Handler Method |
|---------------------|----------------|
| `DIRECT_TRANSACTION_CREDIT`, `ROLLUP_TRANSACTION_CREDIT` | `_parse_credit_rule()` |
| `PRIMARY_MEASUREMENT`, `SECONDARY_MEASUREMENT` | `_parse_measurement_rule()` |
| `BULK_COMMISSION`, `COMMISSION` | `_parse_incentive_rule()` |
| `DEPOSIT` | `_parse_deposit_rule()` |

**Key Patterns:**
- Each `_parse_*` method follows similar structure:
  1. Extract attributes from node
  2. Iterate over child nodes
  3. Delegate expression parsing to `function_parser`
  4. Build output rows and append to `rows` dict

**When to modify:**
- Adding support for new XML element types
- Extracting additional fields from existing elements
- Changing how data is structured/organized
- Fixing parsing bugs for specific XML structures

---

### source/sap_commissions_xml/writer.py

**Purpose:** Writes parsed data to output files (Excel or CSV).

**Key Data Structures:**
- `Column` - Dataclass mapping internal keys to display headers
- `SHEET_COLUMNS` - Dict defining columns for each output sheet

**Key Functions:**
| Function | Description |
|----------|-------------|
| `write_xlsx_output()` | Creates Excel workbook with all sheets |
| `write_csv_outputs()` | Creates separate CSV file per sheet |
| `_row_for_sheet()` | Extracts row values in column order |
| `_metric_columns()` | Generates GA1-16, GN1-6, GD1-6, GB1-6 columns |

**Sheet Features (Excel):**
- Frozen header row (`freeze_panes = "A2"`)
- Auto-filter enabled on all columns
- One sheet per data type

**When to modify:**
- Adding new columns to existing sheets
- Creating new output sheets
- Changing column headers/order
- Adding Excel formatting (colors, column widths)
- Adding new output formats

---

### source/requirements.txt

**Purpose:** Lists Python package dependencies.

**Current Dependencies:**
```
openpyxl>=3.1.0  # For Excel output
# pyinstaller>=6.0.0  # For building executables (dev only)
```

**When to modify:**
- Adding new dependencies for features
- Updating version requirements
- Adding optional dependencies

---

## Common Modification Scenarios

### Adding a New Data Field to Extract from XML

**Example:** Extract a new attribute `BUSINESS_UNIT` from PLAN nodes

1. **Update parser.py** - Modify `_parse_plans()`:
   ```python
   rows["PLANS"].append({
       # ... existing fields ...
       "BUSINESS_UNIT": plan.get("BUSINESS_UNIT", ""),  # Add new field
   })
   ```

2. **Update writer.py** - Add column to `SHEET_COLUMNS["PLANS"]`:
   ```python
   "PLANS": [
       # ... existing columns ...
       Column("BUSINESS_UNIT", "Business Unit"),  # Add new column
   ],
   ```

3. **Test** - Run against XML that contains the new attribute

---

### Changing Excel Output Format/Columns

**Example:** Rename a column header

1. **Edit writer.py** - Find the column in `SHEET_COLUMNS`:
   ```python
   # Before
   Column("EFFECTIVE_START_DATE", "Start Date"),
   # After
   Column("EFFECTIVE_START_DATE", "Effective Start"),
   ```

**Example:** Reorder columns

1. **Edit writer.py** - Rearrange `Column` entries in the list (order matters)

**Example:** Add Excel formatting

1. **Edit writer.py** - Modify `write_xlsx_output()`:
   ```python
   from openpyxl.styles import Font, PatternFill
   
   # After creating worksheet
   header_font = Font(bold=True)
   header_fill = PatternFill(start_color="449877", fill_type="solid")
   
   for cell in ws[1]:  # First row
       cell.font = header_font
       cell.fill = header_fill
   ```

---

### Adding New Parsing Logic

**Example:** Support a new XML SET type `CUSTOM_DATA_SET`

1. **Update parser.py** - Add handler method:
   ```python
   def _parse_custom_data(self, node: Element, rows: dict) -> None:
       for item_node in list(node):
           item = dict(item_node.attrib)
           rows["CUSTOM_DATA"].append({
               "NAME": item.get("NAME", ""),
               "VALUE": item.get("VALUE", ""),
           })
   ```

2. **Update `_parse_node()`** in parser.py:
   ```python
   elif node_name == "CUSTOM_DATA_SET":
       self._parse_custom_data(node, rows)
   ```

3. **Add to `DATA_SHEETS`** list in parser.py:
   ```python
   DATA_SHEETS = [
       # ... existing ...
       "CUSTOM_DATA",
   ]
   ```

4. **Add columns** in writer.py:
   ```python
   "CUSTOM_DATA": [
       Column("NAME", "Name"),
       Column("VALUE", "Value"),
   ],
   ```

---

### Modifying the GUI

**Example:** Change brand colors

1. **Edit gui_app.py** - Update color constants at top:
   ```python
   PRIMARY_COLOR = "#FF5733"      # New primary color
   SECONDARY_COLOR = "#1A1A2E"    # New secondary color
   ```

**Example:** Add a new button

1. **Edit `_create_main_content()`** in gui_app.py:
   ```python
   self.new_button = tk.Button(
       button_frame,
       text="New Action",
       command=self._new_action_handler
   )
   self.new_button.pack()
   ```

2. **Add handler method**:
   ```python
   def _new_action_handler(self):
       # Handle button click
       pass
   ```

**Example:** Add format selection dropdown

1. **Create ttk.Combobox** in content area
2. **Store selection** in instance variable
3. **Use selection** in `_run_conversion()` to choose output format

---

### Adding New Dependencies

1. **Add to requirements.txt**:
   ```
   new-package>=1.0.0
   ```

2. **Update build scripts** if needed (spec files may need `hiddenimports`)

3. **Update spec files** in `source/build_config/`:
   ```python
   hiddenimports=['new_package'],
   ```

---

## Development Workflow

### Setting Up a Dev Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aaronwesthoff84/SpectrumTek-Commissions-Converter.git
   cd SpectrumTek-Commissions-Converter
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r source/requirements.txt
   pip install pyinstaller  # For building executables
   ```

### Testing Changes Locally (Running Python Scripts Directly)

**Run the GUI directly:**
```bash
cd source
python gui_app.py
```

**Run the CLI directly:**
```bash
cd source
python parse_commissions_xml.py input.xml -o output.xlsx
```

**Test from project root:**
```bash
python source/gui_app.py
python source/parse_commissions_xml.py input.xml -o output.xlsx
```

### Rebuilding After Changes

After making code changes, you'll need to rebuild the executable:

**Windows:**
```batch
cd source
BUILD_EXE.bat
```

**macOS:**
```bash
cd source
./BUILD_APP.sh
```

**Linux:**
```bash
cd source
./BUILD_LINUX.sh
```

**Output locations:**
- Windows: `releases/windows/SpectrumTek_Commissions_Converter.exe`
- macOS: `releases/macos/SpectrumTek Commissions Converter.app`
- Linux: `releases/linux/SpectrumTek_Commissions_Converter`

### Testing the Built Executable

1. **Navigate to releases folder:**
   ```bash
   cd releases/windows  # or macos/linux
   ```

2. **Run the executable:**
   - Windows: Double-click `SpectrumTek_Commissions_Converter.exe`
   - macOS: Open `SpectrumTek Commissions Converter.app`
   - Linux: `./SpectrumTek_Commissions_Converter`

3. **Test with sample XML:**
   - Select your test XML file
   - Verify conversion completes
   - Check output Excel file has expected data

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
# ...

# Commit changes
git add .
git commit -m "Add: description of changes"

# Push and create PR
git push origin feature/your-feature-name
```

---

## Troubleshooting Common Issues

### "Module not found" errors when running from source

**Cause:** Python can't find the `sap_commissions_xml` package

**Solution:**
```bash
# Run from the source directory
cd source
python gui_app.py

# Or set PYTHONPATH
export PYTHONPATH=/path/to/Commissions-XML-To-XLS/source
python gui_app.py
```

### "openpyxl not installed" error

**Cause:** Missing dependency

**Solution:**
```bash
pip install openpyxl
# or
pip install -r source/requirements.txt
```

### GUI doesn't launch (Tkinter errors)

**Cause:** Tkinter not installed (common on Linux)

**Solution (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**Solution (Fedora/RHEL):**
```bash
sudo dnf install python3-tkinter
```

### Build fails with PyInstaller

**Common causes and solutions:**

1. **Missing PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Permission denied (Linux/macOS):**
   ```bash
   chmod +x source/BUILD_LINUX.sh  # or BUILD_APP.sh
   ```

3. **Hidden imports missing:** Update spec file:
   ```python
   hiddenimports=['missing_module'],
   ```

### XML parsing errors

**Cause:** Invalid or unsupported XML structure

**Debug steps:**
1. Check the LOG sheet in output for specific errors
2. Validate XML is well-formed
3. Check if XML uses expected SAP Commissions format
4. Look for unsupported element types in parser warnings

### Output Excel is empty or missing data

**Debug steps:**
1. Check LOG sheet for parsing warnings
2. Run CLI with verbose output to see row counts
3. Verify XML contains expected data types
4. Check if new element types need parser support

### Changes not appearing in rebuilt executable

**Cause:** Old build artifacts

**Solution:**
1. Delete `source/dist/` and `source/build_temp/` folders
2. Rebuild from scratch

### Performance issues with large XML files

**Tips:**
- Large XML files (>100MB) may take time to parse
- Progress bar indicates conversion is running
- Consider streaming parsing for very large files (advanced modification)

---

## Additional Resources

- [BUILD_GUIDE.md](BUILD_GUIDE.md) - Detailed build instructions
- [README.md](../README.md) - Project overview and quick start
- [openpyxl documentation](https://openpyxl.readthedocs.io/) - Excel writing library
- [PyInstaller documentation](https://pyinstaller.org/) - Executable bundling
