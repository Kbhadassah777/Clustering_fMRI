# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 20:56:18 2022

@author: BlessyKonedana
"""
import cv2
import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from typing import Sized
from PIL import Image
import math
import random
import time
import csv

Test_Dir=os.getcwd()+"/testPatient"
filePath=Test_Dir
Slices_path=os.getcwd()+"/Slices"
cluster_path=os.getcwd()+"/Cluster"
filename=[]

def check_files(folderName,imageName):
    
    if not os.path.isdir(folderName):
        os.mkdir(folderName)
    if not os.path.isdir(os.path.join(folderName,imageName)):
        os.mkdir(os.path.join(folderName,imageName))

    
def Assignment2():
    if os.path.isdir(Slices_path):
        shutil.rmtree(Slices_path)
    if os.path.isdir(cluster_path):
        shutil.rmtree(cluster_path)
    for FMRI in os.listdir(filePath):
        if 'thresh' in FMRI:
            Task_1(filePath, FMRI)
            

    
def Task_1(filePath,imageName):
    
    check_files(Slices_path,imageName.split('.')[0])
    check_files(cluster_path,imageName.split('.')[0])
    image = cv2.imread(os.path.join(filePath,imageName)) 
    BGR2GRAY=cv2.Canny(cv2.inRange(cv2.cvtColor(image,cv2.COLOR_BGR2GRAY),255,255),255, 255) 
    contours, hierarchy = cv2.findContours(BGR2GRAY.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    i=0
    image = cv2.imread(os.path.join(filePath,imageName))
    x, y, z, h = cv2.boundingRect(contours[len(contours)-1])
    while(i<len(contours)):
        x1, y1, z, h = cv2.boundingRect(contours[len(contours)-i-1])
        if(y1 != y and abs(y1-y) > h):
            break
        i+=1
    i=0    
    while(i<len(contours)):    
        x2, y2, z, h = cv2.boundingRect(contours[len(contours)-i-1])
        if(x2 != x and abs(x2-x) > z):
            break
        i+=1 
    Image_width =  x2 - x 
    Image_height = y1 - y
    
    Image_slicer(contours,imageName,filePath,Image_width,Image_height,x,y)
    
    
def result_generator(x,y,x1,y1,image,imageId,imageName):     
    BGR2GRAY=cv2.Canny(cv2.inRange(cv2.cvtColor(image[y1:y, x:x1],cv2.COLOR_BGR2GRAY),0,25), 50, 100) 
    contour, hierarchy = cv2.findContours(BGR2GRAY, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    if(len(contour)):
        cv2.imwrite(os.path.join(Slices_path,imageName.split('.')[0])+'/'+'sliceID '+str(imageId-2) +'.png', image[y1:y, x:x1])
        imgc,imgk=task2(image[y1:y, x:x1])
        cv2.imwrite(os.path.join(cluster_path,imageName.split('.')[0])+'/'+'sliceID '+str(imageId-2) +'.png', imgc)
        
        header = ['SliceNumber','ClusterCount']
        data=['sliceID '+str(imageId-2),imgk]

           
        pat=os.path.join(cluster_path,imageName.split('.')[0])+'/'+imageName.split('.')[0]+'.csv'
        
        
        with open(pat, 'a', encoding='UTF8',newline ='') as f:
            writer = csv.writer(f)
            if pat not in filename:
                writer.writerow(header)
                filename.append(pat)
            writer.writerow(data)

def Image_slicer(contours,imageName,filePath,Image_width,Image_height,Max_x,Max_y):
    Image_num=0
    image = cv2.imread(os.path.join(filePath,imageName)) 
    for i in range(len(contours)):
        contours_contours = contours[len(contours)-i-1]
        x, y, z, h = cv2.boundingRect(contours_contours)
        x1 = x+Image_width-z
        y1 = y-Image_height
        x +=2 * z
        y +=2 * h
        if not (x < Max_x or y1 < Max_y): 
            result_generator(x,y,x1,y1,image,Image_num,imageName)
            Image_num+= 1
          
def tohsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    m = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        if g >= b:
            h = ((g-b)/m)*60
        else:
            h = ((g-b)/m)*60 + 360
    elif mx == g:
        h = ((b-r)/m)*60 + 120
    elif mx == b:
        h = ((r-g)/m)*60 + 240
    if mx == 0:
        s = 0
    else:
        s = m/mx
    v = mx
    H = h / 2
    S = s * 255.0
    V = v * 255.0
    return H, S, V

    
    
def task2(img):    
    dataset=np.array(img)
    size = dataset.shape
    count = 0
    dataset2=[[0,0]]
    for i in range(size[0]):
        for j in range(size[1]):
            H,S,V = tohsv(dataset[i,j,0],dataset[i,j,1],dataset[i,j,2])
            if(((H>=0 and H<=10) or (H>=156 and H<=180)) and S>=43 and S<=255 and V>=46 and V<=255):
                count = count + 1 
                dataset[i,j,0] = 255
                dataset[i,j,1] = 255
                dataset[i,j,2] = 0
                coords=tuple([i,j])
                dataset2.append(coords)
            elif ((((H>=11 and H<=25)) and S>=43 and S<=255 and V>=46 and V<=255)):
                count = count + 1 
                dataset[i,j,0] = 255
                dataset[i,j,1] = 255
                dataset[i,j,2] = 0
                coords=tuple([i,j])
                dataset2.append(coords)
            elif ((((H>=26 and H<=34)) and S>=43 and S<=255 and V>=46 and V<=255)):
                count = count + 1 
                dataset[i,j,0] = 255
                dataset[i,j,1] = 255
                dataset[i,j,2] = 0
                coords=tuple([i,j])
                dataset2.append(coords)
            elif ((((H>=100 and H<=124)) and S>=43 and S<=255 and V>=46 and V<=255)):
                count = count + 1 
                dataset[i,j,0] = 255
                dataset[i,j,1] = 255
                dataset[i,j,2] = 0
                coords=tuple([i,j])
                dataset2.append(coords)
            else:
                dataset[i,j,0] = 0
                dataset[i,j,1] = 0
                dataset[i,j,2] = 0

    plt.imshow(dataset)
    gray = cv2.cvtColor(dataset, cv2.COLOR_BGR2GRAY)
    db = DBSCAN(eps=2.5,min_samples=5)
    clustering=db.fit(dataset2)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    n_clusters=0

    data_pd = pd.DataFrame(pd.value_counts(labels))
    data_pd.columns=['date']
    for index, row in data_pd.iterrows():
      if(row['date']>135):
        n_clusters+=1
    return [dataset,n_clusters]


            
            
           
               
            
            
            
        
            

        

     
    
    
    
    
    
    
    