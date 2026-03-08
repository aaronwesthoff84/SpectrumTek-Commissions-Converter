# Commissions XML Python V3

This folder contains the minimal Python-only version of the SAP Commissions XML parser.

## Files

- `parse_commissions_xml.py` - entry point
- `sap_commissions_xml/` - parser package
- `requirements.txt` - Python dependency list
- `Example_Plan_For_Testing_D_B.xlsx` - example workbook output copied into this folder
- `commissions-xml-ui.ps1` - UI wrapper for setup, run, ship, and exit

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

You can also use the UI controller:

```powershell
.\commissions-xml-ui.ps1
```

Menu 1:

- `Setup`
- `Run`
- `Ship`
- `Exit`

Menu 2 after setup:

- `Run`
- `Exit`

## Run

Generate an Excel workbook from an SAP Commissions XML export:

```powershell
New-Item -ItemType Directory -Force .\generated | Out-Null
python .\parse_commissions_xml.py "C:\path\to\plan.xml" -o ".\generated\parsed_plan.xlsx"
```

Generate CSV output instead of an Excel workbook:

```powershell
New-Item -ItemType Directory -Force .\generated | Out-Null
python .\parse_commissions_xml.py "C:\path\to\plan.xml" -o ".\generated\output_csv" --format csv
```

## D&B Example

This folder includes `Example_Plan_For_Testing_D_B.xlsx` as an example of the parser output.

To run the parser against the matching D&B sample XML without modifying the shipped example file:

```powershell
New-Item -ItemType Directory -Force .\generated | Out-Null
python .\parse_commissions_xml.py "C:\Users\Work\OneDrive - SPECTRUMTEK\Documents\Spectrum Internal\Tech\XML Tool\TestPython\Commissions-XML-mainV2\D&B\D_B_Plan.xml" -o ".\generated\Example_Plan_For_Testing_D_B.xlsx"
```

Compare the generated file to the shipped sample at `.\Example_Plan_For_Testing_D_B.xlsx`.

## Ship

For testing, keep local output in `generated\`. When you are ready to ship, use the `Ship` menu option in `.\commissions-xml-ui.ps1`. It creates the next version folder from a whitelist of approved product files only.

Example from `V3`:

- Run `.\commissions-xml-ui.ps1`
- Choose `Ship`

That creates `F:\projects\Commissions-XML-Python_V4` and copies only the shipped project files into it. Extra local files such as `generated\`, `.venv`, caches, scratch notes, or stray test files are left behind in the old version and are not copied.

The shipped file set is:

- `.gitignore`
- `commissions-xml-ui.ps1`
- `Example_Plan_For_Testing_D_B.xlsx`
- `parse_commissions_xml.py`
- `README.md`
- `requirements.txt`
- `sap_commissions_xml\`
