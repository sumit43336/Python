import numpy as np
import matplotlib.pyplot as plt
import cv2


def show_masks_on_image(image, masks, show_plot=True):
    # show all masks overlaid
    if len(masks) == 0:
        print("No masks to display")
        return image
    
    sorted_masks = sorted(masks, key=lambda x: x['area'], reverse=True)
    
    overlay = np.ones((image.shape[0], image.shape[1], 4))
    overlay[:, :, 3] = 0  # transparent
    
    # add masks with random colors
    for mask_data in sorted_masks:
        mask = mask_data['segmentation']
        color = np.concatenate([np.random.random(3), [0.35]])
        overlay[mask] = color
    
    if show_plot:
        plt.figure(figsize=(12, 8))
        plt.imshow(image)
        plt.imshow(overlay)
        plt.axis('off')
        plt.title(f'All Masks ({len(masks)} masks)')
        plt.tight_layout()
        plt.show()
    
    return overlay


def show_single_mask(image, mask_data, show_plot=True):
    # display single mask
    mask = mask_data['segmentation']
    
    color_mask = np.zeros((image.shape[0], image.shape[1], 4))
    color_mask[:, :, 3] = 0
    
    # blue color
    color = np.array([30/255, 144/255, 255/255, 0.6])
    color_mask[mask] = color
    
    if show_plot:
        plt.figure(figsize=(10, 8))
        plt.imshow(image)
        plt.imshow(color_mask)
        plt.axis('off')
        plt.title(f"Mask - Area: {mask_data['area']} pixels")
        plt.tight_layout()
        plt.show()
    
    return color_mask


def create_mask_grid(image, masks, max_masks=None):
    # grid view of masks
    if max_masks is None:
        num_masks = len(masks)
    else:
        num_masks = min(len(masks), max_masks)
    
    if num_masks == 0:
        print("No masks to display")
        return
    
    cols = 3
    rows = (num_masks + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, 5*rows))
    if rows == 1:
        axes = axes.reshape(1, -1)
    
    sorted_masks = sorted(masks, key=lambda x: x['area'], reverse=True)
    
    for idx in range(rows * cols):
        row = idx // cols
        col = idx % cols
        ax = axes[row, col]
        
        if idx < num_masks:
            mask_data = sorted_masks[idx]
            mask = mask_data['segmentation']
            
            overlay = image.copy()
            overlay[mask] = [255, 0, 0]  # red
            
            ax.imshow(overlay)
            ax.set_title(f"Mask {idx+1}\nArea: {mask_data['area']}")
            ax.axis('off')
        else:
            ax.axis('off')
    
    plt.tight_layout()
    plt.show()


def save_mask_visualization(image, masks, output_path):
    # save visualization
    try:
        overlay = show_masks_on_image(image, masks, show_plot=False)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(image)
        ax.imshow(overlay)
        ax.axis('off')
        
        plt.savefig(output_path, bbox_inches='tight', dpi=150)
        plt.close()
        
        print(f"Saved visualization to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error saving visualization: {e}")
        return False


