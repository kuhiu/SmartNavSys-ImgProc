# Transformacion que conserva puntos lineas rectas y planos. mapeo.

import numpy as np
from scipy import ndimage as ndi
from skimage.io import imread
from skimage.color import rgb2lab, rgb2gray, lab2rgb
from skimage.transform import rotate
import matplotlib.pylab as plt

im = imread('img/flowers.png')

#img = rgb2gray(im)

img = rgb2lab(im)
img[...,1] = img[...,2] = 0
img = lab2rgb(img)
h, w, d = im.shape

# Matriz identidad
mat_identity = np.array([[1,0,0],[0,1,0],[0,0,1]])
img1 = ndi.affine_transform(img, mat_identity)

# Reflexion
#mat_reflect = np.array([[1,0,0],[0,-1,0],[0,0,1]]) @ np.array([[1,0,0],[0,1,-h],[0,0,1]])
#img2 = ndi.affine_transform(img, mat_reflect) # offset=(0,h)
img2 = img[:,::-1]

# Scale
s_x, s_y = 0.75, 1.25
mat_scale = np.array([[s_x,0,0],[0,s_y,0],[0,0,1]])
img3 = ndi.affine_transform(img, mat_scale)

# Rotate
theta = np.pi/6
#mat_rotate = np.array([[1,0,w/2],[0,1,h/2],[0,0,1]]) @ np.array([[np.cos(theta),np.sin(theta),0],[np.sin(theta),-np.cos(theta),0],[0,0,1]]) @ np.array([[1,0,-w/2],[0,1,-h/2],[0,0,1]])
#img4 = ndi.affine_transform(img, mat_rotate)
img4 = rotate(img, 30)

# Corte
lambda1 = 0.2
mat_shear = np.array([[1,lambda1,0],[lambda1,1,0],[0,0,1]])
img5 = ndi.affine_transform(img, mat_shear)

# Junto todo

mat_all = mat_identity @ mat_scale @ mat_shear
#mat_all = mat_identity @ mat_reflect @ mat_scale @ mat_rotate @ mat_shear
imgf = ndi.affine_transform(img, mat_all)

# Plot
plt.subplot(331)
plt.imshow(img, cmap='gray')
plt.axis('off')
plt.title('Original Image', size=10)

plt.subplot(332)
plt.imshow(img1, cmap='gray')
plt.axis('off')
plt.title('Identidad', size=10)

plt.subplot(333)
plt.imshow(img2, cmap='gray')
plt.axis('off')
plt.title('Reflexion', size=10)

plt.subplot(334)
plt.imshow(img3, cmap='gray')
plt.axis('off')
plt.title('Escalado', size=10)

plt.subplot(335)
plt.imshow(img4, cmap='gray')
plt.axis('off')
plt.title('Rotar', size=10)

plt.subplot(336)
plt.imshow(img5, cmap='gray')
plt.axis('off')
plt.title('Corte', size=10)

plt.subplot(337)
plt.imshow(imgf, cmap='gray')
plt.axis('off')
plt.title('Todo', size=10)

plt.show()

