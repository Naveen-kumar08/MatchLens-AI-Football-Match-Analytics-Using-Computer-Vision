import cv2
import pandas as pd

INPUT_VIDEO='input.mp4'; TRACKS_FILE='outputs/tracks_with_speed.csv'; OUTPUT_VIDEO='outputs/matchlens_stats.mp4'
df=pd.read_csv(TRACKS_FILE); df=df[df['class']=='player'].copy(); df['frame']=df['frame'].astype(int); df['track_id']=df['track_id'].astype(int); frames={k:g for k,g in df.groupby('frame')}
cap=cv2.VideoCapture(INPUT_VIDEO)
if not cap.isOpened(): raise RuntimeError('Cannot open input.mp4')
fps=cap.get(cv2.CAP_PROP_FPS) or 25; w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)); total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); out=cv2.VideoWriter(OUTPUT_VIDEO,cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h))
for n in range(total):
    ok,frame=cap.read()
    if not ok: break
    p=frames.get(n,pd.DataFrame()); t1=int((p.team==1).sum()) if not p.empty else 0; t2=int((p.team==2).sum()) if not p.empty else 0; unk=int(p.team.isna().sum()) if not p.empty else 0; speeds=pd.to_numeric(p.get('speed_kmh',pd.Series(dtype=float)),errors='coerce').dropna(); speeds=speeds[(speeds>=0)&(speeds<=40)]; avg=float(speeds.mean()) if len(speeds) else 0; mx=float(speeds.max()) if len(speeds) else 0
    cv2.rectangle(frame,(10,10),(320,200),(0,0,0),-1); lines=[('MATCHLENS AI',.7,(255,255,255)),('LIVE MATCH ANALYTICS',.45,(200,200,200)),(f'Players Detected : {len(p)}',.48,(255,255,255)),(f'Team 1           : {t1}',.48,(255,120,120)),(f'Team 2           : {t2}',.48,(120,120,255)),(f'Unknown          : {unk}',.48,(200,200,200)),(f'Average Speed    : {avg:.1f} km/h',.48,(255,255,255)),(f'Maximum Speed    : {mx:.1f} km/h',.48,(255,255,255))]
    y=42
    for i,(txt,scale,col) in enumerate(lines): cv2.putText(frame,txt,(25,y),cv2.FONT_HERSHEY_SIMPLEX,scale,col,2 if i==0 else 1,cv2.LINE_AA); y+=25
    for _,r in p.iterrows():
        x1,y1,x2,y2=map(int,[r.x1,r.y1,r.x2,r.y2]); team=r.team; col=(180,180,180) if pd.isna(team) else ((255,100,100) if int(team)==1 else (100,100,255)); sp=r.speed_kmh if pd.notna(r.speed_kmh) else 0; cv2.rectangle(frame,(x1,y1),(x2,y2),col,2); cv2.putText(frame,f'ID {int(r.track_id)} | {sp:.1f} km/h',(x1,max(15,y1-7)),cv2.FONT_HERSHEY_SIMPLEX,.42,col,1,cv2.LINE_AA)
    out.write(frame)
cap.release(); out.release(); print(f'Statistics video saved: {OUTPUT_VIDEO}')
