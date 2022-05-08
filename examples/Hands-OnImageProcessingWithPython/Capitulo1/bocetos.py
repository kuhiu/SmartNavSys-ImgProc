import numpy as np
from skimage.io import imread
from skimage.color import rgb2gray
from skimage import util
from skimage import img_as_float
import matplotlib.pylab as plt
#from medpy.filter.smoothing import anisotropic_diffusion
from skimage.filters import gaussian, threshold_otsu

# Min y Max en una imagen
def normalize(img):
    return (img-np.min(img))/(np.max(img)-np.min(img))

 # Extrae bordes de una imagen
def sketch(img, edges):
    output = np.multiply(img, edges)
    output[output>1]=1
    output[edges==1]=1
    return output

#def edges_with_anisotropic_diffusion(img, niter=100, kappa=10,gamma=0.1):
#    output = img - anisotropic_diffusion(img, niter=niter, \
#    kappa=kappa, gamma=gamma, voxelspacing=None, \
#    option=1)
#    output[output > 0] = 1
#    output[output < 0]
#    return output

def sketch_with_dodge(img):
    orig = img
    blur = gaussian(util.invert(img), sigma=20)
    result = blur / util.invert(orig)
    result[result>1] = 1
    result[orig==1] = 1
    return result

def edges_with_dodge2(img):
    img_blurred = gaussian(util.invert(img), sigma=5)
    output = np.divide(img, util.invert(img_blurred) + 0.001)
    output = normalize(output)
    thresh = threshold_otsu(output)
    output = output > thresh
    return output

def edges_with_DOG(img, k = 200, gamma = 1):
    sigma = 0.5
    output = gaussian(img, sigma=sigma) - gamma*gaussian(img, \
    sigma=k*sigma)
    output[output > 0] = 1
    output[output < 0] = 0
    return output

im = imread('img/humming.png')
img = rgb2gray(im)

imgf = edges_with_dodge2(img)

plt.subplot(111)
plt.imshow(imgf, cmap='gray')
plt.axis('off')
plt.title('Boceto', size=10)

plt.show()
