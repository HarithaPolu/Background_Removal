import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk
from rembg import remove
import numpy as np

class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover")
        self.root.geometry("800x600")

        self.original_image = None
        self.processed_image = None

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.transparent_button = tk.Button(root, text="Transparent Background", command=self.remove_background_transparent)
        self.transparent_button.pack(pady=10)

        self.solid_button = tk.Button(root, text="Solid Background", command=self.remove_background_solid)
        self.solid_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Save Image", command=self.save_image)
        self.save_button.pack(pady=10)

        self.color_button = tk.Button(root, text="Choose Solid Color", command=self.choose_color)
        self.color_button.pack(pady=10)

        self.color = (255, 255, 255)  # Default to white

        self.original_label = tk.Label(root)
        self.original_label.pack(side=tk.LEFT, padx=10)

        self.processed_label = tk.Label(root)
        self.processed_label.pack(side=tk.RIGHT, padx=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image, self.original_label)

    def remove_background_transparent(self):
        if self.original_image:
            input_image = np.array(self.original_image)
            output_image = remove(input_image)
            self.processed_image = Image.fromarray(output_image)
            self.display_image(self.processed_image, self.processed_label)
        else:
            messagebox.showerror("Error", "Please upload an image first.")

    def remove_background_solid(self):
        if self.original_image:
            input_image = np.array(self.original_image)
            output_image = remove(input_image)
            output_image = Image.fromarray(output_image)

               # Create a solid background
            solid_background = Image.new("RGBA", output_image.size, self.color)
            solid_background.paste(output_image, (0, 0), output_image)

            self.processed_image = solid_background
            self.display_image(self.processed_image, self.processed_label)
        else:
            messagebox.showerror("Error", "Please upload an image first.")

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose Solid Color")
        if color[1]:  # If a color was chosen
            self.color = tuple(int(c) for c in color[0]) + (255,)  # Add alpha channel

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                          filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if file_path:
                self.processed_image.save(file_path)
        else:
            messagebox.showerror("Error", "No processed image to save.")

    def display_image(self, image, label):
        image.thumbnail((300, 300))  # Resize for display
        img_tk = ImageTk.PhotoImage(image)
        label.config(image=img_tk)
        label.image = img_tk  # Keep a reference to avoid garbage collection

if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()