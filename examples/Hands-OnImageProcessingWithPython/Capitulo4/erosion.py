from skimage.io import imread
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from scipy.ndimage.morphology import binary_erosion, binary_dilation, binary_fill_holes
from scipy.ndimage.morphology import morphological_gradient, distance_transform_edt
from skimage import morphology as morph
import numpy as np
import matplotlib.pylab as plt


im = rgb2gray(imread('img/out1.png'))
thres = threshold_otsu(im)
img = (im > thres).astype(np.uint8)

# Erosion de imagen
eroded = binary_erosion(img, structure=np.ones((3,3)),iterations=5)[20:,20:]
eroded = 1 - eroded

# Dilata
dilated = binary_dilation(eroded, structure=np.ones((11,11)))
boundary = np.clip(dilated.astype(np.int) - eroded.astype(np.int),0, 1)
dt = distance_transform_edt(np.logical_not(boundary))

plt.subplot(2,3,1)
plt.imshow(im, cmap='gray')
plt.title('Original', size=10)

plt.subplot(2,3,2)
plt.imshow(img, cmap='gray')
plt.title('Th hole', size=10)

plt.subplot(2,3,3)
plt.imshow(eroded, cmap='gray')
plt.title('Erosion', size=10)

plt.subplot(2,3,4)
plt.imshow(dilated, cmap='gray')
plt.title('Dilata', size=10)

plt.show()