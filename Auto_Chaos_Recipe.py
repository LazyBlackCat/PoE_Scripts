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

QUERY = "rare %s"
CLEAR_LOCATION = [633, 895]
QUERY_LOCATION = [475, 895]

SIX_SOCKET_OFFSETS_ARMOUR = [[-9, 69]]

# Init possible pieces of gear for recipe
gear_dict = OrderedDict()
gear_dict["armour"] = {
						"bases": ["energy shield", "armour", "evasion"],
					  	"dimension": "2x3",
					  	"count": 0,
					  	"wanted_count": 2,
					}

gear_dict["helmet"] = {
						"bases": ["hat", "helmet", "burgonet", "hood", "pelt", "circlet", "cage", "bascinet", "helm", "sallet", "crown", "mask"],
					  	"dimension": "2x2",
					  	"count": 0,
					  	"wanted_count": 2,
					}

gear_dict["gloves"] = {
						"bases": ["gauntlets", "gloves", "mitts"],
					  	"dimension": "2x2",
					  	"count": 0,
					  	"wanted_count": 2,
					}

gear_dict["boots"] = {
						"bases": ["boots", "greaves", "slippers"],
					  	"dimension": "2x2",
					  	"count": 0,
					  	"wanted_count": 2,
					}

gear_dict["weapons"] = {
						"bases": ["wand", "dagger", "sword", "cutlass"],
					  	"dimension": "1x3",
					  	"count": 0,
					  	"wanted_count": 4,
					}

gear_dict["bows"] = {
						"bases": ["bow"],
					  	"dimension": "2x3",
					  	"count": 0,
					  	"wanted_count": 2,
					}

gear_dict["belt"] = {
						"bases": ["belt", "sash"],
					  	"dimension": "2x1",
					  	"count": 0,
					  	"wanted_count": 2,
					}

gear_dict["rings"] = {
						"bases": ["ring"],
					  	"dimension": "1x1",
					  	"count": 0,
					  	"wanted_count": 4,
					}

gear_dict["amulet"] = {
						"bases": ["amulet"],
					  	"dimension": "1x1",
					  	"count": 0,
					  	"wanted_count": 2,
					}

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
		for x in range(0, 3):
			for y in range(0, 3):
				if (x_start + (-x * 2) - 1) >= 0 and (y_start + (y * 2) + 1) < len(Y_LOCATIONS):
					x_range = x + 1
					y_range = y + 1
					end_x = X_LOCATIONS[x_start + (-x * 2) - 1]
					end_y = Y_LOCATIONS[y_start + (y * 2) + 1]
					cell_key = "%sx%s" % (x_range, y_range)
					cell_map[map_key][cell_key] = [end_x, end_y]

with open('cell_mapping.json', 'w') as fp:
    json.dump(cell_map, fp, indent=4)

set_1 = []
set_2 = []

set_1_count = 0
set_2_count = 0


# go through each basetype and search for unid rare varients
for basetype in gear_dict:
	gear_dict[basetype]["count"] = 0
	for base in gear_dict[basetype]["bases"]:
		if gear_dict["weapons"]["count"] > 2:
			gear_dict["bows"]["count"] = 2
		elif gear_dict["weapons"]["count"] > 0:
			gear_dict["bows"]["count"] = 1
		if gear_dict[basetype]["count"] == gear_dict[basetype]["wanted_count"]:
			continue
		pyautogui.PAUSE = random.random()*.025 + .025
		pyautogui.moveTo(CLEAR_LOCATION[0], CLEAR_LOCATION[1])
		pyautogui.click()
		pyautogui.moveTo(QUERY_LOCATION[0], QUERY_LOCATION[1])
		pyautogui.click()
		pyautogui.write(QUERY % base, random.random()*(.005) + .0075)
		time.sleep(.2)
		screenshot = ImageGrab.grab()
		screenshot_array = numpy.array(screenshot)
		for cell_loc in cell_map:
			if gear_dict[basetype]["count"] == gear_dict[basetype]["wanted_count"]:
				continue
			start_x_loc = int(cell_loc.split("_")[0])
			start_y_loc = int(cell_loc.split("_")[1])
			if (abs(numpy.sum(screenshot_array[start_y_loc][start_x_loc]) - 530) < 20
			   and abs(numpy.sum(screenshot_array[start_y_loc + 1][start_x_loc]) - 530) < 20
			   and abs(numpy.sum(screenshot_array[start_y_loc][start_x_loc - 1]) - 530) < 20):
				if gear_dict[basetype]["dimension"] in cell_map[cell_loc]:
					end_x_loc = int(cell_map[cell_loc][gear_dict[basetype]["dimension"]][0])
					end_y_loc = int(cell_map[cell_loc][gear_dict[basetype]["dimension"]][1])
					if (abs(numpy.sum(screenshot_array[end_y_loc][end_x_loc]) - 530) < 20
					   and abs(numpy.sum(screenshot_array[end_y_loc - 1][end_x_loc]) - 530) < 20
					   and abs(numpy.sum(screenshot_array[end_y_loc][end_x_loc + 1]) - 530) < 20):

					# Check six sockets
						six_socket = True
						for offset in SIX_SOCKET_OFFSETS_ARMOUR:
							test_pixel_x = start_x_loc + offset[0]
							test_pixel_y = start_y_loc + offset[1]
							r,g,b = screenshot_array[test_pixel_y][test_pixel_x]
							average_red = abs(r-163)
							average_green = abs(g-152)
							average_blue = abs(b-120)
							if not (average_red + average_green + average_blue < 150):
								six_socket = False

						if not six_socket:
							if gear_dict[basetype]["count"] < (gear_dict[basetype]["wanted_count"]/2):
								set_1.append([start_x_loc-10, start_y_loc+10])
								if basetype == "bows":
									set_1_count += 1
								set_1_count += 1


							else:
								set_2.append([start_x_loc-10, start_y_loc+10])
								if basetype == "bows":
									set_2_count += 1
								set_2_count += 1
							gear_dict[basetype]["count"] += 1
	if (gear_dict[basetype]["count"] == 0):
		break

pyautogui.moveTo(CLEAR_LOCATION[0], CLEAR_LOCATION[1])
pyautogui.click()

if set_1_count == 10:
	pyautogui.keyDown('ctrl')
	for loc in set_1:
		pyautogui.PAUSE = random.random()*.025 + .025
		pyautogui.moveTo(loc[0], loc[1])
		pyautogui.click()
	pyautogui.keyUp('ctrl')

if set_2_count == 10:
	pyautogui.keyDown('ctrl')
	for loc in set_2:
		pyautogui.PAUSE = random.random()*.025 + .025
		pyautogui.moveTo(loc[0], loc[1])
		pyautogui.click()
	pyautogui.keyUp('ctrl')