# SAM Segmentation Tool

A GUI-based image segmentation tool built for educational purposes using Meta's Segment Anything Model (SAM).

## ⚠️ Important Attribution

This project is built using the **Segment Anything Model (SAM)** developed by Meta AI Research (FAIR). This is an educational implementation created for learning purposes only.

### Original SAM Repository
- **Repository**: [facebookresearch/segment-anything](https://github.com/facebookresearch/segment-anything)
- **Paper**: [Segment Anything](https://arxiv.org/abs/2304.02643)
- **License**: Apache 2.0
- **Authors**: Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alex Berg, Wan-Yen Lo, Piotr Dollar, Ross Girshick

### Citation
If you use this tool or SAM in your work, please cite the original paper:
```bibtex
@article{kirillov2023segany,
  title={Segment Anything},
  author={Kirillov, Alexander and Mintun, Eric and Ravi, Nikhila and Mao, Hanzi and Rolland, Chloe and Gustafson, Laura and Xiao, Tete and Whitehead, Spencer and Berg, Alexander C. and Lo, Wan-Yen and Doll{\'a}r, Piotr and Girshick, Ross},
  journal={arXiv:2304.02643},
  year={2023}
}
```

## About This Tool

This is a simple GUI wrapper around SAM that allows users to:
- Load and browse through images
- Generate segmentation masks automatically
- Preview and select masks interactively
- Save accepted masks with metadata

This tool was created as a learning project to understand how SAM works and to practice building GUI applications with image processing capabilities.

## Features

- 🖼️ Load and browse images from a folder
- 🤖 Automatic mask generation using SAM
- 👁️ Preview masks individually or in grid view
- ✅ Accept/reject masks interactively
- 💾 Save accepted masks (binary masks, overlays, and metadata)
- 🎨 Simple and intuitive GUI interface

## Installation

### Prerequisites
- Python 3.8 or higher
- PyTorch 1.7+ with CUDA support (recommended)

### Step 1: Install Dependencies

```bash
pip install torch torchvision opencv-python matplotlib pillow numpy
```

### Step 2: Install Segment Anything

```bash
pip install git+https://github.com/facebookresearch/segment-anything.git
```

Or clone and install locally:
```bash
git clone https://github.com/facebookresearch/segment-anything.git
cd segment-anything
pip install -e .
```

### Step 3: Download SAM Model Checkpoint

Download one of the model checkpoints from Meta:

- **vit_b** (smallest): [Download](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth) - ~375MB
- **vit_l** (medium): [Download](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth) - ~1.2GB
- **vit_h** (largest): [Download](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth) - ~2.4GB

Place the checkpoint file in a known location (you'll browse to it in the GUI).

## Usage

### Running the GUI

```bash
python gui.py
```

### Workflow

1. **Load SAM Model**: Click "Browse" next to "Model Checkpoint" and select your downloaded `.pth` file
2. **Select Input Folder**: Choose a folder containing images you want to segment
3. **Select Output Folder**: Choose where to save the segmentation results
4. **Navigate Images**: Use "Previous" and "Next" buttons to browse through images
5. **Process Image**: Click "Process Image" to run SAM on the current image
6. **Review Masks**: Browse through generated masks using the mask navigation
7. **Accept Masks**: Click "Accept Mask" for masks you want to keep
8. **Save Results**: Click "Save Accepted Masks" to export your selections

## Project Structure

```
Segmentaion_tool/
├── gui.py              # Main GUI application (Tkinter interface)
├── main.py             # Core application logic and workflow
├── load_images.py      # Image loading utilities
├── sam_processor.py    # SAM model loading and processing
├── mask_preview.py     # Mask visualization functions
├── save_manager.py     # Mask saving and export utilities
├── config.py           # Configuration settings
└── README.md           # This file
```

## Output Format

When you save accepted masks, the tool creates:

- **Binary masks**: PNG files with white (255) for mask regions and black (0) for background
- **Overlay images**: Original image with colored mask overlay
- **Metadata**: JSON file containing mask statistics (area, bounding box, etc.)

## Configuration

Edit `config.py` to customize:
- Default model type
- Device (CPU/CUDA)
- Mask visualization colors
- Output file naming conventions

## Limitations

- This is an educational tool and not optimized for production use
- Processing large images or generating many masks can be memory-intensive
- GUI is basic and may not handle edge cases gracefully

## Learning Resources

To learn more about SAM:
- [SAM Project Page](https://segment-anything.com/)
- [SAM Demo](https://segment-anything.com/demo)
- [SAM Paper](https://arxiv.org/abs/2304.02643)
- [SAM GitHub Repository](https://github.com/facebookresearch/segment-anything)

## License

This educational tool is provided as-is for learning purposes. The Segment Anything Model itself is licensed under Apache 2.0 by Meta AI Research. Please refer to the [original repository](https://github.com/facebookresearch/segment-anything) for full license details.

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by Meta Platforms, Inc. It is an independent educational project created to learn about image segmentation and the SAM model.
