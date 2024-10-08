import os
import sys
import rawpy
import io
from PIL import Image, ExifTags
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # For modern widgets

def rotate_image_based_on_exif(image):
    try:
        exif = image.getexif()
        exif = {
            ExifTags.TAGS.get(k, k): v
            for k, v in exif.items()
        }

        orientation = exif.get('Orientation')
        if orientation == 3:
            image = image.rotate(180, expand=True)
        elif orientation == 6:
            image = image.rotate(270, expand=True)
        elif orientation == 8:
            image = image.rotate(90, expand=True)
    except Exception as e:
        print(f"Error processing EXIF data: {e}")
    return image

def process_image(raw_file_path, output_file):
    with rawpy.imread(raw_file_path) as raw:
        embedded_image = raw.extract_thumb()
        if embedded_image.format == rawpy.ThumbFormat.JPEG:
            img = Image.open(io.BytesIO(embedded_image.data))
            img = rotate_image_based_on_exif(img)
            img.save(output_file)
            print(f"Saved and rotated JPG preview at: {output_file}")
        else:
            print("Embedded JPG image not found in RAW file.")

def process_raw_folder(raws_dir):
    jpg_folder_path = os.path.join(raws_dir, 'exported_jpg')
    
    if not os.path.exists(jpg_folder_path):
        os.makedirs(jpg_folder_path)
    
    for filename in os.listdir(raws_dir):
        if filename.lower().endswith(('.arw', '.cr2')):
            output_file = os.path.join(jpg_folder_path, os.path.splitext(os.path.basename(filename))[0] + '.jpg')
            if os.path.exists(output_file):
                print(f"Skipping {output_file} (it already exists)")
            else:
                process_image(os.path.join(raws_dir, filename), output_file)
    messagebox.showinfo("Completed", "All images have been processed and saved in 'exported_jpg' folder.")

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        if os.path.isdir(folder_selected):
            process_raw_folder(folder_selected)
        else:
            messagebox.showerror("Error", "Selected path is not a directory.")

def create_gui():
    root = tk.Tk()
    root.title("RAW to JPG Processor")
    root.geometry("600x400")
    root.configure(bg="#f0f0f0")  # Set background color

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=10)
    style.configure("TLabel", font=("Arial", 10), background="#f0f0f0")

    # Header
    header_frame = ttk.Frame(root)
    header_frame.pack(pady=10)

    header_label = ttk.Label(header_frame, text="RAW to JPG Processor", font=("Arial", 16, "bold"))
    header_label.pack()

    # Info section
    info_frame = ttk.Frame(root)
    info_frame.pack(pady=20)

    info_label = ttk.Label(info_frame, text=(
        "This application processes RAW files (.arw, .cr2) and extracts JPG previews.\n"
        "The JPG previews are rotated based on EXIF data (if available) and saved in\n"
        "a folder named 'exported_jpg' inside the selected folder.\n"
        "\n"
        "Steps:\n"
        "1. Select a folder with RAW files.\n"
        "2. The app will process each RAW file and save the JPGs in 'exported_jpg'.\n"
        "3. If the JPG already exists, the file will be skipped."
    ), wraplength=550, justify="left")
    info_label.pack()

    # Button section
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=20)

    select_button = ttk.Button(button_frame, text="Select Folder", command=select_folder)
    select_button.grid(row=0, column=0, padx=20)

    quit_button = ttk.Button(button_frame, text="Quit", command=root.quit)
    quit_button.grid(row=0, column=1, padx=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
