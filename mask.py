"""
NIFTI MASK LOADER AND PRINT
Read the MASK nifti image and overlap it to the corresponding DICOM image.
11/2022
by: Aranca2504
"""

import pydicom as pydicom
import matplotlib.pyplot as plt
import os
import nibabel as nb

mask = nb.load('/Users/macbook/Desktop/ej_dcm_prostata/mask.nii')
mask_data = mask.get_fdata()
fpath = '/Users/macbook/Desktop/ej_dcm_prostata/prostate_axial'
# load the DICOM files
files_id = next(os.walk(fpath))[2]
slices = []
path_file = 'prostate_axial/' + files_id[0]
for fname in files_id:
    r,extension = os.path.splitext(fname)
    if extension == '.dcm':
        slices.append(pydicom.dcmread('prostate_axial/' + fname))
slices = sorted(slices, key=lambda s: s.SliceLocation)

# Plot images
plt.figure()
plt.imshow(slices[12].pixel_array, 'gray')
plt.imshow(mask_data[:,:,12], interpolation='none', alpha=0.2)
plt.show()

for i in range(mask.shape[2]):
    #if mask_data[:,:,i].sum() != 0: #show only slices with mask
        plt.figure()
        plt.imshow(slices[i].pixel_array, 'gray')
        plt.imshow(mask_data[:, :, i], alpha=0.2)
        plt.show()