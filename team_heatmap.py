import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def create_team_heatmap(team_number):
    df = pd.read_csv('outputs/tracks.csv')
    df = df[(df['class'] == 'player') & (df['team'] == team_number)].dropna(subset=['pitch_x_m', 'pitch_y_m'])
    if df.empty:
        print(f'No valid data found for Team {team_number}'); return
    x, y = df['pitch_x_m'].to_numpy(), df['pitch_y_m'].to_numpy()
    fig, ax = plt.subplots(figsize=(12, 7))
    heatmap, _, _ = np.histogram2d(x, y, bins=[52, 34], range=[[0, 105], [0, 68]])
    ax.imshow(heatmap.T, origin='lower', extent=[0, 105, 0, 68], aspect='auto', interpolation='gaussian')
    ax.plot([0,105,105,0,0],[0,0,68,68,0]); ax.plot([52.5,52.5],[0,68])
    ax.add_patch(plt.Circle((52.5,34),9.15,fill=False))
    ax.plot([0,16.5,16.5,0],[13.84,13.84,54.16,54.16]); ax.plot([105,88.5,88.5,105],[13.84,13.84,54.16,54.16])
    ax.set(xlim=(0,105), ylim=(0,68), xlabel='Pitch X (metres)', ylabel='Pitch Y (metres)', title=f'MatchLens AI - Team {team_number} Player Heatmap')
    plt.tight_layout(); out=f'outputs/team{team_number}_heatmap.png'; plt.savefig(out,dpi=200); plt.close(); print(f'Team {team_number} heatmap saved: {out}')

if __name__ == '__main__':
    create_team_heatmap(1); create_team_heatmap(2)
