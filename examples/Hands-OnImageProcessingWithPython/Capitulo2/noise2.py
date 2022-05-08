# denoise with pca dft and dwt

import numpy as np
from skimage.io import imread
from numpy.random import RandomState
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
#from sklearn.datasets import fetch_olivetti_faces
#from sklearn import decomposition
from skimage.util import random_noise
from skimage import img_as_float
from time import time
import scipy.fftpack as fp
import pywt


im = rgb2gray(imread('img/Test1.png'))

img = random_noise(im, var=0.005)

n_components = 2
plt.figure(figsize=(20,4))

#freq = fp.fftshift(fp.fft2((np.reshape(im, image_shape)).astype(float)))
freq = fp.fftshift(fp.fft2(im.astype(float)))

print (freq)

freq[:freq.shape[0]//2 - n_components//2,:] = freq[freq.shape[0]//2 + n_components//2:,:] = 0
freq[:,:freq.shape[1]//2 - n_components//2] = freq[:,freq.shape[1]//2 + n_components//2:] = 0

plt.axis('off')
plt.subplot(2,2,1)
plt.imshow(im, cmap='gray')
plt.title('Original', size=10)

plt.axis('off')
plt.subplot(2,2,2)
plt.imshow(img, cmap='gray')
plt.title('Noised (mean)', size=10)

plt.axis('off')
plt.subplot(2,2,3)
plt.imshow(fp.ifft2(fp.ifftshift(freq)).real, cmap='gray')
plt.title('FFT LPF', size=10)

plt.show()

plt.plot(freq, np.abs(freq), cmap='gray')
plt.title('Espectro', size=10)
plt.legend()