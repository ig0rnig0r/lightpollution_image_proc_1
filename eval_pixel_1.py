# general imports
import sys
import os

from PIL import Image
from PIL import ImageStat
import numpy as np

sys_path = sys.path[0]

os.system('clear')

## Some functions from here
# https://stackoverflow.com/questions/3490727/what-are-some-methods-to-analyze-image-brightness-using-python
def brightness_avgPixel( im_file ):
   im = Image.open(im_file).convert('L')
   stat = ImageStat.Stat(im)
   return stat.mean[0]

def brightness_rmsPixel( im_file ):
   im = Image.open(im_file).convert('L')
   stat = ImageStat.Stat(im)
   return stat.rms[0]

def brightness_avgPixelPerceived( im_file ):
   im = Image.open(im_file)
   stat = ImageStat.Stat(im)
   r,g,b = stat.mean
   return np.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))


def brightness_rmsPixelPerceived( im_file ):
   im = Image.open(im_file)
   stat = ImageStat.Stat(im)
   r,g,b = stat.rms
   return np.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))


def brightness_rmsPixel_percent( im_file ): # as above, but relative to max = 255
   im = Image.open(im_file).convert('L')
   stat = ImageStat.Stat(im)
   stat_rms_perc = stat.rms[0] * 100 / 255
   return stat_rms_perc

################################################

#image_file = sys_path+"/old_orig.JPG"
image_file = sys_path+"/old_orig_save.jpg"
#image_file = sys_path+"/old_edit1.JPG"
#image_file = sys_path+"/old_brightTopLeft.jpg"
#image_file = sys_path+"/old_noIFX.jpg"
#image_file = sys_path+"/old_noAtrioTrials.jpg"
#image_file = sys_path+"/old_noHalf.jpg"
#image_file = sys_path+"/old_black.jpg"
#image_file = sys_path+"/old_white.jpg"

# Manual pixel brightness trials
imag = Image.open(image_file)
w = imag.width
h = imag.height

print("Width:" +str(w))
print("Height:" +str(h))

imag = imag.convert('RGB')
X,Y = 0,0
pixelRGB = imag.getpixel((X,Y))
R,G,B = pixelRGB 
brightness = sum([R,G,B])/3 ##0 is dark (black) and 255 is bright (white)
print(brightness)

# Try some functions
avg_pixel_brightness = brightness_avgPixel(image_file)
print("Image brightness via average pixels:" +str(avg_pixel_brightness))

rms_pixel_brightness = brightness_rmsPixel(image_file)
print("Image brightness via rms pixels:" +str(rms_pixel_brightness))

avg_pixel_perceived_brightness = brightness_avgPixelPerceived(image_file)
print("Image brightness via average pixels perceived:" +str(avg_pixel_perceived_brightness))

rms_pixel_perceived_brightness = brightness_rmsPixelPerceived(image_file)
print("Image brightness via rms pixels perceived:" +str(rms_pixel_perceived_brightness))

#rms_pixel_brightness_percent = brightness_rmsPixel_percent(image_file)
#print("Image brightness via rms pixels in %:" +str(rms_pixel_brightness_percent))