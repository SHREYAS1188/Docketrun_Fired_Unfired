# Docketrun_Fired_Unfired


Docketrun fired and unfired project 

the project aims at detcting the percentage of the fired and unfired portion on the moving bed 

so when the bed moves the camera is kept in place for the continous feed, the frame is taken into consideration where the bed is present then 
later fed into an ai model which detects the bed position 

the then detected image with the bed is then taken and is cropped where the bed area is detected. then we use different methods like 
0] Accentaute snapseed 
1] background removal 
2] convert to hsv channel and later apply the custom filter
3] morphological operations(dilation +erosion)
4] then apply the final mask 


when the final mask is applied only the blue/grey area  is remaining, so now we need the calculate the pixels which are remaining for both 
the blue and grey area later we need to calculate the ration for the blue: grey ratio


----------------------------------------------------------------------------------------------------

reqirements.txt file

to run the project we need to run only one .sh file main.sh 
using the command in the command prompt

./main.sh

the model .pt is used for the bed detection 


-------------------------------

built with 
python, shell, yolov7, docketrun 
-----------------------------

getting started 

prerequesties

python 


Installation is using the .sh file 



---------------------------------
![Screenshot from 2025-04-17 13-42-19](https://github.com/user-attachments/assets/9d7cbf95-de45-4eb5-8e93-68e5cd592ad3)

so the interface has 2 modes 
mode 1 = start application 
mode 2 =  configure application 


start application 

so the application need to be run in this mode 
so when we get the main window we get the start application button on the left 
when we click on that 
an window opens to get the camera rtsp
give the camera rtsp and click on verify stream button, if the camera rtsp is present then only it gets verified and the start application button is visble 
if the camera rtsp verification does not occur then the start application button is not visible 

 reasons why the verification fails
 1] camera is not active 
 2] internet issue presentin the network 
 
 
so once we click on the start application button a new window opens with 3 frames, one is the live video feed, the previous window, graph for showing 
percentages of blue and grey percentages 

so as the bed moves  in the live frame it is detected and then in the previous feed the image of the caught bed comes and the respective fired and unfired percenteges






configure application 

so in this window we configure various different thing like the blueand grey hsv values the model confidence etc

so in this screen we have different section the top feed where the live video runs and then we have a window adjacent to it which catches the detected
bed by the model

so once the model detctes the bed in the optimum position then that frame is then taken into the HSV output frame here we can set the hsv values for the 
fired and unfired region   
also we can set the model percentage 

their are ___ buttons

clear all = clears all the hsv values 
load blue\grey hsv values = loads the hsv values from the config file
save blue\grey hsv values = saves the hsv values to the config file
save confidence = saves the confidence percentage of the model for the config file
next = this button switches the hsv values from blue to grey 
start app = once all the values are set this button is pressed to start the application where the detection and percentage calculation occurs 


==================================
