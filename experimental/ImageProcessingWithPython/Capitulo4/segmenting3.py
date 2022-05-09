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
import cv2

def segment_with_watershed(im, cell_thresh, bg_thresh):
    if np.max(im) != 1.0:
        im = (im - im.min()) / (im.max() - im.min())
    im_mask = im < cell_thresh

    basins = np.zeros_like(im)
    basins[im < cell_thresh] = 2
    basins[im > bg_thresh] = 1

    flood_seg = watershed(im , basins)
    flood_seg = flood_seg > 1.0

    #selem = square(3)
    #flood_erode = binary_erosion(flood_seg, selem=selem)
    #flood_seg = clear_border(flood_seg, buffer_size=1)

    distances = distance_transform_edt(flood_seg)

    local_max = peak_local_max(distances, indices=False, footprint=None, labels=flood_seg, min_distance=10)
    max_lab = label(local_max)

    final_seg = watershed(-distances, max_lab, mask=flood_seg)
    final_seg = remove_small_objects(final_seg, min_size=5)

    props = regionprops(final_seg)
    num_cells = len(props)

    print("El numero de piernas encontradas: ", num_cells)

    #if num_cells != 2:
    #    print("No se encontraron las dos piernas")
    #    exit(1)

    indices = np.where(distances != [0])
    coordinates = list(zip(indices[0], indices[1]))
    #print("Coordenadas: ", coordinates)
    #print("Coordenadas: ", coordinates[0])
    #print("Coordenadas: ", coordinates[-1])
    #print("Disntancia entre piernas [PIXELES]: ", (coordinates[0][1] - coordinates[-1][1]) )

    plt.subplot(2,3,1)
    plt.imshow(im, cmap='gray')
    plt.axis('off')
    plt.title('im', size=10)

    plt.subplot(2,3,2)
    plt.imshow(im_mask, cmap='gray')
    plt.axis('off')
    plt.title('mask', size=10)

    plt.subplot(2,3,3)
    plt.imshow(basins, cmap='gray')
    plt.axis('off')
    plt.title('basins', size=10)

    plt.subplot(2,3,4)
    plt.imshow(flood_seg, cmap='gray')
    plt.axis('off')
    plt.title('flood_seg', size=10)

    plt.subplot(2,3,5)
    plt.imshow(distances, cmap='gray')
    plt.axis('off')
    plt.title('distances', size=10)

    plt.subplot(2,3,6)
    plt.imshow(final_seg, cmap='gray')
    plt.axis('off')
    plt.title('final_seg', size=10)

    plt.show()

    cv2.imwrite('img/out11.png', final_seg)

    return final_seg, distances, basins, num_cells



#image = img_as_ubyte(rgb2gray(imread('img/out2.png')))
image = img_as_ubyte(rgb2gray(imread('img/out1.png')))
image = rank.median(image, disk(30))
labels, distances, markers, nseg = segment_with_watershed(image,0.2, 0.1)
#labels, distances, markers, nseg = segment_with_watershed(image,0.3, 0.6)
