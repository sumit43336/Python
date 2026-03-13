# Generative Adversarial Networks (GANs)

Implementation of GAN architectures for image generation and manipulation tasks.

## Project Structure

### [basic-gan/](./basic-gan/)
**Fundamental GAN Implementation**
- Core GAN theory and concepts
- Generator and Discriminator architecture
- DCGAN implementation with MNIST dataset
- Training dynamics and loss analysis

### [colorgan-project/](./colorgan-project/)
**Advanced Image Colorization**
- U-Net Generator for image-to-image translation
- CNN Discriminator for realistic color validation
- Anime image colorization using adversarial training
- Multiple loss functions (Adversarial, L1, Perceptual)

## Key Learning Areas

- **Adversarial Training**: Two-network competition dynamics
- **Generator Design**: Creating realistic data from noise
- **Discriminator Design**: Distinguishing real from generated data
- **Training Stability**: Techniques for stable GAN training
- **Loss Functions**: Various approaches to GAN optimization

## Technical Implementation

- PyTorch-based implementations
- Custom dataset handling
- Advanced optimization techniques
- Comprehensive training metrics
- Visual result analysis

## Applications Demonstrated

- Digit generation (MNIST)
- Image colorization (Anime dataset)
- Style transfer concepts
- Data augmentation techniques

---
Part of Deep Learning Learning Path