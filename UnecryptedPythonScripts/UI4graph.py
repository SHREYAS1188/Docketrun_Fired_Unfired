from tkinter import *
from tkinter import messagebox,PhotoImage,Canvas
from PIL import Image, ImageTk
import os, cv2, json, logging
from functools import partial
import numpy as np
import cv2
from ultralytics import YOLO
import math
import time
import openpyxl
from PIL import Image, ImageTk
from accentauteSnapseed import apply_accentuate
from Final_grey_1 import run as GreyRun
from Final_grey_1 import run_return_mask_grey as GreyMask
from hsvFilter_darkBlue_dilate_bgRemover1 import run as BlueRun 
from hsvFilter_darkBlue_dilate_bgRemover1 import run_return_mask as BlueMask
import json
from DatabaseSave import save_to_database
import datetime
import pytz
import pandas as pd
import threading
import queue
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

base_path = os.getcwd()


def close_window(event,window):
    if event.char.lower() == 'c':  # Allow closing only when 'C' or 'c' is pressed
        window.destroy()

def disable_close():
    pass  # Do nothing when the "X" button is clicked

class App(Tk):
    def __init__(self):
        super().__init__()
    
        image = Image.open(os.path.join(base_path, "logo.png"))
        photo = ImageTk.PhotoImage(image)

        label = Label(self, image = photo, bg="#222222")
        label.image = photo
        label.grid(columnspan=3, row=0, column=0, ipadx=45, ipady=3)

        Label(
            self, text="Installation of Docketrun App System\nPlease do configure this app if it is first time or you want to re-configure \nand hit start app if you want to start analytics", 
            font=("Arial", 18, "bold"),
            borderwidth=10,
            bg="#222222",
            fg="white"
            ).grid(columnspan=3, row=1, column=0, padx=10) 

        self.configure(background='#222222')
        self.eval('tk::PlaceWindow . center')
        self.resizable(False, False)
        self.title('DOCKETRUN')
        # Disable 'X' button close functionality
        self.protocol("WM_DELETE_WINDOW", disable_close)

        # Bind key press event to close on 'C'
        self.bind("<KeyPress>", lambda event: close_window(event, self))

        Button(self, 
                text="START APP", 
                bg="#515151", 
                fg="white",
                font=("Arial", 12, "bold"),
                command=self.start_app).grid(columnspan=1, row=2, column=0, 
                ipadx=50, pady=10)

        Button(self, 
                text="CONFIGURE APP", 
                bg="#515151", 
                fg="white",
                font=("Arial", 12, "bold"),
                command=self.configure_app).grid(columnspan=1, row=2, column=2, 
                ipadx=30, pady=10)

        try:
            self.wm_iconbitmap(os.path.join(base_path, 'logo.ico'))
        except:
            img = PhotoImage(file=os.path.join(base_path, 'logo.png'))
            self.tk.call('wm', 'iconphoto', self._w, img)

    def configure_app(self):
        self.destroy()

        app = configure_app(1)
        app.mainloop()        

    def start_app(self):
        try:
            self.destroy()

            logging.info("App started")
            
            app = configure_app(0)
            app.mainloop(0)

            logging.info("App exited")
        except Exception as e:
            logging.error(str(e))
            
            
