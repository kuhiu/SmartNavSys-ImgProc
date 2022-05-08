from scipy import ndimage as ndi
from skimage.morphology import watershed, binary_dilation, binary_erosion, remove_small_objects
from skimage.morphology import disk, square
from scipy.ndimage import distance_transform_edt
from skimage.measure import label, regionprops
from skimage.segmentation import clear_border
from skimage.filters import rank, threshold_otsu
from skimage.feature import peak_local_max, blob_log
from skimage.util import img_as_ubyte
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
import matplotlib.pyplot as plt

image = img_as_ubyte(rgb2gray(imread('img/sunflowers.png')))

distance = ndi.distance_transform_edt(image)
local_maximum = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)), labels=image)
markers = ndi.label(local_maximum)[0]

labels = watershed(-distance, markers, mask=image)
labels = remove_small_objects(labels, min_size=100)

props = regionprops(labels)
print(len(np.unique(labels)), len(props))

plt.subplot(3,3,1)
plt.imshow(image, cmap='gray')
plt.title('Image', size=10)

plt.subplot(3,3,2)
plt.imshow(distance, cmap='gray')
plt.title('Distance', size=10)

plt.subplot(3,3,3)
plt.imshow(markers, cmap='gray')
plt.title('Markers', size=10)

plt.subplot(3,3,4)
plt.imshow(labels)
plt.title('Labels', size=10)

image = img_as_ubyte(rgb2gray(imread('img/flowers.png')))

denoised = rank.median(image, disk(2))
markers1 = rank.gradient(denoised, disk(5)) < 20
markers2 = ndi.label(markers1)[0]

gradient = rank.gradient(denoised, disk(2))
labels1 = watershed(gradient, markers2)
labels2 = remove_small_objects(labels1, min_size=100)
props = regionprops(labels)
print(len(np.unique(labels)), len(props))

plt.subplot(3,3,5)
plt.imshow(denoised, cmap='gray')
plt.title('Erosion', size=10)

plt.subplot(3,3,6)
plt.imshow(markers1, cmap='gray')
plt.title('Erosion', size=10)

plt.subplot(3,3,7)
plt.imshow(labels1, cmap='gray')
plt.title('Dilata', size=10)

plt.subplot(3,3,8)
plt.imshow(gradient, cmap='gray')
plt.title('Gradient', size=10)

plt.subplot(3,3,9)
plt.imshow(markers2, cmap='gray')
plt.title('Props', size=10)

plt.show()


