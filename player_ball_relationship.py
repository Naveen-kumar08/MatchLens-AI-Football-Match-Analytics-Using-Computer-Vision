import pandas as pd
import numpy as np

TRACKS='outputs/tracks.csv'; OUT='outputs/player_ball_relationship.csv'; MAX_DISTANCE_M=3.0

df=pd.read_csv(TRACKS); players=df[df['class']=='player'].dropna(subset=['pitch_x_m','pitch_y_m']).copy(); balls=df[df['class']=='ball'].dropna(subset=['pitch_x_m','pitch_y_m']).copy()
if balls.empty:
    print('No ball pitch coordinates available. Re-run run.py with updated pipeline.'); raise SystemExit
rows=[]
for frame,g in players.groupby('frame'):
    b=balls[balls.frame==frame]
    if b.empty: continue
    bx=float(b.iloc[0].pitch_x_m); by=float(b.iloc[0].pitch_y_m)
    for _,p in g.iterrows():
        d=float(np.hypot(float(p.pitch_x_m)-bx,float(p.pitch_y_m)-by))
        if d<=MAX_DISTANCE_M: rows.append([frame,int(p.track_id),p.team,bx,by,d])
pd.DataFrame(rows,columns=['frame','track_id','team','ball_x_m','ball_y_m','distance_to_ball_m']).to_csv(OUT,index=False); print(f'Player-ball relationships saved: {OUT}')
