import pandas as pd
import numpy as np

TRACKS='outputs/tracks_with_speed.csv'; OUT='outputs/advanced_movement_metrics.csv'
df=pd.read_csv(TRACKS); df=df[df['class']=='player'].dropna(subset=['track_id','frame','pitch_x_m','pitch_y_m']).sort_values(['track_id','frame']).copy()
df['dt']=df.groupby('track_id').frame.diff()/25.0; df['dx']=df.groupby('track_id').pitch_x_m.diff(); df['dy']=df.groupby('track_id').pitch_y_m.diff(); df['distance_m']=np.hypot(df.dx,df.dy); df['speed_mps']=df.distance_m/df.dt; df.loc[(df.dt<=0)|(df.speed_mps>12),'speed_mps']=np.nan; df['accel_mps2']=df.groupby('track_id').speed_mps.diff()/df.dt; df.loc[df.accel_mps2.abs()>6,'accel_mps2']=np.nan
rows=[]
for tid,g in df.groupby('track_id'):
    rows.append({'track_id':int(tid),'team':g.team.dropna().iloc[0] if g.team.notna().any() else np.nan,'distance_m':g.distance_m.sum(),'max_speed_kmh':g.speed_mps.max()*3.6 if g.speed_mps.notna().any() else np.nan,'max_acceleration_mps2':g.accel_mps2.max() if g.accel_mps2.notna().any() else np.nan,'high_speed_frames':int((g.speed_mps>=5.0).sum()),'observed_frames':len(g)})
pd.DataFrame(rows).to_csv(OUT,index=False); print(f'Advanced movement metrics saved: {OUT}')
