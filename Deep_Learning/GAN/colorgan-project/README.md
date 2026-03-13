#                     Image Colorization Using GANs

# 1. Project Overview
## Objective:
 Convert black-and-white images into colorized versions using a GAN-based framework.
## High-Level Approach:
 A generator network learns to add plausible colors to grayscale images while a discriminator network distinguishes between real color images and those produced by the generator.
## Key Components:
Generator (G): Uses a U-Net architecture with skip connections.
Discriminator (D): Uses a plain CNN architecture without skip connections.

## Why Use U-Net for the Generator?
### Preserving Details:
    U-Net is known for its encoder-decoder structure with skip connections. These connections allow the model to pass low-level details (such as edges and textures) directly from the input to the output. This is very helpful in image-to-image translation tasks like colorization because it preserves the important spatial information from the grayscale image.
### Improved Learning:
    The skip connections in U-Net help the network learn better by reducing the loss of information during the encoding and decoding process. This often results in more realistic and sharper colorized images.

## Why Use a Plain CNN for the Discriminator?
### Simpler Architecture:
    The role of the discriminator is to classify images as either “real” (from the dataset) or “fake” (generated). For this task, a straightforward CNN is effective because it can focus on the overall structure and quality of the images without needing the detailed, pixel-level information that skip connections provide.
### Faster Training and Fewer Parameters:
    A simpler CNN means fewer parameters, which can help in faster training and reduce the risk of overfitting.

# 2. Loss Functions

I am using a combination of three losses:
- **Adversarial Loss:**  
  Forces the generator to create images that can fool the discriminator.
- **Reconstruction Loss (L1 Loss):**  
  Ensures that the generated image is close to the ground truth in a pixel-wise manner.
- **Perceptual Loss (Optional):**  
  Uses high-level features from a pre-trained network (like VGG) to help maintain texture and overall visual quality.

The total loss can be represented as:  
**Total Loss = Adversarial Loss + λ₁ × Reconstruction Loss + λ₂ × Perceptual Loss**  
(Here, λ₁ and λ₂ are weight factors that you can tune based on experiments.)

# 3. Dataset

We are using the [Anime Images Dataset with Their Description](https://www.kaggle.com/datasets/imsahibnanda/anime-images-dataset-with-their-description) from Kaggle. This dataset contains color images which we will convert to grayscale on the fly to create paired training samples.

# 4. Image Resolution

- **Original Resolution:** 768×768  
- **Working Resolution:** Will resize the images to **512×512**[Can change].  
  This lower resolution helps reduce computational load and memory requirements while still preserving sufficient detail for effective colorization.

# 5. Hyperparameters & Training Details

- **Optimizer:** AdamW (an adaptive optimizer with weight decay)
  - **Initial Learning Rate:** 0.0002  
  - **Adaptive Learning Rate:** I will use a learning rate scheduler (CosineAnnealingLR) to adjust the learning rate during training based on model performance.
  
- **Batch Size:** 8  
  (A smaller batch size is chosen to accommodate 8GB VRAM[4060ti], even though it might lead to slightly noisier gradient updates.)

- **Number of Epochs:** 10  
  (For initial experiments, with detailed logging of training progress and loss values.)

- **Additional Considerations:**  
  - **Dropout:** Not necessary for the generator (thanks to skip connections) and optional for the discriminator. Start without dropout and add it later if overfitting becomes an issue.
  - **Logging:** Detailed logging of training losses (each individual loss and the total loss) at every epoch to track progress and diagnose issues.

## Conclusion

This project is designed to be a practical introduction to GANs and image colorization. Starting with a well-defined framework using U-Net and a simple CNN, and combining multiple loss functions with adaptive training strategies, the project offers a balanced approach between simplicity and performance. Enjoy exploring and learning through this hands-on project!
