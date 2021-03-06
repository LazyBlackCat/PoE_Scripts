from PIL import ImageGrab, Image
from collections import OrderedDict
import d3dshot
import argparse
import keyboard
import pyautogui
import numpy
import os
import time
import random
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug',action="store_true", help='Enable debug mode', )
# parser.add_argument('-v', '--vulcan',action="store_true", help='Changes read values to the corresponding Vulcan equivalents', )
args = parser.parse_args()

DEBUG = True if args.debug else False
HIGHLIGHT_RGB_SUM = 530

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

BASE_DURATION = .025
VARIANCE = .025
SCREENSHOT_DELAY = .15
MATCH_THRESHOLD = 40
SOCKET_RGB = [163, 152, 120,]
SOCKET_RGB_THRESHOLD = 150

# Init possible pieces of gear for recipe
gear_dict = OrderedDict()
gear_dict["armour"] = {
						"bases": ["energy shield", "armour", "evasion"],
					  	"dimension": "2x3",
					  	"count": 0,
					  	"wanted_count": 2,
					}

gear_dict["bows"] = {
						"bases": ["bow"],
					  	"dimension": "2x3",
					  	"count": 0,
					  	"wanted_count": 2,
					}
					
gear_dict["weapons"] = {
						"bases": ["wand", "dagger", "sword", "cutlass", "club", "tenderizer"],
					  	"dimension": "1x3",
					  	"count": 0,
					  	"wanted_count": 4,
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

set_1 = []
set_2 = []
consumed_cells = []

set_1_count = 0
set_2_count = 0
no_set_2 = False

if DEBUG:
	screenshot = d3dshot.create().screenshot()
	og_sc = numpy.array(screenshot)
	print (og_sc[162][69])

# go through each basetype and search for unid rare varients
for basetype in gear_dict:
	gear_dict[basetype]["count"] = 0
	if set_1_count > set_2_count:
		no_set_2 = True
	for base in gear_dict[basetype]["bases"]:
		if keyboard.is_pressed('esc'):
			sys.exit(0)
		# 2 weapons or 1 bow
		if gear_dict["bows"]["count"] == 2:
			gear_dict["weapons"]["count"] = 4
		elif gear_dict["bows"]["count"] == 1:
			gear_dict["weapons"]["count"] = 2
		# short circuit
		if gear_dict[basetype]["count"] == gear_dict[basetype]["wanted_count"]:
			continue
		if no_set_2:
			if gear_dict[basetype]["count"] == gear_dict[basetype]["wanted_count"]/2:
				continue

		if DEBUG:
			print(base)

		# text field filter
		pyautogui.PAUSE = random.random() * VARIANCE + BASE_DURATION
		pyautogui.moveTo(CLEAR_LOCATION[0], CLEAR_LOCATION[1])
		pyautogui.click()
		pyautogui.moveTo(QUERY_LOCATION[0], QUERY_LOCATION[1])
		pyautogui.click()
		pyautogui.write(QUERY % base, random.random()*(.005) + .0075)
		# take screenshot with filter
		time.sleep(SCREENSHOT_DELAY)
		screenshot = d3dshot.create().screenshot()
		screenshot_array = numpy.array(screenshot)
		# check corners for highlight color
		for cell_loc in cell_map:
			if keyboard.is_pressed('esc'):
				sys.exit(0)
			if cell_loc in consumed_cells:
				continue
			if gear_dict[basetype]["count"] == gear_dict[basetype]["wanted_count"]:
				continue
			start_x_loc = int(cell_loc.split("_")[0])
			start_y_loc = int(cell_loc.split("_")[1])
			valid = True
			for x in range(0, 2):
				if abs(numpy.sum(screenshot_array[start_y_loc][start_x_loc - x]) - HIGHLIGHT_RGB_SUM) > MATCH_THRESHOLD:
					if DEBUG:
						og_sc[start_y_loc][start_x_loc - x] = [255, 150, 150]
					valid = False
					break
			for y in range(0, 2):
				if abs(numpy.sum(screenshot_array[start_y_loc + y][start_x_loc]) - HIGHLIGHT_RGB_SUM) > MATCH_THRESHOLD:
					if DEBUG:
						og_sc[start_y_loc + y][start_x_loc] = [255, 150, 150]
					valid = False
					break

			if valid:
				if DEBUG:
					print (start_x_loc, start_y_loc, screenshot_array[start_y_loc][start_x_loc])
					print ("VALID 1")

				# Check if there is a nxm highlighted rectangle at that location
				if gear_dict[basetype]["dimension"] in cell_map[cell_loc]:
					end_x_loc = int(cell_map[cell_loc][gear_dict[basetype]["dimension"]][0])
					end_y_loc = int(cell_map[cell_loc][gear_dict[basetype]["dimension"]][1])
					valid = True
					for x in range(0, 2):
						if abs(numpy.sum(screenshot_array[end_y_loc][end_x_loc + x]) - HIGHLIGHT_RGB_SUM) > MATCH_THRESHOLD:
							if DEBUG:
								og_sc[end_y_loc][end_x_loc + x] = [255, 150, 150]
							valid = False
							break
					for y in range(0, 2):
						if abs(numpy.sum(screenshot_array[end_y_loc - y][end_x_loc]) - HIGHLIGHT_RGB_SUM) > MATCH_THRESHOLD:
							if DEBUG:
								og_sc[end_y_loc - y][end_x_loc] = [255, 150, 150]
							valid = False
							break
					if valid:
						if DEBUG:
							print ("VALID 2")
						# Check six sockets
						if basetype == "armour":
							six_socket = False
							abs_red = 255
							abs_green = 255
							abs_blue = 255
							for offset in SIX_SOCKET_OFFSETS_ARMOUR:
								test_pixel_x = start_x_loc + offset[0]
								test_pixel_y = start_y_loc + offset[1]
								r,g,b = screenshot_array[test_pixel_y][test_pixel_x]
								abs_red = abs(r-SOCKET_RGB[0])
								abs_green = abs(g-SOCKET_RGB[1])
								abs_blue = abs(b-SOCKET_RGB[2])
								if not (abs_red + abs_green + abs_blue < SOCKET_RGB_THRESHOLD):
									six_socket = False
						else:
							six_socket = False
						# Add the gear location to the apporpriate set
						if not six_socket:
							if gear_dict[basetype]["count"] < (gear_dict[basetype]["wanted_count"]/2):
								set_1.append([start_x_loc-10, start_y_loc+10])
								if basetype == "bows":
									set_1_count += 1
								set_1_count += 1
								if DEBUG:
									print ("Added to set 1")
							else:
								set_2.append([start_x_loc-10, start_y_loc+10])
								if basetype == "bows":
									set_2_count += 1
								set_2_count += 1
								if DEBUG:
									print ("Added to set 2")
							gear_dict[basetype]["count"] += 1
							if DEBUG:
								for y in range(0, end_y_loc - start_y_loc):
									og_sc[start_y_loc + y][start_x_loc] = [150, 255, 150]
									og_sc[start_y_loc + y][end_x_loc] = [150, 255, 150]

								for x in range(0, start_x_loc - end_x_loc):
									og_sc[start_y_loc][start_x_loc - x] = [150, 255, 150]
									og_sc[end_y_loc][start_x_loc - x] = [150, 255, 150]
						consumed_cells.append(cell_loc)

		if base == "wand":
			if gear_dict[basetype]["count"] == 1:
				gear_dict[basetype]["count"] -= 1
				set_1_count -= 1
				set_1 = set_1[:-1]
			if gear_dict[basetype]["count"] == 3:
				gear_dict[basetype]["count"] -= 1
				set_2_count -= 1
				set_2 = set_2[:-1]

	# if missing all of any gear piece short circuit
	if (gear_dict[basetype]["count"] < gear_dict[basetype]["wanted_count"]/2) and not basetype == "bows":
		break
if DEBUG:
	print (set_1_count)
	print (set_2_count)

# Clear selection if found set
if set_1_count == 10:
	pyautogui.moveTo(CLEAR_LOCATION[0], CLEAR_LOCATION[1])
	pyautogui.click()

if set_1_count == 10 and set_2_count == 10:
	combined = [None]*(len(set_1)+len(set_2))
	combined[::2] = set_1
	combined[1::2] = set_2
	pyautogui.keyDown('ctrl')
	for loc in combined:
		if keyboard.is_pressed('esc'):
			sys.exit(0)
		pyautogui.PAUSE = random.random() * VARIANCE + BASE_DURATION
		pyautogui.moveTo(loc[0], loc[1])
		pyautogui.click()
	pyautogui.keyUp('ctrl')

# run set 1 if its complete
elif set_1_count == 10:
	pyautogui.keyDown('ctrl')
	for loc in set_1:
		if keyboard.is_pressed('esc'):
			sys.exit(0)
		pyautogui.PAUSE = random.random() * VARIANCE + BASE_DURATION
		pyautogui.moveTo(loc[0], loc[1])
		pyautogui.click()
	pyautogui.keyUp('ctrl')

# run set 2 if its complete
elif set_2_count == 10:
	pyautogui.keyDown('ctrl')
	for loc in set_2:
		if keyboard.is_pressed('esc'):
			sys.exit(0)
		pyautogui.PAUSE = random.random() * VARIANCE + BASE_DURATION
		pyautogui.moveTo(loc[0], loc[1])
		pyautogui.click()
	pyautogui.keyUp('ctrl')

if DEBUG:
	Image.fromarray(og_sc).save("Chaos_Recipe_Debug_Map.png")
	print (json.dumps(gear_dict, indent=4))