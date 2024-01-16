# general imports
import sys
import os

from PIL import Image, ImageChops, ImageStat, ImageOps
import numpy as np

sys_path = sys.path[0]

os.system('clear')
sys.stdout = open(sys_path+"/output.txt", 'w')

## Maybe the goto function from
# https://stackoverflow.com/questions/3490727/what-are-some-methods-to-analyze-image-brightness-using-python
def brightness_rmsPixel(im):
   im = im.convert('L')
   stat = ImageStat.Stat(im) # RMS (root-mean-square) for each band in the image
   return stat.rms[0]

def find_saturated_pixel(im):
   rr, gg, bb = im.split()
   im_gray = im.convert('L') # this is the color space we do our rmx pixel evaluation in

   # Slow loop to paint the fully saturated pixels red (better visibility)
   bright_counter = 0
   sat_counter = 0
   pixels = im_gray.load()
   for i in range(im.size[0]): # for every pixel:
      for j in range(im.size[1]):
         if pixels[i,j] > 255*0.90:
            bright_counter = bright_counter + 1 # to know how many pixels are bright (90% of maximum)
            if pixels[i,j] == 255: # if saturated change color to red
               rr.putpixel((i,j),(255))
               gg.putpixel((i,j),(0))
               bb.putpixel((i,j),(0))
               sat_counter = sat_counter + 1 # to know how many pixels are actually saturated
   bright_counter_perc = bright_counter*100/(im.size[0]*im.size[1])
   print("In this image " +str(bright_counter)+ " pixels are 90% of maximum brightness ("+str(bright_counter_perc)+"%)")
   sat_counter_perc = sat_counter*100/(im.size[0]*im.size[1])
   print("In this image " +str(sat_counter)+ " pixels are fully saturated ("+str(sat_counter_perc)+"%)")
   bright_sat_counter_perc = sat_counter*100/bright_counter
   print(str(bright_sat_counter_perc)+"% of bright pixels are saturated")
   out_img = Image.merge("RGB", (rr, gg, bb))
   #out_img.show()
   out_img.save(sys_path+"/result_images/saturated_red.jpg","JPEG") # somehow this looks different to the "show()" from before!?!
   out_img_inv = ImageOps.invert(out_img)
   out_img_inv.save(sys_path+"/result_images/saturated_red_inverted.jpg","JPEG")

   # Fast evaluation of each pixel within an grayscale image in terms of rms brightness and paint them black (bad visibility later on)
   im_offset = Image.eval(im_gray, (lambda x: x + 1)) # remove all potential "completely dark pixel" by a tiny offset
   im_eval = Image.eval(im_offset, (lambda px: 0 if px == 255 else px)) # if a pixel is saturating, set it's brightness to zero to make them visible later on
   im_eval_inv = ImageOps.invert(im_eval)
   im_eval_inv.save(sys_path+"/result_images/saturated_+offset_inverted.jpg","JPEG")
      

################################################
# Reference (original quality imag)
# reference_orig_image_file = sys_path+"/source_images/202310262130_DoP2_lowISO_orig.jpg"
# reference_orig_image_file = sys_path+"/source_images/202312281950_GeKan_pano_hdr_v5_orig.png" # rms pixel brightness check on png not possible
reference_orig_image_file = sys_path+"/source_images/202312281950_GeKan_pano_hdr_v5_reference_export.jpg" # TEMPORARY WORKAROUND until I get the proper original jpg
img_orig_ref = Image.open(reference_orig_image_file)
reference_orig_rms_pixel_brightness = brightness_rmsPixel(img_orig_ref)
print("Reference original image brightness via rms pixels is " +str(reference_orig_rms_pixel_brightness))

# Check for possible brightness saturation
find_saturated_pixel(img_orig_ref)

################################################
# Reference export (to compare with other exports, should be the real reference)
# reference_image_file = sys_path+"/source_images/202310262130_DoP2_lowISO_reference_export.jpg"
reference_image_file = sys_path+"/source_images/202312281950_GeKan_pano_hdr_v5_reference_export.jpg"
img_ref = Image.open(reference_image_file)
reference_rms_pixel_brightness = brightness_rmsPixel(img_ref)
print("Reference exported image brightness via rms pixels is " +str(reference_rms_pixel_brightness))

# Find the difference between the two images -> here the difference should virtually be zero! 
diff = ImageChops.difference(img_ref, img_orig_ref)
diff.save(sys_path+"/result_images/delta_orig_vs_export_reference.jpg","JPEG")
diff_inv = ImageOps.invert(diff)
diff_inv.save(sys_path+"/result_images/delta_orig_vs_export_reference_inverted.jpg","JPEG")

# Check for possible brightness saturation
find_saturated_pixel(img_ref)

################################################
# No Streetlights
# brush_width: 6px (GIMP 2.10)
# noStreetL_image_file = sys_path+"/source_images/202310262130_DoP2_lowISO_noStreetlights_full_1.jpg"
noStreetL_image_file = sys_path+"/source_images/202312281950_GeKan_pano_hdr_v5_noStreetlights.jpg"
img_noStreetL = Image.open(noStreetL_image_file)
noStreetL_rms_pixel_brightness = brightness_rmsPixel(img_noStreetL)
print("No Streetlights: Image brightness via rms pixels is " +str(noStreetL_rms_pixel_brightness))

