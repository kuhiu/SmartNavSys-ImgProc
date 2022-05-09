from skimage.color import rgb2lab, rgb2gray, lab2rgb
from skimage import img_as_ubyte
import numpy as np
import matplotlib.pylab as plt
import inspect, itertools 
from scipy import fftpack
import cv2

def normalize8(I):
  mn = I.min()
  mx = I.max()
  mx -= mn
  I = ((I - mn)/mx) * 255
  return I.astype(np.uint8)


def lum(im,lum):
    """RGB2Gray and modifies the brightness. ex: lum(img, +20) increase 20 the brightness"""
    im1 = rgb2lab(im)
    im1[...,1] = im1[...,2] = 0
    im1[...,0] = im1[...,0] + lum
    im1 = lab2rgb(im1)
    im1 = normalize8(im1)   # float to uint8
    im1 = im1[...,0]
    return im1

def ploteo(columnas, filas, **kwargs):
    """Plots"""
    i=1
    plt.figure(figsize=(40,40))
    for key,n in kwargs.items():
        plt.subplot(columnas, filas, i)
        plt.imshow(n, plt.cm.gray)
        plt.axis('off')
        plt.title('Imagen nro. %d: %s' %(i-1 , format(key)), size=10)
        i = i + 1
    plt.show()

def mylpf_fft(im, keep_fraction, plot_spectrum=True):
    """LPF with FFT"""    
    im_fft = fftpack.fft2(im)
    im_fft2 = im_fft.copy() # Call ff a copy of the original transform.
    r, c = im_fft2.shape    # Rows and columns of the array.
    # Set to zero all rows with indices between r*keep_fraction and r*(1-keep_fraction):
    im_fft2[int(r*keep_fraction):int(r*(1-keep_fraction))] = 0  
    # Similarly with the columns:
    im_fft2[:, int(c*keep_fraction):int(c*(1-keep_fraction))] = 0
    # Show the results
    if plot_spectrum == True:
        from matplotlib.colors import LogNorm
        # A logarithmic colormap
        plt.figure(figsize=(40,40))
        plt.subplot(2, 2, 1)
        plt.imshow(np.abs(im_fft), norm=LogNorm(vmin=5))
        plt.subplot(2, 2, 2)
        plt.imshow(np.abs(im_fft2), norm=LogNorm(vmin=5))
        plt.colorbar()
    # Reconstruct the denoised image from the filtered spectrum, keep only the real part for display.
    return fftpack.ifft2(im_fft2).real

def contrast(img, rango, plot):
    """Set contrast"""
    if rango == 1:
        cdf = np.zeros(256)
        hist, bins = np.histogram(img[...].flatten(),256,[0,256])
        cdf[...] = hist.cumsum()
        cdf_normalized = cdf[...] * hist.max() / cdf.max()
        binWidth = bins[1] - bins[0]
        if plot == True:
            plt.figure(figsize=(40,40))
            plt.subplot(1, 2, 1)
            hist, bins = np.histogram(img[...].flatten(),256,[0,256], normed=True)
            cdf[...] = hist.cumsum()
            cdf_normalized = cdf[...] * hist.max() / cdf.max()
            plt.plot(cdf_normalized, color = 'gray')
            plt.bar(bins[:-1], hist*binWidth, binWidth)
            plt.xlim([0,256])
            plt.legend(loc = 'upper left')

        img2 = np.copy(img)
        cdf_m = np.ma.masked_equal(cdf[...],0)
        cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min()) # min-max normalize
        cdf2 = np.ma.filled(cdf_m,0).astype('uint8')
        img2[...] = cdf2[img[...]]
        return img2
    else:
        colors = ['r', 'g', 'b']
        cdf = np.zeros((256,rango))
        for i in range(rango):
            hist, bins = np.histogram(img[...,i].flatten(),256,[0,256], normed=True)
            cdf[...,i] = hist.cumsum()
            cdf_normalized = cdf[...,i] * hist.max() / cdf.max()
            binWidth = bins[1] - bins[0]
        if plot == True:
            plt.figure(figsize=(40,40))
            plt.subplot(1, 2, 1)
            for i in range(rango):
                hist, bins = np.histogram(img[...,i].flatten(),256,[0,256], normed=True)
                cdf[...,i] = hist.cumsum()
                cdf_normalized = cdf[...,i] * hist.max() / cdf.max()
                plt.plot(cdf_normalized, color = colors[i], label='cdf ({})'.format(colors[i]))
                plt.bar(bins[:-1], hist*binWidth, binWidth, label='hist ({})'.format(colors[i]))
                plt.xlim([0,256])
                plt.legend(loc = 'upper left')
        img2 = np.copy(img)
        for i in range(rango):
            cdf_m = np.ma.masked_equal(cdf[...,i],0)
            cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min()) # min-max normalize
            cdf2 = np.ma.filled(cdf_m,0).astype('uint8')
            if rango == 1 :
                img2[...] = cdf2[img[...]]
            else:
                img2[...,i] = cdf2[img[...,i]]
        if plot == True:
            plt.subplot(1, 2, 2)
            for i in range(rango):
                hist, bins = np.histogram(img2[...,i].flatten(),256,[0,256], normed=True)
                cdf[...,i] = hist.cumsum()
                cdf_normalized = cdf[...,i] * hist.max() / cdf.max()
                plt.plot(cdf_normalized, color = colors[i], label='cdf ({})'.format(colors[i]))
                plt.bar(bins[:-1], hist*binWidth, binWidth, label='hist ({})'.format(colors[i]))
                plt.xlim([0,256])
                plt.legend(loc = 'upper left')
        return img2


def objchangecolor (img):
    """Object detect"""
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, (110, 145, 0), (120, 255, 255))
    imask = mask>0
    color = img.copy()
    hsv[...,0] = 0
    hsv[...,1] = 0
    hsv[...,2] = 0
    color[imask] = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)[imask]
    color = np.clip(color, 0, 255)
    return color

def objremove (img, color="blue"):
    """Object detect"""
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    if color == "blue":
        mask = cv2.inRange(hsv, (100, 150, 0), (125, 255, 255))
    elif color== "black":
        mask = cv2.inRange(hsv, (0, 0, 0), (255, 255, 30))
    elif color== "brown":
        mask = cv2.inRange(hsv, (10, 70, 20), (20, 150, 200))
    else: 
        mask = cv2.inRange(hsv, (0, 0, 0), (75, 75, 75))
    # Quitar el objeto a remover
    imask = mask>0
    remove = np.zeros_like(img, np.uint8)
    remove[imask] = img[imask]
    return remove

def objcbright(img, value):
    """Object high bright"""
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    final_hsv = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)
    return final_hsv

