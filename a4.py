# assignment 4 starter code
# by Abe Davis

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
    return scale * np.log10(np.maximum(E_x2, np.array([1e-6]*3)) / variance) # prevent log(0) errors

def align(im1, im2, maxOffset=20):
    '''takes two images and a maxOffset. Returns the y, x offset that best aligns im2 to im1.'''
    mindiff = im1.shape[0] * im1.shape[1] * 3
    for y in xrange(-maxOffset, maxOffset + 1):
        for x in xrange(-maxOffset, maxOffset + 1):
            shift = np.roll(np.roll(im2, x, axis=1), y, axis=0)
            differences = np.sum((im1[maxOffset:-maxOffset, maxOffset:-maxOffset] - shift[maxOffset:-maxOffset, maxOffset:-maxOffset])**2)
            if differences < mindiff:
                mindiff, xmin, ymin = (differences, x, y)
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
    out = np.zeros(raw.shape)
    height, width = (raw.shape[0], raw.shape[1])
    for y, x in imIter(out):
        if y > 0 and y < height-1 and x > 0 and x < width-1:
            if (x + y + offset) % 2 == 0:
                out[y, x] = raw[y, x]
            else:
                out[y, x] = 0.25 * (raw[y+1, x] + raw[y-1, x] + raw[y, x+1] + raw[y, x-1])
    return out

def basicRorB(raw, offsetY, offsetX):
    '''takes a raw image and an offset in x and y. Returns the interpolated red or blue channel of your image using the basic technique.'''
    out = np.zeros(raw.shape)
    height, width = (raw.shape[0], raw.shape[1])
    for y, x in imIter(out):
        if y > 0 and y < height-1 and x > 0 and x < width-1:
            if (x + offsetX) % 2 == 0:
                if (y + offsetY) % 2 == 0:
                    out[y, x] = raw[y, x]
                else:
                    out[y, x] = 0.5 * (raw[y-1, x] + raw[y+1, x])
            else:
                if (y + offsetY) % 2 == 0:
                    out[y, x] = 0.5 * (raw[y, x-1] + raw[y, x + 1])
                else:
                    out[y, x] = 0.25 * (raw[y+1, x+1] + raw[y-1, x+1] + raw[y+1, x-1] + raw[y-1, x-1])
    return out

def basicDemosaic(raw, offsetGreen=0, offsetRedY=1, offsetRedX=1, offsetBlueY=0, offsetBlueX=0):
    '''takes a raw image and a bunch of offsets. Returns an rgb image computed with our basic techniche.'''
    out = np.zeros(raw.shape + (3,))
    out[:,:,0] = basicRorB(raw, offsetRedY, offsetRedX)
    out[:,:,1] = basicGreen(raw, offsetGreen)
    out[:,:,2] = basicRorB(raw, offsetBlueY, offsetBlueX)
    return out

def edgeBasedGreenDemosaic(raw, offsetGreen=0, offsetRedY=1, offsetRedX=1, offsetBlueY=0, offsetBlueX=0):
    '''same as basicDemosaic except it uses the edge based technique to produce the green channel.'''
    out = np.zeros(raw.shape + (3,))
    out[:,:,0] = basicRorB(raw, offsetRedY, offsetRedX)
    out[:,:,1] = edgeBasedGreen(raw, offsetGreen)
    out[:,:,2] = basicRorB(raw, offsetBlueY, offsetBlueX)
    return out

def edgeBasedGreen(raw, offset=1):
    '''same as basicGreen, but uses the edge based technique.'''
    offset = (offset + 1) % 2
    out = np.zeros(raw.shape)
    height, width = (raw.shape[0], raw.shape[1])
    for y, x in imIter(out):
        if y > 0 and y < height-1 and x > 0 and x < width-1:
            if (x + y + offset) % 2 == 0:
                out[y, x] = raw[y, x]
            else:
                vert = abs(raw[y-1, x] - raw[y+1, x])
                hori = abs(raw[y, x-1] - raw[y, x+1])
                if vert < hori:
                    out[y, x] = 0.5 * (raw[y-1, x] + raw[y+1, x])
                else:
                    out[y, x] = 0.5 * (raw[y, x-1] + raw[y, x+1])
    return out

def greenBasedRorB(raw, green, offsetY, offsetX):
    '''Same as basicRorB but also takes an interpolated green channel and uses this channel to implement the green based technique.'''
    subtracted = np.zeros(green.shape)
    for y, x in imIter(subtracted):
        if (x + offsetX) % 2 == 0 and (y + offsetY) % 2 == 0:
            subtracted[y, x] = max(raw[y, x] - green[y, x], 0)
    return basicRorB(subtracted, offsetY, offsetX) + green

def improvedDemosaic(raw, offsetGreen=0, offsetRedY=1, offsetRedX=1, offsetBlueY=0, offsetBlueX=0):
    out = np.zeros(raw.shape + (3,))
    green = edgeBasedGreen(raw, offsetGreen)
    out[:,:,0] = greenBasedRorB(raw, green, offsetRedY, offsetRedX)
    out[:,:,1] = green
    out[:,:,2] = greenBasedRorB(raw, green, offsetBlueY, offsetBlueX)
    return out

def split(raw):
    '''splits one of Sergei's images into a 3-channel image with height that is floor(height_of_raw/3.0). Returns the 3-channel image.'''
    height = int(raw.shape[0] / 3.0)
    out = np.zeros((height, raw.shape[1], 3))
    for i in xrange(3):
        out[:,:,2-i] = raw[i * height : (i+1) * height]
    return out

def sergeiRGB(raw, alignTo=1):
    '''Splits the raw image, then aligns two of the channels to the third. Returns the aligned color image.'''
    channels = split(raw)
    im1 = channels[:,:,alignTo]
    for i in xrange(3):
        if i != alignTo:
            im2 = channels[:,:,i]
            yshift, xshift = align(im1, im2)
            channels[:,:,i] = np.roll(np.roll(im2, xshift, axis=1), yshift, axis=0)
    return channels

def imIter(im):
    for y in xrange(im.shape[0]):
        for x in xrange(im.shape[1]):
            yield y, x
