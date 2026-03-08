#!/usr/bin/env python3
"""
SpectrumTek Commissions Converter
A GUI application to convert SAP Commissions XML exports to Excel workbooks.
"""

import os
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Optional

# Add the project directory to path for imports when running as a script
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = Path(sys.executable).parent
else:
    # Running as script
    application_path = Path(__file__).parent

sys.path.insert(0, str(application_path))

from sap_commissions_xml.parser import SAPCommissionsXMLParser
from sap_commissions_xml.writer import SHEET_COLUMNS, write_xlsx_output


# SpectrumTek Brand Colors
PRIMARY_COLOR = "#449877"       # Teal/Green
SECONDARY_COLOR = "#062B33"     # Dark Navy
ACCENT_COLOR = "#5DB592"        # Lighter teal for hover states
BG_COLOR = "#FFFFFF"            # White background
TEXT_LIGHT = "#FFFFFF"          # White text
TEXT_DARK = "#062B33"           # Dark text


class SpectrumTekConverterApp:
    """Main GUI Application for SpectrumTek Commissions Converter."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.xml_file_path: Optional[Path] = None
        self.output_dir: Optional[Path] = None
        self.is_converting = False
        
        self._setup_window()
        self._setup_styles()
        self._create_widgets()
    
    def _setup_window(self):
        """Configure the main window."""
        self.root.title("SpectrumTek Commissions Converter")
        self.root.geometry("600x450")
        self.root.minsize(500, 400)
        self.root.configure(bg=BG_COLOR)
        
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")
        
        # Configure grid weights for responsive layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
    
    def _setup_styles(self):
        """Configure ttk styles for the application."""
        self.style = ttk.Style()
        
        # Configure button style
        self.style.configure(
            "Primary.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(20, 10)
        )
        
        self.style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 10),
            padding=(15, 8)
        )
        
        # Configure label styles
        self.style.configure(
            "Header.TLabel",
            font=("Segoe UI", 24, "bold"),
            background=SECONDARY_COLOR,
            foreground=TEXT_LIGHT
        )
        
        self.style.configure(
            "Subheader.TLabel",
            font=("Segoe UI", 11),
            background=SECONDARY_COLOR,
            foreground=PRIMARY_COLOR
        )
        
        self.style.configure(
            "Info.TLabel",
            font=("Segoe UI", 10),
            background=BG_COLOR,
            foreground=TEXT_DARK
        )
        
        self.style.configure(
            "Path.TLabel",
            font=("Segoe UI", 9),
            background=BG_COLOR,
            foreground="#666666"
        )
        
        # Configure progress bar
        self.style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="#E0E0E0",
            background=PRIMARY_COLOR,
            thickness=8
        )
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Header section
        self._create_header()
        
        # Main content section
        self._create_main_content()
        
        # Status bar
        self._create_status_bar()
    
    def _create_header(self):
        """Create the branded header section."""
        header_frame = tk.Frame(self.root, bg=SECONDARY_COLOR, height=100)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_propagate(False)
        
        # App title
        title_label = ttk.Label(
            header_frame,
            text="SpectrumTek",
            style="Header.TLabel"
        )
        title_label.grid(row=0, column=0, pady=(20, 0))
        
        # Subtitle
        subtitle_label = ttk.Label(
            header_frame,
            text="Commissions XML to Excel Converter",
            style="Subheader.TLabel"
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 10))
    
    def _create_main_content(self):
        """Create the main content area."""
        content_frame = tk.Frame(self.root, bg=BG_COLOR, padx=30, pady=20)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Step 1: Select XML File
        step1_frame = tk.Frame(content_frame, bg=BG_COLOR)
        step1_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        step1_frame.grid_columnconfigure(1, weight=1)
        
        step1_label = ttk.Label(
            step1_frame,
            text="1. XML File:",
            style="Info.TLabel"
        )
        step1_label.grid(row=0, column=0, sticky="w")
        
        self.xml_path_var = tk.StringVar(value="No file selected")
        self.xml_path_label = ttk.Label(
            step1_frame,
            textvariable=self.xml_path_var,
            style="Path.TLabel"
        )
        self.xml_path_label.grid(row=0, column=1, sticky="w", padx=(10, 0))
        
        self.select_xml_btn = tk.Button(
            step1_frame,
            text="Select XML File",
            font=("Segoe UI", 10),
            bg=PRIMARY_COLOR,
            fg=TEXT_LIGHT,
            activebackground=ACCENT_COLOR,
            activeforeground=TEXT_LIGHT,
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._select_xml_file
        )
        self.select_xml_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Step 2: Output Location
        step2_frame = tk.Frame(content_frame, bg=BG_COLOR)
        step2_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        step2_frame.grid_columnconfigure(1, weight=1)
        
        step2_label = ttk.Label(
            step2_frame,
            text="2. Output Folder:",
            style="Info.TLabel"
        )
        step2_label.grid(row=0, column=0, sticky="w")
        
        self.output_path_var = tk.StringVar(value="Same as XML file location")
        self.output_path_label = ttk.Label(
            step2_frame,
            textvariable=self.output_path_var,
            style="Path.TLabel"
        )
        self.output_path_label.grid(row=0, column=1, sticky="w", padx=(10, 0))
        
        self.select_output_btn = tk.Button(
            step2_frame,
            text="Change...",
            font=("Segoe UI", 9),
            bg="#E0E0E0",
            fg=TEXT_DARK,
            activebackground="#D0D0D0",
            relief="flat",
            padx=10,
            pady=3,
            cursor="hand2",
            command=self._select_output_folder
        )
        self.select_output_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Separator line
        separator = tk.Frame(content_frame, height=1, bg="#E0E0E0")
        separator.grid(row=2, column=0, sticky="ew", pady=15)
        
        # Progress section
        progress_frame = tk.Frame(content_frame, bg=BG_COLOR)
        progress_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="")
        self.progress_label = ttk.Label(
            progress_frame,
            textvariable=self.progress_var,
            style="Info.TLabel"
        )
        self.progress_label.grid(row=0, column=0, sticky="w")
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            style="Custom.Horizontal.TProgressbar",
            mode="indeterminate",
            length=300
        )
        # Progress bar hidden initially
        
        # Convert button
        button_frame = tk.Frame(content_frame, bg=BG_COLOR)
        button_frame.grid(row=4, column=0, pady=(10, 0))
        
        self.convert_btn = tk.Button(
            button_frame,
            text="Convert to Excel",
            font=("Segoe UI", 12, "bold"),
            bg=PRIMARY_COLOR,
            fg=TEXT_LIGHT,
            activebackground=ACCENT_COLOR,
            activeforeground=TEXT_LIGHT,
            relief="flat",
            padx=40,
            pady=12,
            cursor="hand2",
            state="disabled",
            command=self._start_conversion
        )
        self.convert_btn.pack()
        
        # Results section
        self.results_frame = tk.Frame(content_frame, bg=BG_COLOR)
        self.results_frame.grid(row=5, column=0, sticky="ew", pady=(20, 0))
        self.results_frame.grid_columnconfigure(0, weight=1)
    
    def _create_status_bar(self):
        """Create the status bar at the bottom."""
        status_frame = tk.Frame(self.root, bg="#F5F5F5", height=30)
        status_frame.grid(row=4, column=0, sticky="ew")
        status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            bg="#F5F5F5",
            fg="#666666",
            anchor="w",
            padx=10
        )
        status_label.pack(fill="x", pady=5)
    
    def _select_xml_file(self):
        """Open file dialog to select XML file."""
        filetypes = [
            ("XML Files", "*.xml"),
            ("All Files", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="Select SAP Commissions XML File",
            filetypes=filetypes
        )
        
        if filepath:
            self.xml_file_path = Path(filepath)
            # Show truncated path if too long
            display_path = self._truncate_path(filepath, 50)
            self.xml_path_var.set(display_path)
            
            # Set default output to same directory
            self.output_dir = self.xml_file_path.parent
            self.output_path_var.set(self._truncate_path(str(self.output_dir), 45))
            
            # Enable convert button
            self.convert_btn.config(state="normal")
            self.status_var.set(f"Selected: {self.xml_file_path.name}")
    
    def _select_output_folder(self):
        """Open folder dialog to select output location."""
        initial_dir = str(self.output_dir) if self.output_dir else "/"
        
        folder_path = filedialog.askdirectory(
            title="Select Output Folder",
            initialdir=initial_dir
        )
        
        if folder_path:
            self.output_dir = Path(folder_path)
            self.output_path_var.set(self._truncate_path(folder_path, 45))
            self.status_var.set(f"Output folder: {self.output_dir.name}")
    
    def _truncate_path(self, path: str, max_length: int) -> str:
        """Truncate path string for display."""
        if len(path) <= max_length:
            return path
        return "..." + path[-(max_length - 3):]
    
    def _start_conversion(self):
        """Start the conversion process in a background thread."""
        if self.is_converting:
            return
        
        if not self.xml_file_path or not self.xml_file_path.exists():
            messagebox.showerror("Error", "Please select a valid XML file.")
            return
        
        self.is_converting = True
        self._update_ui_for_conversion(True)
        
        # Run conversion in background thread
        thread = threading.Thread(target=self._run_conversion, daemon=True)
        thread.start()
    
    def _update_ui_for_conversion(self, is_converting: bool):
        """Update UI state during conversion."""
        if is_converting:
            self.convert_btn.config(state="disabled", text="Converting...")
            self.select_xml_btn.config(state="disabled")
            self.select_output_btn.config(state="disabled")
            self.progress_var.set("Processing XML file...")
            self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(5, 0))
            self.progress_bar.start(10)
            self.status_var.set("Converting...")
        else:
            self.convert_btn.config(state="normal", text="Convert to Excel")
            self.select_xml_btn.config(state="normal")
            self.select_output_btn.config(state="normal")
            self.progress_bar.stop()
            self.progress_bar.grid_remove()
    
    def _run_conversion(self):
        """Run the actual conversion (called from background thread)."""
        try:
            # Parse the XML file
            parser = SAPCommissionsXMLParser()
            result = parser.parse_file(self.xml_file_path)
            
            # Generate output filename
            output_filename = self.xml_file_path.stem + "_converted.xlsx"
            output_path = self.output_dir / output_filename
            
            # Write Excel output
            written_path = write_xlsx_output(result.rows, output_path)
            
            # Collect statistics
            stats = {
                name: len(result.rows.get(name, []))
                for name in SHEET_COLUMNS.keys()
                if name != "LOG"
            }
            warnings = result.logger.count_warnings()
            errors = result.logger.count_errors()
            
            # Update UI on main thread
            self.root.after(0, lambda: self._conversion_complete(
                success=True,
                output_path=written_path,
                stats=stats,
                warnings=warnings,
                errors=errors
            ))
            
        except Exception as e:
            error_message = str(e)
            self.root.after(0, lambda: self._conversion_complete(
                success=False,
                error=error_message
            ))
    
    def _conversion_complete(self, success: bool, output_path: Path = None,
                            stats: dict = None, warnings: int = 0,
                            errors: int = 0, error: str = None):
        """Handle conversion completion (called on main thread)."""
        self.is_converting = False
        self._update_ui_for_conversion(False)
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        if success:
            self.progress_var.set("✓ Conversion complete!")
            self.status_var.set(f"Output saved: {output_path.name}")
            
            # Show success message with details
            result_text = f"Output: {output_path.name}\n\n"
            result_text += "Records processed:\n"
            total_rows = 0
            for sheet, count in stats.items():
                if count > 0:
                    result_text += f"  • {sheet}: {count} rows\n"
                    total_rows += count
            result_text += f"\nTotal: {total_rows} rows"
            
            if warnings > 0 or errors > 0:
                result_text += f"\n\nWarnings: {warnings}, Errors: {errors}"
            
            # Create results display
            result_label = tk.Label(
                self.results_frame,
                text=result_text,
                font=("Segoe UI", 9),
                bg="#E8F5E9",
                fg="#2E7D32",
                justify="left",
                anchor="w",
                padx=15,
                pady=10
            )
            result_label.pack(fill="x")
            
            # Open folder button
            open_btn = tk.Button(
                self.results_frame,
                text="Open Output Folder",
                font=("Segoe UI", 9),
                bg="#E0E0E0",
                fg=TEXT_DARK,
                relief="flat",
                padx=10,
                pady=5,
                cursor="hand2",
                command=lambda: self._open_folder(output_path.parent)
            )
            open_btn.pack(pady=(10, 0))
            
        else:
            self.progress_var.set("✗ Conversion failed")
            self.status_var.set("Error during conversion")
            
            # Show error message
            error_label = tk.Label(
                self.results_frame,
                text=f"Error: {error}",
                font=("Segoe UI", 9),
                bg="#FFEBEE",
                fg="#C62828",
                justify="left",
                anchor="w",
                padx=15,
                pady=10,
                wraplength=500
            )
            error_label.pack(fill="x")
            
            messagebox.showerror(
                "Conversion Error",
                f"Failed to convert the XML file:\n\n{error}"
            )
    
    def _open_folder(self, folder_path: Path):
        """Open the folder in the system file explorer."""
        import subprocess
        import platform
        
        system = platform.system()
        try:
            if system == "Windows":
                os.startfile(str(folder_path))
            elif system == "Darwin":  # macOS
                subprocess.run(["open", str(folder_path)])
            else:  # Linux
                subprocess.run(["xdg-open", str(folder_path)])
        except Exception as e:
            messagebox.showwarning(
                "Could not open folder",
                f"Unable to open folder: {e}"
            )


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    
    # Set application icon if available
    try:
        if getattr(sys, 'frozen', False):
            # Running as executable
            icon_path = Path(sys.executable).parent / "icon.ico"
        else:
            icon_path = Path(__file__).parent / "assets" / "icon.ico"
        
        if icon_path.exists():
            root.iconbitmap(str(icon_path))
    except Exception:
        pass  # Icon not critical
    
    app = SpectrumTekConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
