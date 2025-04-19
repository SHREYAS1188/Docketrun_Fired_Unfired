# Docketrun_Fired_Unfired


Docketrun fired and unfired project 
Built with 🛠️ 

![](https://cdn-icons-png.flaticon.com/128/10090/10090320.png)
![](https://img.icons8.com/?size=160&id=YX03OUiHE3rz&format=png)
![](https://img.icons8.com/?size=96&id=9MJf0ngDwS8z&format=png)
![](https://opencv.org/wp-content/uploads/2022/05/logo.png)
![](https://avatars.githubusercontent.com/u/26833451?s=48&v=4)


This project aims at detecting the percentage of the fired and unfired region in the moving bed 

Setup: When the bed moves the camera is used for the continous feed, the frame is taken into consideration where the bed is present in the frame then 
later fed into an ai model for detection of the bed.

Detected bed image with the bed is then taken and is cropped to only contain the detcted portion excluding all the other things. This is then post processed using different methods like
1] Accentuate snapseed Function  = This function is used to manage the white saturation and get the neutral image irrespective of the lighting conditions.
2] Background removal = This function is used to remove the unnecessary things from the background. 
3] Convert to HSV channel and later apply the custom filter
4] Morphological operations(dilation +erosion) 
5] Application of the final mask 


When the final mask is applied only the blue/grey area  is remaining from the detected image, so now we need to calculate the pixels which are remaining for both 
the blue and grey area later we need to calculate the ratio for the blue grey ratio

requirements.txt = file contains all the necessary libraries for this project

To run the project we need to run only one .sh file docketrunmain.sh. Using this command in the command prompt
```shell
./docketrunmain.sh
```
model.pt is used for the bed detection the model which is used in this project  is [best_small_model_Mar_29.pt](https://github.com/SHREYAS1188/Docketrun_Fired_Unfired/blob/main/best_small_model_Mar_29.pt "best_small_model_Mar_29.pt")

-----------------------------
Getting started  
Prerequisites:
1] python should be installed in the system
2] Download the project as zip file
Installation of the package is using the docketrunmain.sh file

---------------------------------
Below screenshot shows the interface of the main window which appears when the program is run

![Screenshot from 2025-04-17 13-42-19](https://github.com/user-attachments/assets/9d7cbf95-de45-4eb5-8e93-68e5cd592ad3)

The interface has 2 modes 

Mode 1 = start app

Mode 2 = configure app

Start App: In this the application runs and starts detecting the fired and unfired percentages of the bed.

Configure App: The configure app is used when we need to set the confidence of the model or set the HSV values for detecting the fired and unfired region

Start app

When we click on start app button an input box for the camera rtsp opens up as seen in the below picture. 
We need to input the camera rtsp here. 
If the camera is offline or the rtsp is wrong we will get the message as shown in below screenshot. 
![Screenshot from 2025-04-17 18-27-37](https://github.com/user-attachments/assets/18359be0-a99e-4d0d-ac53-ed577a898f4e)
If the camera rtsp is correct we get a success message as shown below.
![Screenshot from 2025-04-17 13-44-37](https://github.com/user-attachments/assets/543aa8b5-c78e-4c2d-88bb-90d827aedd5d)
Once the stream is verified then the start application button is visible to the right. ![Screenshot from 2025-04-17 13-44-49](https://github.com/user-attachments/assets/3d028113-1e6b-4d70-927d-0e02364dfcf6)

If the camera rtsp is present and only when it gets verified the start application button is visible. If the camera rtsp verification does not occur then the start application button is not visible.
Reasons why the verification fails
 1] Camera is not active 
 2] Internet issue present in the network 

When we click on the start application button a new window opens with 3 frames, one is the live video feed, the previous output, graph for showing 
percentages of fired/unfired vs Time graph. So as the bed moves in the live frame it is detected and then in the previous feed the image of the caught bed comes and the respective fired and unfired percentages.

![Screenshot from 2025-04-17 13-45-36](https://github.com/user-attachments/assets/d488dbbb-03bc-4387-8a92-32b6182e6f24)

Configure application 
This window is used to configure various different thing like the blue and grey HSV values the model confidence etc.
In this screen we have different section the top feed where the live video runs and then we have a window adjacent to it which catches the detected
bed by the model

Once the model detects the bed in the optimum position then that frame is then taken into the HSV output frame here we can set the HSV values for the 
fired and unfired region, also we can set the model percentage here. 
![Screenshot from 2025-04-17 13-47-02](https://github.com/user-attachments/assets/3009fbcb-929a-46b5-8bcf-041789259cf5)
setting the blue hsv
![Screenshot from 2025-04-17 13-48-27](https://github.com/user-attachments/assets/ca8283ff-efca-446a-8724-13633c773480)
setting the grey hsv
![Screenshot from 2025-04-17 13-52-12](https://github.com/user-attachments/assets/9369b66b-dafc-4f5b-b6a2-57d375c44fbc)

Their are 6 buttons in total in this window

Clear all = clears all the hsv values. 
Load blue\grey hsv values = loads the hsv values from the config file
Save blue\grey hsv values = saves the hsv values to the config file
Save confidence = saves the confidence percentage of the model for the config file
Next = this button switches the hsv values button from blue to grey 
Start app = once all the values are set this button is pressed to start the application where the detection and percentage calculation occurs 

------------
happy coding ⌨️
