import numpy as np
from skimage.io import imread
from skimage.color import rgb2lab, lab2rgb
import matplotlib.pylab as plt

im = imread('img/img_girl.jpg')

# LAB : espacio de color
# L : Luminosidad, A : De rojo a verde, B: De azul a amrillo

im1 = rgb2lab(im)
im2 = rgb2lab(im)
im3 = rgb2lab(im)
im4 = rgb2lab(im)
im5 = rgb2lab(im)

#print (im1)

im1[...,1] = im1[...,2] = 0
im2[...,0] = im2[...,0] + 30
im3[...,0] = im3[...,0] - 30
im4[...,0] = np.max(im4[...,0]) - im4[...,0]
im5[...,1] = np.max(im5[...,1]) - im5[...,1]

im1 = lab2rgb(im1)
im2 = lab2rgb(im2)
im3 = lab2rgb(im3)
im4 = lab2rgb(im4)
im5 = lab2rgb(im5)

plt.figure(figsize=(40,40))

plt.subplot(331)
plt.imshow(im)
plt.axis('off')
plt.title('Original Image', size=20)

plt.subplot(332)
plt.imshow(im1) 
plt.axis('off')
plt.title('Grayscale Image', size=20)

plt.subplot(333)
plt.imshow(im2) 
plt.axis('off')
plt.title('Brighter Image', size=20)

plt.subplot(334)
plt.imshow(im3) 
plt.axis('off')
plt.title('Darker Image', size=20)

plt.subplot(335)
plt.imshow(im4) 
plt.axis('off')
plt.title('Inverted Image', size=20)

plt.subplot(336)
plt.imshow(im5) 
plt.axis('off')
plt.title('Inverted Image', size=20)

plt.show()
