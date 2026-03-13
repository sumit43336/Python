import sys
from pathlib import Path

from load_images import load_images_from_folder
from sam_processor import load_sam_model, process_image, get_mask_info
from mask_preview import show_masks_on_image, show_single_mask, create_mask_grid
from save_manager import save_accepted_mask


class SegmentationTool:
    
    def __init__(self):
        self.image_paths = []
        self.current_index = 0
        self.current_image = None
        self.current_masks = []
        self.mask_generator = None
        self.output_folder = None
        self.accepted_masks = []
        
    def load_model(self, checkpoint_path, model_type="vit_b", device="cpu"):
        print(f"\n=== Loading SAM Model ===")
        self.mask_generator = load_sam_model(checkpoint_path, model_type, device)
        return self.mask_generator is not None
    
    def load_images(self, folder_path):
        print(f"\n=== Loading Images ===")
        self.image_paths = load_images_from_folder(folder_path)
        if self.image_paths:
            self.current_index = 0
            return True
        return False
    
    def set_output_folder(self, output_path):
        self.output_folder = output_path
        Path(output_path).mkdir(parents=True, exist_ok=True)
        print(f"Output folder set to: {output_path}")
    
    def process_current_image(self):
        if not self.image_paths or not self.mask_generator:
            print("Error: Load images and model first!")
            return False
        
        print(f"\n=== Processing Image {self.current_index + 1}/{len(self.image_paths)} ===")
        current_path = self.image_paths[self.current_index]
        
        self.current_image, self.current_masks = process_image(current_path, self.mask_generator)
        self.accepted_masks = []
        
        if self.current_image is not None:
            info = get_mask_info(self.current_masks)
            print(f"✓ Generated {info['count']} masks")
            return True
        return False
    
    def next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.current_image = None
            self.current_masks = []
            self.accepted_masks = []
            return True
        else:
            print("Already at last image")
            return False
    
    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.current_image = None
            self.current_masks = []
            self.accepted_masks = []
            return True
        else:
            print("Already at first image")
            return False
    
    def get_current_image_name(self):
        if self.image_paths:
            return Path(self.image_paths[self.current_index]).name
        return None
    
    def get_progress(self):
        return self.current_index + 1, len(self.image_paths)
    
    def accept_mask(self, mask_index):
        if 0 <= mask_index < len(self.current_masks):
            if mask_index not in self.accepted_masks:
                self.accepted_masks.append(mask_index)
                print(f"✓ Accepted mask {mask_index}")
                return True
        return False
    
    def remove_accepted_mask(self, mask_index):
        if mask_index in self.accepted_masks:
            self.accepted_masks.remove(mask_index)
            print(f"✗ Removed mask {mask_index} from accepted")
            return True
        return False
    
    def save_accepted_masks(self):
        if not self.output_folder:
            print("Error: Set output folder first!")
            return False
        
        if not self.accepted_masks:
            print("No masks accepted for this image")
            return False
        
        print(f"\n=== Saving {len(self.accepted_masks)} Accepted Masks ===")
        image_name = self.get_current_image_name()
        
        saved_count = 0
        for mask_idx in self.accepted_masks:
            mask_data = self.current_masks[mask_idx]
            result = save_accepted_mask(
                self.current_image, 
                mask_data, 
                image_name, 
                self.output_folder, 
                mask_idx
            )
            if result:
                saved_count += 1
        
        print(f"✓ Saved {saved_count}/{len(self.accepted_masks)} masks")
        return saved_count > 0
    
    def preview_all_masks(self):
        if self.current_image is not None and self.current_masks:
            show_masks_on_image(self.current_image, self.current_masks)
            return True
        return False
    
    def preview_single_mask(self, mask_index):
        if 0 <= mask_index < len(self.current_masks):
            show_single_mask(self.current_image, self.current_masks[mask_index])
            return True
        return False
    
    def preview_mask_grid(self, max_masks=None):
        if self.current_image is not None and self.current_masks:
            if max_masks is None:
                max_masks = len(self.current_masks)
            create_mask_grid(self.current_image, self.current_masks, max_masks)
            return True
        return False