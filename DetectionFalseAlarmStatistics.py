# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 11:07:53 2021

@author: Emily
"""

import numpy as np
import math
import matplotlib.pyplot as plt

def calc_prob_detection_falsealarm(detection_image, roi_image):
    """
    Calculate the probability of detection and false alarm at each detection threshold
    """
    # Find image dimensions
    y_size = np.size(detection_image,0)
    x_size = np.size(detection_image,1)
    
    # Calculate number of pixels that target is present in (from roi image)
    target_pixels = np.sum(roi_image)
    
    # Calculate range of values in detection image
    min_value = math.floor(np.min(detection_image))
    max_value = math.ceil(np.max(detection_image))
    
    # Initialize detection and false alarm tables
    P_detection = np.empty(max_value-min_value+1)
    P_fa = np.empty(max_value-min_value+1)
    
    # Calculate detection and false alarm for each value in detection image
    for thresh in range(min_value,max_value+1):
        above_thresh = np.zeros((y_size,x_size))
        for y in range(0,y_size):
            for x in range(0,x_size):
                if detection_image[y,x] > thresh:
                    above_thresh[y,x] = 1
        # Probability of detection and false alarm at that threshold
        P_detection[thresh-min_value] = (np.sum(roi_image + above_thresh > 1))/target_pixels
        P_fa[thresh-min_value] = (np.sum(roi_image - above_thresh < 0))/(y_size*x_size - target_pixels)
    
    return P_detection, P_fa

def plot_ROC_curve(P_detection, P_fa, option = 'semilog'):
    """
    
    Parameters
    ----------
    P_detection : TYPE
        DESCRIPTION.
    P_fa : TYPE
        DESCRIPTION.
    option : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    if option == 'semilog':
        plt.plot(np.log(P_fa[P_fa != 0]),P_detection[P_fa != 0])
        plt.xlabel('log(P(False Alarm))')
    else:
        plt.plot(P_fa,P_detection)
        plt.xlabel('P(False Alarm)')
    plt.ylabel('P(Detection)')
    plt.show()
    return
    