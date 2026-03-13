import os
from pathlib import Path

def load_images_from_folder(folder_path):
    # supported formats
    supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    
    image_paths = []
    
    try:
        folder = Path(folder_path)
        
        if not folder.exists():
            print(f"Error: Folder '{folder_path}' does not exist")
            return []
        
        # get all image files
        for file in folder.iterdir():
            if file.is_file() and file.suffix.lower() in supported_formats:
                image_paths.append(str(file))
        
        image_paths.sort()
        
        print(f"Found {len(image_paths)} images in '{folder_path}'")
        return image_paths
        
    except Exception as e:
        print(f"Error loading images: {e}")
        return []


if __name__ == "__main__":
    test_folder = input("Enter folder path: ")
    images = load_images_from_folder(test_folder)
    
    if images:
        print("\nImages found:")
        for img in images:
            print(f"  - {img}")
    else:
        print("No images found!")
