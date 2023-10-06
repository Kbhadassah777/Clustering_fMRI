# Clustering_fMRI

I executed this project as part of data mining subject in my 2nd semester of masters. I would like to put the problem statement and approach in STAR format.

Situation: 
I was given a dataset with image on the resting state functional magnetic resonance imaging (rs-fMRI) scans. I was asked to read each image – find clusters in the image. This project is divided into two parts throughout the semester.
Note: Worked on images ending with thresh

Task:
1.	To slice the images and find the boundary of the brain in each slice.
2.	To find clusters in these images.

Action:
For Task 1: 
1.	Accessing the folder with images and making another folder in there to save the slices.
2.	From the folder selecting the ones ending with thresh
3.	Then working on each image, gray scaling the image
4.	Finding the reference point as it is white.
5.	Using Canny to find the boundaries.
6.	Iterating through the contours and slicing respectively.
7.	Saving the slices and ignoring the blank images



For Task 2:
1.	In Continuation to task 1, used the slices from previous task.
2.	Before sending the slices through the algorithm, making HSV mattress of the image
3.	Then running the slices through DBSCAN.
4.	Counting the clusters for each image and returning the number.
   
Result:
 	The respective files and code is being pushed.

The code and pushes are also aligned with the tasks, make sure to run the test.py file.
Thank you.


Note for recruiters: Although I have done this project in Fall 2022, I didn’t know the importance of having an updated GitHub repo until I attended GHC 2023. I am pushing all my projects at once. I can provide the reports submitted to school if needed. Thank you

