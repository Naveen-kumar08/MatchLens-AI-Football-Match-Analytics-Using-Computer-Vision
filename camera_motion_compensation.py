import cv2
import numpy as np

INPUT='input.mp4'; OUTPUT='outputs/stabilized.mp4'; MAX_CORNERS=300; MIN_TRACKED=30
cap=cv2.VideoCapture(INPUT)
if not cap.isOpened(): raise RuntimeError('Cannot open input.mp4')
fps=cap.get(cv2.CAP_PROP_FPS) or 25; w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)); out=cv2.VideoWriter(OUTPUT,cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h))
ret,prev=cap.read()
if not ret: raise RuntimeError('Cannot read first frame')
prev_gray=cv2.cvtColor(prev,cv2.COLOR_BGR2GRAY); out.write(prev); n=1
while True:
    ret,frame=cap.read()
    if not ret: break
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY); pts=cv2.goodFeaturesToTrack(prev_gray,maxCorners=MAX_CORNERS,qualityLevel=.01,minDistance=8)
    if pts is None or len(pts)<MIN_TRACKED:
        out.write(frame); prev_gray=gray; n+=1; continue
    nxt,status,_=cv2.calcOpticalFlowPyrLK(prev_gray,gray,pts,None)
    a=pts[status==1]; b=nxt[status==1]
    if len(a)<MIN_TRACKED:
        out.write(frame); prev_gray=gray; n+=1; continue
    M,_=cv2.estimateAffinePartial2D(b,a,method=cv2.RANSAC,ransacReprojThreshold=3)
    stabilized=cv2.warpAffine(frame,M,(w,h)) if M is not None else frame
    out.write(stabilized); prev_gray=gray; n+=1
cap.release(); out.release(); print(f'Stabilized video saved: {OUTPUT}')