noStreetL_brightness_relToRef_perc = noStreetL_rms_pixel_brightness * 100 / reference_rms_pixel_brightness # how much less brightness ([%])
print("No Streetlights image has " +str(np.round(100-noStreetL_brightness_relToRef_perc,2)) +"% less brightness")

# Find the difference between the two images
diff = ImageChops.difference(img_ref, img_noStreetL)
diff.save(sys_path+"/result_images/delta_noStreetlights.jpg","JPEG")
diff_inv = ImageOps.invert(diff)
diff_inv.save(sys_path+"/result_images/delta_noStreetlights_inverted.jpg","JPEG")

# # Create a gif to check picture in daylight vs night (to identify objects)
# image_list = [img_ref,img_noStreetL]
# image_list[0].save(sys_path+"/result_images/ref_vs_noStreetlights.gif",save_all=True, append_images=image_list[1:],duration=200,loop=1) # ATTENTION: in IrfanView the upper right corner doesn't show animation!?

################################################
# No Advertisments
# noAds_image_file = sys_path+"/source_images/202310262130_DoP2_lowISO_noAds_full_1.jpg"
noAds_image_file = sys_path+"/source_images/202312281950_GeKan_pano_hdr_v5_noAds.jpg"
img_noAds = Image.open(noAds_image_file)
noAds_rms_pixel_brightness = brightness_rmsPixel(img_noAds)
print("No Advertisments: Image brightness via rms pixels is " +str(noAds_rms_pixel_brightness))

noAds_brightness_relToRef_perc = noAds_rms_pixel_brightness * 100 / reference_rms_pixel_brightness # how much less brightness ([%])
print("No Advertisments image has " +str(np.round(100-noAds_brightness_relToRef_perc,2)) +"% less brightness")

# Find the difference between the two images
diff = ImageChops.difference(img_ref, img_noAds)
diff.save(sys_path+"/result_images/delta_noAds.jpg","JPEG")
diff_inv = ImageOps.invert(diff)
diff_inv.save(sys_path+"/result_images/delta_noAds_inverted.jpg","JPEG")

# # Create a gif to check picture in daylight vs night (to identify objects)
# image_list = [img_ref,img_noAds]
# image_list[0].save(sys_path+"/result_images/ref_vs_noAds.gif",save_all=True, append_images=image_list[1:],duration=200,loop=1) # ATTENTION: in IrfanView the upper right corner doesn't show animation!?

################################################
# No Industry / Privates
# noInd_image_file = sys_path+"/source_images/202310262130_DoP2_lowISO_noIndustry_full_1.jpg"
noInd_image_file = sys_path+"/source_images/202312281950_GeKan_pano_hdr_v5_noIndustry.jpg"
img_noIndustry = Image.open(noInd_image_file)
noInd_rms_pixel_brightness = brightness_rmsPixel(img_noIndustry)
print("No Industry/Trainstation: Image brightness via rms pixels is " +str(noInd_rms_pixel_brightness))

noInd_brightness_relToRef_perc = noInd_rms_pixel_brightness * 100 / reference_rms_pixel_brightness # how much less brightness ([%])
print("No Industry/Trainstation image has " +str(np.round(100-noInd_brightness_relToRef_perc,2)) +"% less brightness")

# Find the difference between the two images
diff = ImageChops.difference(img_ref, img_noIndustry)
diff.save(sys_path+"/result_images/delta_noIndustry.jpg","JPEG")
diff_inv = ImageOps.invert(diff)
diff_inv.save(sys_path+"/result_images/delta_noIndustry_inverted.jpg","JPEG")

# # Create a gif to check picture in daylight vs night (to identify objects)
# image_list = [img_ref,img_compare]
# image_list[0].save(sys_path+"/result_images/ref_vs_noInd.gif",save_all=True, append_images=image_list[1:],duration=200,loop=1) # ATTENTION: in IrfanView the upper right corner doesn't show animation!?

################################################
# Comparison: Who has more impact? (quantitative evaluation)
result_dict_perc = {"NoStreetlights":noStreetL_brightness_relToRef_perc,"NoAdvertisments":noAds_brightness_relToRef_perc,"NoIndustry":noInd_brightness_relToRef_perc}
maxReduction = min(result_dict_perc, key=result_dict_perc.get) # who has the minimum value, hence the biggest reduction
minReduction = max(result_dict_perc, key=result_dict_perc.get) # who has the maximum value, hence the smallest reduction

print("Biggest reduction seen with "+maxReduction+" by "+str(np.round(100-result_dict_perc.get(maxReduction),2))+"%")
print("Smallest reduction seen with "+minReduction+" by "+str(np.round(100-result_dict_perc.get(minReduction),2))+"%")

# # TODO: 
# # Stack all individual "image classes" and crosscheck the delta to the original (did we account for something double/not at all ?)
# # https://www.geeksforgeeks.org/overlay-an-image-on-another-image-in-python/

sys.stdout.close()