class configure_app(Tk):
    def __init__(self,mode):
        super().__init__()

        rtsp_val = StringVar()

        Label(
            self, text="Please add required camera's RTSP and \nconfigure HSV higher and lower via GUI", 
            font=("Arial", 18, "bold"),
            borderwidth=10,
            bg="#222222",
            fg="white").grid(columnspan=3, row=1, column=0, padx=10)  

        Label(
            self, text="RTSP URL:", 
            font=("Arial", 18, "bold"),
            borderwidth=10,
            bg="#222222",
            fg="white").grid(columnspan=1, row=2, column=0, pady=8)            
            
        Entry(self, textvariable=rtsp_val).grid(columnspan=2, row=2, 
            column=1, padx=25, pady=10, ipadx=75, ipady=10)  

        
        record_func2 = partial(self.configure_stream, rtsp_val,mode)

        if mode == 0:
            configButtonName = "START APPLICATION"
        elif mode == 1:
            configButtonName = "CONFIGURE STREAM"
        ConfigButton = Button(self, 
                text=configButtonName, 
                bg="#515151", 
                fg="white",
                font=("Arial", 12, "bold"),
                command=record_func2)
        ConfigButton.grid(columnspan=1, row=3, column=2, 
                ipadx=30, padx=10, pady=10)
        ConfigButton.grid_forget()
        record_func = partial(self.verify_stream, rtsp_val,ConfigButton)
        
        Button(self, 
                text="VERIFY STREAM", 
                bg="#515151", 
                fg="white",
                font=("Arial", 12, "bold"),
                command=record_func).grid(columnspan=1, row=3, column=0, 
                ipadx=50, padx=10, pady=10)
                
        self.configure(background='#222222')
        self.eval('tk::PlaceWindow . center')
        self.resizable(False, False)
        self.title('DOCKETRUN')
        # Disable 'X' button close functionality
        self.protocol("WM_DELETE_WINDOW", disable_close)

        # Bind key press event to close on 'C'
        self.bind("<KeyPress>", lambda event: close_window(event, self))

        try:
            self.wm_iconbitmap(os.path.join(base_path, 'logo.ico'))
        except:
            img = PhotoImage(file=os.path.join(base_path, 'logo.png'))
            self.tk.call('wm', 'iconphoto', self._w, img)

    def verify_stream(self, stream_url,ConfigButton):
        try:
            if stream_url.get().isdigit():
                stream_url = int(stream_url.get())
            else:
                stream_url = stream_url.get()

            cap = cv2.VideoCapture(stream_url)
            if cap.isOpened():
                _, frame = cap.read()
                cv2.imwrite("image.jpg", frame)

                messagebox.showinfo("DOCKETRUN", "INFO: Successfully fetched the stream, Press 'OK' to configure the stream.")
                ConfigButton.grid(columnspan=1, row=3, column=2, ipadx=30, padx=10, pady=10)
            
            else:
                messagebox.showinfo("DOCKETRUN", "INFO: RTSP, not available/working.")
                

            cap.release()
            
            # Check if config file exists, if not, create it
            if not os.path.exists("info.json"):
                with open("info.json", "w") as f:
                    json.dump({}, f)  # Create an empty JSON file

            with open('info.json', 'r') as f:
                data = json.load(f)

            data["url"] = stream_url

            with open('info.json', 'w') as f:
                json.dump(data, f)

        except Exception as e:
            print(e)
            messagebox.showerror("DOCKETRUN", "ERROR: There's an error while fetching stream, Please enter the valid RTSP.")

    def configure_stream(self,stream_url,mode):
        
        try:
            if stream_url is not None:
        
                if stream_url.get().isdigit():
                        stream_url = int(stream_url.get())
                else:
                        stream_url = stream_url.get()
                
                print('stream url='+str(stream_url))
                
                if (os.path.isfile(stream_url) and stream_url.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))) or stream_url.lower().startswith(('rtsp')):
                    self.destroy()  # Close current window
                    VideoPlayer(stream_url,mode)  # Open video player window
                else:
                    messagebox.showerror("Error", "Invalid file path. Please enter a valid video file or RTSP stream.")
                
        except Exception as e:
            print(e)
            messagebox.showerror("DOCKETRUN", "ERROR: There's an error while fetching stream, Please enter the valid RTSP.")
            
