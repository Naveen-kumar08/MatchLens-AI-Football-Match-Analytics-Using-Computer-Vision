import cv2
import pandas as pd
from collections import defaultdict, deque

INPUT_VIDEO='input.mp4'; TRACKS_FILE='outputs/tracks_with_speed.csv'; OUTPUT_VIDEO='outputs/matchlens_trajectory.mp4'; TRAIL_LENGTH=40

df=pd.read_csv(TRACKS_FILE); df=df[df['class']=='player'].copy(); df['frame']=df['frame'].astype(int); df['track_id']=df['track_id'].astype(int)
frames={k:g for k,g in df.groupby('frame')}
cap=cv2.VideoCapture(INPUT_VIDEO)
if not cap.isOpened(): raise RuntimeError('Cannot open input.mp4')
fps=cap.get(cv2.CAP_PROP_FPS) or 25; w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)); total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
out=cv2.VideoWriter(OUTPUT_VIDEO,cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h)); trails=defaultdict(lambda:deque(maxlen=TRAIL_LENGTH))
frame_no=0
while True:
    ok,frame=cap.read()
    if not ok: break
    players=frames.get(frame_no,pd.DataFrame())
    active=set()
    for _,p in players.iterrows():
        tid=int(p.track_id); active.add(tid); x1,y1,x2,y2=map(int,[p.x1,p.y1,p.x2,p.y2]); foot=((x1+x2)//2,y2); trails[tid].append(foot)
        team=p.team; color=(180,180,180) if pd.isna(team) else ((255,100,100) if int(team)==1 else (100,100,255))
        pts=list(trails[tid])
        for i in range(1,len(pts)): cv2.line(frame,pts[i-1],pts[i],color,2)
        cv2.rectangle(frame,(x1,y1),(x2,y2),color,2); cv2.putText(frame,f'ID {tid}',(x1,max(15,y1-6)),cv2.FONT_HERSHEY_SIMPLEX,.45,color,1,cv2.LINE_AA)
    cv2.putText(frame,f'MatchLens AI - Trajectory Trails | Frame {frame_no}',(10,h-15),cv2.FONT_HERSHEY_SIMPLEX,.55,(255,255,255),2,cv2.LINE_AA)
    out.write(frame); frame_no+=1
    if frame_no%100==0: print(f'Processed {frame_no}/{total}')
cap.release(); out.release(); print(f'Trajectory video saved: {OUTPUT_VIDEO}')
