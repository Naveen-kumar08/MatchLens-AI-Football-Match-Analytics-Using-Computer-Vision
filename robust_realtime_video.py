"""Render a consolidated analytics video from existing track CSVs.
This avoids rerunning detection and is suitable for demonstrations."""
import cv2
import pandas as pd
from collections import defaultdict, deque

INPUT='input.mp4'; TRACKS='outputs/tracks_with_speed.csv'; OUTPUT='outputs/matchlens_professional.mp4'; TRAIL=30

df=pd.read_csv(TRACKS); df=df[df['class']=='player'].copy(); df['frame']=df.frame.astype(int); df['track_id']=df.track_id.astype(int); frames={k:g for k,g in df.groupby('frame')}
cap=cv2.VideoCapture(INPUT)
if not cap.isOpened(): raise RuntimeError('Cannot open input.mp4')
fps=cap.get(cv2.CAP_PROP_FPS) or 25; w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)); out=cv2.VideoWriter(OUTPUT,cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h)); trails=defaultdict(lambda:deque(maxlen=TRAIL)); n=0
while True:
    ok,frame=cap.read()
    if not ok: break
    p=frames.get(n,pd.DataFrame())
    for _,r in p.iterrows():
        tid=int(r.track_id); x1,y1,x2,y2=map(int,[r.x1,r.y1,r.x2,r.y2]); team=r.team; col=(180,180,180) if pd.isna(team) else ((255,100,100) if int(team)==1 else (100,100,255)); trails[tid].append(((x1+x2)//2,y2)); pts=list(trails[tid]);
        for i in range(1,len(pts)): cv2.line(frame,pts[i-1],pts[i],col,2)
        sp=float(r.speed_kmh) if pd.notna(r.speed_kmh) else 0; cv2.rectangle(frame,(x1,y1),(x2,y2),col,2); cv2.putText(frame,f'ID {tid} T{team if pd.notna(team) else "?"} {sp:.1f} km/h',(x1,max(15,y1-6)),cv2.FONT_HERSHEY_SIMPLEX,.42,col,1,cv2.LINE_AA)
    cv2.rectangle(frame,(10,10),(290,115),(0,0,0),-1); cv2.putText(frame,'MATCHLENS AI - PROFESSIONAL VIEW',(20,35),cv2.FONT_HERSHEY_SIMPLEX,.55,(255,255,255),2,cv2.LINE_AA); cv2.putText(frame,f'Frame: {n}',(20,60),cv2.FONT_HERSHEY_SIMPLEX,.45,(220,220,220),1,cv2.LINE_AA); cv2.putText(frame,f'Players: {len(p)}',(20,82),cv2.FONT_HERSHEY_SIMPLEX,.45,(220,220,220),1,cv2.LINE_AA); cv2.putText(frame,'Trails + IDs + Speed',(20,103),cv2.FONT_HERSHEY_SIMPLEX,.45,(220,220,220),1,cv2.LINE_AA)
    out.write(frame); n+=1
cap.release(); out.release(); print(f'Professional analytics video saved: {OUTPUT}')
