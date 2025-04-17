# Docketrun_Fired_Unfired


Docketrun fired and unfired project 

This project aims at detcting the percentage of the fired and unfired region in the moving bed 

Setup: When the bed moves the camera is used for the continous feed, the frame is taken into consideration where the bed is present in the frame then 
later fed into an ai model for detection of the bed.

Detected bed image with the bed is then taken and is cropped to only contain the detcted portion excluding all the other things. This is then post processed using different methods like
1] Accentaute snapseed Function 
2] Background removal 
3] Convert to hsv channel and later apply the custom filter
4] Morphological operations(dilation +erosion)
5] Application of the final mask 


When the final mask is applied only the blue/grey area  is remaining from the detectied image, so now we need to calculate the pixels which are remaining for both 
the blue and grey area later we need to calculate the ratio for the blue:e grey ratio


----------------------------------------------------------------------------------------------------

reqirements.txt file

To run the project we need to run only one .sh file main.sh. Useing this command in the command prompt
```
./docketrunmain.sh
```

the model .pt is used for the bed detection 


-------------------------------

built with 
python, shell, yolov7
-----------------------------

getting started 

prerequesties:
1] python should be installed in the system

Installation of the package is using the .sh file

---------------------------------

Below screenshot shows the interface of the main window which appears when the program is run

![Screenshot from 2025-04-17 13-42-19](https://github.com/user-attachments/assets/9d7cbf95-de45-4eb5-8e93-68e5cd592ad3)

The interface has 2 modes 

mode 1 = start app

mode 2 = configure app

Start App: In this the application runs and starts detecting the fired and unfired percentages of the bed.

Configure App: The configure app is used when we need to set the confidence of the model or set the HSV values for detecting the fired and unfired region

start app

when we click on start app button an input box for the camera rtsp opens up as seen in the below picture 

we need to input the camera rtsp here if the camera is offline or the rtsp is wrong we will get the message as shown in below screenshot  
![Screenshot from 2025-04-17 18-27-37](https://github.com/user-attachments/assets/18359be0-a99e-4d0d-ac53-ed577a898f4e)
![Screenshot from 2025-04-17 13-44-37](https://github.com/user-attachments/assets/543aa8b5-c78e-4c2d-88bb-90d827aedd5d)
![Screenshot from 2025-04-17 13-44-49](https://github.com/user-attachments/assets/3d028113-1e6b-4d70-927d-0e02364dfcf6)


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

![Screenshot from 2025-04-17 13-45-36](https://github.com/user-attachments/assets/d488dbbb-03bc-4387-8a92-32b6182e6f24)





configure application 

so in this window we configure various different thing like the blueand grey hsv values the model confidence etc

so in this screen we have different section the top feed where the live video runs and then we have a window adjacent to it which catches the detected
bed by the model

so once the model detctes the bed in the optimum position then that frame is then taken into the HSV output frame here we can set the hsv values for the 
fired and unfired region   
also we can set the model percentage 
![Screenshot from 2025-04-17 13-47-02](https://github.com/user-attachments/assets/3009fbcb-929a-46b5-8bcf-041789259cf5)
![Screenshot from 2025-04-17 13-48-27](https://github.com/user-attachments/assets/ca8283ff-efca-446a-8724-13633c773480)
![Screenshot from 2025-04-17 13-52-12](https://github.com/user-attachments/assets/9369b66b-dafc-4f5b-b6a2-57d375c44fbc)

their are ___ buttons

clear all = clears all the hsv values 
load blue\grey hsv values = loads the hsv values from the config file
save blue\grey hsv values = saves the hsv values to the config file
save confidence = saves the confidence percentage of the model for the config file
next = this button switches the hsv values from blue to grey 
start app = once all the values are set this button is pressed to start the application where the detection and percentage calculation occurs 


==================================
