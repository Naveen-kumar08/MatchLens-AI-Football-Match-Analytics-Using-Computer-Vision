import pandas as pd
import numpy as np

TRACKS='outputs/tracks.csv'; OUT='outputs/player_positioning.csv'
df=pd.read_csv(TRACKS); p=df[df['class']=='player'].dropna(subset=['team','pitch_x_m','pitch_y_m'])
rows=[]
for (team,tid),g in p.groupby(['team','track_id']):
    x=g.pitch_x_m; y=g.pitch_y_m; rows.append({'team':int(team),'track_id':int(tid),'median_x_m':x.median(),'median_y_m':y.median(),'min_x_m':x.min(),'max_x_m':x.max(),'min_y_m':y.min(),'max_y_m':y.max(),'observations':len(g)})
pd.DataFrame(rows).to_csv(OUT,index=False); print(f'Player positioning saved: {OUT}')
