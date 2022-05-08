import numpy as np
import matplotlib.pylab as plt
from skimage.io import imread
from skimage.exposure import equalize_hist, equalize_adapthist
from skimage.color import rgb2lab, rgb2gray, lab2rgb
import cv2

def plot_hist(img):
    cdf = np.zeros(256)
    hist, bins = np.histogram(img[...].flatten(),256,[0,256])
    cdf[...] = hist.cumsum()
    cdf_normalized = cdf[...] * hist.max() / cdf.max()
    plt.plot(cdf_normalized)
    binWidth = bins[1] - bins[0]
    plt.xlim([0,256])
    plt.legend(loc = 'upper left')
    plt.show()
    return cdf

img = imread('img/flowers.png')
#img = rgb2gray(img)
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

cdf = plot_hist(img)
img2 = np.copy(img)

cdf_m = np.ma.masked_equal(cdf[...],0)
cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min()) # min-max normalize
cdf2 = np.ma.filled(cdf_m,0).astype('uint8')
img2[...] = cdf2[img[...]]


plt.subplot(2,3,1)
plt.imshow(img, cmap='gray')
plt.title('Original', size=10)


plt.subplot(2,3,2)
plt.imshow(img2, cmap='gray')
plt.title('High Contrast', size=10)


plt.show()