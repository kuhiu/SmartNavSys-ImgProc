import numpy as np
import scipy.fftpack as fp
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.restoration import wiener, unsupervised_wiener
from skimage.measure import compare_psnr
import matplotlib.pylab as plt


def cls_filter(y,h,c,lambd):
    Hf = fp.fft2(fp.ifftshift(h))
    Cf = fp.fft2(fp.ifftshift(c))
    Hf = np.conj(Hf) / (Hf*np.conj(Hf) + lambd*Cf*np.conj(Cf))
    Yf = fp.fft2(y)
    I = Yf*Hf
    im = np.abs(fp.ifft2(I))
    return (im, Hf)


x = rgb2gray(imread('img/me3.png'))

# Add noise
M, N = x.shape
h = np.ones((4,4))/16 # blur filter
h = np.pad(h, [(M//2-2, M//2-2), (N//2-2, N//2-2)], mode='constant')
sigma = 0.05
#Xf = fp.fft2(x)
#Hf = fp.fft2(fp.ifftshift(h))
#Y = Hf*Xf
#y = fp.ifft2(Y).real + sigma*np.random.normal(size=(M,N))

# Inverse filter
#epsilon = 0.25
#pix, F_pseudo = pseudo_inverse_filter(y, h, epsilon)

# Wiener filter
#wx = wiener(y, h, balance=0.25)

# CLS filter
c = np.array([[0,1/4,0],[1/4,-1,1/4],[0,1/4,0]])    # High pass filter
c = np.pad(c, [(M//2-1, M//2-2), (N//2-2, N//2-1)], mode='constant')
Cf = fp.fft2(fp.ifftshift(c))
lambd = 20
clx, F_restored = cls_filter(x, h, c, lambd)
print(r'Restored (CLS, $\lambda=${}) PSNR: {}'.format(lambd, np.round(compare_psnr(x, clx),3)))


# Plot
plt.subplot(2,3,1)
plt.imshow(x, cmap='gray')
plt.title('Original', size=10)

plt.subplot(2,3,2)
plt.imshow(clx, cmap='gray')
plt.title('CLS', size=10)

plt.show()