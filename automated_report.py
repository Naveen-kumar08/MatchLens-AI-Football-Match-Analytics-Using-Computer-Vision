import json
from pathlib import Path
import pandas as pd

outdir=Path('outputs'); report={'title':'MatchLens AI Automated Match Report','notes':['Metrics are computer-vision estimates and depend on tracking and calibration quality.']}
for name,key in [('player_analytics.csv','player_analytics'),('possession_summary.csv','possession'),('passing_events.csv','passing_events'),('team_formation_summary.csv','formations'),('tactical_shape.csv','tactical_shape'),('advanced_movement_metrics.csv','advanced_movement'),('events.csv','events')]:
    p=outdir/name
    if p.exists():
        df=pd.read_csv(p); report[key]=df.to_dict(orient='records')
json.dump(report,open(outdir/'match_report.json','w'),indent=2,default=str); print('Automated report saved: outputs/match_report.json')
