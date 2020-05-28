from PIL import ImageGrab, Image
import pyautogui
import numpy
import os
import time
import random

X_LOCATIONS = [0, 25, 26, 52, 53, 78, 79, 104, 105, 131, 132, 157, 158, 183, 184, 209, 210, 236, 237, 262, 263, 288, 289, 315, 316, 341, 342, 367, 368, 394, 395, 420, 421, 446, 447, 473, 474, 499, 500, 525, 526, 552, 553, 578, 579, 604, 605, 631]
Y_LOCATIONS = [ 0, 25, 26, 51, 52, 78, 79, 104, 105, 130, 131, 157, 158, 183, 184, 209, 210, 236, 237, 262, 263, 288, 289, 315, 316, 341, 342, 367, 368, 394, 395, 420, 421, 446, 447, 473, 474, 499, 500, 525, 526, 551, 552, 578, 579, 604, 605, 630]
CORNERS = {}
CLICK_LOCATIONS = []

screenshot = ImageGrab.grab()
screenshot_array = numpy.array(screenshot)

# starts at 17, 162
# ends at 648, 792
# rgb == 231, 180, 119, sum 530

for y in range(0, len(Y_LOCATIONS)):
	for x in range(0, len(X_LOCATIONS)):
		if x % 2 == 0 and y % 2 == 0:
			CORNERS[str(Y_LOCATIONS[y]) + "_" + str(X_LOCATIONS[x])] = True

y_offset = 0
for y in range(162, 793):
	x_offset = 0
	for x in range(17, 649):
		if str(y_offset) + "_" + str(x_offset) in CORNERS:
			if abs(numpy.sum(screenshot_array[y+1][x]) - 530) < 2:
				if abs(numpy.sum(screenshot_array[y][x+1]) - 530) < 2:
					CLICK_LOCATIONS.append([y+10, x+10])

		x_offset += 1
	y_offset += 1

pyautogui.keyDown('ctrl')
for loc in CLICK_LOCATIONS:
	pyautogui.PAUSE = random.random()*.075 + .025
	pyautogui.moveTo(loc[1], loc[0])
	pyautogui.click()
pyautogui.keyUp('ctrl')