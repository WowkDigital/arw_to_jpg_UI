import os
import sys
import rawpy
import io
import re
from PIL import Image, ExifTags, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def rotate_image_based_on_exif(image):
    """Obraca obraz na podstawie danych EXIF."""
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
        # Błąd EXIF nie jest krytyczny, można go zignorować w konsoli
        # print(f"Błąd przetwarzania danych EXIF: {e}")
        pass
    return image

def process_image(raw_file_path, output_file, filename, add_watermark):
    """Przetwarza pojedynczy plik RAW, wyciąga podgląd i opcjonalnie dodaje znak wodny."""
    with rawpy.imread(raw_file_path) as raw:
        try:
            embedded_image = raw.extract_thumb()
            if embedded_image.format == rawpy.ThumbFormat.JPEG:
                img = Image.open(io.BytesIO(embedded_image.data))
                img = rotate_image_based_on_exif(img)

                if add_watermark:
                    draw = ImageDraw.Draw(img)
                    text = os.path.splitext(filename)[0]
                    
                    font_size = int(img.width / 40)
                    
                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except IOError:
                        font = ImageFont.load_default()

                    margin = 15
                    text_bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    
                    position_x = img.width - text_width - margin
                    position_y = img.height - text_height - margin

                    shadow_color = "black"
                    main_color = "white"
                    draw.text((position_x - 1, position_y - 1), text, font=font, fill=shadow_color)
                    draw.text((position_x + 1, position_y - 1), text, font=font, fill=shadow_color)
                    draw.text((position_x - 1, position_y + 1), text, font=font, fill=shadow_color)
                    draw.text((position_x + 1, position_y + 1), text, font=font, fill=shadow_color)
                    draw.text((position_x, position_y), text, font=font, fill=main_color)
                
                img.save(output_file, quality=95, subsampling=0)
            # Komunikaty o błędach wciąż mogą być przydatne w konsoli
            else:
                print(f"Brak podglądu JPG w pliku RAW: {os.path.basename(raw_file_path)}")
        except rawpy.LibRawNoThumbnailError:
            print(f"Brak miniatury w pliku: {os.path.basename(raw_file_path)}")
        except Exception as e:
            print(f"Wystąpił błąd podczas przetwarzania {os.path.basename(raw_file_path)}: {e}")

def process_raw_folder(raws_dir, add_watermark, progress_bar, progress_label, root):
    """Przetwarza cały folder plików RAW, aktualizując pasek postępu w GUI."""
    jpg_folder_path = os.path.join(raws_dir, 'exported_jpg')
    
    if not os.path.exists(jpg_folder_path):
        os.makedirs(jpg_folder_path)

    def extract_number(filename):
        match = re.search(r'\((\d+)\)', filename)
        if match:
            return int(match.group(1))
        return 0

    try:
        raw_files = [f for f in os.listdir(raws_dir) if f.lower().endswith(('.arw', '.cr2'))]
    except FileNotFoundError:
        messagebox.showerror("Błąd", f"Nie znaleziono folderu: {raws_dir}")
        return
        
    raw_files.sort(key=extract_number)
    
    #progress bar
    total_files = len(raw_files)
    progress_bar['maximum'] = total_files
    progress_bar['value'] = 0
    
    for i, filename in enumerate(raw_files):
        progress_label.config(text=f"Przetwarzanie {i + 1} / {total_files}: {filename}")
        progress_bar['value'] = i + 1
        root.update_idletasks() 

        output_file = os.path.join(jpg_folder_path, os.path.splitext(os.path.basename(filename))[0] + '.jpg')
        if os.path.exists(output_file):
            continue
        else:
            process_image(os.path.join(raws_dir, filename), output_file, filename, add_watermark)
    
    progress_label.config(text="Przetwarzanie zakończone!")
    messagebox.showinfo("Ukończono", "Wszystkie obrazy zostały przetworzone i zapisane w folderze 'exported_jpg'.")
    progress_bar['value'] = 0
    progress_label.config(text="")


def select_folder(add_watermark_var, progress_bar, progress_label, root):
    """Otwiera dialog wyboru folderu i uruchamia przetwarzanie."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        if os.path.isdir(folder_selected):
            process_raw_folder(folder_selected, add_watermark_var.get(), progress_bar, progress_label, root)
        else:
            messagebox.showerror("Błąd", "Wybrana ścieżka nie jest folderem.")


def create_gui():
    """Tworzy główny interfejs graficzny aplikacji."""
    root = tk.Tk()
    root.title("RAW to JPG Processor")
    root.geometry("600x520")
    root.configure(bg="#f0f0f0")

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=10)
    style.configure("TLabel", font=("Arial", 10), background="#f0f0f0")
    style.configure("TCheckbutton", background="#f0f0f0", font=("Arial", 10))

    header_frame = ttk.Frame(root)
    header_frame.pack(pady=10)

    header_label = ttk.Label(header_frame, text="RAW to JPG Processor", font=("Arial", 16, "bold"))
    header_label.pack()

    info_frame = ttk.Frame(root, padding=10)
    info_frame.pack(pady=10)

    info_label = ttk.Label(info_frame, text=(
        "Ta aplikacja przetwarza pliki RAW (.arw, .cr2) i eksportuje z nich podglądy JPG. "
        "Podglądy są automatycznie obracane na podstawie danych EXIF i zapisywane w folderze 'exported_jpg'."
    ), wraplength=550, justify="center")
    info_label.pack()

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=20)

    watermark_var = tk.BooleanVar(value=True)
    
    watermark_check = ttk.Checkbutton(
        button_frame, 
        text="Dodaj nazwę pliku jako znak wodny",
        variable=watermark_var,
        style="TCheckbutton"
    )
    watermark_check.grid(row=0, column=0, columnspan=2, padx=20, pady=(0, 15), sticky='w')

    # --- POCZĄTEK ZMIAN: Widżety postępu ---
    progress_frame = ttk.Frame(root, padding=10)
    progress_frame.pack(fill='x', padx=20)

    progress_label = ttk.Label(progress_frame, text="", font=("Arial", 9))
    progress_label.pack(fill='x')
    
    progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', mode='determinate')
    progress_bar.pack(fill='x', pady=5)
    # --- KONIEC ZMIAN ---
    
    # Przekazujemy widżety postępu i okno `root` do funkcji `select_folder`
    select_button = ttk.Button(
        button_frame, 
        text="Wybierz Folder", 
        command=lambda: select_folder(watermark_var, progress_bar, progress_label, root)
    )
    select_button.grid(row=1, column=0, padx=20)

    quit_button = ttk.Button(button_frame, text="Zakończ", command=root.quit)
    quit_button.grid(row=1, column=1, padx=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()