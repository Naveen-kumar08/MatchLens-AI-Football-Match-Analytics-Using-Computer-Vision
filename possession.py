import pandas as pd

REL='outputs/player_ball_relationship.csv'; OUT='outputs/possession_summary.csv'
df=pd.read_csv(REL)
if df.empty:
    print('No player-ball relationships found.'); raise SystemExit
nearest=df.sort_values(['frame','distance_to_ball_m']).drop_duplicates('frame')
nearest['team']=pd.to_numeric(nearest['team'],errors='coerce')
counts=nearest['team'].value_counts(dropna=False).to_dict(); total=len(nearest)
rows=[]
for team in [1,2]: rows.append({'team':team,'frames_nearest_to_ball':int(counts.get(team,0)),'estimated_possession_pct':100*counts.get(team,0)/total})
rows.append({'team':'Unknown','frames_nearest_to_ball':int(counts.get(float('nan'),0)) if False else int(nearest.team.isna().sum()),'estimated_possession_pct':100*nearest.team.isna().sum()/total})
pd.DataFrame(rows).to_csv(OUT,index=False); print(f'Estimated possession saved: {OUT}')
