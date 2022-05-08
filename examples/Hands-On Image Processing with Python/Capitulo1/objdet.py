import cv2
import numpy as np
import matplotlib.pylab as plt

# Leo imagen y obtengo su HSV (modelo de color)
img = cv2.imread("img/fish.png")
bck = cv2.imread("img/fish_bg.png")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Mascara
mask = cv2.inRange(hsv, (5, 100, 25), (20, 255, 255))

# Quitar el objeto a remover
imask = mask>0
orange = np.zeros_like(img, np.uint8)
orange[imask] = img[imask]

# Cambia el objeto de color
yellow = img.copy()
hsv[...,0] = hsv[...,0] + 170
yellow[imask] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[imask]
yellow = np.clip(yellow, 0, 255)

# 
bckfish = cv2.bitwise_and(bck, bck, mask=imask.astype(np.uint8))
nofish = img.copy()
nofish = cv2.bitwise_and(nofish, nofish, mask = np.bitwise_not(imask).astype(np.uint8) )
nofish = nofish + bckfish

# Plot
plt.subplot(331)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title('Imagen original', size=10)

plt.subplot(332)
plt.imshow(cv2.cvtColor(hsv, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title('hsv', size=10)

plt.subplot(333)
plt.imshow(cv2.cvtColor(yellow, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title('Cambio de color', size=10)

plt.subplot(334)
plt.imshow(cv2.cvtColor(nofish, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title('nofish', size=10)

plt.subplot(335)
plt.imshow(cv2.cvtColor(bckfish, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title('bckfish', size=10)

plt.show()
