import pandas as pd
import numpy as np

TRACKS='outputs/tracks.csv'; OUT='outputs/team_formation_summary.csv'
df=pd.read_csv(TRACKS); df=df[(df['class']=='player')].dropna(subset=['team','pitch_x_m','pitch_y_m'])
rows=[]
for team,g in df.groupby('team'):
    # Median position per track reduces frame-count bias.
    pos=g.groupby('track_id')[['pitch_x_m','pitch_y_m']].median().sort_values('pitch_x_m')
    for rank,(tid,r) in enumerate(pos.iterrows(),1): rows.append({'team':int(team),'player_track_id':int(tid),'role_order_x':rank,'median_x_m':r.pitch_x_m,'median_y_m':r.pitch_y_m})
pd.DataFrame(rows).to_csv(OUT,index=False); print(f'Formation summary saved: {OUT}')
