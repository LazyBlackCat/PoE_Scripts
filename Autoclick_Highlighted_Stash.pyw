from PIL import ImageGrab, Image
import argparse
import keyboard
import pyautogui
import numpy
import os
import time
import random

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug',action="store_true", help='Enable debug mode', )
args = parser.parse_args()

DEBUG = True if args.debug else False

X_LOCATIONS = [0, 25, 26, 52, 53, 78, 79, 104, 105, 131, 132, 157, 158, 183, 184, 209, 210, 236, 237, 262, 263, 288, 289, 315, 316, 341, 342, 367, 368, 394, 395, 420, 421, 446, 447, 473, 474, 499, 500, 525, 526, 552, 553, 578, 579, 604, 605, 631]
Y_LOCATIONS = [ 0, 25, 26, 51, 52, 78, 79, 104, 105, 130, 131, 157, 158, 183, 184, 209, 210, 236, 237, 262, 263, 288, 289, 315, 316, 341, 342, 367, 368, 394, 395, 420, 421, 446, 447, 473, 474, 499, 500, 525, 526, 551, 552, 578, 579, 604, 605, 630]
CORNERS = {}
CLICK_LOCATIONS = []

X_OFFSET = 17
Y_OFFSET = 162

X_LOCATIONS = [x + X_OFFSET for x in X_LOCATIONS]
Y_LOCATIONS = [y + Y_OFFSET for y in Y_LOCATIONS]

screenshot = ImageGrab.grab()
screenshot_array = numpy.array(screenshot)

for y in range(0, len(Y_LOCATIONS)):
	for x in range(1, len(X_LOCATIONS)):
		if x % 2 == 1 and y % 2 == 0:
			CORNERS[str(Y_LOCATIONS[y]) + "_" + str(X_LOCATIONS[x])] = True

for corner in CORNERS:
	if keyboard.is_pressed('esc'):
		sys.exit(0)
	start_x_loc = int(corner.split("_")[1])
	start_y_loc = int(corner.split("_")[0])
	valid = True
	for x in range(0, 2):
		if (abs(numpy.sum(screenshot_array[start_y_loc][start_x_loc - x]) - 530)) > 40:
			valid = False
			break
	for y in range(0, 2):
		if (abs(numpy.sum(screenshot_array[start_y_loc + y][start_x_loc]) - 530)) > 40:
			valid = False
			break
	if valid:
		CLICK_LOCATIONS.append([start_y_loc+10, start_x_loc-10])

pyautogui.keyDown('ctrl')
for loc in CLICK_LOCATIONS:
	if keyboard.is_pressed('esc'):
		sys.exit(0)
	pyautogui.PAUSE = random.random()*.075 + .025
	pyautogui.moveTo(loc[1], loc[0])
	pyautogui.click()
pyautogui.keyUp('ctrl')