import json
from pathlib import Path
import pandas as pd

out=Path('outputs'); insights=[]
pa=out/'player_analytics.csv'
if pa.exists():
    d=pd.read_csv(pa)
    if not d.empty:
        top=d.sort_values('total_distance_m',ascending=False).iloc[0]; insights.append(f'Track {int(top.track_id)} has the highest observed distance at {top.total_distance_m:.1f} m.')
        valid=d[d.max_speed_kmh.notna()]
        if not valid.empty:
            s=valid.sort_values('max_speed_kmh',ascending=False).iloc[0]; insights.append(f'Track {int(s.track_id)} has the highest estimated peak speed at {s.max_speed_kmh:.1f} km/h.')
pos=out/'possession_summary.csv'
if pos.exists():
    d=pd.read_csv(pos); insights.append('Estimated possession is based on the player nearest to the detected ball on each frame; it is not official event-data possession.')
shape=out/'tactical_shape.csv'
if shape.exists(): insights.append('Tactical shape metrics summarize team centroid, width, depth and spatial spread over tracked frames.')
json.dump({'generated_by':'MatchLens AI heuristic insight engine','insights':insights},open(out/'ai_insights.json','w'),indent=2)
print('AI-style insights saved: outputs/ai_insights.json')
