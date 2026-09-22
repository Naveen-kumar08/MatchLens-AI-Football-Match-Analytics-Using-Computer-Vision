"""Experimental pitch-line calibration helper.

This detects long straight field markings with HoughLinesP and writes candidate
line segments. It is a diagnostic, not a production homography estimator.
"""
import cv2
import json

INPUT='input.mp4'; OUTPUT_IMAGE='outputs/dynamic_calibration_candidates.jpg'; OUTPUT_JSON='outputs/dynamic_calibration_candidates.json'
cap=cv2.VideoCapture(INPUT); cap.set(cv2.CAP_PROP_POS_FRAMES,0); ok,frame=cap.read(); cap.release()
if not ok: raise RuntimeError('Cannot read input.mp4')
gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY); edges=cv2.Canny(gray,50,150); lines=cv2.HoughLinesP(edges,1,3.14159/180,threshold=60,minLineLength=80,maxLineGap=15)
candidates=[]
if lines is not None:
    for l in lines[:,0,:]:
        x1,y1,x2,y2=map(int,l); candidates.append({'x1':x1,'y1':y1,'x2':x2,'y2':y2})
        cv2.line(frame,(x1,y1),(x2,y2),(0,255,255),2)
cv2.imwrite(OUTPUT_IMAGE,frame)
json.dump(candidates,open(OUTPUT_JSON,'w'),indent=2); print(f'Candidates image: {OUTPUT_IMAGE}'); print(f'Candidates JSON: {OUTPUT_JSON}')
