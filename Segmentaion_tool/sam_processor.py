import sys
import torch
import cv2
import numpy as np

sys.path.append("..")
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator


def load_sam_model(checkpoint_path, model_type="vit_b", device="cpu"):
    # load SAM model
    try:
        print(f"Loading SAM model: {model_type}")
        print(f"Checkpoint: {checkpoint_path}")
        print(f"Device: {device}")
        
        sam = sam_model_registry[model_type](checkpoint=checkpoint_path)
        sam.to(device=device)
        
        mask_generator = SamAutomaticMaskGenerator(sam)
        
        print("SAM model loaded successfully!")
        return mask_generator
        
    except Exception as e:
        print(f"Error loading SAM model: {e}")
        return None


def process_image(image_path, mask_generator):
    # process image with SAM
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image {image_path}")
            return None, None
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        print(f"Processing image: {image_path}")
        print(f"Image shape: {image.shape}")
        
        # generate masks
        masks = mask_generator.generate(image)
        
        print(f"Generated {len(masks)} masks")
        
        return image, masks
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None, None


def get_mask_info(masks):
    # get mask stats
    if not masks:
        return {"count": 0}
    
    info = {
        "count": len(masks),
        "areas": [mask["area"] for mask in masks],
        "avg_area": sum(mask["area"] for mask in masks) / len(masks),
        "total_area": sum(mask["area"] for mask in masks)
    }
    
    return info
