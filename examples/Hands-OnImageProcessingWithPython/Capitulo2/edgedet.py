import numpy as np
import cv2 
from matplotlib import pyplot as plt


im = cv2.imread('img/flowers.png')
img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(img,30,100)

fig = plt.figure(figsize=(20, 6))
plt.subplot(121)
plt.imshow(img, cmap=plt.cm.gray)
plt.axis('off')

plt.subplot(122)
plt.imshow(edges, cmap=plt.cm.gray)
plt.axis('off')

plt.show()