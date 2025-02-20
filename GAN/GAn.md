# (GAN) Generative Adversarial Network

## Gan working is designed to imitate the working of human brain.

It's a machine Learning model called a neural network.

It trains two neural networks to compete against one another to generate more realistic data from the dataset.

## Generator 

Generator is used to generate images from random noise. 
It is CNN (Convolutional Neural Network), that takes image as an input and can differentiate between the object in the image.And it assignes importance to them. These importace is known as weights. 
It generates images that can be mistaken for real ones

## Discriminator

They are DNN (Deconvolutional Neural Network).
They work in revarsal figuring out the features of the input. 
Aiming to identify the features of an input that were either missed by the CNN or convoluted with other signals.
A discriminator network aims to identify which received output is artificial.

### Inshort the Gan has a Generator and a Discriminator. Generator generate images and Discriminator tells if its close to real or fake.


