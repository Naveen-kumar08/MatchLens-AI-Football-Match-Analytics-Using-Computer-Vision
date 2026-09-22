import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('outputs/player_analytics.csv').dropna(subset=['track_id','total_distance_m']).sort_values('total_distance_m', ascending=False).head(20)
plt.figure(figsize=(12,7)); plt.bar(df['track_id'].astype(int).astype(str), df['total_distance_m']); plt.xlabel('Track ID'); plt.ylabel('Distance Covered (metres)'); plt.title('MatchLens AI - Player Distance Analysis'); plt.xticks(rotation=45); plt.tight_layout(); plt.savefig('outputs/player_distance.png', dpi=200); plt.close(); print('Distance chart saved: outputs/player_distance.png')
