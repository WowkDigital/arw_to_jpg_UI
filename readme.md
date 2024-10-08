# RAW to JPG Processor

[code](https://github.com/WowkDigital/arw_to_jpg_UI/commit/25ce7fec9288a11a0ed0ba6e99df7d13e105e694)

A simple and modern tool for extracting JPG previews from RAW files (e.g., `.arw`, `.cr2`) and automatically rotating them based on EXIF data. The processed JPG images are saved in a separate folder inside the selected directory.

## Features

- **Extract JPG Previews**: Extracts embedded JPG previews from RAW files like `.arw` (Sony) and `.cr2` (Canon).
- **Automatic Rotation**: JPG previews are rotated according to the EXIF orientation tag.
- **Batch Processing**: Process all RAW files in a folder and save the JPGs in a subfolder called `exported_jpg`.
- **File Skipping**: If a JPG already exists in the export folder, it will be skipped to prevent overwriting.
- **View Exported Photos**: After processing, open the folder with the exported JPG files directly from the application.

## Requirements

- Python 3.x
- Required packages:
  - `rawpy`
  - `Pillow`
  - `tkinter` (standard in most Python installations)
  
You can install the required packages by running:

```bash
pip install rawpy Pillow
```

## Usage

1. Clone or download this repository.
2. Install the required dependencies (`rawpy`, `Pillow`).
3. Run the application:

```bash
python main.py
```

4. In the GUI, select a folder containing RAW files (.arw, .cr2).
5. The application will process each RAW file and save the JPG previews in the `exported_jpg` folder within the selected directory.
6. After processing, you can view the exported JPG files by clicking the **View Exported Photos** button.

## How It Works

1. **Select Folder**: The user selects a folder containing RAW files.
2. **Processing**: The application processes each RAW file, extracting the embedded JPG preview (if available), rotating it based on EXIF data, and saving it to a subfolder.
3. **Skip Existing Files**: If a JPG file with the same name already exists in the `exported_jpg` folder, it will not be overwritten.
4. **View Exported Photos**: After the process is complete, the user can open the folder with the exported images by clicking the **View Exported Photos** button.

## GUI Overview

* **Select Folder**: Opens a dialog to select the folder containing RAW files.
* **View Exported Photos**: After processing, opens the folder containing the exported JPG files.
* **Quit**: Exits the application.

## Example Screenshot

[Insert screenshot here]

## Supported RAW Formats

* Sony `.arw`
* Canon `.cr2`

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
