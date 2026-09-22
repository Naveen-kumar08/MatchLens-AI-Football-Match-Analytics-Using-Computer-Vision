import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('outputs/player_analytics.csv').dropna(subset=['track_id','max_speed_kmh','average_speed_kmh']).sort_values('max_speed_kmh', ascending=False).head(20)
x=range(len(df)); w=0.35
plt.figure(figsize=(13,7)); plt.bar([i-w/2 for i in x],df['max_speed_kmh'],width=w,label='Maximum Speed'); plt.bar([i+w/2 for i in x],df['average_speed_kmh'],width=w,label='Average Speed'); plt.xlabel('Track ID'); plt.ylabel('Speed (km/h)'); plt.title('MatchLens AI - Player Speed Analysis'); plt.xticks(list(x),df['track_id'].astype(int).astype(str),rotation=45); plt.legend(); plt.tight_layout(); plt.savefig('outputs/player_speed.png',dpi=200); plt.close(); print('Speed chart saved: outputs/player_speed.png')
