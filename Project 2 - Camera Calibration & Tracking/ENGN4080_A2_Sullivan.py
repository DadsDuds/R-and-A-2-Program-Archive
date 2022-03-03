import numpy as np
import cv2 as cv
import glob
import tkinter as tk
from imageai import Detection

class LiveLeak:
    def __init__(self):
        
        self.mw = tk.Tk()
        self.mw.title("Assignment 2")
        
        self.i_quit = tk.Button(self.mw,
                                text = "Quit",
                                command = self.destroyEVERYTHING)
        
        self.cap = cv.VideoCapture(0)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
        
        self.i_quit.pack()
        
        self.mw.after(10, self.task)
        tk.mainloop()
        
    def task(self):
        self.show_frame()
        self.mw.after(10, self.task)
    
    def show_frame(self):
            
        ret, frame = self.cap.read()
        
        frame, preds = yolo.detectObjectsFromImage(input_image = frame,
                                                   custom_objects = None,
                                                   input_type = "array",
                                                   output_type = "array",
                                                   minimum_percentage_probability = 70,
                                                   display_percentage_probability = False,
                                                   display_object_name = True)
        if ret == True:
            dst = cv.remap(frame, map1, map2, interpolation = cv.INTER_LINEAR, borderMode = cv.BORDER_CONSTANT)
            x,y,w,h = roi
            dst = dst[y:y+h, x:x+w]
            cv.imshow('Frame', dst)
            cv.waitKey(1)
            
        cv.setMouseCallback('Frame', self.onMouse)
    
    def onMouse(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            print('x = %d, y = %d'%(x, y))
                
    def destroyEVERYTHING(self):
        self.mw.destroy()
        cv.destroyAllWindows()
        self.cap.release()

modelpath = "yolo.h5"

yolo = Detection.ObjectDetection()
yolo.setModelTypeAsYOLOv3()
yolo.setModelPath(modelpath)
yolo.loadModel()

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((8*6, 3), np.float32)
objp[:, :2] = (np.mgrid[0:8, 0:6].T.reshape(-1, 2) * 48)

objpoints = []
imgpoints = []

images = glob.glob("*.jpg")

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(gray, (8,6), None)

    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

        cv.drawChessboardCorners(img, (8,6), corners2, ret)
        #cv.imshow('img', img)
        #cv.waitKey(500)

ret, mtx, dist, rvecs, tvecs, = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

img = cv.imread('result.jpg')
h, w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

size = (1920, 1080)

map1, map2 = cv.initUndistortRectifyMap(mtx, dist, np.eye(3), newcameramtx, size, cv.CV_32FC1)

if __name__ == "__main__":
    my_gui = LiveLeak()
