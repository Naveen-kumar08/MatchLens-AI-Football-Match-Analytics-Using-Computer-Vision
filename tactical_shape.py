import pandas as pd
import numpy as np

TRACKS='outputs/tracks.csv'; OUT='outputs/tactical_shape.csv'
df=pd.read_csv(TRACKS); df=df[(df['class']=='player')].dropna(subset=['team','pitch_x_m','pitch_y_m'])
rows=[]
for frame,g in df.groupby('frame'):
    for team,t in g.groupby('team'):
        if len(t)<3: continue
        xs=t.pitch_x_m.to_numpy(); ys=t.pitch_y_m.to_numpy(); rows.append({'frame':int(frame),'team':int(team),'players':len(t),'centroid_x_m':xs.mean(),'centroid_y_m':ys.mean(),'width_m':xs.max()-xs.min(),'depth_m':ys.max()-ys.min(),'spread_m':float(np.sqrt(xs.var()+ys.var()))})
pd.DataFrame(rows).to_csv(OUT,index=False); print(f'Tactical shape saved: {OUT}')
