from scipy.ndimage import label
from scipy.ndimage.morphology import binary_closing
from skimage.filters import threshold_otsu
import matplotlib.pylab as plt
import numpy as np
from skimage.util import img_as_ubyte
from skimage.color import rgb2gray
from skimage.io import imread

#original = plt.imread('img/sunflowers.png')
original = img_as_ubyte(rgb2gray(imread('img/out2.png')))
thres = threshold_otsu(original)
binary = original > thres
binary_closed = binary_closing(binary, structure=np.ones((2,2)))
labeled_image, num_features = label(binary_closed)
feature_areas = np.bincount(labeled_image.ravel())[1:]   
#print(feature_areas) # if we use 3x3 SE we shall get two regions with areas 24, 46

plt.figure(figsize=(8,7))
plt.gray()
plt.subplot(221), plt.imshow(original), plt.axis('off'), plt.title('original')
plt.subplot(222), plt.imshow(binary), plt.axis('off'), plt.title('binray')
plt.subplot(223), plt.imshow(binary_closed), plt.axis('off'), plt.title('binray closed')
plt.subplot(224), plt.imshow(labeled_image, cmap='inferno'), plt.axis('off'), plt.title('labelled')
plt.show()