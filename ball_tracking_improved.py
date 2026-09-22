import cv2
import pandas as pd
import numpy as np

INPUT_VIDEO='input.mp4'; TRACKS_FILE='outputs/tracks.csv'; OUTPUT_CSV='outputs/ball_tracks.csv'

df=pd.read_csv(TRACKS_FILE)
ball=df[df['class']=='ball'].copy()
if ball.empty:
    print('No ball rows found in tracks.csv. Re-run run.py with the updated pipeline first.')
else:
    ball=ball.dropna(subset=['x1','y1','x2','y2']).sort_values(['track_id','frame'])
    ball['cx']=(ball.x1+ball.x2)/2; ball['cy']=(ball.y1+ball.y2)/2
    ball['dt']=ball.groupby('track_id').frame.diff()/25.0
    ball['pixel_speed']=np.sqrt(ball.groupby('track_id').cx.diff()**2+ball.groupby('track_id').cy.diff()**2)/ball.dt
    ball.loc[(ball.dt<=0)|(ball.pixel_speed>2500),'pixel_speed']=np.nan
    ball.to_csv(OUTPUT_CSV,index=False); print(f'Improved ball tracks saved: {OUTPUT_CSV}')
