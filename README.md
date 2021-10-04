# spectral-matched-filter-example
Implementation of the global spectral matched filter (SMF) algorithm to detect a target within a hyperspectral image.

## Files

* **SpectralMatchedFiltering.py** - The main code. Takes in a hyperspectral radiance image and several target reflectance spectra, performs simple atmospheric compensation to bring target spectra into the radiance domain, and performs spectral matched filtering to detect one of those target spectra (green panel) within the scene. The output is an array (r_SMF_green) with the same dimensions as the input image, with different values at each image pixel corresponding to the amount of spectral match between that pixel and the target spectrum. Higher values indicate a higher amount of spectral match (i.e. higher probability that the target is present within that pixel). Also plots the detection image and the probability of detection vs. false alarm for different thresholds.
* **DetectionFalseAlarmStatistics.py** - Contains two functions. The first function, calc_prob_detection_falsealarm, calculates the probabilities of detection and false alarm for different thresholds. The second function, plot_ROC_curve, plots the receiver operating characteristic (ROC) curve from these probabilities. These functions are both called within SpectralMatchedFiltering.py.
* **HSI_data.mat** - A file containing 'hsi', a 62-band radiance image (in array format) of four different-colored panels on top of grass, and 'wav', an array containing the wavelength centers (in nm) of each spectral band.
* **Library_Reflectance.mat** - A file containing arrays of spectral reflectance for different objects in the image.
* **green_target.mat** - A file containing 'green_target', an array with the same spatial dimensions as 'hsi' that holds ground truth information about the green panel in the image. Values of '1' indicate that the green panel is present in that pixel, and values of '0' indicate that the green panel is not present in that pixel.

## Notes

* This code was written to work with a specific image, but could easily be modified to work with other data. To perform SMF, all that is needed is an image that can be read into a numpy array and a corresponding signal spectrum to attempt to detect within the image. To calculate detection and false alarm probabilities, ground truth information for the image is also needed.
* Was implemented using matplotlib version 3.4.3, numpy version 1.19.3, and scipy version 1.7.1
* The equation for SMF was taken from equation 14.79 in *Hyperspectral Remote Sensing* by Michael T. Eismann.
