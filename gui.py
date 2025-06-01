import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from datetime import datetime
from pypdf import PdfReader

class PDFMetadataExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("📄 PDF Metadata Extractor")
        self.root.geometry("380x680")
        self.root.configure(bg="#f5f7fa")
        self.root.resizable(False, False)

        self.selected_file = tk.StringVar()
        self.metadata_text = ""

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="PDF Metadata Extractor", font=("Helvetica", 18, "bold"),
                 fg="#333", bg="#f5f7fa", pady=15).pack()

        file_frame = tk.Frame(self.root, bg="#f5f7fa")
        file_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(file_frame, text="Selected File", font=("Helvetica", 10, "bold"), bg="#f5f7fa").pack(anchor="w")
        self.file_label = tk.Label(file_frame, textvariable=self.selected_file, bg="#ffffff",
                                   relief="groove", anchor="w", height=2, wraplength=330, justify="left")
        self.file_label.pack(fill="x", pady=(5, 10))

        browse_btn = tk.Button(file_frame, text="📁 Browse PDF", command=self.browse_file,
                               bg="#20c997", fg="white", font=("Helvetica", 11, "bold"),
                               relief="flat", padx=10, pady=8)
        browse_btn.pack(fill="x", pady=5)

        extract_btn = tk.Button(file_frame, text="🔍 Extract Metadata", command=self.extract_metadata,
                                bg="#007bff", fg="white", font=("Helvetica", 11, "bold"),
                                relief="flat", padx=10, pady=8)
        extract_btn.pack(fill="x", pady=(10, 0))

        tk.Label(self.root, text="Metadata Results", font=("Helvetica", 12, "bold"),
                 bg="#f5f7fa", fg="#444").pack(anchor="w", padx=20, pady=(20, 5))

        self.results_text = scrolledtext.ScrolledText(self.root, font=("Courier New", 10),
                                                      height=18, wrap="word", bg="#ffffff")
        self.results_text.pack(padx=20, fill="both", expand=True)

        self.status_var = tk.StringVar(value="Ready to extract PDF metadata")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bg="#dee2e6", fg="#333",
                              relief="flat", anchor="w", padx=10)
        status_bar.pack(fill="x", pady=(5, 0))

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select PDF File",
                                               filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.selected_file.set(file_path)
            self.status_var.set("📄 File selected: " + os.path.basename(file_path))
            self.results_text.delete(1.0, tk.END)

    def extract_metadata(self):
        file_path = self.selected_file.get()
        if not file_path:
            messagebox.showwarning("No File", "Please select a PDF file.")
            return

        if not file_path.lower().endswith(".pdf"):
            self.handle_error("The selected file is not a valid PDF file.")
            return

        try:
            reader = PdfReader(file_path)
            if reader.is_encrypted:
                raise Exception("This PDF is encrypted.")

            metadata = reader.metadata or {}
            info = {
                "file_path": file_path,
                "file_size": os.path.getsize(file_path),
                "title": metadata.get("/Title", "Unknown"),
                "author": metadata.get("/Author", "Unknown"),
                "subject": metadata.get("/Subject", "Unknown"),
                "creator": metadata.get("/Creator", "Unknown"),
                "producer": metadata.get("/Producer", "Unknown"),
                "creation_date": metadata.get("/CreationDate", "Unknown"),
                "modification_date": metadata.get("/ModDate", "Unknown"),
                "pages": len(reader.pages),
                "encrypted": reader.is_encrypted
            }

            self.display_metadata(info)
            self.save_report(info)
            self.status_var.set("✅ Metadata extracted successfully!")

        except Exception as e:
            self.handle_error(str(e))

    def display_metadata(self, info):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = f"""
📄 PDF Metadata Report
Generated on: {now}
{'='*40}

📁 File: {os.path.basename(info['file_path'])}
📂 Path: {info['file_path']}
🧮 Size: {info['file_size']/1024:.2f} KB

📑 Title: {info['title']}
✍️ Author: {info['author']}
🗂️ Subject: {info['subject']}
⚙️ Creator: {info['creator']}
🏷️ Producer: {info['producer']}
🕓 Created: {info['creation_date']}
🕘 Modified: {info['modification_date']}
📃 Pages: {info['pages']}
🔒 Encrypted: {"Yes" if info['encrypted'] else "No"}

{'='*40}
"""
        self.metadata_text = text
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, text)

    def save_report(self, info):
        try:
            report_path = os.path.join(os.path.dirname(info['file_path']), "pdf_report.txt")
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(self.metadata_text)
        except Exception as e:
            messagebox.showwarning("Save Error", f"Could not save report: {e}")

    def handle_error(self, msg):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"❌ Error: {msg}\n")
        self.results_text.insert(tk.END, "Please check the PDF file and try again.")
        self.status_var.set("⚠️ Error during extraction")
        messagebox.showerror("Error", msg)

def main():
    root = tk.Tk()
    app = PDFMetadataExtractor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