class VideoPlayer(Tk):
    
    def key_handler(self, event):
        # This method is now defined in your class
        if event.char.lower() == 'c':
            if hasattr(self, 'cap') and self.cap.isOpened():
                self.cap.release()
            cv2.destroyAllWindows()
            self.destroy()
            
    def __init__(self, video_path, mode):
        super().__init__()
        self.video_path = video_path
        self.title("DOCKETRUN")
        if mode == 0:
            #self.geometry("970x420")
            self.geometry("1480x490")
        elif mode == 1:
            self.geometry("1400x800")
        self.configure(background='#222222')
        self.frame_detected = False
        self.conf_val = StringVar()
        self.play = True
        self.result_queue = queue.Queue()  # ✅ Initialize result queue
        self.greyPer=0.0
        self.bluePer=0.0
        
        # Flags
        self.video_running = True  # Controls video playback
        self.detected_frame = None  # Stores the first detected frame
        self.detected_image = None  # Stores the first cropped image
        self.accentuated_imagepd = None
        
        # Disable 'X' button close functionality
        self.protocol("WM_DELETE_WINDOW", disable_close)

        # Bind key press event to close on 'C'
        self.bind("<KeyPress>", lambda event: close_window(event, self))
        
        if mode == 1:
            print("play early")
            print(self.play)
        
            # Create Frames
            parent_frame = Frame(self, width=830, height=340, bd=2, relief="ridge")
            parent_frame.grid(row=0, column=0, sticky="nw")
            parent_frame.grid_propagate(False)  # Prevent resizing
            
            video_frame = Frame(parent_frame, bg='#222222', bd=5, relief="ridge")
            video_frame.grid(row=0, column=0, padx=0, pady=0,sticky="w")
            video_frame.grid_propagate(False)

            model_frame = Frame(parent_frame, bg='#222222', bd=5, relief="ridge")
            model_frame.grid(row=0, column=1, padx=0, pady=0,sticky="w")
            model_frame.grid_propagate(False)

            hsv_frame = Frame(self, bg='#222222', bd=5, relief="ridge")
            hsv_frame.grid(row=1, column=0, padx=10, pady=10)
            
            slider_frame = Frame(self, bg='#222222', bd=5, relief="ridge")
            slider_frame.grid(row=1, column=1, columnspan=2, pady=10)
            
            #startapp_frame = Frame(self, bg='#222222', bd=5)
            #startapp_frame.grid(row=2, column=0, columnspan=2, pady=10)

            # Create Label for displaying video
            Label(video_frame, text="Live Video Stream", fg="white", bg="#222222", font=("Arial", 12, "bold")).pack()
            self.video_label = Label(video_frame)
            self.video_label.pack()
            
            # Model Output Display
            Label(model_frame, text="Model Output", fg="white", bg="#222222", font=("Arial", 12, "bold")).pack()
            self.model_label = Label(model_frame)
            self.model_label.pack()

            self.playpause_btn = Button(hsv_frame, text="Pause", command=self.playpause, bg="#515151", fg="white", font=("Arial", 12, "bold"), width=15)
            self.playpause_btn.pack()
            
            self.message_box = Label(hsv_frame, text="Frame Detection In Progress",font=("Arial", 12, "bold"),pady=5)
            self.message_box.pack()
            
            canvas = Canvas(hsv_frame, width=250, height=2, relief="ridge")
            canvas.pack(pady=5)
            canvas.create_line(0, 1, 250, 1, fill="black", width=10)  # Draw a horizontal line
            
            # HSV Output Display
            dummyimage = PhotoImage(file="logo.png", width=800, height=300)
            Label(hsv_frame, text="HSV Output", fg="white", bg="#222222", font=("Arial", 12, "bold")).pack()
            self.hsv_label = Label(hsv_frame, bg="#222222", text="stream still running", font=("Arial", 20), fg="#AAAAAA")
            self.hsv_label.image = dummyimage 
            self.hsv_label.pack()

            # HSV Controls
            self.save_blue_hsv_btn = Button(slider_frame, text="Save Blue HSV", command=lambda: self.save_hsv_values('blue'), bg="#515151", fg="white", font=("Arial", 12, "bold"), width=15)
            self.save_blue_hsv_btn.grid(row=1, column=2, padx=10)
            
            self.load_blue_hsv_btn = Button(slider_frame, text="Previous Blue HSV", command=lambda: self.load_hsv_values('blue'), bg="#515151", fg="white", font=("Arial", 12, "bold"), width=15)
            self.load_blue_hsv_btn.grid(row=2, column=2, padx=10)
            
            self.next_btn = Button(slider_frame, text="Next", command=self.nextButton, bg="#515151", fg="white", font=("Arial", 12, "bold"), width=15)
            self.next_btn.grid(row=4, column=2, padx=10)
            self.next_btn.grid_forget()
            
            self.clear_btn = Button(slider_frame, text="Clear All", command=self.clearAllButton, bg="#515151", fg="white", font=("Arial", 12, "bold"), width=15)
            self.clear_btn.grid(row=5, column=2, padx=10)
            
            self.save_conf_btn = Button(slider_frame, text="Save Confidence", command=self.saveConfidence, bg="#515151", fg="white", font=("Arial", 12, "bold"), width=15)
            self.save_conf_btn.grid(row=0, column=2, padx=10)
            
            self.save_white_hsv_btn = Button(slider_frame, text="Save White HSV", command=lambda: self.save_hsv_values('white'), bg="#515151", fg="white", font=("Arial", 12, "bold"), width=15)
            self.save_white_hsv_btn.grid(row=1, column=2, padx=10)
            self.save_white_hsv_btn.grid_forget()
            
            self.load_white_hsv_btn = Button(slider_frame, text="Previous White HSV", command=lambda: self.load_hsv_values('white'), bg="#515151", fg="white", font=("Arial", 12, "bold"), width=15)
            self.load_white_hsv_btn.grid(row=2, column=2, padx=10)
            self.load_white_hsv_btn.grid_forget()
            
            # HSV Sliders
            Label(slider_frame, text="Hmin", fg="white", bg="#222222").grid(row=1, column=0)
            self.hmin_slider = Scale(slider_frame, from_=0, to=179, orient=HORIZONTAL)
            self.hmin_slider.grid(row=1, column=1,ipadx=50, ipady=2)
            
            Label(slider_frame, text="Smin", fg="white", bg="#222222").grid(row=2, column=0)
            self.smin_slider = Scale(slider_frame, from_=0, to=255, orient=HORIZONTAL)
            self.smin_slider.grid(row=2, column=1,ipadx=50, ipady=2)
            
            Label(slider_frame, text="Vmin", fg="white", bg="#222222").grid(row=3, column=0)
            self.vmin_slider = Scale(slider_frame, from_=0, to=255, orient=HORIZONTAL)
            self.vmin_slider.grid(row=3, column=1,ipadx=50, ipady=2)
            
            Label(slider_frame, text="Hmax", fg="white", bg="#222222").grid(row=4, column=0)
            self.hmax_slider = Scale(slider_frame, from_=0, to=179, orient=HORIZONTAL)
            self.hmax_slider.set(179)
            self.hmax_slider.grid(row=4, column=1,ipadx=50, ipady=2)
            
            Label(slider_frame, text="Smax", fg="white", bg="#222222").grid(row=5, column=0)
            self.smax_slider = Scale(slider_frame, from_=0, to=255, orient=HORIZONTAL)
            self.smax_slider.set(255)
            self.smax_slider.grid(row=5, column=1,ipadx=50, ipady=2)
            
            Label(slider_frame, text="Vmax", fg="white", bg="#222222").grid(row=6, column=0)
            self.vmax_slider = Scale(slider_frame, from_=0, to=255, orient=HORIZONTAL)
            self.vmax_slider.set(255)
            self.vmax_slider.grid(row=6, column=1,ipadx=50, ipady=2)
            
            Label(slider_frame, text="Confidence Level", fg="white", bg="#222222").grid(row=0, column=0)
            Entry(slider_frame, textvariable=self.conf_val).grid(row=0, column=1, padx=0, pady=10, ipadx=42, ipady=2)
            
            self.hmin_slider.config(command=lambda value: self.update_hsv(self.accentuated_imagepd))
            self.smin_slider.config(command=lambda value: self.update_hsv(self.accentuated_imagepd))
            self.vmin_slider.config(command=lambda value: self.update_hsv(self.accentuated_imagepd))
            self.hmax_slider.config(command=lambda value: self.update_hsv(self.accentuated_imagepd))
            self.smax_slider.config(command=lambda value: self.update_hsv(self.accentuated_imagepd))
            self.vmax_slider.config(command=lambda value: self.update_hsv(self.accentuated_imagepd))
            
            self.startapp_button=Button(slider_frame, 
                text="START APP", 
                bg="#515151", 
                fg="white",
                font=("Arial", 12, "bold"),
                command=self.start_app,
                width=15)
            self.startapp_button.grid(row=6, column=2, padx=10)
            self.startapp_button.grid_forget()
            

            # Open video file
            self.cap = cv2.VideoCapture(self.video_path)
            last_detection = self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Get time in seconds

            # Play video
            self.play_video(mode,last_detection)
        elif mode == 0:
            print('in mode 0')
            # Create Frames
            #425,330
            video_frame = Frame(self, bg='#222222', bd=5, relief="ridge", width=425, height=420)
            video_frame.grid(row=0, column=0, padx=10, pady=10,sticky="nw")
            video_frame.grid_propagate(False)
            
            output_frame = Frame(self, bg='#222222', bd=5, relief="ridge", width=480, height=420)
            output_frame.grid(row=0, column=1, padx=10, pady=10,sticky="nw")
            output_frame.grid_propagate(False)
            
            self.graph_frame = Frame(self, bg='#222222', bd=5, relief="groove", width=680, height=500)
            self.graph_frame.grid(row=0, column=2, padx=10, pady=10,sticky="nw")
            self.graph_frame.grid_propagate(False)
            
            # Create Label for displaying video
            Label(video_frame, text="Live Video", fg="white", bg="#222222", font=("Arial", 12, "bold")).grid(row=0, column=0)
            self.video_label = Label(video_frame)
            self.video_label.grid(row=1, column=0, padx=5, pady=5)
            
            '''Label(output_frame, text="Previous Output", fg="white", bg="#222222", font=("Arial", 12, "bold")).pack()
            self.previous_output_label = Label(output_frame)
            self.previous_output_label.pack()'''
            
            Label(output_frame, text="Previous Output", fg="white", bg="#222222", font=("Arial", 12, "bold")).grid(row=0, column=0)
            self.out_img_label = Label(output_frame, bg="#222222", text="  stream\n    still\n    running", font=("Arial", 65), fg="#AAAAAA")
            self.out_img_label.grid(row=1, column=0, padx=5, pady=5)
            
            self.labelBluePixel = Label(output_frame, text="Fired Percentage: ", font=("Arial", 12, "bold"))
            self.labelBluePixel.grid(row=2, column=0, padx=5, pady=5,sticky="nw")
            self.labelGreyPixel = Label(output_frame, text="Unfired Percentage: ", font=("Arial", 12, "bold"))
            self.labelGreyPixel.grid(row=3, column=0, padx=5, pady=5,sticky="nw")
            
            self.frame_count = 0
            self.graph_x = []
            self.graph_y = []
            self.graph_y_for_grey = []
            
            # Create matplotlib figure and axes
            self.fig = Figure(figsize=(4.7, 4.5), dpi=100)
            self.ax = self.fig.add_subplot(111)
            (self.line,) = self.ax.plot([], [], marker='o', color='blue', label='Blue %')
            (self.grey_line,) = self.ax.plot([], [], marker='x', color='gray', label='Grey %')
            self.ax.set_title('Fired/Unfired VS Time', fontsize=10)
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel('%')
            self.ax.set_ylim(0, 100)
            self.ax.legend()
            self.ax.grid(True)

            # Embed it in tkinter
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
            self.fig.tight_layout()
            self.fig.subplots_adjust(bottom=0.30)  # Play with the value
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(expand=True, fill='both')
            self.first = True
            self.timeStamp=''
            
            # Open video file
            self.cap = cv2.VideoCapture(self.video_path)
            last_detection = self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Get time in seconds
            self.play_video(mode,last_detection)
        try:
            self.wm_iconbitmap(os.path.join(base_path, 'logo.ico'))
        except:
            img = PhotoImage(file=os.path.join(base_path, 'logo.png'))
            self.tk.call('wm', 'iconphoto', self._w, img)
            
    def playpause(self):
        print("inside play")
        if self.play:
            self.play = False
            self.playpause_btn.config(text="Play")
            self.playpause_btn.pack()
            
            if self.detected_image is not None and self.detected_frame is None:
                    self.video_running = False  # Stop video playback
                    #self.detected_frame = frame  # Store the detected frame
                    self.message_box.config(text=f"Frame Detected")
                    self.frame_detected = True
                    IST = pytz.timezone('Asia/Kolkata')
                    current_time = datetime.datetime.now(IST)
                    fimg_name = str(str(current_time.day) + str(current_time.month) + str(current_time.year) + str(current_time.hour) + str(current_time.minute) + str(current_time.second))
                    self.accentuated_imagepd = apply_accentuate(self.detected_image,fimg_name)
                    #self.update_hsv(apply_accentuate(detected_image,fimg_name))
                    self.update_hsv(self.accentuated_imagepd)
            
        else:
            self.play = True
            self.playpause_btn.config(text="Pause")
            self.playpause_btn.pack()
            self.after(33, self.play_video, 1, None)
            
        print(self.play)
            
    def start_app(self):
        try:
            self.destroy()

            logging.info("App started")
            with open('info.json', 'r') as f:
                data = json.load(f)

            stream_url = data["url"]
            mode = 0
            app = VideoPlayer(stream_url,mode)
            app.mainloop(0)

            logging.info("App exited")
        except Exception as e:
            logging.error(str(e))
    
    
    def saveConfidence(self):
        
        try:
            conf = self.conf_val.get()
            
            if(float(conf) <= 1.00):

            
                # Check if config file exists, if not, create it
                if not os.path.exists("config.json"):
                    with open("config.json", "w") as f:
                        json.dump({}, f)  # Create an empty JSON file
                try:
                    with open("config.json", "r") as f:
                        config = json.load(f)
                except FileNotFoundError:
                    config = {}
                
                config["confidence_value"] = conf
                
                with open("config.json", "w") as f:
                    json.dump(config, f)
                messagebox.showinfo("Success", "confidence saved successfully!")
                
            else:
                messagebox.showinfo("Error","Confidence cannot be greater then 1.00!")
        except Exception:
                messagebox.showerror("Error", "Invalid confidence.")
        
    def clearAllButton(self):
        self.hmin_slider.set(0)
        self.smin_slider.set(0)
        self.vmin_slider.set(0)
        self.hmax_slider.set(179)
        self.smax_slider.set(255)
        self.vmax_slider.set(255)
        
    
    def nextButton(self):
        self.save_blue_hsv_btn.grid_forget()
        self.load_blue_hsv_btn.grid_forget()
        self.save_white_hsv_btn.grid(row=1, column=2, padx=10)
        self.load_white_hsv_btn.grid(row=2, column=2, padx=10)
    
    def update_hsv(self,detected_image):
        
        if self.frame_detected:
            # Get the values from sliders
            h_min = self.hmin_slider.get()
            h_max = self.hmax_slider.get()
            s_min = self.smin_slider.get()
            s_max = self.smax_slider.get()
            v_min = self.vmin_slider.get()
            v_max = self.vmax_slider.get()
            
            image = detected_image
            # Convert to HSV and apply threshold
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            lower_bound = np.array([h_min, s_min, v_min])
            upper_bound = np.array([h_max, s_max, v_max])
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            
            # Step 3: Morphological Operations (Dilation + Erosion)
            kernel = np.ones((5, 5), np.uint8)
            # here we can use white mask then mask 
            dilated_mask = cv2.dilate(mask, kernel, iterations=2)
            eroded_mask = cv2.erode(dilated_mask, kernel, iterations=1)
            
            # Apply mask onto the original image (only keep detected areas)
            masked_image = cv2.bitwise_and(detected_image, detected_image, mask=eroded_mask)
            
            # Convert mask to 3-channel BGR so it can be concatenated with RGB image
            mask_bgr = cv2.cvtColor(eroded_mask, cv2.COLOR_GRAY2BGR)
            
            # Convert OpenCV Image to PIL format for Tkinter
            combined_image = cv2.cvtColor(mask_bgr, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

            # Create a white strip (height same as images, width = 10 pixels)
            separator = np.zeros((combined_image.shape[0], 10, 3), dtype=np.uint8)
            separator[:, :, 2] = 255  # Set the Red channel to 255 (full red)
            
            # Concatenate Original Image and Mask Side by Side
            combined_image = np.hstack((combined_image,separator,masked_image))

            # Convert mask to displayable format
            combined_image = cv2.resize(combined_image, (800, 300))  
            result = Image.fromarray(combined_image)
            result = ImageTk.PhotoImage(result)
            
            # Update the second screen
            self.hsv_label.config(image=result)
            self.hsv_label.image = result
            
        
        
    def post_processing(self, detected_image,fimg_name,labelBluePixel,labelGreyPixel):
        image = apply_accentuate(detected_image,fimg_name)
        #cv2.imwrite(folder+'test_detected_cropped_accentuated.jpeg',image)
        greyPixels = GreyRun(image)
        bluePixels = BlueRun(image)
        
        print('grey='+str(greyPixels))
        print('blue='+str(bluePixels))
        
        self.greyPer = round((((greyPixels*1.0)/(greyPixels+bluePixels))*100.0),2)
        self.bluePer = round((((bluePixels*1.0)/(greyPixels+bluePixels))*100.0),2)
        
        #################################33
        print('writing to file')
        if not os.path.exists('mydata.xlsx'):
            df = pd.DataFrame(columns=["ImagePath", "bluePercentage", "greyPercentage"])  # Create an empty DataFrame
            df.to_excel('mydata.xlsx', index=False)  # Save as an empty Excel file
        wBook = openpyxl.load_workbook('mydata.xlsx')
        sheet = wBook.active
        data = [fimg_name+'.jpg',str(self.bluePer), str(self.greyPer)]
        sheet.append(data)
        wBook.save('mydata.xlsx')
        print('writing to file complete')
        data = {
            "ImagePath":fimg_name+'.jpg' ,
            "bluePercentage":self.bluePer ,
            "greyPercentage":self.greyPer ,
        }
        #save_to_database(data)
        ###################################3
        #self.after(0, lambda: self.labelBluePixel.config(text=f"Blue Percentage: {bluePer:.2f}"))
        #self.after(0, lambda: self.labelGreyPixel.config(text=f"Grey Percentage: {greyPer:.2f}"))
        #self.labelBluePixel.config(text=f"Blue Percentage: {bluePer:.2f}")
        #self.labelGreyPixel.config(text=f"Grey Percentage: {greyPer:.2f}")
        
        

        
        self.result_queue.put((bluePixels, greyPixels,image,detected_image,fimg_name,self.greyPer,self.bluePer))
    
    def process_results(self):
        try:
            bluePer, greyPer = self.result_queue.get_nowait()
            self.labelBluePixel.config(text=f"Fired Percentage: {bluePer:.2f}")
            self.labelGreyPixel.config(text=f"Unfired Percentage: {greyPer:.2f}")
        except queue.Empty:
            pass
        self.after(100, self.process_results)
    
    
    def play_video(self,mode,last_detection):
        print('in play video')
        detection_interval = 40
        confidence_from_config = 0.0
        with open("config.json", "r") as f:
                config = json.load(f)
                confidence_from_config = config.get("confidence_value")
        
        if confidence_from_config is None:
            confidence_from_config = 0.90
            
        print('confidence_from_config')
        print(confidence_from_config)
        i = 0
        model_path="best_small_model_Mar_29.pt"
        model = YOLO(model_path)
        
        if mode == 1:
            if not self.video_running:
                return  # Stop video playback when detection occurs
            
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert color format
            # Call Model Detection
            #detected_image = detect_objects_image(frame)
            #model = YOLO(model_path)
            results = model(frame)
            
            #model = YOLO("bedDetector.pt")
            #results = model(frame)
            
            detected_image = frame
            bounding_boxes = []
            confidence = 0.0
            for r in results:
                if r.boxes:
                    for box in r.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        confidence = float(box.conf[0])  # Confidence score
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        label = f"Conf: {confidence:.2f}"
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 4)
                        detected_image = frame[math.ceil(y1):math.ceil(y2), math.ceil(x1):math.ceil(x2)]
                        #cropped_img = frame[math.ceil(y1):math.ceil(y2), math.ceil(x1):math.ceil(x2)]
                        
            if mode == 0:
                
                current_time = self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Get time in seconds
                
                if (last_detection == 0 or (current_time - last_detection) >= detection_interval) and confidence >= float(confidence_from_config):
                    folder = "test_Video_withModel/"
                    detected_image = cv2.cvtColor(detected_image, cv2.COLOR_BGR2RGB)
                    #cv2.imwrite(folder+'test_detected_cropped.jpeg',detected_image)
                    last_detection = current_time
                    IST = pytz.timezone('Asia/Kolkata')
                    current_time = datetime.datetime.now(IST)
                    fimg_name = str(str(current_time.day) + str(current_time.month) + str(current_time.year) + str(current_time.hour) + str(current_time.minute) + str(current_time.second))
                    self.timeStamp = fimg_name
                    postprocess_thread = threading.Thread(target=self.post_processing, args=(detected_image,fimg_name,self.labelBluePixel,self.labelGreyPixel), daemon=True)
                    postprocess_thread.start()
                    #self.process_results()
                    
                    
                    
                     # Update label fields
                    detected_image = cv2.cvtColor(detected_image, cv2.COLOR_BGR2RGB)
                    detected_image_display0 = cv2.resize(detected_image, (450, 300))
                    disp_image = ImageTk.PhotoImage(Image.fromarray(detected_image_display0))
                    self.out_img_label.config(image=disp_image)
                    self.out_img_label.image = disp_image
                    

                print("blueper")
                print(self.bluePer)
                print("greyPer")
                print(self.greyPer)
                self.labelBluePixel.config(text=f"Fired Percentage: {self.bluePer:.2f}")
                self.labelGreyPixel.config(text=f"Unfired Percentage: {self.greyPer:.2f}")
                
                print('self timeStamp='+str(self.timeStamp))
                print('first='+str(self.first))
                print('self graph_y=')
                print(self.graph_y)
                print('self graph_y_for_grey=')
                print(self.graph_y_for_grey)
                print('self graph_x=')
                print(self.graph_x)
                if len(self.graph_y) == 0:
                    # First time setup — store initial bluePer
                    self.graph_y.append(self.bluePer)
                    self.graph_y_for_grey.append(self.greyPer)
                    self.graph_x.append(0)
                else:
                    
                    if self.bluePer != self.graph_y[len(self.graph_y)-1]:
                        # Append new data
                        self.frame_count += 1
                        self.graph_x.append(int(self.timeStamp))
                        self.graph_y.append(self.bluePer)
                        self.graph_y_for_grey.append(self.greyPer)
                '''    
                print('graph_x='+str(self.graph_x[len(self.graph_x)-1]))
                print('graph_y='+str(self.graph_y[len(self.graph_y)-1]))
                print('graph_y_for_grey='+str(self.graph_y_for_grey[len(self.graph_y_for_grey)-1]))'''
                    
                

                # Keep only the latest N points (optional for scrolling effect)
                max_points = 5
                if len(self.graph_x) > max_points:
                    self.graph_x = self.graph_x[-max_points:]
                    self.graph_y = self.graph_y[-max_points:]
                    self.graph_y_for_grey = self.graph_y_for_grey[-max_points:]

                # Convert string X-values to positions
                x_vals = list(range(len(self.graph_x)))  # [0, 1, ...]
                
                # Update the line data and redraw
                self.line.set_data(x_vals, self.graph_y)
                self.grey_line.set_data(x_vals, self.graph_y_for_grey)

                #self.ax.set_xlim(max(0, self.frame_count - max_points), self.frame_count + 1)
                self.ax.relim()   
                self.ax.autoscale_view(scalex=True, scaley=False)
                # Set string labels on X-axis
                self.ax.set_xticks(x_vals)
                self.ax.set_xticklabels(self.graph_x, rotation=45, ha='right')
                

                self.canvas.draw()

                '''
                # Example plot data
                x = [1, 2, 3, 4, 5]
                y = [10, 20, 25, 30, 40]

                # Create a matplotlib figure
                fig = Figure(figsize=(4.5, 2.0), dpi=100)
                ax = fig.add_subplot(111)
                ax.plot(x, y, marker='o', color='blue', label='Sample Data')
                ax.set_title('Simple Line Plot', fontsize=10)
                ax.set_xlabel('X-axis')
                ax.set_ylabel('Y-axis')
                ax.legend()
                ax.grid(True)

                # Embed the plot inside the graph_frame
                canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(expand=True, fill='both')'''
                    
            if detected_image is None:
                print('got none')
                
            if mode == 1:
                # If an object is detected for the first time, stop video and save frame
                if detected_image is not None and self.detected_frame is None and confidence >= float(confidence_from_config):
                    self.video_running = False  # Stop video playback
                    self.detected_frame = frame  # Store the detected frame
                    self.message_box.config(text=f"Frame Detected")
                    self.frame_detected = True
                    IST = pytz.timezone('Asia/Kolkata')
                    current_time = datetime.datetime.now(IST)
                    fimg_name = str(str(current_time.day) + str(current_time.month) + str(current_time.year) + str(current_time.hour) + str(current_time.minute) + str(current_time.second))
                    self.accentuated_imagepd = apply_accentuate(detected_image,fimg_name)
                    #self.update_hsv(apply_accentuate(detected_image,fimg_name))
                    self.update_hsv(self.accentuated_imagepd)
                    
                    
            # Convert frame to Tkinter-compatible format
            frame1 = cv2.resize(frame, (400, 300))  # Resize for display
            img = ImageTk.PhotoImage(Image.fromarray(frame1))
            self.video_label.img = img  # Prevent garbage collection
            self.video_label.config(image=img)
                
            if detected_image is not None and mode == 0:
                frame = cv2.resize(frame, (400, 300))  # Resize for display
                det_img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.video_label.img = det_img  # Prevent garbage collection
                self.video_label.config(image=det_img)
            
            # Convert detected image to Tkinter-compatible format
            if detected_image is not None:
                detected_image_display = cv2.resize(detected_image, (400, 300))  # Resize for display
                det_img = ImageTk.PhotoImage(Image.fromarray(detected_image_display))
                if mode == 1:
                    self.model_label.img = det_img
                    self.model_label.config(image=det_img)
                    
                self.detected_image = detected_image
            
            print ('back to ui function')
            
            print(self.play)
            print(mode)

            #self.after(33, self.play_video, mode, last_detection)  # ~30 FPS
            # Schedule next frame update
            if mode == 0:
                self.after(16, self.play_video, mode, last_detection)  # ~30 FPS
            elif mode == 1 and self.play == True:
                self.after(16, self.play_video, mode, last_detection)  # ~30 FPS
        else:
            self.cap.release()  # Release video when finished
                
    
    def save_hsv_values(self, color):
        try:
            #hsv_values = list(map(int, self.hsv_input.get().split(',')))
            hsv_values = [
                self.hmin_slider.get(),
                self.smin_slider.get(),
                self.vmin_slider.get(),
                self.hmax_slider.get(),
                self.smax_slider.get(),
                self.vmax_slider.get()
            ]
            if len(hsv_values) != 6:
                raise ValueError
            
            # Check if config file exists, if not, create it
            if not os.path.exists("config.json"):
                with open("config.json", "w") as f:
                    json.dump({}, f)  # Create an empty JSON file
            try:
                with open("config.json", "r") as f:
                    config = json.load(f)
            except FileNotFoundError:
                config = {}
            
            config[color + "_hsv_values"] = hsv_values
            
            with open("config.json", "w") as f:
                json.dump(config, f)
            messagebox.showinfo("Success", f"{color.capitalize()} HSV values saved successfully!")
            self.clearAllButton()
            
            if color == 'blue':
                self.next_btn.grid(row=4, column=2, padx=10)
            elif color == 'white':
                self.startapp_button.grid(row=6, column=2, padx=10)
        except Exception:
            messagebox.showerror("Error", "Invalid HSV values. Enter six numbers separated by commas.")

    def load_hsv_values(self, color):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                hsv_values = config.get(color + "_hsv_values", [])
                if len(hsv_values) == 6:
                    self.hmin_slider.set(hsv_values[0])
                    self.smin_slider.set(hsv_values[1])
                    self.vmin_slider.set(hsv_values[2])
                    self.hmax_slider.set(hsv_values[3])
                    self.smax_slider.set(hsv_values[4])
                    self.vmax_slider.set(hsv_values[5])
                    messagebox.showinfo("Success", f"{color.capitalize()} HSV values loaded successfully!")
                else:
                    messagebox.showerror("Error", f"Invalid {color.capitalize()} HSV values in config file.")
        except Exception:
            messagebox.showerror("Error", f"Failed to load {color.capitalize()} HSV values. Make sure the config file exists and is valid.")



if __name__ == "__main__":
    
    app = App()
    # Disable window close button (overriding the close event)
    app.protocol("WM_DELETE_WINDOW", disable_close)

    # Bind the 'C' key press event to close the window
    #app.bind("<KeyPress>", close_window)
    app.mainloop()
