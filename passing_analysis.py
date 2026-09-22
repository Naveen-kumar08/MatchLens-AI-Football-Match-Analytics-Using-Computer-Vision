import pandas as pd
import numpy as np

REL='outputs/player_ball_relationship.csv'; OUT='outputs/passing_events.csv'; MAX_GAP=2.5; MIN_TRAVEL=4.0
rel=pd.read_csv(REL)
if rel.empty: print('No relationship data.'); raise SystemExit
rel=rel.dropna(subset=['team','ball_x_m','ball_y_m']).sort_values(['frame','track_id'])
nearest=rel.sort_values(['frame','distance_to_ball_m']).drop_duplicates('frame')
nearest['next_team']=nearest.team.shift(-1); nearest['next_frame']=nearest.frame.shift(-1); nearest['next_x']=nearest.ball_x_m.shift(-1); nearest['next_y']=nearest.ball_y_m.shift(-1)
nearest['ball_travel_m']=np.hypot(nearest.next_x-nearest.ball_x_m,nearest.next_y-nearest.ball_y_m)
events=nearest[(nearest.team==nearest.next_team)&(nearest.next_frame-nearest.frame<=15)&(nearest.ball_travel_m>=MIN_TRAVEL)].copy()
events=events.rename(columns={'team':'team'}); events['from_frame']=events.frame; events['to_frame']=events.next_frame; events['travel_m']=events.ball_travel_m
events[['from_frame','to_frame','team','track_id','travel_m']].to_csv(OUT,index=False); print(f'Pass-like events saved: {OUT}')
