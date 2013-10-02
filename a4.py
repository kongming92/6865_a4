#assignment 4 starter code
#by Abe Davis
#
# Student Name: Charles Liu
# MIT Email: cliu2014@mit.edu

import numpy as np

def denoiseSeq(imageList):
    '''Takes a list of images, returns a denoised image'''
    return sum(imageList) / float(len(imageList))

def logSNR(imageList, scale=1.0/20.0):
    '''takes a list of images and a scale. Returns an image showing log10(snr)*scale'''
    shape = imageList[0].shape
    N = len(imageList)
    mean, E_x2 = tuple(map(lambda x: x/float(N), reduce(lambda x, y: (x[0] + y, x[1] + y**2), imageList, (np.zeros(shape), np.zeros(shape)))))
    variance = np.maximum(reduce(lambda x, y: x + (y - mean) ** 2, imageList, np.zeros(shape)) / float(N-1), np.array([1e-6] * 3))
    return scale * np.log10(np.maximum(E_x2, np.array([1e-6]*3)) / variance)

def align(im1, im2, maxOffset=20):
    '''takes two images and a maxOffset. Returns the y, x offset that best aligns im2 to im1.'''
    mindiff = im1.shape[0] * im1.shape[1] * im1.shape[2]
    for y in xrange(-maxOffset, maxOffset + 1):
        for x in xrange(-maxOffset, maxOffset + 1):
            shift = np.roll(np.roll(im2, x, axis=1), y, axis=0)
            differences = np.sum((im1[maxOffset:-maxOffset, maxOffset:-maxOffset] - shift[maxOffset:-maxOffset, maxOffset:-maxOffset])**2)
            if differences < mindiff:
                mindiff = differences
                xmin = x
                ymin = y
    return ymin, xmin

def alignAndDenoise(imageList, maxOffset=20):
    '''takes a list of images and a max offset. Aligns all of the images to the first image in the list, and averages to denoise. Returns the denoised image.'''
    im1 = imageList[0]
    offsetIms = [im1]
    for i in xrange(1, len(imageList)):
        im2 = imageList[i]
        yoff, xoff = align(im1, im2)
        offsetIms.append(np.roll(np.roll(im2, xoff, axis=1), yoff, axis=0))
    return denoiseSeq(offsetIms)

def basicGreen(raw, offset=1):
    '''takes a raw image and an offset. Returns the interpolated green channel of your image using the basic technique.'''
    offset = (offset + 1) % 2
    out = np.zeros((raw.shape[0] - 2, raw.shape[1] - 2))
    for y, x in imIter(out):
        yorig, xorig = (y+1, x+1)
        if (xorig + yorig + offset) % 2 == 0:
            out[y, x] = raw[yorig, xorig]
        else:
            out[y, x] = 0.25 * (raw[yorig+1, xorig] + raw[yorig-1, xorig] + raw[yorig, xorig+1] + raw[yorig, xorig-1])
    return out

def basicRorB(raw, offsetY, offsetX):
    '''takes a raw image and an offset in x and y. Returns the interpolated red or blue channel of your image using the basic technique.'''
    out = np.zeros((raw.shape[0] - 2, raw.shape[1] - 2))
    for y, x in imIter(out):
        yorig, xorig = (y+1, x+1)
        if (xorig + offsetX) % 2 == 0:
            if (yorig + offsetY) % 2 == 0:
                out[y, x] = raw[yorig, xorig]
            else:
                out[y, x] = 0.5 * (raw[yorig-1, xorig] + raw[yorig+1, xorig])
        else:
            if (yorig + offsetY) % 2 == 0:
                out[y, x] = 0.5 * (raw[yorig, xorig-1] + raw[yorig, xorig + 1])
            else:
                out[y, x] = 0.25 * (raw[yorig+1, xorig+1] + raw[yorig-1, xorig+1] + raw[yorig+1, xorig-1] + raw[yorig-1, xorig-1])
    return out

def basicDemosaic(raw, offsetGreen=0, offsetRedY=1, offsetRedX=1, offsetBlueY=0, offsetBlueX=0):
    '''takes a raw image and a bunch of offsets. Returns an rgb image computed with our basic techniche.'''
    out = np.zeros((raw.shape[0] - 2, raw.shape[1] - 2, 3))
    out[:,:,0] = basicRorB(raw, offsetRedY, offsetRedX)
    out[:,:,1] = basicGreen(raw, offsetGreen)
    out[:,:,2] = basicRorB(raw, offsetBlueY, offsetBlueX)
    return out

def edgeBasedGreenDemosaic(raw, offsetGreen=0, offsetRedY=1, offsetRedX=1, offsetBlueY=0, offsetBlueX=0):
    '''same as basicDemosaic except it uses the edge based technique to produce the green channel.'''
    out = np.zeros((raw.shape[0] - 2, raw.shape[1] - 2, 3))
    out[:,:,0] = basicRorB(raw, offsetRedY, offsetRedX)
    out[:,:,1] = edgeBasedGreen(raw, offsetGreen)
    out[:,:,2] = basicRorB(raw, offsetBlueY, offsetBlueX)
    return out

def edgeBasedGreen(raw, offset=1):
    '''same as basicGreen, but uses the edge based technique.'''
    offset = (offset + 1) % 2
    out = np.zeros((raw.shape[0] - 2, raw.shape[1] - 2))
    for y, x in imIter(out):
        yorig, xorig = (y+1, x+1)
        if (xorig + yorig + offset) % 2 == 0:
            out[y, x] = raw[yorig, xorig]
        else:
            vert = abs(raw[yorig-1, xorig] - raw[yorig+1, xorig])
            hori = abs(raw[yorig, xorig-1] - raw[yorig, xorig+1])
            if vert < hori:
                out[y, x] = 0.5 * (raw[yorig-1, xorig] + raw[yorig+1, xorig])
            else:
                out[y, x] = 0.5 * (raw[yorig, xorig-1] + raw[yorig, xorig+1])
    return out

def greenBasedRorB(raw, green, offsetY, offsetX):
    '''Same as basicRorB but also takes an interpolated green channel and uses this channel to implement the green based technique.'''
    subtracted = np.zeros(green.shape)
    for y, x in imIter(subtracted):
        yorig, xorig = (y+1, x+1)
        if (xorig + offsetX) % 2 == 0 and (yorig + offsetY) % 2 == 0:
            subtracted[y, x] = max(raw[yorig, xorig] - green[y, x], 0)
    interpolated = basicRorB(subtracted, (offsetY + 1) % 2, (offsetX + 1) % 2)
    return interpolated + green[1:-1, 1:-1]

def improvedDemosaic(raw, offsetGreen=0, offsetRedY=1, offsetRedX=1, offsetBlueY=0, offsetBlueX=0):
    out = np.zeros((raw.shape[0] - 4, raw.shape[1] - 4, 3))
    green = edgeBasedGreen(raw, offsetGreen)
    out[:,:,0] = greenBasedRorB(raw, green, offsetRedY, offsetRedX)
    out[:,:,1] = green[1:-1, 1:-1]
    out[:,:,2] = greenBasedRorB(raw, green, offsetBlueY, offsetBlueX)
    return out

def split(raw):
    '''splits one of Sergei's images into a 3-channel image with height that is floor(height_of_raw/3.0). Returns the 3-channel image.'''

def sergeiRGB(raw, alignTo=1):
    '''Splits the raw image, then aligns two of the channels to the third. Returns the aligned color image.'''

def imIter(im):
    for y in xrange(im.shape[0]):
        for x in xrange(im.shape[1]):
            yield y, x
