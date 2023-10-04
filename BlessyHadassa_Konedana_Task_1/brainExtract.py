from asyncio import tasks
import cv2
from more_itertools import sample
import numpy as np
import os
import shutil


def assignment1(path = os.getcwd()):
	#making a check to see if the folders exist, if yes - delete then make a directory for 'slices' and boundaries
	slice_check = os.path.isdir(os.path.join(os.getcwd(),"Slices"))
	if slice_check:
		shutil.rmtree(os.path.join(os.getcwd(),"Slices"))
	os.mkdir(os.path.join(os.getcwd(),"Slices"))
	bound_check = os.path.isdir(os.path.join(os.getcwd(),"Boundaries"))
	if bound_check:
		shutil.rmtree(os.path.join(os.getcwd(),"Boundaries"))
	os.mkdir(os.path.join(os.getcwd(),"Boundaries"))
	#check in test data for the word thresh,then get the file
	for file in os.listdir(os.path.join(path,"testPatient")):
		# From the list selecting only image names ending having thresh
		if("thresh" in file ):
			tasks(os.path.join(path,"testPatient"),file)





def tasks(file_loc,image_name):
	#making image respective folders in slices and boundaries
	checkfld = os.path.isdir(os.path.join(os.path.join(os.getcwd(),"Slices"),image_name.split('.')[0]))
	if not checkfld:
		os.mkdir(os.path.join(os.path.join(os.getcwd(),"Slices"),image_name.split('.')[0]))
	checkfld = os.path.isdir(os.path.join(os.path.join(os.getcwd(),"Boundaries"),image_name.split('.')[0]))
	if not checkfld:
		os.mkdir(os.path.join(os.path.join(os.getcwd(),"Boundaries"),image_name.split('.')[0]))
	#reading image as sample and grayscaling it and saving it as sample_g
	sample = cv2.imread(os.path.join(file_loc,image_name))
	sample_g=cv2.cvtColor(sample,cv2.COLOR_BGR2GRAY)
	#finding R by the range of white-ness
	r_range=cv2.inRange(sample_g,255,255)
	#saving the boundaries and contours
	c = cv2.Canny(r_range, 255, 255)
	(find_find_contours1r, _) = cv2.findContours(c.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	#initializing the variable to save 
	j = 1
	x1, y1, w1, h1 = cv2.boundingRect(find_find_contours1r[len(find_find_contours1r)-1])
	for i in range(1,len(find_find_contours1r)):
		x2, y2, w1, h1 = cv2.boundingRect(find_find_contours1r[len(find_find_contours1r)-i-1])
		if(y2 != y1 and abs(y2-y1) > w1):
			break

	for i in range(1,len(find_find_contours1r)):
		x3, y3, w1, h1 = cv2.boundingRect(find_find_contours1r[len(find_find_contours1r)-i-1])
		if(x3 != x1 and abs(x3-x1) > h1):
			break
	X, Y, w1, h1 = cv2.boundingRect(find_find_contours1r[-1])
	width_slice_image =  x3-x1
	height_sclice_image = y2 - y1
	#iterating through findcountours
	for i in range(0,len(find_find_contours1r)):
		c = find_find_contours1r[len(find_find_contours1r) - i-1]
		x1, y1, w1, h1 = cv2.boundingRect(c)
		x2 = x1+width_slice_image-w1
		y2 = y1-height_sclice_image
		x1 = x1 + w1+w1
		y1 = y1 + h1
		if(x1 < X or y2 < Y):
			continue
		#slicing the new image
		new_img = sample[y2:y1, x1:x2]	
		gray_new_img=cv2.cvtColor(new_img,cv2.COLOR_BGR2GRAY)
		r_range=cv2.inRange(gray_new_img,0,25)
		c = cv2.Canny(r_range, 50, 100)
		(find_contours1, _) = cv2.findContours(c.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		#checking for blank images, if there neglecting other wise saving 
		if(len(find_contours1)):
			new_img = sample[y2:y1, x1:x2]
			cv2.imwrite(os.path.join(os.path.join(os.getcwd(),"Slices"),image_name.split('.')[0])+'/'+str(j) +'.png', new_img)
			cv2.drawContours(new_img, find_contours1, -1, (127,127,255), 1)
			cv2.imwrite(os.path.join(os.path.join(os.getcwd(),"Boundaries"),image_name.split('.')[0])+'/'+str(j) +'.png', new_img)

		else:
			continue
		j+=1




