import numpy as np
import matplotlib.pylab as plt
from skimage.io import imread
from skimage.exposure import equalize_hist, equalize_adapthist

def plot_hist(img):
    colors = ['r', 'g', 'b']
    cdf = np.zeros((256,3))
    for i in range(3):
        hist, bins = np.histogram(img[...,i].flatten(),256,[0,256], normed=True)
        cdf[...,i] = hist.cumsum()
        print (hist.cumsum())
        cdf_normalized = cdf[...,i] * hist.max() / cdf.max()
        plt.plot(cdf_normalized, color = colors[i], label='cdf ({})'.format(colors[i]))
        binWidth = bins[1] - bins[0]
        plt.bar(bins[:-1], hist*binWidth, binWidth, label='hist ({})'.format(colors[i]))
        plt.xlim([0,256])
        plt.legend(loc = 'upper left')
    return cdf

img = imread('img/flowers.png')
cdf = plot_hist(img)
img2 = np.copy(img)
for i in range(3):
    cdf_m = np.ma.masked_equal(cdf[...,i],0)
    cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min()) # min-max normalize
    cdf2 = np.ma.filled(cdf_m,0).astype('uint8')
    img2[...,i] = cdf2[img[...,i]]


plt.subplot(2,3,1)
plt.imshow(img, cmap='gray')
plt.title('Original', size=10)


plt.subplot(2,3,2)
plt.imshow(img2, cmap='gray')
plt.title('High Contrast', size=10)


plt.subplot(2,3,3)
cdf = plot_hist(img)
plt.title('Original', size=10)


plt.subplot(2,3,4)
cdf = plot_hist(img2)
plt.title('High Contrast', size=10)


plt.show()