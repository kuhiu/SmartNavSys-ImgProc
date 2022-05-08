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
from skimage.io import imsave

changeimg = 'img/out2.png'
saveimg = 'img/out22.png'

image = img_as_ubyte(rgb2gray(imread(changeimg)))

#distance = ndi.distance_transform_edt(image)
#local_maximum = peak_local_max(distance, indices=False, footprint=np.ones((5, 5)), labels=image)
#markers = ndi.label(local_maximum)[0]

denoised = rank.median(image, disk(25))
markers = rank.gradient(denoised, disk(10)) < 20
markers = ndi.label(markers)[0]

gradient = rank.gradient(denoised, disk(25))
labels = watershed(gradient, markers)
#labels = remove_small_objects(labels, min_size=10)

labels = clear_border(labels, buffer_size=1)

props = regionprops(labels)
print(len(np.unique(labels)), len(props))

indices = np.where( (1-labels) != [0])
coordinates = list(zip(indices[0], indices[1]))

print("Disntancia entre piernas [PIXELES]: ", (coordinates[0][1] - coordinates[-1][1]) )

# Save
imsave(saveimg, labels)

plt.subplot(2,3,1)
plt.imshow(image, cmap='gray')
plt.axis('off')
plt.title('image', size=10)

plt.subplot(2,3,2)
plt.imshow(denoised, cmap='gray')
plt.axis('off')
plt.title('denoised', size=10)

plt.subplot(2,3,3)
plt.imshow(markers, cmap='gray')
plt.axis('off')
plt.title('markers', size=10)

plt.subplot(2,3,4)
plt.imshow(gradient, cmap='gray')
plt.axis('off')
plt.title('gradient', size=10)

plt.subplot(2,3,5)
plt.imshow(labels, cmap='gray')
plt.axis('off')
plt.title('labels', size=10)

plt.show()

