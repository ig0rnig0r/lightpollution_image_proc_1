# general imports
import sys
import os

from PIL import Image, ImageChops, ImageStat
import numpy as np

sys_path = sys.path[0]

os.system('clear')

## Maybe the goto function from
# https://stackoverflow.com/questions/3490727/what-are-some-methods-to-analyze-image-brightness-using-python
def brightness_rmsPixel( im_file ):
   im = Image.open(im_file).convert('L') # convert to grayscale
   stat = ImageStat.Stat(im) # RMS (root-mean-square) for each band in the image
   return stat.rms[0]

################################################
# Reference
reference_image_file = sys_path+"/source_images/old_orig.JPG"
#reference_image_file = sys_path+"/old_orig_save.jpg"
reference_rms_pixel_brightness = brightness_rmsPixel(reference_image_file)
print("Reference image brightness via rms pixels is " +str(reference_rms_pixel_brightness))

################################################
# No Streetlights
noStreetL_image_file = sys_path+"/source_images/old_noStreetLight1.jpg"
noStreetL_rms_pixel_brightness = brightness_rmsPixel(noStreetL_image_file)
print("No Streetlights: Image brightness via rms pixels is " +str(noStreetL_rms_pixel_brightness))

noStreetL_brightness_relToRef_perc = noStreetL_rms_pixel_brightness * 100 / reference_rms_pixel_brightness # how much less brightness ([%])
print("No Streetlights image has " +str(np.round(100-noStreetL_brightness_relToRef_perc,2)) +"% less brightness")

# Find the difference between the two images
img_ref = Image.open(reference_image_file)
img_compare = Image.open(noStreetL_image_file)
diff = ImageChops.difference(img_ref, img_compare)
diff.save(sys_path+"/delta_noStreetlights.jpg","JPEG")

# Create a gif to check picture in daylight vs night (to identify objects)
image_list = [img_ref,img_compare]
image_list[0].save(sys_path+"/ref_vs_noStreetlights.gif",save_all=True, append_images=image_list[1:],duration=200,loop=1) # ATTENTION: in IrfanView the upper right corner doesn't show animation!?

################################################
# No Advertisments
noAds_image_file = sys_path+"/source_images/old_noAtrioTrials.jpg"
noAds_rms_pixel_brightness = brightness_rmsPixel(noAds_image_file)
print("No Advertisments: Image brightness via rms pixels is " +str(noAds_rms_pixel_brightness))

noAds_brightness_relToRef_perc = noAds_rms_pixel_brightness * 100 / reference_rms_pixel_brightness # how much less brightness ([%])
print("No Advertisments image has " +str(np.round(100-noAds_brightness_relToRef_perc,2)) +"% less brightness")

# Find the difference between the two images
img_compare = Image.open(noAds_image_file)
diff = ImageChops.difference(img_ref, img_compare)
diff.save(sys_path+"/delta_noAds.jpg","JPEG")

# Create a gif to check picture in daylight vs night (to identify objects)
image_list = [img_ref,img_compare]
image_list[0].save(sys_path+"/ref_vs_noAds.gif",save_all=True, append_images=image_list[1:],duration=200,loop=1) # ATTENTION: in IrfanView the upper right corner doesn't show animation!?

################################################
# No Industry / Privates
noInd_image_file = sys_path+"/source_images/old_noIFX.jpg"
noInd_rms_pixel_brightness = brightness_rmsPixel(noInd_image_file)
print("No Industry/Privates: Image brightness via rms pixels is " +str(noInd_rms_pixel_brightness))

noInd_brightness_relToRef_perc = noInd_rms_pixel_brightness * 100 / reference_rms_pixel_brightness # how much less brightness ([%])
print("No Industry/Privates image has " +str(np.round(100-noInd_brightness_relToRef_perc,2)) +"% less brightness")

# Find the difference between the two images
img_compare = Image.open(noInd_image_file)
diff = ImageChops.difference(img_ref, img_compare)
diff.save(sys_path+"/delta_noInd.jpg","JPEG")

# Create a gif to check picture in daylight vs night (to identify objects)
image_list = [img_ref,img_compare]
image_list[0].save(sys_path+"/ref_vs_noInd.gif",save_all=True, append_images=image_list[1:],duration=200,loop=1) # ATTENTION: in IrfanView the upper right corner doesn't show animation!?

################################################
# Comparison: Who has more impact? (quantitative evaluation)
result_dict_perc = {"NoStreetlights":noStreetL_brightness_relToRef_perc,"NoAdvertisments":noAds_brightness_relToRef_perc,"NoIndustryPrivates":noInd_brightness_relToRef_perc}
maxReduction = min(result_dict_perc, key=result_dict_perc.get) # who has the minimum value, hence the biggest reduction
minReduction = max(result_dict_perc, key=result_dict_perc.get) # who has the maximum value, hence the smallest reduction

print("Biggest reduction seen with "+maxReduction+" by "+str(np.round(100-result_dict_perc.get(maxReduction),2))+"%")
print("Smallest reduction seen with "+minReduction+" by "+str(np.round(100-result_dict_perc.get(minReduction),2))+"%")

# TODO: 
# Stack all individual "image classes" and crosscheck the delta to the original (did we account for something double/not at all ?)
# https://www.geeksforgeeks.org/overlay-an-image-on-another-image-in-python/

