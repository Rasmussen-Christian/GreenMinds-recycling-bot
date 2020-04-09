"""Code for the robt and background widget
"""
import tkinter as tk
import cv2
from PIL import Image, ImageTk


class WebcamWidget:
    """Widget code for bart the robot
    """

    def __init__(self, root):
        self.root = root
        self.camera = cv2.VideoCapture(0)

        # creates the view for the camera
        self.panel_video = tk.Label(self.root)
        self.panel_video.place(relx=.95, rely=0.45, relwidth=.4, relheight=.65, anchor="e")

        self.response_label_title = None
        self.response_label_body = None

        self._should_camera_run = True
        self.start_webcam()

    def _update_camera(self):
        """
            Updates camera with new image from webcam
        """
        if self._should_camera_run:
            _, frame = self.camera.read()
            # flips the image
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)
            self.panel_video.configure(image=frame)
            self.panel_video.image = frame
            self.panel_video.after(1, self._update_camera)

    def get_frame(self):
        """takes a picture from the webcam

        Returns:
            cv2 image -- the frame
        """
        return self.camera.read()[1]

    def start_webcam(self):
        """Turns the webcam on
        """
        self._should_camera_run = True
        self._update_camera()

    def stop_webcam(self):
        """Turns the webcam off
        """
        self._should_camera_run = False

    def add_text_title(self, text, for_time=None):
        """Displays text on top of the webcam with format Title

        Arguments:
            text {string} -- the text to be displayed
            for_time {int} -- the time in milliseconds before the text will be removed
        """
        self.response_label_title = tk.Label(self.panel_video, text=text, bg="#2C6E3E", font=('Avenir', 27), wraplength=500, pady=10)
        self.response_label_title.config(anchor=tk.N)
        self.response_label_title.place(relx=0, rely=0, relwidth=1, relheight=.1, anchor="nw")

        if for_time:
            self.response_label_title.after(for_time, self.response_label_title.destroy)

    def add_text_body(self, text, for_time=None):
        """Displays text on top of the webcam with format body

        Arguments:
            text {string} -- the text to be displayed
            for_time {int} -- the time in milliseconds before the text will be removed
        """
        self.response_label_body = tk.Label(self.panel_video, text=text, bg="#2C6E3E", font=('Avenir', 20), wraplength=500, justify=tk.LEFT, pady=20)
        self.response_label_body.config(anchor=tk.N)
        self.response_label_body.place(relx=0, rely=1, relwidth=1, relheight=.15, anchor="sw")

        if for_time:
            self.response_label_body.after(for_time, self.response_label_body.destroy)

    def clear_text(self):
        """Clears the text over the webcam widget
        """
        if self.response_label_title:
            self.response_label_title.destroy()
        if self.response_label_body:
            self.response_label_body.destroy()