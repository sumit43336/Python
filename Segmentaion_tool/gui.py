import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import sys
from main import SegmentationTool


class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        
    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
        self.text_widget.update_idletasks()
        
    def flush(self):
        pass


class SegmentationGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("SAM Segmentation Tool")
        self.root.geometry("1400x800")
        
        self.tool = SegmentationTool()
        
        self.current_mask_index = 0
        self.photo_image = None
        self.mask_photo = None
        
        self.setup_gui()
        
    def setup_gui(self):
        
        # top control panel
        control_frame = tk.Frame(self.root, bg='#2b2b2b', height=100)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        control_frame.pack_propagate(False)
        
        # model settings
        tk.Label(control_frame, text="SAM Checkpoint:", bg='#2b2b2b', fg='white').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.checkpoint_entry = tk.Entry(control_frame, width=40)
        self.checkpoint_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(control_frame, text="Browse", command=self.browse_checkpoint).grid(row=0, column=2, padx=5, pady=5)
        
        tk.Label(control_frame, text="Model Type:", bg='#2b2b2b', fg='white').grid(row=0, column=3, padx=5, pady=5)
        self.model_type = ttk.Combobox(control_frame, values=["vit_b", "vit_l", "vit_h"], width=10)
        self.model_type.set("vit_b")
        self.model_type.grid(row=0, column=4, padx=5, pady=5)
        
        tk.Button(control_frame, text="Load Model", command=self.load_model, bg='#4CAF50', fg='white', width=12).grid(row=0, column=5, padx=5, pady=5)
        
        # folder settings
        tk.Label(control_frame, text="Input Folder:", bg='#2b2b2b', fg='white').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.input_entry = tk.Entry(control_frame, width=40)
        self.input_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(control_frame, text="Browse", command=self.browse_input).grid(row=1, column=2, padx=5, pady=5)
        
        tk.Label(control_frame, text="Output Folder:", bg='#2b2b2b', fg='white').grid(row=1, column=3, padx=5, pady=5)
        self.output_entry = tk.Entry(control_frame, width=20)
        self.output_entry.grid(row=1, column=4, padx=5, pady=5)
        tk.Button(control_frame, text="Browse", command=self.browse_output).grid(row=1, column=5, padx=5, pady=5)
        
        # main content (3 panels)
        content_frame = tk.Frame(self.root)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # left - original image
        left_frame = tk.LabelFrame(content_frame, text="Original Image", font=('Arial', 12, 'bold'))
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.image_canvas = tk.Canvas(left_frame, bg='black')
        self.image_canvas.pack(fill=tk.BOTH, expand=True)
        
        # middle - controls
        middle_frame = tk.LabelFrame(content_frame, text="Controls", font=('Arial', 12, 'bold'), width=250)
        middle_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        middle_frame.pack_propagate(False)
        
        tk.Button(middle_frame, text="Process Image", command=self.process_image, bg='#2196F3', fg='white', height=2).pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(middle_frame, text="Mask Navigation:", font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        
        mask_nav_frame = tk.Frame(middle_frame)
        mask_nav_frame.pack(pady=5)
        tk.Button(mask_nav_frame, text="◀ Prev", command=self.prev_mask, width=8).pack(side=tk.LEFT, padx=5)
        tk.Button(mask_nav_frame, text="Next ▶", command=self.next_mask, width=8).pack(side=tk.LEFT, padx=5)
        
        self.mask_label = tk.Label(middle_frame, text="Mask: 0/0", font=('Arial', 10))
        self.mask_label.pack(pady=5)
        
        tk.Button(middle_frame, text="✓ Accept Mask", command=self.accept_current_mask, bg='#4CAF50', fg='white', height=2).pack(fill=tk.X, padx=10, pady=5)
        tk.Button(middle_frame, text="✗ Remove Mask", command=self.remove_current_mask, bg='#f44336', fg='white', height=2).pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(middle_frame, text="Accepted Masks:", font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        self.accepted_listbox = tk.Listbox(middle_frame, height=8)
        self.accepted_listbox.pack(fill=tk.BOTH, padx=10, pady=5)
        
        tk.Button(middle_frame, text="💾 Save Accepted Masks", command=self.save_masks, bg='#FF9800', fg='white', height=2).pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(middle_frame, text="View Options:", font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        tk.Button(middle_frame, text="Show All Masks", command=self.show_all_masks, width=20).pack(pady=2)
        tk.Button(middle_frame, text="Show Grid View", command=self.show_grid, width=20).pack(pady=2)
        
        # right - mask preview
        right_frame = tk.LabelFrame(content_frame, text="Mask Preview", font=('Arial', 12, 'bold'))
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.mask_canvas = tk.Canvas(right_frame, bg='black')
        self.mask_canvas.pack(fill=tk.BOTH, expand=True)
        
        # console output
        log_frame = tk.LabelFrame(self.root, text="Console Output", font=('Arial', 10, 'bold'))
        log_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        log_scroll = tk.Scrollbar(log_frame)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.console_text = tk.Text(log_frame, height=6, bg='#1e1e1e', fg='#00ff00', 
                                    font=('Consolas', 9), yscrollcommand=log_scroll.set)
        self.console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.config(command=self.console_text.yview)
        
        sys.stdout = ConsoleRedirector(self.console_text)
        
        # bottom navigation
        nav_frame = tk.Frame(self.root, bg='#2b2b2b', height=60)
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        nav_frame.pack_propagate(False)
        
        tk.Button(nav_frame, text="◀◀ Previous Image", command=self.prev_image, width=20, height=2).pack(side=tk.LEFT, padx=20, pady=10)
        
        self.progress_label = tk.Label(nav_frame, text="No images loaded", font=('Arial', 12, 'bold'), bg='#2b2b2b', fg='white')
        self.progress_label.pack(side=tk.LEFT, expand=True)
        
        tk.Button(nav_frame, text="Next Image ▶▶", command=self.next_image, width=20, height=2).pack(side=tk.RIGHT, padx=20, pady=10)
        
    def browse_checkpoint(self):
        filename = filedialog.askopenfilename(title="Select SAM Checkpoint", filetypes=[("PyTorch Model", "*.pth")])
        if filename:
            self.checkpoint_entry.delete(0, tk.END)
            self.checkpoint_entry.insert(0, filename)
    
    def browse_input(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, folder)
            if self.tool.load_images(folder):
                self.update_progress()
                self.load_and_display_current_image()
                messagebox.showinfo("Success", f"Loaded {len(self.tool.image_paths)} images")
    
    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)
            self.tool.set_output_folder(folder)
    
    def load_model(self):
        checkpoint = self.checkpoint_entry.get()
        model_type = self.model_type.get()
        
        if not checkpoint:
            messagebox.showerror("Error", "Please select a checkpoint file")
            return
        
        if self.tool.load_model(checkpoint, model_type, "cpu"):
            messagebox.showinfo("Success", "Model loaded successfully!")
        else:
            messagebox.showerror("Error", "Failed to load model")
    
    def process_image(self):
        if self.tool.process_current_image():
            self.current_mask_index = 0
            self.update_displays()
            self.update_mask_label()
            messagebox.showinfo("Success", f"Generated {len(self.tool.current_masks)} masks")
        else:
            messagebox.showerror("Error", "Failed to process image")
    
    def next_image(self):
        if self.tool.next_image():
            self.current_mask_index = 0
            self.load_and_display_current_image()
            self.update_progress()
            self.update_mask_label()
            self.accepted_listbox.delete(0, tk.END)
    
    def prev_image(self):
        if self.tool.prev_image():
            self.current_mask_index = 0
            self.load_and_display_current_image()
            self.update_progress()
            self.update_mask_label()
            self.accepted_listbox.delete(0, tk.END)
    
    def load_and_display_current_image(self):
        # load and show current image without processing
        if self.tool.image_paths:
            import cv2
            current_path = self.tool.image_paths[self.tool.current_index]
            img = cv2.imread(current_path)
            if img is not None:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                pil_img = Image.fromarray(img)
                pil_img.thumbnail((600, 600))
                self.photo_image = ImageTk.PhotoImage(pil_img)
                
                self.image_canvas.delete("all")
                self.image_canvas.create_image(300, 300, image=self.photo_image)
                
                if not self.tool.current_masks:
                    self.mask_canvas.delete("all")
    
    def next_mask(self):
        if self.current_mask_index < len(self.tool.current_masks) - 1:
            self.current_mask_index += 1
            self.update_mask_preview()
            self.update_mask_label()
    
    def prev_mask(self):
        if self.current_mask_index > 0:
            self.current_mask_index -= 1
            self.update_mask_preview()
            self.update_mask_label()
    
    def accept_current_mask(self):
        if self.tool.accept_mask(self.current_mask_index):
            self.accepted_listbox.insert(tk.END, f"Mask {self.current_mask_index}")
    
    def remove_current_mask(self):
        if self.tool.remove_accepted_mask(self.current_mask_index):
            for i in range(self.accepted_listbox.size()):
                if self.accepted_listbox.get(i) == f"Mask {self.current_mask_index}":
                    self.accepted_listbox.delete(i)
                    break
    
    def save_masks(self):
        if self.tool.save_accepted_masks():
            messagebox.showinfo("Success", "Masks saved successfully!")
        else:
            messagebox.showwarning("Warning", "No masks to save or save failed")
    
    def show_all_masks(self):
        self.tool.preview_all_masks()
    
    def show_grid(self):
        # scrollable grid view
        if not self.tool.current_masks:
            messagebox.showwarning("Warning", "No masks to display")
            return
        
        grid_window = tk.Toplevel(self.root)
        grid_window.title("Grid View - All Masks")
        grid_window.geometry("1200x800")
        
        canvas = tk.Canvas(grid_window, bg='white')
        scrollbar = tk.Scrollbar(grid_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # 3 columns
        cols = 3
        sorted_masks = sorted(self.tool.current_masks, key=lambda x: x['area'], reverse=True)
        
        for idx, mask_data in enumerate(sorted_masks):
            row = idx // cols
            col = idx % cols
            
            mask_frame = tk.Frame(scrollable_frame, relief=tk.RAISED, borderwidth=2, bg='white')
            mask_frame.grid(row=row, column=col, padx=10, pady=10)
            
            mask = mask_data['segmentation']
            overlay = self.tool.current_image.copy()
            overlay[mask] = [255, 0, 0]  # red
            
            img = Image.fromarray(overlay)
            img.thumbnail((350, 350))
            photo = ImageTk.PhotoImage(img)
            
            img_label = tk.Label(mask_frame, image=photo, bg='white')
            img_label.image = photo
            img_label.pack()
            
            info_text = f"Mask {idx}\nArea: {mask_data['area']} px"
            info_label = tk.Label(mask_frame, text=info_text, font=('Arial', 10), bg='white')
            info_label.pack()
            
            accept_btn = tk.Button(
                mask_frame, 
                text="✓ Accept", 
                bg='#4CAF50', 
                fg='white',
                command=lambda i=idx: self.accept_mask_from_grid(i, grid_window)
            )
            accept_btn.pack(pady=5)
        
        # mousewheel scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def accept_mask_from_grid(self, mask_index, window):
        if self.tool.accept_mask(mask_index):
            self.accepted_listbox.insert(tk.END, f"Mask {mask_index}")
            messagebox.showinfo("Success", f"Accepted Mask {mask_index}", parent=window)
    
    def update_displays(self):
        self.update_image_display()
        self.update_mask_preview()
    
    def update_image_display(self):
        if self.tool.current_image is not None:
            img = Image.fromarray(self.tool.current_image)
            img.thumbnail((600, 600))
            self.photo_image = ImageTk.PhotoImage(img)
            
            self.image_canvas.delete("all")
            self.image_canvas.create_image(300, 300, image=self.photo_image)
    
    def update_mask_preview(self):
        if self.tool.current_image is not None and self.tool.current_masks:
            mask_data = self.tool.current_masks[self.current_mask_index]
            mask = mask_data['segmentation']
            
            overlay = self.tool.current_image.copy()
            overlay[mask] = [255, 0, 0]  # red
            
            img = Image.fromarray(overlay)
            img.thumbnail((600, 600))
            self.mask_photo = ImageTk.PhotoImage(img)
            
            self.mask_canvas.delete("all")
            self.mask_canvas.create_image(300, 300, image=self.mask_photo)
    
    def update_progress(self):
        current, total = self.tool.get_progress()
        image_name = self.tool.get_current_image_name()
        self.progress_label.config(text=f"Image {current}/{total}: {image_name}")
    
    def update_mask_label(self):
        if self.tool.current_masks:
            self.mask_label.config(text=f"Mask: {self.current_mask_index + 1}/{len(self.tool.current_masks)}")
        else:
            self.mask_label.config(text="Mask: 0/0")


def main():
    root = tk.Tk()
    app = SegmentationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
