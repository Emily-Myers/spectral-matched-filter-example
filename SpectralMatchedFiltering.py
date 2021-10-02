# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 12:15:13 2021

@author: Emily
"""

# Imports
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import DetectionFalseAlarmStatistics

# Paths and variables
image_data_path = 'HSI_data.mat'
reflectance_library_path = 'Library_Reflectance.mat'
green_target_roi_path = 'green_target.mat'
HSI_data = loadmat(image_data_path)
reflectance_library = loadmat(reflectance_library_path)
green_target_roi = loadmat(green_target_roi_path)

"""
Load hyperspectral image
"""
image = HSI_data.get('hsi')
band_number = np.size(image,0)
y_size = np.size(image,1)
x_size = np.size(image,2)
# 62-band radiance image of four panels (black, green, tan, and aluminum) on top of grass
# dimensions: (1) spectral bands (62), (2) y (400 pixels), (3) x (512 pixels)
# pixel center of black panel: 185, 80
# pixel center of aluminum panel: 185, 280
# pixel center of green panel: 184, 151

"""
Load reflectance library
"""
black_panel_reflectance = reflectance_library.get('black')
aluminum_panel_reflectance = reflectance_library.get('aluminum')
green_panel_reflectance = reflectance_library.get('green')
# ground-measured reflectance for some of the panels

"""
Load ground truth target location data
"""
# Load green panel roi image
# a value of 0 indicates that the panel is not present in that pixel
# a value of 1 indicates that the panel is present in that pixel
green_target_roi_image = green_target_roi.get('green_target')

"""
Perform Empirical Line Method (ELM) to convert green panel reflectance to radiance
"""
# Perform linear regression between bright object (aluminum panel) and dark object
# (black panel) in scene to obtain a relation between radiance and reflectance.
# This is necessary because the signal we are looking for (green panel) is
# currently given in reflectance units while the image is in radiance units.
# We need them to match in order to perform SMF.

# Initialize variables
L1 = image[:,185-1,280-1]   # aluminum panel radiance
L2 = image[:,185-1,80-1]    # black panel radiance
p1 = aluminum_panel_reflectance[0,:] # aluminum panel reflectance
p2 = black_panel_reflectance[0,:]    # black panel reflectance
green = green_panel_reflectance[0,:]    # green panel reflectance

# Perform regression
a = np.divide((L2-L1),(p2-p1))
b = np.divide((np.multiply(L1,p2) - np.multiply(L2,p1)),(p2-p1))

# Convert green panel reflectance to radiance
L_green = np.multiply(a,green) + b

"""
Calculate necessary quantities for Spectral Matched Filtering algorithm
"""
# Calculate mean per-band radiance for image
mean = np.mean(image.reshape(band_number,y_size*x_size),1)

# Subtract mean image radiance from reshaped image
W = image.reshape(band_number,y_size*x_size)
for i in range(0,y_size*x_size):
    W[:,i] = W[:,i]-mean

# Calculate covariance and inverse covariance for W
C = np.matmul(W,np.transpose(W))/(y_size*x_size)  # Covariance matrix
C_inv = np.linalg.inv(C)                    # Inverse of covariance matrix

# Subtract mean image radiance from green radiance signal
S_green = L_green-mean
S_green = S_green.reshape(band_number,1)

"""
Perform Spectral Matched Filtering (SMF) to look for green panel in scene
"""
# For each pixel, the spectral matched filter is calculated using the formula
# transpose(signal-mean) * C_inv * (image-mean)
r_SMF_green = np.empty(y_size*x_size)

for i in range(0,y_size*x_size):
    # multiply the first two terms
    m1 = np.matmul(np.transpose(S_green),C_inv)
    # multiply by the third term
    m2 = np.matmul(m1,W[:,i])
    # populate r_SMF_green array
    r_SMF_green[i] = m2

# Reshape r_SMF_green to match original image dimensions
r_SMF_green = r_SMF_green.reshape(y_size,x_size)

# Plot the results (brighter means higher spectral match)
plt.imshow(r_SMF_green)
plt.show()

"""
Generate detection and false alarm statistics
"""
P_detection, P_fa = DetectionFalseAlarmStatistics.calc_prob_detection_falsealarm(r_SMF_green, green_target_roi_image)

"""
PLot Receiver Operating Characteristics (ROC) Curve
"""
DetectionFalseAlarmStatistics.plot_ROC_curve(P_detection, P_fa)