import os
import torch
print(torch)
from torch import nn
#from torch.nn.Sequential import Sequential
import cv2
import numpy as np
from torch.utils.serialization import load_lua 
import torchvision.utils as vutils

def tensor2image(src):
    out = src.copy() * 255
    out = out.transpose((1, 2, 0)).astype(np.uint8)
    out = cv2.cvtColor(out, cv2.COLOR_RGB2BGR)
    return out

def image2tensor(src):
    out = src.copy()
    out = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
    out = out.transpose((2,0,1)).astype(np.float64) / 255
    return out

image_path = 'img/zebra.png'
mask_path = 'img/inpaint_mask.png'
model_path = 'models/completionnet_places2.t7'
gpu = torch.cuda.is_available()

data = load_lua(model_path, long_size=8)
model = data.model
model.evaluate()

image = cv2.imread(image_path)
mask = cv2.imread(mask_path)
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY) / 255
mask[mask <= 0.5] = 0.0
mask[mask > 0.5] = 1.0

I = torch.from_numpy(image2tensor(image)).float()
M = torch.from_numpy(mask).float()
M = M.view(1, M.size(0), M.size(1))
assert I.size(1) == M.size(1) and I.size(2) == M.size(2)

for i in range(3):
    I[i, :, :] = I[i, :, :] - data.mean[i]

M3 = torch.cat((M, M, M), 0)
im = I * (M3*(-1)+1)
input = torch.cat((im, M), 0)
input = input.view(1, input.size(0), input.size(1), \
 input.size(2)).float()
if gpu:
    model.cuda()
    input = input.cuda()
res = model.forward(input)[0].cpu() # predict

for i in range(3):
    I[i, :, :] = I[i, :, :] + data.mean[i]
out = res.float()*M3.float() + I.float()*(M3*(-1)+1).float()

image[mask == 1] = 255


plt.subplot(2,2,1)
plt.imshow(image, cmap='gray')
plt.title('Image', size=10)

plt.show()