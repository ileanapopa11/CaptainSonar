import numpy as numpy
import cv2

img = cv2.imread("graphics\captain.png", cv2.IMREAD_COLOR)
# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

side_size = 23

locations = [["water" for x in range(15)] for y in range(15)]

land_locations = [(2, 1), (2, 2), (6, 1), (8, 2), (8, 3), (12, 1), (12, 2), (13, 1), (1, 6), (1, 7)]
land_locations += [(3, 6), (3, 7), (3, 8), (6, 6), (6, 7), (7, 8), (8, 6), (11, 8), (12, 8), (13, 8)]
land_locations += [(3, 10), (2, 11), (0, 12), (7, 11), (11, 11), (2, 13), (3, 14), (6, 13), (8, 13), (12, 12), (13, 13)]

for loc in land_locations:
    locations[loc[0]][loc[1]] = "land"

for x in range(15):
    for y in range(15):
    	print "locations: ", y, x, locations[y][x]

    	total_pixels_searched = 25
    	land_pixels = 0

    	target_pixel = [x * side_size, y * side_size]
    	corner_x = target_pixel[0] - 2
    	corner_y = target_pixel[1] - 2
    	for pix_x in range(corner_x, corner_x + 5):
    		for pix_y in range(corner_y, corner_y + 5):
    			color = img[pix_x, pix_y]
    			print color
                if color[0] < 100 and color[1] < 100 and color[2] < 100:
    				land_pixels += 1
    	
    	# p/100*25 = land_pixels   p/4 = land_pixels   p = 4*land_pixels
    	if 4 * land_pixels > 30:
    		ans = "land"
    	else:
    		ans = "water"
    	print ans

    	# if ans != locations[y][x]:
    		# print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    	# print land_pixels

# for it in locations:
	# for el in it:
		# print el
	# print ""
