import pandas as pd
import numpy as np

TRACKS='outputs/tracks_with_speed.csv'; OUT='outputs/events.csv'
df=pd.read_csv(TRACKS); p=df[df['class']=='player'].dropna(subset=['track_id','frame','speed_kmh']).copy(); p=p[p.speed_kmh<=40]
rows=[]
for tid,g in p.groupby('track_id'):
    g=g.sort_values('frame'); fast=g[g.speed_kmh>=18]
    for _,r in fast.iterrows(): rows.append({'frame':int(r.frame),'event':'high_speed_run_candidate','track_id':int(tid),'team':r.team,'speed_kmh':float(r.speed_kmh)})
pd.DataFrame(rows).to_csv(OUT,index=False); print(f'Event candidates saved: {OUT}')
