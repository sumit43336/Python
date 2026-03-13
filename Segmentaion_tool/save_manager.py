# Save and export functionality
import cv2
import numpy as np
import json
from pathlib import Path
from datetime import datetime


def save_mask_binary(mask_data, output_path):
    """
    Save mask as binary image (white mask on black background)
    
    Args:
        mask_data (dict): Mask dictionary from SAM
        output_path (str): Path to save the mask
        
    Returns:
        bool: Success status
    """
    try:
        mask = mask_data['segmentation']
        # Convert boolean mask to 0-255 image
        mask_img = (mask * 255).astype(np.uint8)
        
        cv2.imwrite(output_path, mask_img)
        print(f"Saved binary mask to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error saving binary mask: {e}")
        return False


def save_mask_overlay(image, mask_data, output_path, color=(0, 255, 0), alpha=0.5):
    """
    Save mask overlaid on original image
    
    Args:
        image (np.ndarray): Original image (RGB)
        mask_data (dict): Mask dictionary from SAM
        output_path (str): Path to save the overlay
        color (tuple): RGB color for mask overlay
        alpha (float): Transparency (0-1)
        
    Returns:
        bool: Success status
    """
    try:
        mask = mask_data['segmentation']
        
        # Create overlay
        overlay = image.copy()
        overlay[mask] = overlay[mask] * (1 - alpha) + np.array(color) * alpha
        overlay = overlay.astype(np.uint8)
        
        # Convert RGB to BGR for cv2
        overlay_bgr = cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR)
        
        cv2.imwrite(output_path, overlay_bgr)
        print(f"Saved overlay to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error saving overlay: {e}")
        return False


def save_mask_metadata(mask_data, output_path):
    """
    Save mask metadata as JSON
    
    Args:
        mask_data (dict): Mask dictionary from SAM
        output_path (str): Path to save metadata JSON
        
    Returns:
        bool: Success status
    """
    try:
        # Extract relevant metadata (exclude the large segmentation array)
        metadata = {
            'area': int(mask_data['area']),
            'bbox': [int(x) for x in mask_data['bbox']],  # [x, y, w, h]
            'predicted_iou': float(mask_data['predicted_iou']),
            'stability_score': float(mask_data['stability_score']),
            'crop_box': [int(x) for x in mask_data['crop_box']],
            'timestamp': datetime.now().isoformat()
        }
        
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Saved metadata to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error saving metadata: {e}")
        return False


def save_accepted_mask(image, mask_data, image_name, output_folder, mask_index):
    """
    Save an accepted mask with all formats (binary, overlay, metadata)
    
    Args:
        image (np.ndarray): Original image (RGB)
        mask_data (dict): Mask dictionary from SAM
        image_name (str): Original image filename
        output_folder (str): Base output folder
        mask_index (int): Index of this mask
        
    Returns:
        dict: Paths to saved files
    """
    try:
        # Create output folder structure
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create subfolder for this image
        image_base = Path(image_name).stem
        image_folder = output_path / image_base
        image_folder.mkdir(exist_ok=True)
        
        # Generate filenames
        base_name = f"{image_base}_mask_{mask_index:03d}"
        
        binary_path = image_folder / f"{base_name}_binary.png"
        overlay_path = image_folder / f"{base_name}_overlay.png"
        metadata_path = image_folder / f"{base_name}_metadata.json"
        
        # Save all formats
        results = {
            'binary': save_mask_binary(mask_data, str(binary_path)),
            'overlay': save_mask_overlay(image, mask_data, str(overlay_path)),
            'metadata': save_mask_metadata(mask_data, str(metadata_path))
        }
        
        if all(results.values()):
            print(f"✓ Successfully saved mask {mask_index} for {image_name}")
            return {
                'binary': str(binary_path),
                'overlay': str(overlay_path),
                'metadata': str(metadata_path)
            }
        else:
            print(f"✗ Some files failed to save for mask {mask_index}")
            return None
            
    except Exception as e:
        print(f"Error saving accepted mask: {e}")
        return None


# Test the module
if __name__ == "__main__":
    print("save_manager.py - Mask saving functions")
    print("Import this module to use the save functions")
