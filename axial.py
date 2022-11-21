"""
AXIAL IMAGE SCAN LOADER
Read the axial dicom scan and generate the coronal and sagital slices.
11/2022
by: Aranca2504
"""

import pydicom as pydicom
import matplotlib.pyplot as plt
import os
import numpy as np

#READ AND SAVE THE SCAN
fpath = '/Users/macbook/Desktop/dcm_scan_loader/prostate_axial'
# load the DICOM files
files_id = next(os.walk(fpath))[2]
print(files_id)
files = []
path_file = 'prostate_axial/' + files_id[0]
for fname in files_id:
    r,extension = os.path.splitext(fname)
    if extension == '.dcm':
        print("loading: {}".format(fname))
        files.append(pydicom.dcmread('prostate_axial/' + fname))
print("file count: {}".format(len(files)))

#SKIP FILES WITH NO SLICELOCATION
slices = []
skipcount = 0
for f in files:
    if hasattr(f, 'SliceLocation'):
        slices.append(f)
    else:
        skipcount = skipcount + 1
print("skipcount: {}".format(skipcount))
print("slices count: {}".format(len(slices)))

# ensure they are in the correct order
slices = sorted(slices, key=lambda s: s.SliceLocation)

# pixel aspect ratio (y/x), assuming all slices are the same
ps = slices[0].PixelSpacing
ss = slices[0].SliceThickness
ax_aspect = ps[1]/ps[0]
sag_aspect = ps[1]/ss
cor_aspect = ss/ps[0]

# create 3D array
img_shape = list(slices[0].pixel_array.shape)
img_shape.append(len(slices))
img3d = np.zeros(img_shape)
print('MATRIX SIZE: {}'.format(img3d.shape))

# FILL 3d ARRAY WITH THE SLICES[]
for i, s in enumerate(slices):
    img2d = s.pixel_array
    img3d[:, :, i] = img2d

# PRINT THE MIDDLE IMAGE OF EACH SCAN, ORTHOGONAL VIEWS.
i,j,k = np.array(img_shape)//2
a1_ax = plt.subplot(2, 2, 1)
plt.imshow(img3d[:, :, k],'gray')
a1_ax.set_aspect(ax_aspect)
a1_ax.set_title('AXIAL')

a2_sag = plt.subplot(2, 2, 2)
plt.imshow(img3d[:, j, :],'gray')
a2_sag.set_aspect(sag_aspect)
a2_sag.set_title('SAGITAL')

a3_cor = plt.subplot(2, 2, 3)
plt.imshow(img3d[i, :, :].T,'gray')
a3_cor.set_aspect(cor_aspect)
a3_cor.set_title('CORONAL')

plt.show()