# Unet Arcitecture
![alt text](image.png)
The architecture is U Shaped. 
Encoder is the left side of the image.
Decoder is the right side of the image.
## A. Contracting Path
 1. This takes the image.
 2. Applies convolution (filter that detects the features like edge, tectures etc.)
 3. Repeditly shrings the image, While increases the depth that means 
 4. This helps the network understand "what"is in the iamge.
## B. Bottleneck
 The bottom of the "U"is where the image info is most compressed but has the richest features representation.
## C. Expanding Path (Decoder/Upsampling)
 1. Takes the random image and do Upsameping
 2. Rebuild the spatial dimentions to match the orignal image.
 3. Gives a pixel by pixel classification.(the segmentaion mask).
## D. Skip Connections (The Special Sauce!)
 1. The orange dashed lines in the diagram represent skip connections. These are what make U-Net special:
 2. They connect the contracting path to the expanding path
 3. They allow detailed spatial information to flow directly across the "U"
 4. This helps preserve important spatial details that might get lost during compression
## Think of U-Net like a detective who:
 1. First takes a photo and repeatedly zooms out to see the big picture (contracting path)
 2. Then starts zooming back in to specific areas (expanding path)
 3. But importantly, keeps referring back to the original detailed photos (skip connections) to make sure the fine details aren't lost
## What U-Net Produces
The output is a "segmentation mask" - essentially a map where each pixel is assigned a class. For example, in a medical image:
 1. Pixel value 1 = tumor
 2. Pixel value 0 = normal tissue