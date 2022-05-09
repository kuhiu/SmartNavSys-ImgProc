# Modulos utilizados
import numpy as np
import matplotlib.pylab as plt
from skimage.io import imread
import cv2
# Mis modulos
import f

# Bienvenida
print("Hello")

# Leo imagen
print( "The %s function: %s" % (imread.__name__, imread.__doc__.splitlines()[0]) )
img = cv2.imread('img/ex.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Aumento el brillo
print( "The %s function: %s" % (f.objcbright.__name__, f.objcbright.__doc__.splitlines()[0]) )
img_bright = f.objcbright(img, 0)

# La transformo a blanco y negro y cambio la luminosidad
print( "The %s function: %s" % (f.lum.__name__, f.lum.__doc__.splitlines()[0]) )
img_bAw_bright = f.lum(img, -10)

# LPF with fft
print( "The %s function: %s" % (f.mylpf_fft.__name__, f.mylpf_fft.__doc__.splitlines()[0]) )
img_lpf = f.mylpf_fft(img_bAw_bright, 0.3, plot_spectrum=False)

# Set contrast
print( "The %s function: %s" % (f.contrast.__name__, f.contrast.__doc__.splitlines()[0]) )
img_contrast = f.contrast(img_bright, rango=3, plot=False)

# Set contrast
print( "The %s function: %s" % (f.contrast.__name__, f.contrast.__doc__.splitlines()[0]) )
img_bAw_contrast = f.contrast(img_bAw_bright, rango=1, plot=False)

# Obj detect
print( "The %s function: %s" % (f.objchangecolor.__name__, f.objchangecolor.__doc__.splitlines()[0]) )
img_objdet = f.objchangecolor(img)

# Obj remove
print( "The %s function: %s" % (f.objremove.__name__, f.objremove.__doc__.splitlines()[0]) )
img_objremove = f.objremove(img)

# Edges with Canny
print( "The %s function: %s" % (cv2.Canny.__name__, cv2.Canny.__doc__.splitlines()[0]) )
img_edge = cv2.Canny(img_objremove,10,110)

# Ploteo imagenes
#print( "The %s function: %s" % (f.ploteo.__name__, f.ploteo.__doc__.splitlines()[0]) )
#f.ploteo( 3, 3, Original=img, Bright=img_bright, BrighterOrDarker_gray=img_bAw_bright, LPF_FFT=img_lpf, CONTRAST=img_contrast, gCONTRAST=img_bAw_contrast, 
#Edges=img_edge, ObjetChangeColor=img_objdet, ObjectRemove=img_objremove )

###################################################################
############################### Mix ###############################
###################################################################
#1. Image, Bright, Contrast, Edges?, Obj Remove

# Set contrast
print( "The %s function: %s" % (f.contrast.__name__, f.contrast.__doc__.splitlines()[0]) )
img_contrast2 = f.contrast(img_bright, rango=3, plot=False)

# Obj remove
print( "The %s function: %s" % (f.objremove.__name__, f.objremove.__doc__.splitlines()[0]) )
img_mix = f.objremove(img_contrast2, color="blue")

# Bridge
img_bridge = cv2.imread('img/Bridge.png')
img_bridge = cv2.cvtColor(img_bridge, cv2.COLOR_BGR2RGB)

# Obj remove
print( "The %s function: %s" % (f.objremove.__name__, f.objremove.__doc__.splitlines()[0]) )
img_bridgeDET = f.objremove(img_bridge, color="brown")


# Save
cv2.imwrite('img/out1.png', cv2.cvtColor(img_mix, cv2.COLOR_BGR2RGB))
cv2.imwrite('img/out2.png', cv2.cvtColor(img_bridgeDET, cv2.COLOR_BGR2RGB))

# Ploteo mix
print( "The %s function: %s" % (f.ploteo.__name__, f.ploteo.__doc__.splitlines()[0]) )
f.ploteo( 3, 3, Original=img , Bright=img_bright, Contrast=img_contrast, MIX=img_mix, BlackPod=img_objdet, Bridge=img_bridge, 
bridgeDET=img_bridgeDET)
