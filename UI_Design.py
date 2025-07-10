import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import count_elements
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
import subprocess

def generate_pdf(counts, url, save_path):
    def start_page(c):
        c.setFont("Helvetica", 10)
        return letter[1] - 60  # top margin

    c = pdf_canvas.Canvas(save_path, pagesize=letter)
    width, height = letter
    y = start_page(c)

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "Element Counts Report")
    y -= 30

    # URL
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"URL: {url}")
    y -= 20

    bullet = "\u2022"
    line_height = 16
    indent = 20

    for element, val in counts.items():
        key_title = element.replace('_', ' ').title()

        # Page-break check before each section
        if y < 100:
            c.showPage()
            y = start_page(c)

        # --- Special handling for full tables ---
        if element == "tables_data":
            for tbl_idx, table in enumerate(val, start=1):
                # Page-break if needed
                if y < 100:
                    c.showPage()
                    y = start_page(c)

                # Table header with dimensions
                num_rows = len(table)
                num_cols = max((len(r) for r in table), default=0)
                header_text = f"{bullet} Table {tbl_idx} ({num_rows}×{num_cols}):"
                c.drawString(40, y, header_text)
                y -= line_height

                # Print each row wirth " | "
                c.setFont("Helvetica-Oblique", 9)
                for row in table:
                    row_text = " | ".join(row)
                    # Wrap long rows (~180 chars)
                    chunks = [row_text[i:i+180] for i in range(0, len(row_text), 80)]
                    for chunk in chunks:
                        if y < 50:
                            c.showPage()
                            y = start_page(c)
                        c.drawString(40 + indent, y, chunk)
                        y -= line_height
                c.setFont("Helvetica", 10)

        #  Lists links, buttons, onclicks etc
        elif isinstance(val, list):
            header_text = f"{bullet} {key_title} ({len(val)} items):"
            c.drawString(40, y, header_text)
            y -= line_height

            c.setFont("Helvetica-Oblique", 9)
            for item in val:
                # wrap long items
                text = f"- {item}"
                chunks = [text[i:i+80] for i in range(0, len(text), 80)]
                for chunk in chunks:
                    if y < 50:
                        c.showPage()
                        y = start_page(c)
                    c.drawString(40 + indent, y, chunk)
                    y -= line_height
            c.setFont("Helvetica", 10)

        # --- Scalar counts ---
        else:
            text = f"{bullet} {key_title}: {val}"
            c.drawString(40, y, text)
            y -= line_height

    c.save()
    messagebox.showinfo("Success", f"PDF saved to: {save_path}")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Web Element Analyzer")
        self.geometry("720x480")
        self.configure(bg="#1e1e2e")

        # Styles
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Futuristic.TFrame', background='#1e1e2e')
        style.configure('Header.TLabel', background='#1e1e2e', foreground='#00ffea', font=('Segoe UI', 20, 'bold'))
        style.configure('Futuristic.TLabel', background='#1e1e2e', foreground='#00ffea', font=('Segoe UI', 12))
        style.configure('Futuristic.TEntry', fieldbackground='#2e2e3e', background='#2e2e3e', foreground='#ffffff', font=('Segoe UI', 11), relief='raised', padding=8)
        style.configure('Futuristic.TButton', font=('Segoe UI', 12, 'bold'), background='#00aaff', foreground='#1e1e2e', borderwidth=3, relief='raised', padding=8)
        style.map('Futuristic.TButton', background=[('active', '#00ddff')])
        style.configure('Status.TLabel', background='#1e1e2e', foreground='#00ffea', font=('Segoe UI', 10))

        # Header
        header = ttk.Frame(self, style='Futuristic.TFrame')
        header.pack(fill='x', padx=20, pady=(20, 10))
        ttk.Label(header, text="Web Element Analyzer", style='Header.TLabel').pack()

        # URL Input
        input_frame = ttk.Frame(self, style='Futuristic.TFrame')
        input_frame.pack(fill='x', padx=20, pady=(0, 10))
        ttk.Label(input_frame, text="URL:", style='Futuristic.TLabel')\
            .grid(row=0, column=0, sticky='w')
        self.url_entry = ttk.Entry(input_frame, width=50, style='Futuristic.TEntry')
        self.url_entry.grid(row=0, column=1, padx=10)

        # Buttons
        btn_frame = ttk.Frame(self, style='Futuristic.TFrame')
        btn_frame.pack(pady=(10, 20))
        self.check_btn = ttk.Button(btn_frame, text="Check Elements", style='Futuristic.TButton', command=self.on_check)
        self.check_btn.grid(row=0, column=0, padx=10)
        self.test_btn = ttk.Button(btn_frame, text="Test Web Application", style='Futuristic.TButton', command=self.on_test)
        self.test_btn.grid(row=0, column=1, padx=10)
        self.custom_btn = ttk.Button(btn_frame, text="Custom Button", style='Futuristic.TButton', command=self.on_custom)
        self.custom_btn.grid(row=0, column=2, padx=10)

        # Status Bar
        self.status = ttk.Label(self, text="Ready", style='Status.TLabel', anchor='w', relief='sunken')
        self.status.pack(fill='x', side='bottom')

    def on_check(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Input Required", "Please enter a URL.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Save PDF Report")
        if not save_path:
            return
        self.status.config(text="Analyzing...", foreground='#00ffea')
        threading.Thread(target=self.run_check, args=(url, save_path), daemon=True).start()

    def run_check(self, url, save_path):
        try:
            counts = count_elements.count_media_elements(url)
            generate_pdf(counts, url, save_path)
            self.status.config(text="Report generated successfully!", foreground='#00ffea')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze URL:\n{e}")
            self.status.config(text="Error occurred.", foreground='#ff4466')

    def on_test(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Input Required", "Please enter a URL before testing.")
            return

        # Run Robot Framework suite, passing TEST_URL variable
        try:
            self.status.config(text="Running tests...", foreground='#00ffea')
            result = subprocess.run(
                ['robot', '--variable', f"TEST_URL:{url}", 'count_elements_tests.robot'],
                capture_output=True, text=True
            )

            if result.returncode == 0:
                messagebox.showinfo("Tests Passed", result.stdout)
                self.status.config(text="All tests passed!", foreground='#00ffea')
            else:
                messagebox.showerror("Tests Failed",
                                     f"Exit code: {result.returncode}\n\n"
                                     f"{result.stdout}\n{result.stderr}")
                self.status.config(text="Tests failed.", foreground='#ff4466')

        except FileNotFoundError:
            messagebox.showerror("Robot Not Found",
                                 "Cannot find the 'robot' command. Make sure Robot Framework is installed and on your PATH.")
            self.status.config(text="Error: robot not found.", foreground='#ff4466')

    def on_custom(self):
        messagebox.showinfo("Custom", "Custom Button clicked.")

if __name__ == "__main__":
    app = App()
    app.mainloop()