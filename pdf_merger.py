import os
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfMerger
import customtkinter as ctk

class PDFMergerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("PDF Merger")
        self.geometry("600x500")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # File list frame
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Buttons
        self.add_btn = ctk.CTkButton(self.list_frame, text="Add PDFs", command=self.add_files)
        self.add_btn.grid(row=0, column=0, padx=5, pady=5)

        self.remove_btn = ctk.CTkButton(self.list_frame, text="Remove Selected", command=self.remove_file)
        self.remove_btn.grid(row=0, column=1, padx=5, pady=5)

        self.up_btn = ctk.CTkButton(self.list_frame, text="↑", width=30, command=lambda: self.move_file(-1))
        self.up_btn.grid(row=0, column=2, padx=5, pady=5)

        self.down_btn = ctk.CTkButton(self.list_frame, text="↓", width=30, command=lambda: self.move_file(1))
        self.down_btn.grid(row=0, column=3, padx=5, pady=5)

        # File list
        self.file_list = tk.Listbox(self, selectmode=tk.SINGLE, bg="#343638", fg="white", 
                                   selectbackground="#565b5e", font=("Arial", 12))
        self.file_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Merge button
        self.merge_btn = ctk.CTkButton(self, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_btn.grid(row=2, column=0, padx=10, pady=10)

        # Status label
        self.status_label = ctk.CTkLabel(self, text="", anchor="center")
        self.status_label.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF Files", "*.pdf")]
        )
        for file in files:
            if file not in self.file_list.get(0, tk.END):
                self.file_list.insert(tk.END, file)
        self.update_status()

    def remove_file(self):
        selected = self.file_list.curselection()
        if selected:
            self.file_list.delete(selected[0])
        self.update_status()

    def move_file(self, direction):
        selected = self.file_list.curselection()
        if not selected:
            return
        index = selected[0]
        new_index = index + direction
        if 0 <= new_index < self.file_list.size():
            item = self.file_list.get(index)
            self.file_list.delete(index)
            self.file_list.insert(new_index, item)
            self.file_list.select_set(new_index)

    def merge_pdfs(self):
        if self.file_list.size() < 1:
            self.status_label.configure(text="No files selected!", text_color="red")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not output_path:
            return

        merger = PdfMerger()
        try:
            for file in self.file_list.get(0, tk.END):
                merger.append(file)
            merger.write(output_path)
            merger.close()
            self.status_label.configure(text=f"Merged successfully!\nSaved to: {output_path}", text_color="green")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")

    def update_status(self):
        count = self.file_list.size()
        self.status_label.configure(text=f"{count} file(s) selected", text_color="white")

if __name__ == "__main__":
    app = PDFMergerApp()
    app.mainloop()