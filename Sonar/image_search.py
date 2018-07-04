import numpy as np
import cv2
import math

def make_denoised_mask(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # AQUA/TEAL
    lower_blue = np.array([70,50,50])
    upper_blue = np.array([110,255,255])
    mask_aqua_teal = cv2.inRange(img_hsv, lower_blue, upper_blue)

    # BLUE/NAVY
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    mask_blue_navy = cv2.inRange(img_hsv, lower_blue, upper_blue)

    mask = mask_aqua_teal + mask_blue_navy

    # set my output img to zero everywhere except my mask
    result_img = img.copy()
    result_img[np.where(mask==0)] = 0

    # Denoising image
    denoised_img = cv2.fastNlMeansDenoisingColored(result_img, None, 50, 50)
    
    # denoised_img = result_img
    
    # cv2.imshow("Display window", denoised_img)
    # cv2.waitKey(0)

    return denoised_img

    
def get_locations_list(map_path):
    water_img = make_denoised_mask(map_path)

    side_size = 23
    map_size = 327
    
    locations = [["water" for x in range(15)] for y in range(15)]

    for x in range(15):
            for y in range(15):
                target_pixel = [x * side_size, y * side_size]
                corner_x = target_pixel[0] - 9
                corner_y = target_pixel[1] - 9
                
                corner_x_down = corner_x + side_size
                corner_y_down = corner_y + side_size
                
                black_pixels = 0
                plus_x = side_size
                plus_y = side_size
                
                if corner_x < 0 and y not in [0, 14]: # first row
                    corner_x = 0
                    plus_x = side_size // 2
                    
                elif corner_y < 0 and x not in [0, 14]: # first column
                    corner_y = 0
                    plus_y = side_size // 2
                    
                elif corner_y_down > map_size and x not in [0, 14]: # last column
                    plus_y = side_size // 2
                    
                elif corner_x_down > map_size and y not in [0, 14]: # last row
                    plus_x = side_size // 2
                
                elif x == 0 and y == 0: # corner up-left
                    corner_x = 0
                    corner_y = 0
                    plus_x = side_size // 2
                    plus_y = side_size // 2
                    
                elif x == 0 and y == 14: # corner up-right
                    corner_x = 0
                    plus_x = side_size // 2
                    plus_y = side_size // 2
                    
                elif x == 14 and y == 14: # corner down-right
                    plus_x = side_size // 2
                    plus_y = side_size // 2
                    
                elif x == 14 and y == 0: # corner down-left
                    corner_y = 0
                    plus_x = side_size // 2
                    plus_y = side_size // 2
                    
                total_pixels = plus_x * plus_y
                
                for pix_x in range(corner_x, corner_x + plus_x):
                    for pix_y in range(corner_y, corner_y + plus_y):
                            color = water_img[pix_x, pix_y]
                            if color[0] in range(5) and color[1] in range(5) and color[2] in range(5): # color is black (RGB) [0 0 0]
                                black_pixels += 1
                               
                land_percent = black_pixels * 100 / total_pixels
                
                if land_percent > 50:
                    locations[y][x] = "land"
               
    return locations

print "IMAGE SEARCH"
# get_locations_list("graphics\mareaNeagra.jpg")
