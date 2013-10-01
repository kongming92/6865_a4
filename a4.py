#assignment 4 starter code
#by Abe Davis
#
# Student Name:
# MIT Email:

import numpy as np

def denoiseSeq(imageList):
    '''Takes a list of images, returns a denoised image
    '''


def logSNR(imageList, scale=1.0/20.0):
    '''takes a list of images and a scale. Returns an image showing log10(snr)*scale'''

def align(im1, im2, maxOffset=20):
    '''takes two images and a maxOffset. Returns the y, x offset that best aligns im2 to im1.'''
    return y, x

def alignAndDenoise(imageList, maxOffset=20):
    '''takes a list of images and a max offset. Aligns all of the images to the first image in the list, and averages to denoise. Returns the denoised image.'''


def basicGreen(raw, offset=1):
    '''takes a raw image and an offset. Returns the interpolated green channel of your image using the basic technique.'''
    #out =raw.copy()
    

def basicRorB(raw, offsetY, offsetX):
    '''takes a raw image and an offset in x and y. Returns the interpolated red or blue channel of your image using the basic technique.'''
    #out =raw.copy()

def basicDemosaic(raw, offsetGreen=0, offsetRedY=1, offsetRedX=1, offsetBlueY=0, offsetBlueX=0):
    '''takes a raw image and a bunch of offsets. Returns an rgb image computed with our basic techniche.'''

def edgeBasedGreenDemosaic(raw, offsetGreen=0, offsetRedY=1, offsetRedX=1, offsetBlueY=0, offsetBlueX=0):
    '''same as basicDemosaic except it uses the edge based technique to produce the green channel.'''

def edgeBasedGreen(raw, offset=1):
    '''same as basicGreen, but uses the edge based technique.'''
    #out =raw.copy()
    

def greenBasedRorB(raw, green, offsetY, offsetX):
    '''Same as basicRorB but also takes an interpolated green channel and uses this channel to implement the green based technique.'''
    #out =raw.copy()

def improvedDemosaic(raw, offsetGreen=0, offsetRedY=1, offsetRedX=1, offsetBlueY=0, offsetBlueX=0):
    '''Same as basicDemosaic but uses edgeBasedGreen and greenBasedRorB.'''


def split(raw):
    '''splits one of Sergei's images into a 3-channel image with height that is floor(height_of_raw/3.0). Returns the 3-channel image.'''

def sergeiRGB(raw, alignTo=1):
    '''Splits the raw image, then aligns two of the channels to the third. Returns the aligned color image.'''
