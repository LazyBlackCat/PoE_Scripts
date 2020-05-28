from PIL import ImageGrab, Image
from collections import OrderedDict
import pyautogui
import numpy
import os
import time
import random
import json
import sys

X_LOCATIONS = [0, 25, 26, 52, 53, 78, 79, 104, 105, 131, 132, 157, 158, 183, 184, 209, 210, 236, 237, 262, 263, 288, 289, 315, 316, 341, 342, 367, 368, 394, 395, 420, 421, 446, 447, 473, 474, 499, 500, 525, 526, 552, 553, 578, 579, 604, 605, 631]
Y_LOCATIONS = [ 0, 25, 26, 51, 52, 78, 79, 104, 105, 130, 131, 157, 158, 183, 184, 209, 210, 236, 237, 262, 263, 288, 289, 315, 316, 341, 342, 367, 368, 394, 395, 420, 421, 446, 447, 473, 474, 499, 500, 525, 526, 551, 552, 578, 579, 604, 605, 630]

X_OFFSET = 17
Y_OFFSET = 162

X_LOCATIONS = [x + X_OFFSET for x in X_LOCATIONS]
Y_LOCATIONS = [y + Y_OFFSET for y in Y_LOCATIONS]

QUERY = "%s"
CLEAR_LOCATION = [633, 895]
QUERY_LOCATION = [475, 895]

SIX_SOCKET_OFFSETS_ARMOUR = [[-9, 69]]
SIX_SOCKET_OFFSETS_OTHER =  [[-9, 82]]

BASE_DURATION = .025
VARIANCE = .025
SCREENSHOT_DELAY = .2
HIGHLIGHT_RGB_SUM = 530
MATCH_THRESHOLD = 40
SOCKET_RGB = [163, 152, 120,]
SOCKET_RGB_THRESHOLD = 150

# Init possible pieces of gear for recipe
gear_dict = OrderedDict()
gear_dict["armour"] = {
						"bases": ["energy shield", "armour", "evasion", "physical"],
					  	"dimension": "2x3",
					}
gear_dict["weapon"] = {
						"bases": ["physical"],
					  	"dimension": "2x4",
					}
count = 0
wanted_count = 6

# Cell map has the start / end pixel locations for all dimensions that items can come in
# top key is starting x/y, inner key is dimension, final val is end x/y
cell_map = {}
for x_start in range(1, len(X_LOCATIONS)):
	if x_start % 2 == 0:
		continue
	for y_start in range(0, len(Y_LOCATIONS)):
		if y_start % 2 == 1:
			continue
		map_key = "%s_%s" % (X_LOCATIONS[x_start], Y_LOCATIONS[y_start])
		cell_map[map_key] = {}
		for x in range(0, 4):
			for y in range(0, 4):
				if (x_start + (-x * 2) - 1) >= 0 and (y_start + (y * 2) + 1) < len(Y_LOCATIONS):
					x_range = x + 1
					y_range = y + 1
					end_x = X_LOCATIONS[x_start + (-x * 2) - 1]
					end_y = Y_LOCATIONS[y_start + (y * 2) + 1]
					cell_key = "%sx%s" % (x_range, y_range)
					cell_map[map_key][cell_key] = [end_x, end_y]

screenshot = ImageGrab.grab()
set_1 = []
# go through each basetype and search for unid rare varients
for basetype in gear_dict:
	for base in gear_dict[basetype]["bases"]:
		# short circuit
		if count == wanted_count:
			continue
		# text field filter
		pyautogui.PAUSE = random.random() * VARIANCE + BASE_DURATION
		pyautogui.moveTo(CLEAR_LOCATION[0], CLEAR_LOCATION[1])
		pyautogui.click()
		pyautogui.moveTo(QUERY_LOCATION[0], QUERY_LOCATION[1])
		pyautogui.click()
		pyautogui.write(QUERY % base, random.random()*(.005) + .0075)
		# take screenshot with filter
		time.sleep(SCREENSHOT_DELAY)
		screenshot = ImageGrab.grab()
		screenshot_array = numpy.array(screenshot)
		# check corners for highlight color
		for cell_loc in cell_map:
			if count == wanted_count:
				continue
			start_x_loc = int(cell_loc.split("_")[0])
			start_y_loc = int(cell_loc.split("_")[1])
			valid = True
			for x in range(0, 6):
				if (abs(numpy.sum(screenshot_array[start_y_loc][start_x_loc - x]) - HIGHLIGHT_RGB_SUM)) > MATCH_THRESHOLD:
					valid = False
					break
			for y in range(0, 6):
				if (abs(numpy.sum(screenshot_array[start_y_loc + y][start_x_loc]) - HIGHLIGHT_RGB_SUM)) > MATCH_THRESHOLD:
					valid = False
					break
			if valid:
				# Check if there is a nxm highlighted rectangle at that location
				if gear_dict[basetype]["dimension"] in cell_map[cell_loc]:
					end_x_loc = int(cell_map[cell_loc][gear_dict[basetype]["dimension"]][0])
					end_y_loc = int(cell_map[cell_loc][gear_dict[basetype]["dimension"]][1])
					valid = True
					for x in range(0, 6):
						if (abs(numpy.sum(screenshot_array[end_y_loc][end_x_loc + x]) - HIGHLIGHT_RGB_SUM)) > MATCH_THRESHOLD:
							valid = False
							break
					for y in range(0, 6):
						if (abs(numpy.sum(screenshot_array[end_y_loc - y][end_x_loc]) - HIGHLIGHT_RGB_SUM)) > MATCH_THRESHOLD:
							valid = False
							break
					if valid:
						# Check six sockets
						abs_red = 255
						abs_green = 255
						abs_blue = 255
						six_socket = True
						if basetype == "armour":
							offsets = SIX_SOCKET_OFFSETS_ARMOUR
						else:
							offsets = SIX_SOCKET_OFFSETS_OTHER
						for offset in offsets:
							test_pixel_x = start_x_loc + offset[0]
							test_pixel_y = start_y_loc + offset[1]
							r,g,b = screenshot_array[test_pixel_y][test_pixel_x]
							abs_red = abs(r-SOCKET_RGB[0])
							abs_green = abs(g-SOCKET_RGB[1])
							abs_blue = abs(b-SOCKET_RGB[2])
						if not (abs_red + abs_green + abs_blue < SOCKET_RGB_THRESHOLD):
							six_socket = False

						if six_socket:
							set_1.append([start_x_loc-10, start_y_loc+10])
							count += 1

# run set 1
pyautogui.keyDown('ctrl')
for loc in set_1:
	pyautogui.PAUSE = random.random() * VARIANCE + BASE_DURATION
	pyautogui.moveTo(loc[0], loc[1])
	pyautogui.click()
pyautogui.keyUp('ctrl')