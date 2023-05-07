import cv2
import csv
import time
import numpy as np
import streamlit as st
from ultralytics import YOLO
from PIL import Image
# from utils import draw_line, writes_area_text, which_area

def draw_line(image, xf1, yf1, xf2, yf2):
    w = image.shape[1]
    h = image.shape[0]
    
    start_point = (int(w*xf1), int(h*yf1) )
    end_point = (int(w*xf2), int(h*yf2) )
    
    cv2.line(image, start_point, end_point, (255,0,0), 4)


def writes_area_text(image, text, xf1, yf1):
    w = image.shape[1]
    h = image.shape[0]
    
    start_point = (int(w*xf1), int(h*yf1) )
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.8
    color = (255,100,100)
    thickness = 2
    
    cv2.putText(image, text, 
                start_point, font, fontScale, (0,0,0), thickness+3)
    
    cv2.putText(image, text, 
                start_point, font, fontScale, color, thickness)



def which_area(image, midx, midy):
    w = image.shape[1]
    h = image.shape[0]
    xf = midx/w
    yf = midy/h
    
    x1, x2, x3, x4, x5, x6 = 0.10, 0.30, 0.35, 0.55, 0.65, 0.85
    
    y1 = 0.0*xf + 0.2 # Top-left line
    y2 = -0.444*xf + 0.294 # Top-middle line
    y3 = 2.75*xf + -0.025 # Left line
    y4 = -1.0*xf + 1.1 # Bottom line
    y5 = 1.0*xf + -0.2 # Middle Line
    
    if xf <= x1:
        if yf <= y1: # Top-left line
            area = "A2"
        else:
            area = "Register"
    elif xf > x1 and xf <= x2:
        if yf <= y2: # Top-middle line
            area = "A2"
        elif yf <= y3: # Left line
            area = "A3"
        else:
            area = "Register"
    elif xf > x2 and xf <= x3:
        if yf <= y2: # Top-middle line
            area = "A2"
        elif yf <= y4: # Bottom line
            area = "A3"
        else:
            area = "Entrance"
    elif xf > x3 and xf <= x4:
        if yf <= y2: # Top-middle line
            area = "A2"
        elif yf <= y5: # Middle Line
            area = "A1"
        elif yf <= y4: # Bottom line
            area = "A3"
        else:
            area = "Entrance"
    elif xf > x4 and xf <= x5:
        if yf <= y5: # Middle Line
            area = "A1"
        elif yf <= y4: # Bottom line
            area = "A3"
        else:
            area = "Entrance"
    elif xf > x5 and xf <= x6:
        if yf <= y4: # Bottom line
            area = "A1"
        else:
            area = "Entrance"
    else:
        area = "Entrance"
    
    return area



def people_counter():
    frame_placeholder = st.empty()

    model = YOLO('yolov8m.pt')

    video_path = "object_detection/data/test.mp4"
    cap = cv2.VideoCapture(video_path)


    def draw_everything():
        draw_line(annotated_frame, 0.00, 0.20, 0.10, 0.20) # Top-left line
        draw_line(annotated_frame, 0.10, 0.25, 0.55, 0.05) # Top-middle line
        draw_line(annotated_frame, 0.10, 0.25, 0.30, 0.80) # Left line
        draw_line(annotated_frame, 0.35, 0.15, 0.65, 0.45) # Middle Line
        draw_line(annotated_frame, 0.30, 0.80, 0.85, 0.25) # Bottom line
        draw_line(annotated_frame, 0.55, 0.05, 0.85, 0.25) # Right line

        writes_area_text(annotated_frame, "Register", 0.01, 0.25)
        writes_area_text(annotated_frame, "Area 2 (A2)", 0.20, 0.05)
        writes_area_text(annotated_frame, "Area 3 (A3)", 0.30, 0.40)
        writes_area_text(annotated_frame, "Entrance", 0.70, 0.80)
        writes_area_text(annotated_frame, "Area 1 (A1)", 0.60, 0.20)


    prev_frame_time = 0
    next_frame_time = 0
    areas_names = ['Register','Entrance','A1','A2','A3']

    f = open('values.csv','w',newline='')
    writer = csv.DictWriter(f,fieldnames=areas_names)
    writer.writeheader()

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            break

        results = model.predict(frame, save=False, imgsz=640, conf=0.35, classes=0)
        annotated_frame = results[0].plot()
        boxes = results[0].boxes
        areas = {'Register':0,'Entrance':0,'A1':0,'A2':0,'A3':0}

        for box in boxes:
            x1,y1,x2,y2 = box.xyxy[0].detach().cpu()
            x, y = x2-(x2-x1)/2, y2-(y2-y1)/2
            cv2.circle(annotated_frame,(int(x),int(y)),3,(255,0,0),3)
            area = which_area(annotated_frame,x,y)
            try:
                areas[area] += 1
            except KeyError:
                print("No such area")
            cv2.putText(annotated_frame, area, (int(x),int(y-10)),cv2.FONT_HERSHEY_SIMPLEX,
                        1,(0,255,0),2,cv2.LINE_AA)
        #frame_placeholder = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        annotated_frame=cv2.resize(annotated_frame, (0,0), fx=0.8, fy=0.8)
        #frame=image_resize(image=frame, width=640)
        frame_placeholder.image(annotated_frame, channels='BGR', use_column_width=True)
        draw_everything()
        # st.video(annotated_frame, channels="BGR")
        # print(areas)
        writer.writerow(areas)

        next_frame_time = time.time()
        try:
            fps = str(round(1/(next_frame_time-prev_frame_time),2))
        except ZeroDivisionError:
            fps = ""
        prev_frame_time = next_frame_time

        cv2.putText(annotated_frame,"FPS: "+fps,(7,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3,cv2.LINE_AA)
        # cv2.imshow("YOLOv8 Inference", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    f.close()
    cap.release()
    cv2.destroyAllWindows()
    
