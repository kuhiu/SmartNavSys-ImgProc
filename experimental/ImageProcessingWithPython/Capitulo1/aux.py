import cv2

img = cv2.imread("img/fish.png")

print(type(img))
print(img)
img[...,1]=0
print(img)