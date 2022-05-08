# denoise with mean and median

#matplotlib inline
from skimage.io import imread
from skimage.util import random_noise
from skimage.color import rgb2gray
from skimage.measure import compare_psnr
from scipy.ndimage import uniform_filter, median_filter
import numpy as np
import matplotlib.pylab as plt


def plt_hist(noise, bins=None):
    plt.grid()
    plt.hist(np.ravel(noise), bins=bins, alpha=0.5, color='green')
    plt.tick_params(labelsize=10)
    plt.title('Noise Historgram', size=10)

def plt_images(im, im_noisy, noise, noise_type, i):
    im_denoised_mean = uniform_filter(im_noisy, 3)
    im_denoised_median = median_filter(im_noisy, 3)

    plt.subplot(2,2,i)
    plt.imshow(im_noisy, cmap='gray')
    plt.title('Noisy ({}), PSNR={}'.format(noise_type, np.round(compare_psnr(im, im_noisy),3)), size=10)
    plt.axis('off')
    plt.subplot(2,2,i+1)
    plt.imshow(im_denoised_mean, cmap='gray')
    plt.title('Denoised (mean), PSNR={}'.format(np.round(compare_psnr(im, im_denoised_mean),3)), size=10)
    plt.axis('off')
    plt.subplot(2,2,i+2)
    plt.imshow(im_denoised_median, cmap='gray')
    plt.title('Denoised (median), PSNR={}'.format(np.round(compare_psnr(im, im_denoised_median),3)), size=10)
    plt.axis('off')
    plt.subplot(2,2,i+3), plt_hist(noise)
    plt.show()


im = rgb2gray(imread('img/Test1.png'))

#im1 = random_noise(im, 'gaussian', var=0.15**2)
im1 = im
plt_images(im, im1, im1-im, 'Gaussian', 1)


rank.mean_percentile()